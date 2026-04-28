# Build Object Detection Model From Scratch

Goal: build a YOLO v1-style single-shot detector to understand how object detection works
under the hood, then iterate toward modern improvements.

Hardware note: AMD Radeon 880M iGPU (no ROCm support on Linux). Training on CPU.
32GB system RAM. PyTorch installed (cu126 build, but running CPU-only).

## Stages

- **Stage 1**: Detect "vehicle" (single class) on any AZ511 camera image, mAP@0.5 >= 0.80
- **Stage 2**: Classify vehicle types (car, truck, motorcycle, bus, etc.)
- **Stage 3**: Predict vehicle make and model. Process all ~1200 cameras in <60 seconds.

---

## Phase 0 — Foundations Refresh

- [x] Implement 2D convolution forward pass by hand (comfortable)
- [x] Remove images in data/1209/ (moved to data/1209/train)
- [x] Restructure training images dir to utilize `torchvision.datasets.ImageFolder`

```
  data/1209/binary/
    vehicle/
      img1.jpg
      img2.jpg
    no_vehicle/
      img3.jpg
      img4.jpg
```

- [x] Build binary image classifier with full PyTorch training loop (comfortable)
- [x] **Visualize intermediate feature maps** from a CNN on camera images
  - Load a pretrained model (or build a small one), hook into intermediate layers
  - Plot feature maps at early vs deep layers
  - Goal: see that early layers = edges/textures, deep layers = vehicle-like shapes

## Phase 1 — From Classification to Detection

- [ ] **Read the YOLO v1 paper** ([Redmon et al. 2016](https://arxiv.org/abs/1506.02640))
  - Focus on: grid cells, bounding box parameterization (x, y, w, h, confidence), loss function
- [ ] **Implement IoU from scratch**
  - Given two boxes as (x, y, w, h), compute their overlap
  - This is the core metric for evaluating box predictions
- [ ] **Implement NMS (Non-Maximum Suppression) from scratch**
  - Given predicted boxes + confidence scores, suppress overlapping duplicates
  - This is how detectors go from noisy guesses to clean output
- [ ] **Understand anchor boxes / grid cells visually**
  - Draw a 7x7 grid over a camera 1209 image
  - For each cell, draw what bounding box it would be "responsible" for predicting
  - Goal: understand detection as regression over a spatial grid

## Phase 2 — Build the Detector

- [ ] **Prepare the dataset**
  - Collapse YOLO labels to single "vehicle" class
  - Split into train/val/test
  - Write a PyTorch `Dataset` class (image + label → tensors)
  - Handle coordinate normalization (YOLO format is already 0-1 normalized)
- [ ] **Design the CNN backbone**
  - Small feature extractor: 6-8 conv layers, batch norm, max pooling
  - Input: 448x448x3 → Output: 7x7xD feature map
  - This is the "seeing" part of the model
- [ ] **Design the detection head**
  - Takes 7x7xD feature map → outputs 7x7x(B\*5 + C)
  - B=2 boxes/cell, 5=(x, y, w, h, conf), C=1 class → 7x7x11
  - This is the "deciding" part of the model
- [ ] **Implement the YOLO v1 loss function**
  - Localization loss: MSE on (x, y) and (√w, √h) for responsible predictors
  - Confidence loss: MSE on objectness (weighted differently for obj vs no-obj cells)
  - Classification loss: MSE on class probabilities (trivial w/ 1 class, but build to generalize)
  - "Responsible predictor" assignment: box with highest IoU to ground truth owns it
- [ ] **Write the training loop**
  - Optimizer (SGD w/ momentum or Adam), LR schedule, loss logging
  - Overfit on 10 images first to validate the full pipeline
  - Then scale to full dataset
- [ ] **Write inference + visualization pipeline**
  - Model output → confidence threshold → NMS → draw boxes on image
  - Test on real camera frames

## Phase 3 — Evaluation and Iteration

- [ ] **Implement mAP calculation**
  - Precision-recall curve at different IoU thresholds
  - Area under the curve → mAP@0.5
  - Target: >= 0.80
- [ ] **Error analysis**
  - Categorize failures: missed small/distant vehicles? Edge-of-frame misses? False positives?
  - This determines what to improve next
- [ ] **Data augmentation for detection**
  - Horizontal flips, color jitter, random crops
  - Must transform bounding boxes alongside the image
- [ ] **Collect data from more cameras**
  - Different cameras = different angles, lighting, vehicle sizes
  - Needed to generalize beyond camera 1209

## Phase 4 — Modern Improvements

- [ ] **ResNet-style backbone with skip connections**
  - Replace vanilla CNN backbone
  - Understand why: vanishing gradients in deeper networks
- [ ] **Feature Pyramid Network (FPN)**
  - Detect at multiple scales by fusing features from different backbone depths
  - Addresses the "misses distant vehicles" problem from YOLO label audit
- [ ] **Anchor-free prediction** (FCOS / CenterNet style)
  - Predict object center + regress distances to box edges
  - Modern YOLO v8+ are anchor-free — this bridges to understanding current YOLO
- [ ] **Optimize for speed**
  - Batch inference across cameras
  - FP16 quantization
  - TorchScript or ONNX export
  - Profile and find bottlenecks — target: 1200 images in <60s
