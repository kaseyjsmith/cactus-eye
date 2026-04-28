import logging
from contextlib import asynccontextmanager
from datetime import datetime
from io import BytesIO
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from fastapi.responses import FileResponse, StreamingResponse

from src.service.camera_sync import sync_cameras
from src.service.cameras import CameraHandler
from src.service.database import DatabaseManager

TEMPLATES_DIR = Path(__file__).parent / "templates"


@asynccontextmanager
async def lifespan(app: FastAPI):
    sync_cameras()
    yield


app = FastAPI(
    title="AZ511 Object Detection API", version="0.0.1", lifespan=lifespan
)

file_handler = logging.FileHandler("log/server.log")
file_handler.setFormatter(
    logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
)
logging.getLogger("uvicorn").addHandler(file_handler)
logging.getLogger("uvicorn.access").addHandler(file_handler)
logger = logging.getLogger("uvicorn")

handler = CameraHandler()
db = DatabaseManager()


@app.get("/favicon.ico")
async def favicon():
    return ""


@app.get("/health")
async def health():
    return {"up": "true", "datetime": datetime.now()}


@app.get("/")
async def index():
    return FileResponse(TEMPLATES_DIR / "index.html")


@app.get("/cameras")
async def get_cameras():
    """
    Gets all cameras, regardless of availability
    """
    return db.list_cameras()


@app.get("/available_cameras")
async def get_available_cameras():
    """
    Gets all available cameras that are currently working
    """
    # call available cameras service
    pass


@app.get("/{view_id}/latest")
async def get_latest_still(view_id: int):
    url = db.get_view_url(view_id)
    if url is None:
        raise HTTPException(
            status_code=404, detail=f"Camera view {view_id} not found"
        )
    content = handler.get_latest_still(view_id, url)
    logger.info(f"Got latest still from view id: {view_id}")
    return StreamingResponse(BytesIO(content), media_type="image/jpeg")


@app.post("/{camera_id}/save")
async def save_image(camera_id: str, request: Request):
    content = await request.body()
    file = handler._save_to_dir(camera_id, content)
    logger.info(f"Saved posted image to: {file}")
    return {"status": "saved", "camera_id": camera_id, "file": file}
