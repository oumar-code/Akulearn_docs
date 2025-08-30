
# Akulearn Hub Networking & AI Deployment

## Overview

This folder contains configuration and scripts for deploying the Akulearn Hub's local Wi-Fi hotspot, web server, and offline AI inference.

## Files

- `hostapd.conf`: Wi-Fi hotspot configuration
- `nginx.conf`: Nginx web server config
- `local_server.py`: Flask API server for offline AI and content
- `gemma_inference.py`: Placeholder for Gemma AI model inference
- `Dockerfile`: Container setup for Python app, Nginx, hostapd, dnsmasq
- `startup.sh`: Startup script for all services

## Deployment (Docker)

1. Build the Docker image:

   ```bash
   docker build -t akulearn-hub .
   ```

2. Run the container:

   ```bash
   docker run --privileged -p 80:80 -p 5000:5000 --network host akulearn-hub
   ```

   - `--privileged` is required for hostapd/dnsmasq to manage Wi-Fi.
   - `--network host` allows direct access to network interfaces.

## Manual Startup (Linux SBC)

1. Make `startup.sh` executable:

   ```bash
   chmod +x startup.sh
   ```

2. Run the script:

   ```bash
   ./startup.sh
   ```

## Notes

- Ensure Wi-Fi hardware supports AP mode.
- Update passwords and security settings as needed.
- For production, replace the AI placeholder with the actual Gemma model.

## Notes
- Ensure Wi-Fi hardware supports AP mode.
- Update passwords and security settings as needed.
- For production, replace the AI placeholder with the actual Gemma model.
