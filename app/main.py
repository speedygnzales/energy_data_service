from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.api_handler import (
    SWISS_POPULATION,
    DatasetsApiResponse,
    ExternalAPIError,
    ExternalAPITimeout,
    StromverbrauchApiResponse,
    fetch_consumption,
    fetch_datasets
)


app = FastAPI(title="Energy Data Service")

ERROR_RESPONSES = {
    502: {"description": "Energy data source failed or sent invalid data"},
    504: {"description": "Energy data source did not respond in time"},
}

class ConsumptionPerCapitaResponse(BaseModel):
    year: int = Field(description="Year of the data")
    days: int = Field(description="Number of days with data")
    avg_final_consumption_gwh_per_day: float = Field(
        description="Average final electricity consumption of Switzerland per day, in GWh"
    )
    kwh_per_person_per_day: float = Field(
        description="Average final electricity consumption per person per day, in kWh"
    )
    kwh_per_person_per_year: int = Field(
        description="Final electricity consumption per person for the whole year, in kWh"
    )

@app.get("/")
def read_root() -> dict[str, str]:
    return {"service": "Energy Data Service"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/datasets", response_model=DatasetsApiResponse, responses=ERROR_RESPONSES)
def get_datasets():
    try:
        return fetch_datasets()
    except ExternalAPITimeout as exc:
        raise HTTPException(status_code=504, detail=str(exc))
    except ExternalAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@app.get(
    "/consumption/per-capita",
    response_model=ConsumptionPerCapitaResponse,
    responses=ERROR_RESPONSES,
)
def get_consumption_per_capita(year: int = 2025) -> ConsumptionPerCapitaResponse:
    try:
        records: StromverbrauchApiResponse = fetch_consumption(year)
    except ExternalAPITimeout as exc:
        raise HTTPException(status_code=504, detail=str(exc))
    except ExternalAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    if not records.data:
        raise HTTPException(status_code=404, detail=f"No consumption data for {year}")

    total_gwh = 0
    for record in records.data:
        total_gwh += record.endverbrauch_gwh

    days = len(records.data)
    avg_gwh_per_day = total_gwh / days
    kwh_per_person_per_day = avg_gwh_per_day * 1_000_000 / SWISS_POPULATION

    return ConsumptionPerCapitaResponse(
        year=year,
        days=days,
        avg_final_consumption_gwh_per_day=round(avg_gwh_per_day, 1),
        kwh_per_person_per_day=round(kwh_per_person_per_day, 1),
        kwh_per_person_per_year=round(kwh_per_person_per_day * days),
    )

