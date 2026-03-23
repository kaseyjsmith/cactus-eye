# Project Overview

I want to understand object detection ML models and how to build them. Namely, this is three parts:

1. Object detection in static images
2. Object detection in video (prerecorded)
3. Object detection in live video

# Specifics

1. I want to build my own detection
2. I want to be able to deploy this detection
   a. This isn't just a notebook. I want a model that I can run.

# Use Cases

1. Compile a dataset of types of vehicles that travel on the 24
2. When a certain car is seen, notify user
   a. Refine to be during a specific time of the day

# Build Process

- Built API to fetch images to build dataset (FastAPI)
- Used pretrained model to generate label files for training
  - My goal is to learn the inner workings of object detection, less so to label images.
