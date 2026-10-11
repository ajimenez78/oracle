## Context

`vectorize.py` calls `requests.get` directly in two places: `get_block_children` (recursive, with a pagination loop) and `get_page_content` (page properties for the title). Neither checks the status code or sets a timeout; `get_block_children` indexes `data["results"]` straight away and `get_page_content` silently falls back to an empty title on an error body. The pipeline runs at import time (last line of the module). See proposal.md for motivation and specs/legacy-ingestion/spec.md for the required behavior.

The response body is discarded, so the traceback cannot say which error Notion returned. Two runs failed at different depths (3 and 5 levels), which fits `429 rate_limited`: the recursion fires requests back to back and Notion allows about 3 requests/second per integration. A `404` for an unreadable block or a `400` for a block type the API cannot list would fail at the same place every run. The design handles all of them; the end-of-run summary will confirm which one it was.

## Goals / Non-Goals

**Goals:**
- Resilience at the HTTP layer (status check, timeout, retries) with no new dependency.
- Failure isolation at two levels: nested subtree and root page.
- Leave successful-path output byte-for-byte identical, so the RAG baseline is not affected.

**Non-Goals:**
- Committed automated tests: there is no test setup for the PoC code; verification uses a throwaway offline harness (see tasks).

## Decisions

**Use one `requests.Session` with `HTTPAdapter(max_retries=Retry(...))`.**
`urllib3.util.Retry` (urllib3 2.8 is installed) already implements what the spec asks: `status_forcelist=[429, 500, 502, 503, 504]`, `respect_retry_after_header=True`, exponential `backoff_factor` plus `backoff_jitter`, and retries on connect/read errors. Settings: `total=5`, `backoff_factor=1`, `backoff_jitter=1`, `allowed_methods={"GET"}`, `raise_on_status=False` so the last response comes back for our own status check. Every call passes `timeout=(5, 30)`.
Alternatives: a hand-written retry loop (more code, easy to get `Retry-After` wrong); `tenacity` or `httpx` (new dependency, needs an ADR).

**A single `notion_get(url, params)` helper that raises `NotionRequestError` on failure.**
It returns the parsed JSON on 2xx. Otherwise it raises `NotionRequestError` carrying the HTTP status (or `"timeout"`/`"connection"` for `requests.RequestException` after retries) and Notion's `code` field from the error body when present. Both call sites use it, so no code path reads an unchecked body. Pagination switches to `params={"start_cursor": ...}` instead of string-building the URL.

**Catch at two places, matching the two isolation levels.**
- In `get_block_children`'s recursion loop: wrap the recursive call for a child; on `NotionRequestError` keep the child block itself, record the skip (block id, block type, status, code), and continue with siblings. A failure partway through a child's pagination skips that child's whole subtree; partial subtrees are not indexed.
- In `vectorize_notion_notes`' loop over roots: wrap `get_page_content`; on `NotionRequestError` record the root as skipped and continue with the next root. The root fetch's own failure propagates here because only child recursion is guarded inside `get_block_children`.

**Skips are collected in a module-level list and printed as a summary at the end of `vectorize_notion_notes`.**
Warnings are printed as they happen too. Entries contain ids, block type, status and error code only; never headers, the token or block text.

**Entry point under `if __name__ == "__main__":`.**
Lets the verification harness import the module and call the functions against a stub server without running the real pipeline. Running `python src/oracle/vectorize.py` behaves as before.

## Risks / Trade-offs

- [Skipped root keeps its old chunks in Chroma] → Acceptable for the PoC; the summary makes the skip visible so the user can re-run.
- [Long `Retry-After` values stall the run] → Acceptable; a slow run is better than a crash.
- [Persistent rate limiting exhausts 5 retries and skips subtrees] → The summary shows `429` entries; if they appear, raise `total`/`backoff_factor` or add a small delay between requests in a follow-up.
- [Importing the module loads the real `.env`] → The verification harness stubs `dotenv.load_dotenv` before import and uses a dummy token, so no real credential is used or printed.
