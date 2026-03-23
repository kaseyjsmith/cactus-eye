# Questions

- [ ] The cameras are static. Do I need images of cars from multiple angles for testing?
  - [ ] If yes, can I source images from the internet of these angles and use that as part of training?

# Tasks

- [!] Get API key for AZ511 API
- [ ] Test AZ511 API
  - Get images from specific camera

- [x] implement retry logic and backoff factor to `img_fetch_loop`

# Vehicle Identification

- [ ] Detect vehicles (no model identification; just vehicle detection)
- [ ] ~Label vehicles (_can I get Claude to do this??_)~
- [x] Use YOLO ~or COCO~ model to get label files for images (script)
- [ ] Audit YOLO results (seems that it only picks up vehicles close to the camera)
- [ ] create files with box locations and classes for training
