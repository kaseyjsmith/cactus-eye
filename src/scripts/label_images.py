"""
My goal is to learn to build an object detection model,
and less so to learn labeling tools. For now, I'm
going to use an existing model to give me labels on the
vehicles that I can train on.

Later, it may be interesting to compare my model to the model
I use here for labeling.
"""

from ultralytics import YOLO
from ultralytics.engine.results import Results
from pathlib import Path


class Processor:
    def __init__(self, img_dir: Path):
        self.img_dir = img_dir
        self.results = []
        self.processed_imgs = []
        self.model = YOLO("yolo11x.pt")

    def process(self, verbose=False):
        for file in self.img_dir.glob("*.jpg"):
            if verbose:
                print(f"Processing: {file}")
            result = self.model.predict(file, verbose=False)
            self.results.append(result)
            for idx, r in enumerate(result):
                if r.boxes.__len__() > 0:
                    self._write_boxes(r, file, verbose=verbose)

    def _write_boxes(self, result: Results, file: Path, verbose=False):
        cls = result.boxes.cls
        xywh = result.boxes.xywh
        if len(cls) == len(xywh):
            rows = []
            for idx, c in enumerate(cls):
                rows.append(
                    f"{int(c)} {' '.join(str(v) for v in xywh[idx].tolist())}"
                )
        with open(f"data/1209/train_labels/{file.name[:-4]}.txt", "w") as f:
            for row in rows:
                f.write(row + "\n")
                if verbose:
                    print(row)


if __name__ == "__main__":
    p = Processor(Path("data/1209"))
    p.process(verbose=True)
