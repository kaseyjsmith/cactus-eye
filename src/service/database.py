import dataclasses
import os
from datetime import datetime
from typing import List, Optional

import duckdb

from src.service.data_models import CameraDetails


class DatabaseManager:
    def __init__(self):
        self.db_dir = "db/"

    def create_connection(self, db: str):
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        return duckdb.connect(database=f"{self.db_dir}{db}.duckdb")

    def _ensure_cameras_table(self, conn) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cameras (
                view_id INTEGER PRIMARY KEY,
                view_url VARCHAR,
                view_status VARCHAR,
                view_desc VARCHAR,
                base_id INTEGER,
                source VARCHAR,
                source_id VARCHAR,
                roadway VARCHAR,
                direction VARCHAR,
                latitude DOUBLE,
                longitude DOUBLE,
                location VARCHAR,
                last_updated TIMESTAMP
            )
            """
        )

    def list_cameras(self) -> List[dict]:
        conn = self.create_connection("cameras")
        try:
            self._ensure_cameras_table(conn)
            rows = conn.execute(
                "SELECT view_id, location FROM cameras ORDER BY location, view_id"
            ).fetchall()
            return [{"view_id": r[0], "location": r[1]} for r in rows]
        finally:
            conn.close()

    def get_view_url(self, view_id: int) -> Optional[str]:
        conn = self.create_connection("cameras")
        try:
            self._ensure_cameras_table(conn)
            row = conn.execute(
                "SELECT view_url FROM cameras WHERE view_id = ?", [view_id]
            ).fetchone()
            return row[0] if row else None
        finally:
            conn.close()

    def get_cameras_last_updated(self) -> Optional[datetime]:
        conn = self.create_connection("cameras")
        try:
            self._ensure_cameras_table(conn)
            row = conn.execute("SELECT MAX(last_updated) FROM cameras").fetchone()
            return row[0] if row else None
        finally:
            conn.close()

    def upsert_cameras(self, cameras: List[CameraDetails]) -> None:
        conn = self.create_connection("cameras")
        try:
            self._ensure_cameras_table(conn)
            rows = [dataclasses.astuple(c) for c in cameras]
            conn.execute("BEGIN TRANSACTION")
            try:
                conn.executemany(
                    "INSERT OR REPLACE INTO cameras VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    rows,
                )
                conn.execute("COMMIT")
            except Exception:
                conn.execute("ROLLBACK")
                raise
        finally:
            conn.close()
