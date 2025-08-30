import os
import time
import requests
import gzip
import socket
from models import LocalDatabase

def is_internet_available(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

def compress_data(data: bytes) -> bytes:
    return gzip.compress(data)

def sync_to_cloud(local_db: LocalDatabase, cloud_url: str):
    # Upload student profiles
    students = local_db.conn.execute('SELECT * FROM student_profile').fetchall()
    for row in students:
        payload = {
            'student_id': row[0], 'name': row[1],
            'progress': row[2], 'quiz_results': row[3], 'chat_history': row[4]
        }
        compressed = compress_data(str(payload).encode())
        try:
            requests.post(f'{cloud_url}/api/sync/student', data=compressed, headers={'Content-Encoding': 'gzip'})
        except Exception as e:
            print(f"Sync error: {e}")
    # Upload learning content (if needed)
    # ...similar logic...

def download_updates(local_db: LocalDatabase, cloud_url: str):
    try:
        r = requests.get(f'{cloud_url}/api/sync/content', timeout=10)
        if r.ok:
            # Assume response is compressed JSON
            content_list = gzip.decompress(r.content).decode()
            # Parse and update local DB
            # ...parse and update logic...
    except Exception as e:
        print(f"Download error: {e}")

def run_sync_agent(local_db: LocalDatabase, cloud_url: str, interval=3600):
    while True:
        if is_internet_available():
            print("Internet detected. Syncing...")
            sync_to_cloud(local_db, cloud_url)
            download_updates(local_db, cloud_url)
        else:
            print("No internet. Waiting...")
        time.sleep(interval)

if __name__ == "__main__":
    db = LocalDatabase()
    run_sync_agent(db, cloud_url="https://akulearn-cloud.example.com")
