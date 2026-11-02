import ssl
import truststore
import httpx
import json


class ExternalAPIError(Exception):
    """The external energy API could not be used."""

class ExternalAPITimeout(ExternalAPIError):
    """The external energy API took too long to respond."""


__URL = "https://energiedashboard.ch/api/v1/datasets"
ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

CONSUMPTION_URL = "https://energiedashboard.ch/api/v1/datasets/stromverbrauch-swissgrid-lv-und-endv/data"
SWISS_POPULATION = 9_127_100


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


def fetch_datasets():
    return _get_json(__URL)


def fetch_consumption(year):
    params = {"from": f"{year}-01-01", "to": f"{year}-12-31", "limit": 400}
    return _get_json(CONSUMPTION_URL, params)["data"]
