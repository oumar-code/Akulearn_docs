# Akulearn Hub Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y nginx hostapd dnsmasq && rm -rf /var/lib/apt/lists/*

# Copy Python app
WORKDIR /app
COPY local_server.py gemma_inference.py ./

# Install Python dependencies
RUN pip install flask

# Copy Nginx config
COPY nginx.conf /etc/nginx/sites-available/default

# Copy hostapd config
COPY hostapd.conf /etc/hostapd/hostapd.conf

# Expose ports
EXPOSE 80 5000

# Start services
CMD service nginx start && python local_server.py
