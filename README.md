# Python Task Manager

A console-based task management application written in Python. It supports task creation, viewing, editing, completion, and deletion, with JSON persistence so changes survive application restarts.

This project is a learning and portfolio exercise in Python software engineering, testing, error handling, and separation of concerns. Database storage, a FastAPI REST API, and AI features are planned extensions, not current functionality.

## Requirements

- Python 3.10 or newer
- [pytest](https://docs.pytest.org/) to run the tests

The application itself uses the Python standard library and does not require third-party runtime packages.

## Getting started

Clone the repository and change into the project directory:

```bash
git clone https://github.com/mikehoe/task-manager.git
cd task-manager
```

Run the CLI from the project root:

```bash
python cli.py
```

On systems where Python is invoked as `python3`, use `python3 cli.py` instead.

## Features

- Add tasks with automatically assigned IDs.
- List tasks and see their completion status.
- Mark tasks as completed.
- Edit task titles.
- Delete tasks.
- Save changes to JSON after successful create, complete, edit, and delete operations.
- Restore saved tasks and continue assigning unique IDs when the application starts again.
- Reject empty or whitespace-only task titles.
- Report errors for invalid saved data or failed file operations.

The interactive menu offers six choices: add, list, complete, delete, edit, and exit.

## Task model

Each task is represented by a `Task` dataclass with:

| Field | Type | Description |
| --- | --- | --- |
| `id` | `int` | Positive, unique task identifier |
| `title` | `str` | Non-empty task title |
| `completed` | `bool` | Completion status; defaults to `False` |

The CLI displays tasks as a numbered list with `[ ]` for incomplete tasks and `[x]` for completed tasks. Menu selection uses the displayed list number, which is not necessarily the task's ID.

## JSON persistence

The application reads from and writes to `tasks.json` in the **current working directory**. Run it from the project root if you want the file there.

- If `tasks.json` is missing, the application starts with an empty task list.
- Changes are saved immediately after each successful modification.
- Saving writes a temporary file and replaces the destination file, with temporary-file cleanup.
- Loading validates the JSON structure, required fields, data types, positive IDs, and duplicate IDs.
- Invalid or unreadable saved data cause an error message and prevent the CLI from starting its interactive menu.
- An I/O error while saving is reported and causes the CLI to exit.
- `/tasks.json` is excluded from Git via `.gitignore`.

Example storage format:

```json
[
    {
        "id": 1,
        "title": "Learn Python",
        "completed": false
    },
    {
        "id": 2,
        "title": "Write tests",
        "completed": true
    }
]
```

## Project structure

```text
cli.py                            # Console interface and persistence coordination
models/task.py                    # Task dataclass
services/task_service.py          # Task operations, validation, and ID generation
persistence/json_storage.py       # JSON serialization, loading, and saving
tests/                            # Unit and integration tests
```

The CLI creates `JsonStorage`, loads saved tasks into `TaskService`, and saves changes after successful operations. `TaskService` manages task behavior and in-memory state; `JsonStorage` handles file persistence.

## Running tests

Install pytest in your preferred Python environment:

```bash
python -m pip install pytest
```

Run the full test suite from the project root:

```bash
python -m pytest -v
```

The tests cover task operations, title validation, JSON load/save behavior, malformed data, ID continuity, restarts, CLI workflows, and simulated file-operation failures. They use pytest fixtures such as `tmp_path`, `monkeypatch`, and `capsys` to isolate test data and simulate interactions.

## Roadmap

The current CLI application and basic JSON persistence are implemented. Potential next steps include:

- SQLite and PostgreSQL persistence
- FastAPI REST API
- Docker and deployment
- AI-powered functionality

These items are planned, not implemented.
