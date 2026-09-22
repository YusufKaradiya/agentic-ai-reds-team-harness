import sqlite3
from threading import RLock
from pathlib import Path


class Database:
	"""Creates and manages the local SQLite database connection."""

	def __init__(self, database_path: Path | str | None = None):
		project_root = Path(__file__).resolve().parent.parent
		self.database_path = Path(database_path or project_root / "data" / "redteam.db")
		self.database_path.parent.mkdir(parents=True, exist_ok=True)
		self._lock = RLock()
		self.connection = sqlite3.connect(
			self.database_path,
			check_same_thread=False,
		)
		self.connection.row_factory = sqlite3.Row
		self._initialize_schema()

	def _initialize_schema(self) -> None:
		with self._lock:
			self.connection.executescript(
				"""
			CREATE TABLE IF NOT EXISTS runs (
				run_id TEXT PRIMARY KEY,
				attack_id TEXT NOT NULL,
				attack_name TEXT NOT NULL,
				category TEXT NOT NULL,
				severity TEXT NOT NULL,
				status TEXT NOT NULL,
				decision TEXT NOT NULL,
				attack_success INTEGER NOT NULL,
				data_leakage INTEGER NOT NULL,
				tool_called INTEGER NOT NULL,
				latency_ms REAL NOT NULL,
				created_at TEXT NOT NULL
			);

			CREATE TABLE IF NOT EXISTS events (
				event_id TEXT PRIMARY KEY,
				run_id TEXT NOT NULL,
				event_type TEXT NOT NULL,
				component TEXT NOT NULL,
				decision TEXT,
				reason TEXT,
				metadata TEXT NOT NULL,
				created_at TEXT NOT NULL
			);
				"""
			)
			self.connection.commit()

	def insert_run(self, **run: object) -> None:
		columns = ", ".join(run)
		placeholders = ", ".join("?" for _ in run)
		with self._lock:
			self.connection.execute(
				f"INSERT INTO runs ({columns}) VALUES ({placeholders})",
				tuple(run.values()),
			)
			self.connection.commit()

	def insert_event(self, **event: object) -> None:
		columns = ", ".join(event)
		placeholders = ", ".join("?" for _ in event)
		with self._lock:
			self.connection.execute(
				f"INSERT INTO events ({columns}) VALUES ({placeholders})",
				tuple(event.values()),
			)
			self.connection.commit()

	def get_runs(self, limit: int = 50) -> list[dict[str, object]]:
		with self._lock:
			rows = self.connection.execute(
				"SELECT * FROM runs ORDER BY created_at DESC LIMIT ?",
				(limit,),
			)
			return [dict(row) for row in rows.fetchall()]

	def get_events(self, limit: int = 100) -> list[dict[str, object]]:
		with self._lock:
			rows = self.connection.execute(
				"SELECT * FROM events ORDER BY created_at DESC LIMIT ?",
				(limit,),
			)
			return [dict(row) for row in rows.fetchall()]

	def close(self) -> None:
		with self._lock:
			self.connection.close()
