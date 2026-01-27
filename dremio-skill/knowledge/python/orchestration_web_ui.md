# Orchestration Web UI

`dremioframe` includes a lightweight Web UI to visualize pipeline runs and task statuses.

## Features

- **Dashboard**: View all pipelines and their recent runs.
- **Real-time Updates**: Auto-refreshing status of tasks and runs.
- **Manual Trigger**: Trigger pipeline runs directly from the UI.
- **Task Status**: Visual indicators for task success, failure, and skipping.

## Starting the UI

You can start the UI from your Python script:

```python
from dremioframe.orchestration import start_ui, Pipeline
from dremioframe.orchestration.backend import SQLiteBackend

# Setup backend and pipelines
backend = SQLiteBackend("history.db")
pipeline1 = Pipeline("etl_job", backend=backend)
pipeline2 = Pipeline("maintenance", backend=backend)

# Start UI
# Pass the pipelines dict to enable manual triggering
start_ui(backend=backend, pipelines={"etl_job": pipeline1, "maintenance": pipeline2}, port=8080)
```

Visit `http://localhost:8080` in your browser.

## Security

The UI supports Basic Authentication.

### Enabling Authentication

Pass `username` and `password` to `start_ui` or via the CLI.

```python
from dremioframe.orchestration.ui import start_ui

start_ui(backend, port=8080, username="admin", password="secret_password")
```

### CLI Usage

(CLI support for auth args is pending, currently only via python script or hardcoded in custom entrypoint)
*Note: The `dremio-cli pipeline ui` command does not yet expose auth flags, but you can wrap `start_ui` in your own script.*

## Architecture

The UI is a Single Page Application (SPA) built with **Vue.js** (loaded via CDN). It communicates with the Python backend via a simple REST API:

- `GET /api/runs`: List recent pipeline runs.
- `GET /api/pipelines`: List available pipelines.
- `POST /api/pipelines/{name}/trigger`: Trigger a new run.
nd
backend = SQLiteBackend("pipeline.db")

