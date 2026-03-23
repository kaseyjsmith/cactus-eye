import time
from src.service.cameras import CameraHandler
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# call get_latest_still every 30 seconds
# check if this image is the same as the last image

if __name__ == "__main__":
    # handler = CameraHandler()

    base_url = "http://localhost:8000"
    # # get the new image every 10 minutes
    run = True
    while run:
        session = requests.Session()
        retries = Retry(
            total=10, backoff_factor=1, status_forcelist=[500, 502, 503, 504]
        )
        session.mount("http://", HTTPAdapter(max_retries=retries))
        latest = session.get(f"{base_url}/1209/latest")
        requests.post(f"{base_url}/1209/save", data=latest.content)
        # handler.get_latest_still("1209", save=True)
        time.sleep(60)
