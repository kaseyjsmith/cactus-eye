from ultralytics import YOLO
import numpy as np
import cv2

model = YOLO("yolo26n.pt")


def get_prediction(img, save=False):
    if img is not None:
        # img is expected as Python bytes
        arr = np.frombuffer(img, np.uint8)  # convert to np array
        # decode to BGR 2D arr
        decoded_img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        # predict on the decoded
        results = model.predict(source=decoded_img, conf=0.1, save=save)
        # returns numpy.ndarray encoded as jpg
        plot_img = results[0].plot()
        return cv2.imencode(".jpg", plot_img)[1].tobytes()
    else:
        return {"message": "Error predicting on image"}


if __name__ == "__main__":
    import sys

    get_prediction(sys.argv[1], save=True)
