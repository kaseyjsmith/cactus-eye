VENV := .venv

setup:
	$(VENV) -m src.scripts.create_databases

start:
	$(VENV)/bin/uvicorn main:app --reload

start_api:
	$(VENV)/bin/uvicorn src.api.routes:app --reload

fetch_image_loop:
	$(VENV) -m src.scripts.img_fetch_loop



