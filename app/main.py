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
def data_filter():
    data_set = fetch_datasets()["datasets"]
    filtered_ds = {"datasets": []}

    for ds in data_set:
        filtered_ds["datasets"].append({"id": ds["id"],
                                        "name": ds["name"],
                                        "description": ds["description"]})

    return filtered_ds



