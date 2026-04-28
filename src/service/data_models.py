from dataclasses import dataclass
from datetime import datetime


@dataclass
class CameraDetails:
    view_id: int
    view_url: str
    view_status: str
    view_desc: str
    base_id: int
    source: str
    source_id: str
    roadway: str
    direction: str
    latitude: float
    longitude: float
    location: str
    last_updated: datetime
