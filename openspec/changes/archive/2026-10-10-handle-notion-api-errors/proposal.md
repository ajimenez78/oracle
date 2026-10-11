## Why

`src/oracle/vectorize.py` crashes with `KeyError: 'results'` deep inside the recursion of `get_block_children`: it parses every Notion response as a success without checking the HTTP status, so any error payload aborts the whole run. The crash has happened at different recursion depths on different runs (3 levels, then 5), which points to Notion's rate limit (`429 rate_limited`) rather than one unreadable block. SPEC section 10 lists this as PoC finding #3; FR-32 and FR-6 define the expected behavior.

## What Changes

- Check the HTTP status of every Notion request before reading its body.
- Retry rate-limited (`429`, honoring `Retry-After`) and transient (`5xx`, timeouts, connection errors) failures with exponential backoff and jitter, up to a fixed number of attempts.
- Give every Notion request a timeout.
- When a non-retryable error (or exhausted retries) hits a nested block, skip that block's subtree, log a warning, and keep processing the rest of the page.
- When it hits one of the root pages, skip that root, log it, and continue with the other roots.
- Print a summary at the end of the run listing skipped subtrees and roots with their HTTP status and Notion error code.
- Run the pipeline only under `if __name__ == "__main__":` so the fetch logic can be checked offline against a stub server.

Non-goals:
- Changing what gets indexed when Notion responds successfully: block-to-text conversion, chunking (1000/200), embedding defaults, chunk ids and metadata stay as they are (RAG baseline).
- Per-page documents, child page handling, stale-chunk cleanup, parallel fetching (ingestion/knowledge services' job).
- Proactive throttling (token bucket); retrying `429` is enough for a sequential script.
- A shared resilient HTTP client in `libs/common` (target architecture, not this script).

## Capabilities

### New Capabilities
- `legacy-ingestion`: how the PoC vectorizer (`vectorize.py`) fetches Notion content and behaves when the Notion API returns errors.

### Modified Capabilities
<!-- none: the only existing spec is legacy-chat, which this change does not touch -->

## Impact

- Code: `src/oracle/vectorize.py` only (fetch helpers and entry point). `legacy/vectorize.py` stays untouched.
- Dependencies: none added; retries use `urllib3.util.Retry` through `requests`' `HTTPAdapter` (both already installed with `requests`).
- Baseline: a run that would have succeeded indexes the same content. A run that crashed now completes, minus any skipped subtrees reported in the summary.
- Behavior: runs take longer when Notion rate-limits, instead of crashing.
