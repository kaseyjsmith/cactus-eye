import logging
from datetime import datetime
from io import BytesIO
from src.service.cameras import CameraHandler

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.requests import Request

app = FastAPI(title="AZ511 Object Detection API", version="0.0.1")

file_handler = logging.FileHandler("log/server.log")
file_handler.setFormatter(
    logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
)
logging.getLogger("uvicorn").addHandler(file_handler)
logging.getLogger("uvicorn.access").addHandler(file_handler)
logger = logging.getLogger("uvicorn")

handler = CameraHandler()


@app.get("/favicon.ico")
async def favicon():
    return ""


@app.get("/health")
async def health():
    return {"up": "true", "datetime": datetime.now()}


@app.get("/cameras")
async def get_cameras():
    """
    Gets all cameras, regardless of availability
    """
    pass


@app.get("/available_cameras")
async def get_available_cameras():
    """
    Gets all available cameras that are currently working
    """
    # call available cameras service
    pass


@app.get("/{camera_id}/latest")
async def get_latest_still(camera_id):
    latest = handler.get_latest_still(camera_id)
    logger.info(f"Got latest still from camera id: {camera_id}")
    return StreamingResponse(BytesIO(latest.content), media_type="image/jpeg")


@app.post("/{camera_id}/save")
async def save_image(camera_id: str, request: Request):
    content = await request.body()
    file = handler._save_to_dir(camera_id, content)
    logger.info(f"Saved posted image to: {file}")
    return {"status": "saved", "camera_id": camera_id, "file": file}
