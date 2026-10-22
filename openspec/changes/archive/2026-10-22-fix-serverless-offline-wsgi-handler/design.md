## Context

See proposal.md (Why) for the failure. Relevant facts verified in `node_modules`:

- `serverless-wsgi@3.1.0` writes `wsgi_handler.py`, `serverless_wsgi.py` and `.serverless-wsgi` into the service root in `packWsgiHandler()`. For offline use it registers only `before:offline:start:init` (generate) and `after:offline:start:end` (cleanup).
- `serverless-offline@14.8.4` defines two commands. `offline` has lifecycle `["start"]` (hook `offline:start`). `offline start` has lifecycle `["init", "ready", "end"]`. Only the second fires the events serverless-wsgi listens to. The plugin's own source comment says `serverless offline start` is the form that provides init/end hooks for other plugins.
- `PythonRunner` spawns `runtime.split(".")[0]` (that is, `python3`) and prepends `$VIRTUAL_ENV/bin` to `PATH`. With `.venv` active, the handler runs on the project's uv Python 3.12.
- `.venv` currently has Flask 3.1.3 installed, but `pyproject.toml` doesn't declare it, so `uv sync` would remove it.
- `custom.wsgi.packRequirements: false` means serverless-wsgi's offline hook only writes the shim and doesn't pip-install anything. This is the desired behavior.

## Goals / Non-Goals

**Goals:**
- Make local emulation work with a single, discoverable command.
- Keep generated shims out of git.
- Make the local Python environment reproducible via uv.

**Non-Goals:**
- Changing the deployed handler, packaging, or `serverless.yml` function config.
- Patching or forking serverless-wsgi/serverless-offline.
- Fixing the `DEP0190` Node deprecation warning (it comes from serverless-offline internals and is harmless).
- Deciding the provider `runtime` (3.12 vs 3.14). That's a separate concern.

## Decisions

### D1: Use `serverless offline start`, wrapped in an npm script
Add `"scripts": { "offline": "serverless offline start" }` to `package.json` and document `npm run offline`.

- *Why*: This is the upstream-supported way to get init/end hooks, and it needs zero custom code. The npm script removes the "which form do I type" trap.
- *Alternative: commit a static `wsgi_handler.py`*. Rejected. It duplicates vendored plugin code, drifts on plugin upgrades, and conflicts with serverless-wsgi copying/cleaning the same path during `package` (cleanup would delete the committed file).
- *Alternative: run `serverless wsgi install` before `serverless offline`*. Rejected. It's two commands, it leaves artifacts behind (no end hook), and it's easy to forget.
- *Alternative: point `handler` at a hand-written module using `serverless_wsgi` from pip*. Rejected. It changes the deployed handler path, which is out of scope.

### D2: Gitignore the three generated artifacts at the repo root
Add `/wsgi_handler.py`, `/serverless_wsgi.py` and `/.serverless-wsgi` under the existing "Serverless Framework" block. Anchor them to the root, because `packageRootPath` is the service root (no `package.individually`).

### D3: Add a uv `dev` dependency group mirroring `requirements.txt` pins
`uv add --group dev flask==3.1.3 werkzeug==3.1.3`. A dependency group isn't part of the project's runtime deps. The Lambda package is unaffected either way, because `custom.pythonRequirements` uses `requirements.txt` with `useUv: false`.

- *Alternative: document `pip install -r requirements.txt` only*. Rejected. It's the current state and is wiped by `uv sync`.

## Risks / Trade-offs

- [A developer still types bare `serverless offline`] → The README states it explicitly and shows the error it produces. The npm script is the advertised path.
- [Abnormal termination (kill -9) skips the end hook and leaves shims in the root] → They're gitignored (D2) and get overwritten on the next start. `serverless wsgi clean` removes them manually.
- [Pins in `pyproject.toml` and `requirements.txt` drift apart] → The README notes that both must be bumped together. The duplication is small (two packages).
- [`.venv` not active when starting] → serverless-offline falls back to `python3` on `PATH`, which may not have Flask. The README instructs running from an activated venv, or with `uv run npm run offline`.
