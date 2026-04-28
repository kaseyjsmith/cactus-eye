"""
I need to resturcutre the images data to be ready for
torchvision.datasets.ImageFolder

Current structure
data/1209/
    train/
        img1.jpg
        img2.jpg
    train_labels/
        # YOLO formatted label files
        img1.txt
        img2.txt

New structure
data/1209/binary
    vehicle/
        img1.jpg
        img3.jpg
    no_vehicle/
        img2.jpg
        img4.jpg
"""

import shutil
from pathlib import Path

# get filenames without extensions from /data/1209/train_labels
dir = "data/1209/train"
p = Path(dir)
for file in p.glob("*"):
    name = file.name[:-4]
    if Path(f"data/1209/train_labels/{name}.txt").exists():
        # print(f"{dir}/{name}")
        shutil.copy(f"data/1209/train/{name}.jpg", "data/1209/binary/vehicle/")
    else:
        shutil.copy(
            f"data/1209/train/{name}.jpg", "data/1209/binary/no_vehicle/"
        )

    # print(f"{name}.jpg exists")
    # print(file.name[:-4])

# move all {filename}.jpg in data/1209/train/ to data/1209/binary/vehicle

# move all others to data/1209/binary/vehicle
