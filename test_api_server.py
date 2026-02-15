"""
Simple test script to verify the API server works
"""
import sys
import time
import webbrowser
from wave3_rest_api import app

def test_server():
    print("=" * 60)
    print("Testing Wave 3 REST API Server")
    print("=" * 60)
    
    # Test import
    print("\n✓ Successfully imported wave3_rest_api")
    print(f"✓ App object created: {app}")
    
    # Start server in background
    import uvicorn
    import threading
    
    def run_server():
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    
    print("\n🚀 Starting server on http://127.0.0.1:8000")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test the API
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/api/health")
        print(f"\n✓ Health check: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        # Open browser
        print("\n🌐 Opening browser to API documentation...")
        webbrowser.open("http://127.0.0.1:8000/api/docs")
        
        print("\n" + "=" * 60)
        print("✅ Server is running successfully!")
        print("=" * 60)
        print("\nAPI Documentation: http://127.0.0.1:8000/api/docs")
        print("Health Endpoint:   http://127.0.0.1:8000/api/health")
        print("All Subjects:      http://127.0.0.1:8000/api/subjects")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 60)
        
        # Keep running
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"\n❌ Error testing server: {e}")
        print("\nTrying to open browser anyway...")
        webbrowser.open("http://127.0.0.1:8000/api/docs")
        
        print("\nServer should be running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)

if __name__ == "__main__":
    test_server()
