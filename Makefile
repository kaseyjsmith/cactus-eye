VENV := ~/.venvs/data_stuffs

start:
	$(VENV)/bin/uvicorn main:app --reload

start_api:
	$(VENV)/bin/uvicorn src.api.routes:app --reload

fetch_image_loop:
	$(VENV)/bin/python -m src.scripts.img_fetch_loop



