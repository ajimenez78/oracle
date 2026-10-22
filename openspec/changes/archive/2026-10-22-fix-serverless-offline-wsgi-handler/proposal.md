## Why

Running the API locally with `serverless offline` fails on every request with `ModuleNotFoundError: No module named 'wsgi_handler'`. The `api` function's handler (`wsgi_handler.handler`) is a shim that `serverless-wsgi` writes into the service root only during specific lifecycle hooks (`before:offline:start:init`). serverless-offline v14's bare `serverless offline` command runs the `offline:start` lifecycle, not `offline:start:init`, so the shim is never generated and the Python runner can't import it. Local development of the Lambda API is currently blocked.

## What Changes

- Provide one documented, scripted entry point for running the API locally (`npm run offline` → `serverless offline start`). This command fires the `init`/`end` lifecycle events that serverless-wsgi hooks into, so the shim is generated on start and removed on shutdown.
- Ignore the serverless-wsgi generated artifacts (`wsgi_handler.py`, `serverless_wsgi.py`, `.serverless-wsgi`) in git, so an interrupted run that leaves them behind can't be committed by mistake.
- Declare the Python packages the local Lambda emulation needs (Flask, Werkzeug, pinned the same as `requirements.txt`) in the uv project as a dev dependency group, so `uv sync` doesn't remove them from `.venv`.
- Update `README-SERVERLESS.md` with a "Run locally with serverless-offline" section, and a warning that bare `serverless offline` does not work with serverless-wsgi.

## Capabilities

### New Capabilities
- `serverless-local-dev`: Running the serverless `api` function locally behind an emulated API Gateway, including the start command, the handler shim's lifecycle, and the local Python environment it needs.

### Modified Capabilities
<!-- None: existing specs (legacy-chat, legacy-ingestion) are unaffected. -->

## Impact

- `package.json`: new `offline` npm script.
- `.gitignore`: serverless-wsgi artifact entries.
- `pyproject.toml` / `uv.lock`: new `dev` dependency group (Flask, Werkzeug). These are not added to the Lambda package, which still comes only from `requirements.txt`.
- `README-SERVERLESS.md`: local development docs.
- No change to `serverless.yml` function/handler configuration or to the deployed Lambda. The uncommitted `runtime: python3.12` edit in the working tree is unrelated to this failure and out of scope. serverless-offline picks the interpreter as `python3` from `VIRTUAL_ENV`/`PATH` regardless of the minor version.
