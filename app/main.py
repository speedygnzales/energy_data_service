from fastapi import FastAPI
import ssl
import truststore
import httpx


__URL = "https://energiedashboard.ch/api/v1/datasets"
ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
response = httpx.get(__URL, verify=ctx)
app = FastAPI(title="Energy Data Service")



@app.get("/")
def read_root() -> dict[str, str]:
    return {"service": "Energy Data Service"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/datasets")
def raw_dataset():
    
    return response.json()


