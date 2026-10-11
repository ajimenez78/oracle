# legacy-ingestion Specification

## Purpose

Defines how the PoC vectorizer fetches content from the Notion API and how it behaves when Notion returns errors, so one bad response never aborts the whole indexing run.

## Requirements

### Requirement: Notion responses are checked before use
The vectorizer SHALL check the HTTP status of every Notion API response before reading its content. An error response MUST NOT raise an unhandled exception.

#### Scenario: Successful response
- **WHEN** Notion returns HTTP 200 for a block-children request
- **THEN** the vectorizer reads the returned blocks and their pagination fields as before

#### Scenario: Error payload
- **WHEN** Notion returns a non-2xx response with an error body (for example `404 object_not_found`)
- **THEN** the vectorizer treats it as a failed request and does not try to read `results` from it

### Requirement: Rate limits and transient failures are retried
The vectorizer SHALL retry requests that fail with HTTP 429, HTTP 5xx, a timeout or a connection error, using exponential backoff with jitter and honoring the `Retry-After` header when present, up to a bounded number of attempts. Every request SHALL have a timeout.

#### Scenario: Rate limited then succeeds
- **WHEN** Notion returns HTTP 429 with `Retry-After: 1` and the next attempt returns HTTP 200
- **THEN** the vectorizer waits at least one second, retries, and uses the successful response

#### Scenario: Retries exhausted
- **WHEN** every attempt for a request fails with a retryable error
- **THEN** the vectorizer stops retrying after the attempt limit and treats the request as failed

#### Scenario: Client error is not retried
- **WHEN** Notion returns HTTP 400 or 404
- **THEN** the vectorizer does not retry the request

### Requirement: A failed request skips only the affected content
A failed request for a nested block SHALL skip only that block's descendants; the block itself and the rest of the page MUST still be processed. A failed request for a root page SHALL skip only that root; the other roots MUST still be processed and indexed.

#### Scenario: Nested block cannot be read
- **WHEN** fetching the children of a nested block fails with a non-retryable error
- **THEN** the vectorizer keeps that block, skips its descendants, and continues with the block's siblings

#### Scenario: Root page cannot be read
- **WHEN** fetching one of the configured root pages fails
- **THEN** the vectorizer indexes the remaining roots and the run completes

### Requirement: Skipped content is reported
The vectorizer SHALL log a warning for each skipped block subtree or root page and SHALL print a summary at the end of the run. Each entry MUST include the block or page id, the HTTP status (or the failure kind) and the Notion error code when available. Log output MUST NOT contain the Notion token or note content.

#### Scenario: Run with skipped content
- **WHEN** a run finishes after skipping one nested block that returned `404 object_not_found`
- **THEN** the summary lists that block id with `404` and `object_not_found`

#### Scenario: Clean run
- **WHEN** a run finishes without any failed request
- **THEN** the summary reports that nothing was skipped
