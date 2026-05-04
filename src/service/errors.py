from fastapi import HTTPException


def check_url(url):
    if url is None:
        raise HTTPException(
            status_code=404, detail=f"Camera view {view_id} not found"
        )
