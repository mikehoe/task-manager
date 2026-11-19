import sqlite3
from pathlib import Path

from models.task import Task


class SQLiteTaskRepository:

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = Path(db_path)

    def initialize(self) -> None:
        connection = sqlite3.connect(self._db_path)

        try:
            with connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL CHECK (length(trim(title)) > 0),
                        completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0, 1))
                    );
                    """
                )
        finally:
            connection.close()

    def create(self, title: str) -> Task:
        ...

    def get_by_id(self, task_id: int) -> Task | None:
        ...

    def list_all(self) -> list[Task]:
        ...

    def delete(self, task_id: int) -> bool:
        ...

    def update(self, task: Task) -> bool:
        ...
