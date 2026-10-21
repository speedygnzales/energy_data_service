import ssl
import truststore
import httpx


__URL = "https://energiedashboard.ch/api/v1/datasets"
ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


def fetch_datasets():
    response = httpx.get(__URL, verify=ctx)
    return response.json()
