from datetime import datetime, timedelta, timezone

from src.service.cameras import CameraHandler
from src.service.database import DatabaseManager

STALENESS_THRESHOLD = timedelta(days=7)


def sync_cameras() -> None:
    db = DatabaseManager()
    last_updated = db.get_cameras_last_updated()
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    if last_updated is not None and now - last_updated < STALENESS_THRESHOLD:
        return

    handler = CameraHandler()
    cameras = handler.get_cameras(output="object_list")
    db.upsert_cameras(cameras)
