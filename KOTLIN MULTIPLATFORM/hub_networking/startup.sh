#!/bin/bash
# Akulearn Hub startup script

# Start hostapd for Wi-Fi hotspot
sudo systemctl start hostapd

# Start dnsmasq for DHCP
sudo systemctl start dnsmasq

# Start Nginx web server
sudo systemctl start nginx

# Start local Flask API server
python3 /app/local_server.py
