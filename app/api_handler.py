import json
import ssl
import httpx
import truststore
from pydantic import BaseModel, ValidationError


class ExternalAPIError(Exception):
    """The external energy API could not be used."""


class ExternalAPITimeout(ExternalAPIError):
    """The external energy API took too long to respond."""


class DatasetRecord(BaseModel):
    id: str
    name: str
    description: str | None = None


class DatasetsApiResponse(BaseModel):
    datasets: list[DatasetRecord]


class StromverbrauchRecord(BaseModel):
    datum: str
    landesverbrauch_gwh: float
    endverbrauch_gwh: float


class StromverbrauchApiResponse(BaseModel):
    data: list[StromverbrauchRecord]


DATASETS_URL = "https://energiedashboard.ch/api/v1/datasets"
CONSUMPTION_URL = "https://energiedashboard.ch/api/v1/datasets/stromverbrauch-swissgrid-lv-und-endv/data"


SWISS_POPULATION = 9_127_100

ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


def _get_json(url, params=None):
    try:
        response = httpx.get(url, params=params, verify=ctx, timeout=10.0)
        response.raise_for_status()
        return response.json()
    except httpx.TimeoutException:
        raise ExternalAPITimeout("Energy data source did not respond in time")
    except httpx.HTTPStatusError:
        raise ExternalAPIError("Energy data source returned an error status")
    except httpx.RequestError:
        raise ExternalAPIError("Energy data source is not reachable")
    except json.JSONDecodeError:
        raise ExternalAPIError("Energy data source returned invalid JSON")


def fetch_datasets() -> DatasetsApiResponse:
    raw = _get_json(DATASETS_URL)
    try:
        return DatasetsApiResponse.model_validate(raw)
    except ValidationError:
        raise ExternalAPIError("Energy data source returned unexpected data")


def fetch_consumption(year: int) -> StromverbrauchApiResponse:
    params = {"from": f"{year}-01-01", "to": f"{year}-12-31", "limit": 400}
    raw = _get_json(CONSUMPTION_URL, params)
    try:
        return StromverbrauchApiResponse.model_validate(raw)
    except ValidationError:
        raise ExternalAPIError("Energy data source returned unexpected data")
