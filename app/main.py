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
    filtered_ds = []
    data_set = fetch_datasets()["datasets"]


    for ds in data_set:
        if ["id" in ds 
            and "name" in ds
            and "description" in ds]:
            filtered_ds.append(ds)

    return filtered_ds



