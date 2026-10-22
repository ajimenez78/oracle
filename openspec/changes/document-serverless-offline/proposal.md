## Why

`README-SERVERLESS.md` only documents `serverless wsgi serve` for local development. That runs Flask directly and skips the Lambda handler and API Gateway emulation. The way that does exercise them, serverless-offline, isn't documented. Its obvious command, `serverless offline`, fails with `ModuleNotFoundError: No module named 'wsgi_handler'`, because only `serverless offline start` triggers the serverless-wsgi hook that generates the handler shim. A developer following the plugin's own docs hits that error.

## What Changes

- Add a "Run locally with serverless-offline" subsection to the "Local development" section of `README-SERVERLESS.md`, covering:
  - Prerequisites: `npm install`, and an activated virtual environment with `requirements.txt` installed (serverless-offline runs the handler with the `python3` from the active venv).
  - The launch command: `serverless offline start`.
  - The check: `curl http://localhost:3000/dev/hello` returns `{"message": "Hello from path!"}`.
  - A warning that bare `serverless offline` fails with `No module named 'wsgi_handler'`, and why.
  - Stopping with Ctrl+C removes the generated `wsgi_handler.py`, `serverless_wsgi.py` and `.serverless-wsgi`. If a run is killed abnormally, `serverless wsgi clean` removes leftovers.
- Keep the existing `serverless wsgi serve` instructions as the lighter alternative.

**Assumption:** "README" means `README-SERVERLESS.md`, where all Serverless Framework usage docs live. `README.md` is the project overview and isn't changed.

## Capabilities

### New Capabilities
<!-- None. -->

### Modified Capabilities
<!-- None. This is a documentation-only change, so the change sets `skip_specs: true`. The existing `serverless-local-dev` spec already requires a documented local start command; this change provides the documentation without altering any requirement. -->

## Impact

- `README-SERVERLESS.md` only. No code, configuration, dependency or deployment changes.
- Out of scope (unlike the archived `fix-serverless-offline-wsgi-handler` change): no npm script, `.gitignore` entries or uv dependency group.
