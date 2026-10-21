from fastapi import FastAPI
from app.api_handler import fetch_datasets


app = FastAPI(title="Energy Data Service")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"service": "Energy Data Service"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/datasets")
def raw_dataset():
    return fetch_datasets()


