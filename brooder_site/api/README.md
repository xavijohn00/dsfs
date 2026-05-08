# Brooder Flask API

REST API for the SALCC Brooder Temperature Control System.
Runs on a cloud server (Render). Shares the same MySQL database as the PHP frontend.

## Endpoints

| Method | Endpoint       | Who calls it | Description                         |
|--------|----------------|--------------|-------------------------------------|
| GET    | /api/health    | Anyone       | Check the API is running            |
| POST   | /api/readings  | RPi          | Push a temperature/humidity reading |
| GET    | /api/readings  | RPi / PHP    | Get latest reading for this brooder |
| GET    | /api/settings  | RPi          | Get current target temperature      |
| POST   | /api/settings  | PHP          | Save a new target temperature       |

## Authentication

Every request needs the brooder API key in the header:
  Authorization: Bearer <api_key>

## Render Setup

- Build Command: pip install -r requirements.txt
- Start Command:  gunicorn app:app
- Environment:    Python 3

## Example — RPi sends a reading (Python)

```python
import requests

API_URL = "https://your-render-url.onrender.com"
API_KEY = "your-brooder-api-key"

requests.post(
    f"{API_URL}/api/readings",
    json={"temperature": 32.5, "humidity": 58.0},
    headers={"Authorization": f"Bearer {API_KEY}"}
)
```
