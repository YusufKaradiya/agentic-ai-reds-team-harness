import json
import sqlite3
from pathlib import Path


class Database:

    def __init__(self, db_path="data/redteam.db"):

        Path(db_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.db_path = db_path
        self.initialize()

    def get_connection(self):

        return sqlite3.connect(
            self.db_path
        )

    def initialize(self):

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            attack_id TEXT,
            attack_name TEXT,
            category TEXT,
            severity TEXT,
            mode TEXT,
            status TEXT,
            decision TEXT,
            attack_success INTEGER,
            false_block INTEGER,
            data_leakage INTEGER,
            tool_called INTEGER,
            llm_called INTEGER,
            llm_model TEXT,
            llm_latency_ms REAL,
            latency_ms REAL,
            risk_score REAL,
            detection_count INTEGER,
            detection_ids TEXT,
            created_at TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_events (
            event_id TEXT PRIMARY KEY,
            run_id TEXT,
            event_type TEXT,
            component TEXT,
            decision TEXT,
            reason TEXT,
            metadata TEXT,
            created_at TEXT
        )
        """)

        connection.commit()
        connection.close()

    def insert_run(
        self,
        run: dict | None = None,
        **fields
    ):

        run = {
            "mode": "",
            "false_block": False,
            "llm_called": False,
            "llm_model": "",
            "llm_latency_ms": 0.0,
            "risk_score": 0.0,
            "detection_count": 0,
            "detection_ids": [],
            **(run or {}),
            **fields,
        }

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
    INSERT INTO runs (
        run_id,
        attack_id,
        attack_name,
        category,
        severity,
        mode,
        status,
        decision,
        attack_success,
        false_block,
        data_leakage,
        tool_called,
        llm_called,
        llm_model,
        llm_latency_ms,
        latency_ms,
        risk_score,
        detection_count,
        detection_ids,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    run["run_id"],
    run["attack_id"],
    run["attack_name"],
    run["category"],
    run["severity"],
    run["mode"],
    run["status"],
    run["decision"],
    int(run["attack_success"]),
    int(run["false_block"]),
    int(run["data_leakage"]),
    int(run["tool_called"]),
    int(run["llm_called"]),
    run["llm_model"],
    run["llm_latency_ms"],
    run["latency_ms"],
    run["risk_score"],
    run["detection_count"],
    json.dumps(run.get("detection_ids", [])),
    run["created_at"],
))

        connection.commit()
        connection.close()

    def insert_event(self, event: dict):

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO audit_events (
                event_id,
                run_id,
                event_type,
                component,
                decision,
                reason,
                metadata,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event["event_id"],
            event["run_id"],
            event["event_type"],
            event["component"],
            event.get("decision"),
            event.get("reason"),
            json.dumps(event.get("metadata", {})),
            event["created_at"],
        ))

        connection.commit()
        connection.close()

    def get_runs(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM runs
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        connection.close()

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    def get_events(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM audit_events
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        connection.close()

        return [
            dict(zip(columns, row))
            for row in rows
        ]