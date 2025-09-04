# Akulearn Cloud Deployment Scripts

## 1. GCP Cloud Run Deployment (FastAPI Microservices)
```yaml
# .github/workflows/deploy-cloudrun.yml
name: Deploy FastAPI Microservice to Cloud Run
on:
  push:
    branches: [main]
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Build Docker image
        run: docker build -t gcr.io/$GCP_PROJECT/akulearn-microservice:latest .
      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      - name: Push to Artifact Registry
        run: docker push gcr.io/$GCP_PROJECT/akulearn-microservice:latest
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy akulearn-microservice \
            --image gcr.io/$GCP_PROJECT/akulearn-microservice:latest \
            --region $GCP_REGION \
            --platform managed \
            --allow-unauthenticated
```

## 2. IoT Device Registration & Monitoring (Cloud Functions)
```python
# cloud/iot_device_register.py
import google.cloud.iot_v1 as iot

def register_device(project_id, cloud_region, registry_id, device_id):
    client = iot.DeviceManagerClient()
    parent = f"projects/{project_id}/locations/{cloud_region}/registries/{registry_id}"
    device = {"id": device_id}
    response = client.create_device(parent=parent, device=device)
    print("Device registered:", response)
```

## 3. OTA Update Script (Linux)
```bash
#!/bin/bash
# ota_update.sh
REPO_URL="https://github.com/oumar-code/Akulearn_docs.git"
APP_DIR="/opt/akulearn-linux-app"
git pull $REPO_URL $APP_DIR
cd $APP_DIR/akulearn-linux-app
./gradlew build
systemctl restart akulearn-linux-app
```
