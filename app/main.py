from fastapi import FastAPI, HTTPException
from app.api_handler import fetch_datasets, fetch_consumption, SWISS_POPULATION, ExternalAPIError, ExternalAPITimeout


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


@app.get(
    "/consumption/per-capita",
    responses={
        502: {"description": "Energy data source failed or sent invalid data"},
        504: {"description": "Energy data source did not respond in time"},
    },
)
def get_consumption_per_capita(year: int = 2025):
    try:
        records = fetch_consumption(year)
    except ExternalAPITimeout as exc:
        raise HTTPException(status_code=504, detail=str(exc))
    except ExternalAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    if not records:
        raise HTTPException(status_code=404, detail=f"No consumption data for {year}")

    total_gwh = 0
    for record in records:
        total_gwh += record["endverbrauch_gwh"]

    days = len(records)
    avg_gwh_per_day = total_gwh / days
    kwh_per_person_per_day = avg_gwh_per_day * 1_000_000 / SWISS_POPULATION

    return {
        "year": year,
        "days": days,
        "avg_final_consumption_gwh_per_day": round(avg_gwh_per_day, 1),
        "kwh_per_person_per_day": round(kwh_per_person_per_day, 1),
        "kwh_per_person_per_year": round(kwh_per_person_per_day * days),
    }
