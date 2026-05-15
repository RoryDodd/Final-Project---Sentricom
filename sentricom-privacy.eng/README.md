# AFERT - Sentricom Privacy Engine
Privacy-First AI for Emergency Response, Building Live Warden Dashboards Without Surveillance - Team 1

Python application that:
- Fetches incoming raw zone-node data
- Applies differential privacy processing
- Sends ONLY the privatised results to the API middleware layer for storage and display
- Exposes a `/health` endpoint for state monitoring

---

## Configuration
Runtime configuration is handled via environment variables.
- env file should be used for local development only and not added to repo
- cloud hosts should have startup commands configured (vercel, railway, etc)

### `.env` (local development)
Create a `.env` file in the project root:

```env
EXTERNAL_API_URL_BASE=https://<your-api-base-url>
API_KEY=<your_api_key>
HEALTH_PORT=<port_for_healthcheck_api(e.g.8032)>
HEALTH_HOST=<host_address_for_healthcheck_api(e.g.172.0.0.2)>
```

### Endpoint Construction

The application constructs full API endpoints using `EXTERNAL_API_URL_BASE`:

- Data retrieval: `<BASE>/occupancy/testdata/next`
- Data ingest: `<BASE>/api/v1/zones/latest`

This avoids duplication and ensures consistency across API calls.

---

## Application Versioning and Metadata
Application metadata defined in settings.py:
- SERVICE_NAME and SERVICE_VERSION exposed in healthcheck API endpoint `/health`

```settings.py
__author__ = "<Firstname, Surname>", "<Firstname, Surname>", "<etc>"
__version__ = "x.x"
__date__ = "yyyy"

SERVICE_NAME = "Sentricom Privacy Engine"
SERVICE_VERSION = "x.x"
```

---

## Requirments file for tracking dependencies
requirements.txt tracks project dependencies and required versions
- will be consumed by cloud hosts at deploy time

---