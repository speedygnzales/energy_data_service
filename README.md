# Energy Data Service

FastAPI backend for the Energy Data Service. For now it only has a root endpoint and a health check. Getting public energy data will come later.

## Setup

Needs Python 3.11 or newer.

```bash
git clone https://github.com/speedygnzales/energy_data_service.git
cd energy_data_service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

The service runs on http://localhost:8000.
API docs (Swagger) are at http://localhost:8000/docs.

## Endpoints

* `GET /` returns the service name
* `GET /health` returns `{"status": "ok"}`
