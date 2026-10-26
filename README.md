
# Energy Data Service

FastAPI backend for the Energy Data Service. It fetches the list of available energy datasets from the public Energy Dashboard API of the Swiss Federal Office of Energy (SFOE) and serves it through its own API.

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
* `GET /datasets` returns all datasets available in the Energy Dashboard API, each with its `id`, `name` and `description`

Example response:

```json
{
  "datasets": [
    {
      "id": "stromproduktion-swissgrid",
      "name": "Stromproduktion Swissgrid",
      "description": ""
    }
  ]
}
```

The list is fetched live from the source on every request.

## Data source

Energy Dashboard API by the Swiss Federal Office of Energy (SFOE):

* API docs: https://energiedashboard.ch/api/swagger-ui/index.html
* Catalog entry: https://www.i14y.admin.ch/en/catalog/dataservices/d61f1d8e-4552-470f-a939-cc175f969c03/description

## Test `/datasets` locally

Start the app, then use one of these:

* Browser: open http://localhost:8000/datasets
* Swagger: open http://localhost:8000/docs, select `GET /datasets`, click **Try it out** and **Execute**
* Terminal: `curl -i http://localhost:8000/datasets`

A working setup returns HTTP 200 and a JSON object with a `datasets` list.

## Note on certificates

The service uses `truststore`, so Python trusts the certificates of your operating system. This is needed on networks that inspect HTTPS traffic, such as many corporate networks. Without it, requests to the external API fail with `CERTIFICATE_VERIFY_FAILED`.
