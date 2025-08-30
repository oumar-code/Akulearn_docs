# Akulearn Projector Hub Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install backend dependencies
COPY ../backend/requirements.txt ./backend/requirements.txt
RUN pip install -r ./backend/requirements.txt

# Copy backend code
COPY ../backend ./backend

# Build PWA
RUN apt-get update && apt-get install -y nodejs npm nginx \
    && cd ../frontend \
    && npm install \
    && npm run build \
    && cp -r dist /usr/share/nginx/html

# Copy Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 8000

CMD service nginx start && uvicorn backend.main:app --host 0.0.0.0 --port 8000
