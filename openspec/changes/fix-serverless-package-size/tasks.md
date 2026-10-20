## 1. serverless.yml configuration

- [x] 1.1 Under `custom.pythonRequirements`, set `fileName: requirements.txt`, `useUv: false`, `usePoetry: false` (D1). Verify that `serverless package` logs show requirements read from `requirements.txt`, with no "Parsed requirements.txt from uv.lock" message.
- [x] 1.2 Set `custom.wsgi.packRequirements: false` and fix its comment (D2). Verify that `src/.requirements/` is not recreated after `serverless package`.
- [x] 1.3 Change `functions.api.handler` to `wsgi_handler.handler` (D3). Verify it matches the `wsgi_handler.py` location shown by `unzip -l .serverless/oracle.zip`.
- [x] 1.4 Replace `package.patterns` with the explicit list from D4. Verify that the zip contains no `__pycache__`, `.pyc`, `CLAUDE.md` or `.requirements` entries, and no top-level files other than `src/` plus the wsgi shims and installed requirements.

## 2. Cleanup

- [x] 2.1 Delete the generated `src/.requirements/` and `.serverless/` directories. Verify with `ls` that both are gone.
- [x] 2.2 Add `.serverless/` and `src/.requirements/` to `.gitignore`. Verify that `git status` no longer lists them as untracked.

## 3. Verification and docs

- [x] 3.1 Run `serverless package` and check the size. `unzip -l .serverless/oracle.zip | tail -1` must report well under 262,144,000 bytes (expected a few MB), and `unzip -l … | grep -E 'gradio|langchain|chromadb'` must return nothing.
- [x] 3.2 Run `serverless deploy` (requires the user's AWS profile/session; the user may need to run it). Verify that the deploy succeeds and that `curl <endpoint>/` and `curl <endpoint>/hello` return the expected JSON messages.
- [x] 3.3 Update `README-SERVERLESS.md` with a short note: Lambda dependencies come only from `requirements.txt` (not `pyproject.toml`/`uv.lock`), and run `serverless package` + the size check before deploying. Verify the section is present.
