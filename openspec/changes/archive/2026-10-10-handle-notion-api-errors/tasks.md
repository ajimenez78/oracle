## 1. Resilient Notion requests

- [x] 1.1 Add a module-level `requests.Session` mounted with `HTTPAdapter(max_retries=Retry(total=5, backoff_factor=1, backoff_jitter=1, status_forcelist=[429, 500, 502, 503, 504], allowed_methods={"GET"}, respect_retry_after_header=True, raise_on_status=False))` and the Notion headers in `src/oracle/vectorize.py`; verify the file parses with `uv run python -c "import ast; ast.parse(open('src/oracle/vectorize.py').read())"`
- [x] 1.2 Add `NotionRequestError` (status or failure kind, Notion `code`, target id) and `notion_get(url, params=None)` that uses the session with `timeout=(5, 30)`, returns JSON on 2xx and raises `NotionRequestError` otherwise, including after `requests.RequestException`; verify with the stub-server harness (3.1) that a 404 body raises `NotionRequestError` with `object_not_found`

## 2. Isolate failures

- [x] 2.1 Switch `get_block_children` and its pagination loop to `notion_get` (pagination via `params={"start_cursor": ...}`); verify with the harness that a paginated 200 response returns all blocks in the same order as before
- [x] 2.2 In `get_block_children`'s recursion, catch `NotionRequestError` per child: keep the child block, record a skip (block id, block type, status, code), print a warning, and continue with siblings; verify with the harness that a 404 on one nested block keeps its siblings and the block itself
- [x] 2.3 Switch `get_page_content`'s page request to `notion_get`; in `vectorize_notion_notes`, catch `NotionRequestError` per root, record and warn, and continue with the next root; verify with the harness that a failing root is skipped and the next root is processed
- [x] 2.4 Print the skip summary at the end of `vectorize_notion_notes` ("nothing skipped" when empty) and move the final `vectorize_notion_notes(...)` call under `if __name__ == "__main__":`; verify importing the module in the harness does not start a run, and `git diff --quiet legacy/` succeeds

## 3. Offline verification

- [x] 3.1 Write a throwaway harness outside the repo (not committed) that stubs `dotenv.load_dotenv`, sets a dummy `NOTION_TOKEN`, starts a local `http.server` stub, points `NOTION_API_BASE_URL` at it, and imports `vectorize.py`; verify it makes no real network call and its output contains no token
- [x] 3.2 Use the harness to check the retry scenarios: `429` with `Retry-After: 1` then 200 (waits at least 1s, succeeds); five `503`s (gives up, raises `NotionRequestError`); a `400` (exactly one request, no retry)
- [x] 3.3 Run the end-to-end skip scenario: one root with a nested `404`, one root returning `404`, one healthy root; verify the summary lists both skips with status and code and the healthy roots' text is extracted unchanged

## 4. Real run (manual, by the user)

- [x] 4.1 Run `uv run python src/oracle/vectorize.py` against Notion; confirm it completes and read the summary to see whether `429`s (or other errors) were behind the original `KeyError`
