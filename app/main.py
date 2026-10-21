from typing import Annotated
from fastapi import FastAPI, Depends
import ssl
import truststore
import httpx

ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ctx)
app = FastAPI(title="Energy Data Service")
URL = 'https://energiedashboard.ch/api/v1/datasets'


@app.get("/")
def read_root() -> dict[str, str]:
    return {"service": "Energy Data Service"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/datasets")
def raw_dataset():
    response = httpx.get(URL, verify=ctx)

    return response.json()


