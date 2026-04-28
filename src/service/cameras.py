import requests
import os
import cv2
import json
from datetime import datetime, timezone
from typing import List
import numpy as np
from dotenv import load_dotenv
from src.service.data_models import CameraDetails

load_dotenv()


class CameraHandler:
    def __init__(self):
        self.api_key = os.getenv("AZ511_API_KEY")
        self.api_url = "https://az511.com/api/v2/get/cameras"

    def _save_to_dir(self, camera_id, latest_content: bytes):
        # make the dir if not there
        os.makedirs(f"data/{camera_id}", exist_ok=True)
        # save the bytes to a jpg
        file = f"data/{camera_id}/{camera_id}_{datetime.now().timestamp()}.jpg"
        with open(
            file,
            "wb",
        ) as f:
            f.write(latest_content)
        return file

    def _show(self, camera_id, latest_content: bytes):
        arr = np.frombuffer(latest_content, np.int8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        cv2.imshow(f"{camera_id}_{datetime.now().timestamp()}", img)
        cv2.waitKey(10)
        # cv2.destroyAllWindows()

    def _map_camera(self, cam: dict) -> List[CameraDetails]:
        """
        Takes in a camera and returns a list of CameraDetails objects.
        """
        cam_list = []
        for view in cam["Views"]:
            cam_list.append(
                CameraDetails(
                    view_id=view["Id"],
                    view_url=view["Url"],
                    view_status=view["Status"],
                    view_desc=view["Description"],
                    base_id=cam["Id"],
                    source=cam["Source"],
                    source_id=cam["SourceId"],
                    roadway=cam["Roadway"],
                    direction=cam["Direction"],
                    latitude=cam["Latitude"],
                    longitude=cam["Longitude"],
                    location=cam["Location"],
                    last_updated=datetime.now(timezone.utc).replace(
                        tzinfo=None
                    ),
                )
            )
        return cam_list

    def get_latest_still(self, view_id, url, show=False, save=False) -> bytes:
        content = requests.get(url).content
        if show:
            self._show(view_id, content)
        if save:
            self._save_to_dir(view_id, content)
        return content

    def get_cameras(self, output: str = "json"):
        # https://www.az511.com/help/endpoint/cameras?{self.api_key}
        results = requests.get(f"{self.api_url}/?key={self.api_key}")
        cameras_json = json.loads(results.content)
        if results.status_code == 200:
            if output == "json":
                return cameras_json
            elif output == "object_list":
                cam_list = []
                for cam in cameras_json:
                    cam_list.extend(self._map_camera(cam))
                return cam_list
            else:
                raise ValueError(
                    "Argument output must be one of: 'json' or 'object_list'"
                )

    def get_available_cameras(self):
        pass
