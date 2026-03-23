import requests
import os
import cv2
from datetime import datetime
import numpy as np
from dotenv import load_dotenv

load_dotenv()


class CameraHandler:
    def __init__(self):
        self.api_key = os.getenv("AZ511_API_KEY")
        self.previous_content = b""
        self.latest_content = b""

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

    def get_latest_still(self, camera_id, show=False, save=False):
        # print(f"https://az511.com/map/Cctv/{camera_id}")
        latest = requests.get(f"https://az511.com/map/Cctv/{camera_id}")
        if latest is not None:
            if self.latest_content is not None:
                # TODO: Check if previous is the same as latest, notify if it
                # is and don't duplicate save
                self.previous_content = self.latest_content
                self.latest_content = latest.content

            if show:
                self._show(camera_id, self.latest_content)

            if save:
                self._save_to_dir(camera_id, self.latest_content)

        return latest

    def get_cameras(self):
        # https://www.az511.com/help/endpoint/cameras?{self.api_key}
        results = requests.get(
            f"https://www.az511.com/help/endpoint/cameras?{self.api_key}"
        )
        return results

    def get_available_camearas(self):
        pass
