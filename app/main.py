from fastapi import FastAPI, HTTPException
from app.api_handler import fetch_datasets, ExternalAPIError, ExternalAPITimeout


app = FastAPI(title="Energy Data Service")

@app.get("/")
def read_root() -> dict[str, str]:
    return {"service": "Energy Data Service"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get(
    "/datasets",
    responses={
        502: {"description": "Energy data source failed or sent invalid data"},
        504: {"description": "Energy data source did not respond in time"},
    },
)
def get_dataset():
        
    try:
        data_set = fetch_datasets()["datasets"]
        filtered_ds = {"datasets": []}
        
        for ds in data_set:
            filtered_ds["datasets"].append({"id": ds.get("id"),
                                            "name": ds.get("name"),
                                            "description": ds.get("description")})

        return filtered_ds
    except ExternalAPITimeout:
        raise HTTPException(status_code=504, detail="Energy data source did not respond in time")
    except ExternalAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

