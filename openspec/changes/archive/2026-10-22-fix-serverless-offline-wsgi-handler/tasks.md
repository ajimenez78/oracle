## 1. Local start command

- [ ] 1.1 Add `"scripts": { "offline": "serverless offline start" }` to `package.json`. Verify that `npm run offline` (with `.venv` active) logs "Packaging Python WSGI handler..." and creates `wsgi_handler.py` in the repo root
- [ ] 1.2 With `npm run offline` running, `curl localhost:3000/dev/`, `/dev/hello` and `/dev/does-not-exist`. Verify the responses are 200 `{"message":"Hello from root!"}`, 200 `{"message":"Hello from path!"}` and 404 `{"error":"Not found!"}`, with no `ModuleNotFoundError` in the logs
- [ ] 1.3 Stop with Ctrl+C. Verify that `wsgi_handler.py`, `serverless_wsgi.py` and `.serverless-wsgi` are gone from the repo root

## 2. Git hygiene

- [ ] 2.1 Add `/wsgi_handler.py`, `/serverless_wsgi.py` and `/.serverless-wsgi` to the "Serverless Framework" block in `.gitignore`. Verify by running `serverless wsgi install` (which creates them), confirming that `git status` doesn't list them, then running `serverless wsgi clean`

## 3. Local Python environment

- [ ] 3.1 Run `uv add --group dev flask==3.1.3 werkzeug==3.1.3`. Verify that `pyproject.toml` has a `[dependency-groups] dev` entry and `uv.lock` is updated
- [ ] 3.2 Run `uv sync`, then repeat task 1.2. Verify the root path still returns 200
- [ ] 3.3 Run `serverless package && unzip -l .serverless/oracle.zip | grep -iE 'gradio|langchain|chromadb'`. Verify there's no output (the package is still derived only from `requirements.txt`)

## 4. Documentation

- [ ] 4.1 Add a "Run locally with serverless-offline" section to `README-SERVERLESS.md`. It should cover `uv sync`, activating `.venv` (or `uv run npm run offline`), `npm run offline`, the example curl URLs, a warning that bare `serverless offline` fails with `No module named 'wsgi_handler'`, `serverless wsgi clean` for leftover shims, and keeping Flask/Werkzeug pins in sync between `pyproject.toml` and `requirements.txt`. Verify by following the section from a fresh shell and reproducing the responses in task 1.2
