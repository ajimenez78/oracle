## Purpose

Lets developers run the serverless `api` Lambda function locally behind an emulated API Gateway, so they can exercise the Flask app through the same handler path used in AWS before deploying.

## ADDED Requirements

### Requirement: Single local start command
The project SHALL provide one documented command that starts the local API Gateway emulation for the `api` function, and requests to it SHALL reach the Flask application through the deployed handler entry point (`wsgi_handler.handler`).

#### Scenario: Root path responds locally
- **WHEN** a developer runs the documented local start command and sends `GET http://localhost:3000/dev/`
- **THEN** the response is HTTP 200 with body `{"message": "Hello from root!"}`

#### Scenario: Proxied path responds locally
- **WHEN** the local emulation is running and a developer sends `GET http://localhost:3000/dev/hello`
- **THEN** the response is HTTP 200 with body `{"message": "Hello from path!"}`

#### Scenario: Unknown path returns app-level 404
- **WHEN** the local emulation is running and a developer sends `GET http://localhost:3000/dev/does-not-exist`
- **THEN** the response is HTTP 404 with body `{"error": "Not found!"}`

#### Scenario: No handler import error
- **WHEN** any request is served by the local emulation
- **THEN** the Python process does not fail with `ModuleNotFoundError: No module named 'wsgi_handler'`

### Requirement: Generated handler artifacts are transient and untracked
The WSGI handler shim files generated for local runs (`wsgi_handler.py`, `serverless_wsgi.py`, `.serverless-wsgi`) SHALL be removed from the service root when the local emulation shuts down normally, and SHALL be ignored by version control.

#### Scenario: Clean shutdown removes artifacts
- **WHEN** a developer stops the local emulation with Ctrl+C
- **THEN** `wsgi_handler.py`, `serverless_wsgi.py` and `.serverless-wsgi` no longer exist in the service root

#### Scenario: Leftover artifacts are not committable
- **WHEN** the local emulation is killed abnormally and the artifacts remain in the service root
- **THEN** `git status` does not list them as untracked files

### Requirement: Reproducible local Python environment
The project's local Python environment definition SHALL include the packages the `api` function needs at runtime, with the same versions as the Lambda requirements. Syncing the environment SHALL NOT remove them, and they SHALL NOT be added to the deployed Lambda package beyond what `requirements.txt` declares.

#### Scenario: Environment sync keeps runtime deps
- **WHEN** a developer runs `uv sync` and then the local start command
- **THEN** the Flask app imports successfully and the root path responds with HTTP 200

#### Scenario: Lambda package unchanged
- **WHEN** a developer runs `serverless package`
- **THEN** the packaged dependencies are derived only from `requirements.txt`, as before this change
