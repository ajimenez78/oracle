## Why

`serverless deploy` fails with `Unzipped size must be smaller than 262144000 bytes`. The generated `.serverless/oracle.zip` is ~237 MB zipped and ~753 MB unzipped (27,701 files). The `package.patterns` already restrict the *code* to `src/**`, but the Framework's built-in Python requirements step ignores those patterns. It found `uv.lock` + `pyproject.toml` at the service root, exported the **entire** local app dependency tree (132 pins: gradio, chromadb, langchain*, openai, pandas, numpy, onnxruntime, kubernetes, …) and injected it at the zip root. The Lambda only needs Flask (+ werkzeug), as declared in `requirements.txt`.

## What Changes

- Make the built-in Python requirements packaging resolve dependencies from `requirements.txt` only, not from `uv.lock`/`pyproject.toml`. To do this, disable the uv (and poetry) auto-detection under `custom.pythonRequirements`.
- Stop `serverless-wsgi` from separately pip-installing requirements into `src/.requirements` (`packRequirements: false`). Dependencies get installed once, by the built-in packager. This removes the stray `src/.requirements/` build directory and the misleading comment.
- Tighten `package.patterns` so that only `src/**` plus the handler shims injected by `serverless-wsgi` are deployed. Exclude `__pycache__`, `*.pyc` and `src/**/CLAUDE.md` from the bundle.
- Fix the function handler path so it matches where `serverless-wsgi` actually places `wsgi_handler.py` (zip root, not `src/`).
- Add a pre-deploy verification step (`serverless package` + size check) to the deployment docs.

## Capabilities

### New Capabilities
<!-- none: deployment tooling/config only -->

### Modified Capabilities
<!-- none: no spec-level behavior changes; change sets skip_specs: true -->

## Impact

- `serverless.yml` (custom.wsgi, custom.pythonRequirements, package.patterns, functions.api.handler)
- `src/.requirements/` (generated artifact, to delete; also add it to `.gitignore`)
- `README-SERVERLESS.md` (packaging/verification notes)
- No application code or runtime API behavior changes. Local development via `uv`/`pyproject.toml` is untouched.
