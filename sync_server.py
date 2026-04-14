from fastapi import FastAPI, HTTPException

from backend import import_sync_payload


app = FastAPI(title="Pigilan Sync Server", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/sync/push")
def sync_push(payload: dict):
    try:
        result = import_sync_payload(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result
