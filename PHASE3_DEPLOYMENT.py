#!/usr/bin/env python3
"""
Phase 3 API Deployment & Testing Guide
Complete integration with FastAPI, React, and endpoint testing
"""

import subprocess
import time
import requests
import json
from pathlib import Path

class Phase3Deployment:
    """Deployment and testing utilities for Phase 3"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.endpoints = {
            "health": "/api/health",
            "phase3_summary": "/api/assets/phase3/summary",
            "diagrams_by_lesson": "/api/assets/phase3/diagrams",
            "diagram_by_id": "/api/assets/phase3/diagram/{diagram_id}",
            "diagrams_by_type": "/api/assets/phase3/diagrams/type/{diagram_type}",
            "phase3_stats": "/api/assets/phase3/stats",
        }
    
    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70)
    
    def test_endpoint(self, name, url, method="GET", params=None):
        """Test a single endpoint"""
        try:
            if method == "GET":
                response = requests.get(f"{self.base_url}{url}", params=params, timeout=5)
            response.raise_for_status()
            
            print(f"✅ {name}")
            print(f"   Status: {response.status_code}")
            
            try:
                data = response.json()
                if isinstance(data, dict):
                    keys = list(data.keys())[:3]
                    print(f"   Response keys: {', '.join(keys)}")
                elif isinstance(data, list):
                    print(f"   Response items: {len(data)}")
            except:
                pass
            
            return response
        except requests.exceptions.ConnectionError:
            print(f"❌ {name} - Connection refused (server not running)")
            return None
        except Exception as e:
            print(f"❌ {name} - {str(e)}")
            return None
    
    def run_deployment_guide(self):
        """Print complete deployment guide"""
        self.print_header("PHASE 3 DEPLOYMENT GUIDE")
        
        print("""
## 1. BACKEND DEPLOYMENT

### Step 1: Verify FastAPI App Setup
The main app is now at: src.backend.api.learning:app

Features:
  ✓ Phase 3 router mounted at /api/assets/phase3
  ✓ Phase 3 loader initialized on startup
  ✓ CORS enabled for all origins
  ✓ Automatic asset initialization

### Step 2: Start the Server

Option A: Using Docker (Recommended)
  docker-compose up --build

Option B: Using Uvicorn directly
  uvicorn src.backend.api.learning:app --host 0.0.0.0 --port 8000 --reload

Option C: Using Python
  python -m uvicorn src.backend.api.learning:app --host 0.0.0.0 --port 8000

### Step 3: Verify Server is Running
  curl http://localhost:8000/api/health

Expected response:
  {
    "status": "healthy",
    "service": "akulearn-api",
    "version": "3.0.0"
  }

## 2. API ENDPOINTS

All Phase 3 endpoints are available at /api/assets/phase3/*

### Diagram Endpoints:
  GET /api/assets/phase3/summary
    - Get overall statistics

  GET /api/assets/phase3/diagrams?lesson_id=<id>
    - Get diagrams for a lesson

  GET /api/assets/phase3/diagram/<diagram_id>
    - Get specific diagram with SVG content

  GET /api/assets/phase3/diagrams/type/<type>
    - Get diagrams by type (venn, flowchart, circuit, chemistry)

  GET /api/assets/phase3/stats
    - Get detailed statistics

## 3. FRONTEND INTEGRATION

### Import Components
  import VennDiagramViewer from '@/components/VennDiagramViewer';
  import FlowchartViewer from '@/components/FlowchartViewer';
  import CircuitViewer from '@/components/CircuitViewer';
  import ChemistryViewer from '@/components/ChemistryViewer';
  import Phase3DiagramsGallery from '@/components/Phase3DiagramsGallery';
  import { usePhase3Diagrams } from '@/hooks/usePhase3Diagrams';

### Use Custom Hook
  const { diagrams, loading, error } = usePhase3Diagrams(lessonId);

  if (loading) return <div>Loading diagrams...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <Phase3DiagramsGallery 
      lessonId={lessonId}
      diagrams={diagrams}
    />
  );

## 4. TESTING

### Load Test
  python -m pytest test_phase3_integration.py -v

### Manual Test
  python validate_phase3.py

### API Test
  python test_phase3_api_endpoints.py

## 5. PRODUCTION CHECKLIST

  [ ] Server starts without errors
  [ ] Health endpoint returns 200
  [ ] All 5 Phase 3 endpoints respond
  [ ] CORS headers present in responses
  [ ] Phase 3 loader initializes successfully
  [ ] 100 diagrams available
  [ ] All 7 diagram types working
  [ ] Frontend components import correctly
  [ ] React hooks fetch data successfully
  [ ] No console errors in browser
  [ ] API response times < 500ms

## 6. DEPLOYMENT COMMANDS

### Build Docker Image
  docker build -t akulearndocs:latest .

### Run Container
  docker run -p 8000:8000 akulearndocs:latest

### View Logs
  docker-compose logs -f akulearndocs

### Stop Container
  docker-compose down

## 7. TROUBLESHOOTING

If Phase 3 endpoints return 404:
  ✓ Ensure assets_v3 router is imported in learning.py
  ✓ Check initialize_phase3_loader is called
  ✓ Verify generated_assets directory exists

If diagrams return empty:
  ✓ Check phase3_manifest.json exists
  ✓ Verify 100 SVG files in generated_assets/diagrams/
  ✓ Run validate_phase3.py

If React components don't render:
  ✓ Check usePhase3Diagrams hook returns data
  ✓ Verify API endpoints respond with correct format
  ✓ Check console for CORS errors

""")
    
    def run_endpoint_tests(self):
        """Test all Phase 3 endpoints"""
        self.print_header("PHASE 3 ENDPOINT TESTING")
        
        print("\nAttempting to connect to server at http://localhost:8000...")
        
        # Test health check
        self.test_endpoint("Health Check", self.endpoints["health"])
        
        # Test summary
        resp = self.test_endpoint("Phase 3 Summary", self.endpoints["phase3_summary"])
        if resp and resp.status_code == 200:
            data = resp.json()
            print(f"   Total diagrams: {data.get('total_diagrams', 'N/A')}")
        
        # Test stats
        resp = self.test_endpoint("Phase 3 Statistics", self.endpoints["phase3_stats"])
        if resp and resp.status_code == 200:
            data = resp.json()
            for key in ['venn_diagrams', 'flowcharts', 'electrical_circuits']:
                if key in data:
                    print(f"   {key}: {data[key]}")
        
        # Test diagrams by type
        self.test_endpoint(
            "Venn Diagrams",
            self.endpoints["diagrams_by_type"].replace("{diagram_type}", "venn")
        )
        
        self.test_endpoint(
            "Flowcharts",
            self.endpoints["diagrams_by_type"].replace("{diagram_type}", "flowchart")
        )
        
        self.test_endpoint(
            "Circuits (Electrical)",
            self.endpoints["diagrams_by_type"].replace("{diagram_type}", "electrical_circuit")
        )
        
        print("\n" + "-" * 70)
        print("Note: To run these tests, start the server first:")
        print("  uvicorn src.backend.api.learning:app --host 0.0.0.0 --port 8000")
        print("-" * 70)


def main():
    deployer = Phase3Deployment()
    
    # Print deployment guide
    deployer.run_deployment_guide()
    
    # Print endpoint tests
    deployer.run_endpoint_tests()


if __name__ == "__main__":
    main()
