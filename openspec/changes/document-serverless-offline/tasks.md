## 1. Documentation

- [x] 1.1 In `README-SERVERLESS.md`, under "Local development", add a "Run locally with serverless-offline" subsection. It should cover the prerequisites (`npm install`, an activated venv with `pip install -r requirements.txt`), the launch command `serverless offline start`, the check `curl http://localhost:3000/dev/hello` with the expected `{"message": "Hello from path!"}` response, a warning that bare `serverless offline` fails with `No module named 'wsgi_handler'`, and cleanup (Ctrl+C, or `serverless wsgi clean` for leftovers). Verify that the existing `serverless wsgi serve` instructions remain intact and the section renders correctly as Markdown

## 2. Verification

- [x] 2.1 Follow the new subsection from a fresh shell. Run `serverless offline start` and `curl http://localhost:3000/dev/hello`, and verify the response is HTTP 200 `{"message": "Hello from path!"}` with no `ModuleNotFoundError` in the server log
- [ ] 2.2 Stop the server with Ctrl+C. Verify that `wsgi_handler.py`, `serverless_wsgi.py` and `.serverless-wsgi` are no longer in the repo root, as the README states
