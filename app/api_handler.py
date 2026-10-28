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

def fetch_datasets():
    try:
        response = httpx.get(__URL, verify=ctx, timeout=10.0)
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
