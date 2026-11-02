# Energy Data Service

FastAPI backend for the Energy Data Service. It uses the public Energy Dashboard API of the Swiss Federal Office of Energy (SFOE) to serve the list of available energy datasets and the average electricity consumption per person in Switzerland.

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
* `GET /consumption/per-capita?year=2025` returns the average final electricity consumption per person for the given year

Example response for `/datasets`:

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

## Electricity consumption per person

`/consumption/per-capita` fetches the daily final electricity consumption ("Endverbrauch") of Switzerland for one year and divides it by the Swiss population.

Example response:

```json
{
  "year": 2025,
  "days": 365,
  "avg_final_consumption_gwh_per_day": 146.6,
  "kwh_per_person_per_day": 16.1,
  "kwh_per_person_per_year": 5861
}
```

Calculation: average daily final consumption in GWh × 1,000,000 ÷ population.

The population is a fixed value: 9,127,100 permanent residents at the end of 2025 (Swiss Federal Statistical Office, definitive results). Duplicate days in the source data are not removed.

## Data source

Energy Dashboard API by the Swiss Federal Office of Energy (SFOE):

* API docs: https://energiedashboard.ch/api/swagger-ui/index.html
* Catalog entry: https://www.i14y.admin.ch/en/catalog/dataservices/d61f1d8e-4552-470f-a939-cc175f969c03/description
* Consumption data: dataset `stromverbrauch-swissgrid-lv-und-endv`
* Population: Swiss Federal Statistical Office (FSO), https://www.bfs.admin.ch

## Test locally

Start the app, then use one of these:

* Browser: open http://localhost:8000/datasets
* Swagger: open http://localhost:8000/docs, select `GET /datasets`, click **Try it out** and **Execute**
* Terminal: `curl -i http://localhost:8000/datasets`

A working setup returns HTTP 200 and a JSON object with a `datasets` list.

To test the consumption endpoint: `curl -i "http://localhost:8000/consumption/per-capita?year=2025"`

## Note on certificates

The service uses `truststore`, so Python trusts the certificates of your operating system. This is needed on networks that inspect HTTPS traffic, such as many corporate networks. Without it, requests to the external API fail with `CERTIFICATE_VERIFY_FAILED`.

## Error responses

If the external API cannot be used, `/datasets` and `/consumption/per-capita` return an error instead of crashing:

* `502` when the source is unreachable, returns an error status or sends invalid JSON
* `504` when the source does not respond within 10 seconds
* `404` (only `/consumption/per-capita`) when there is no data for the given year
* `422` (only `/consumption/per-capita`) when `year` is not a number

The response contains a `detail` field with the reason.
