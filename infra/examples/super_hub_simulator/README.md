Super Hub Simulator

This small script demonstrates how a Super Hub can register with the IG-Hub control panel and publish anonymized metadata.

Usage (local):

```powershell
# Ensure IG-Hub is running locally (uvicorn on port 8080)
python simulator.py
```

Environment variables:

- `IG_HUB_BASE` - base URL of IG-Hub (default: http://localhost:8080)
- `IG_HUB_ADMIN_KEY` - admin API key to register (default: admin-secret-example)

Use the included Dockerfile to run as a container for demos or CI.
