## Context

See proposal.md (Why) for the failure. Current packaging is a pipeline with three independent contributors to `oracle.zip`:

1. **Framework code packaging**: governed by `package.patterns` (`!**`, `src/**`, …). This part already works: only `src/**` code ends up in the zip.
2. **Built-in Python requirements** (activated by `custom.pythonRequirements`): Serverless v4's integrated fork of serverless-python-requirements. With default options it uses `useUv: true` / `usePoetry: true`. If it finds `uv.lock` at the service root, it runs a uv export into `.serverless/requirements.txt`, which takes priority over the hand-written `requirements.txt`. It then installs into a cache dir and injects the result at the zip root **after** pattern filtering, so `package.patterns` cannot exclude it.
3. **serverless-wsgi**: injects `wsgi_handler.py`, `serverless_wsgi.py` and `.serverless-wsgi` at the zip root. With `packRequirements: true` it also pip-installs `requirements.txt` into `src/.requirements` (hence the stray directory).

The repo root doubles as the local `uv` project (pyproject.toml lists gradio, langchain, chromadb, …) and as the Serverless service root. That overlap is what triggers the bug.

## Goals / Non-Goals

**Goals:**
- Unzipped package well under 250 MB. Expected: a few MB (Flask, Werkzeug, Jinja2, MarkupSafe, itsdangerous, click, blinker + wsgi shims).
- A single, explicit source of Lambda dependencies: `requirements.txt`.
- Deployed code limited to `src/` plus the serverless-wsgi handler shims.

**Non-Goals:**
- Splitting dependencies into Lambda layers, or containerizing.
- Deploying the gradio/langchain/chromadb app logic to Lambda. If that is wanted later, it needs a container image (10 GB limit), not a zip.
- Restructuring the repo (e.g., moving the service into its own subdirectory).

## Decisions

**D1: Disable uv/poetry auto-detection rather than hide `uv.lock`.**
Set `custom.pythonRequirements.useUv: false` and `usePoetry: false`, and keep `fileName: requirements.txt` explicit. *Alternatives:* (a) move `serverless.yml` into a subdirectory with its own requirements. This is cleaner isolation but restructures the repo and the paths. (b) Use `package.patterns`. This does not work, because requirements are injected after filtering. (c) Use `noDeploy` lists. That's whack-a-mole over 132 packages. D1 is a two-line, intent-revealing config change.

**D2: Let the built-in packager own dependency installation; set serverless-wsgi `packRequirements: false`.**
Two installers produce duplicate copies, and the existing comment contradicts the value. The built-in packager handles arm64 cross-platform wheels and caching. serverless-wsgi still adds its own `serverless_wsgi.py` shim regardless of this flag.

**D3: Handler = `wsgi_handler.handler`.**
serverless-wsgi writes `wsgi_handler.py` to the zip root (confirmed in the current zip listing). The current `src/wsgi_handler.handler` would fail at invoke time with an import error once deploy succeeds. `custom.wsgi.app: src/app.app` stays as is; the shim resolves it from the root.

**D4: Explicit patterns.**
```
- '!**'
- 'src/**'
- '!src/**/__pycache__/**'
- '!src/**/*.pyc'
- '!src/**/CLAUDE.md'
- '!src/.requirements/**'
```
The bogus `.requirements/**` and `wsgi_handler.py` include lines are dropped (the shims are injected regardless of patterns).

## Risks / Trade-offs

- [`requirements.txt` drifts from what the Lambda code actually imports] → Keep it minimal and pinned. Any new Lambda import must be added there. Documented in README-SERVERLESS.md.
- [Stale cached requirements in `~/.cache/serverless-python-requirements` keyed to the old uv export] → The cache key is derived from the requirements file hash, so it changes automatically. If in doubt, run `serverless requirements cleanCache`. Also delete `.serverless/` before re-packaging.
- [python3.14 wheels for arm64 not available for some dependency] → Not an issue for Flask's pure-Python deps. Revisit only if compiled deps are added.

## Migration Plan

1. Apply the config changes and delete `src/.requirements/` and `.serverless/`.
2. Run `serverless package`. Inspect `.serverless/oracle.zip` (`unzip -l | tail -1` should show a few MB / a few hundred files, with no gradio/langchain).
3. Run `serverless deploy` and curl `/` and `/hello`.
Rollback: the previous config never deployed successfully, so there is nothing to roll back in AWS. Revert `serverless.yml` via git if needed.
