# Asset Manager API Testing Guide

## Prerequisites
1. FastAPI server running: `uvicorn src.backend.api.learning:app --reload`
2. API keys configured in `.env` file
3. Dependencies installed: `pip install aiohttp replicate openai pillow supabase`

---

## Test 1: Health Check (No API Keys Required)

### Command Prompt (curl)
```cmd
curl http://localhost:8000/api/assets/health
```

### PowerShell
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/assets/health" -Method Get
```

### Expected Response
```json
{
  "status": "healthy",
  "apis": {
    "unsplash": false,
    "pexels": false,
    "replicate": false,
    "openai": false
  }
}
```

---

## Test 2: Search Unsplash Images (Requires UNSPLASH_ACCESS_KEY)

### Command Prompt (curl)
```cmd
curl "http://localhost:8000/api/assets/search?query=photosynthesis&source=unsplash&per_page=5"
```

### PowerShell
```powershell
$query = "photosynthesis"
$url = "http://localhost:8000/api/assets/search?query=$query&source=unsplash&per_page=5"
Invoke-RestMethod -Uri $url -Method Get | ConvertTo-Json -Depth 5
```

### Expected Response
```json
[
  {
    "id": "abc123",
    "url": "https://images.unsplash.com/photo-xyz",
    "thumbnail_url": "https://images.unsplash.com/photo-xyz?w=200",
    "description": "Green plant photosynthesis process",
    "source": "unsplash",
    "photographer": "John Doe",
    "photographer_url": "https://unsplash.com/@johndoe"
  }
]
```

---

## Test 3: Search Pexels Images (Requires PEXELS_API_KEY)

### Command Prompt (curl)
```cmd
curl "http://localhost:8000/api/assets/search?query=DNA&source=pexels&per_page=5"
```

### PowerShell
```powershell
$query = "DNA"
$url = "http://localhost:8000/api/assets/search?query=$query&source=pexels&per_page=5"
Invoke-RestMethod -Uri $url -Method Get | ConvertTo-Json -Depth 5
```

---

## Test 4: Search All Sources

### Command Prompt (curl)
```cmd
curl "http://localhost:8000/api/assets/search?query=cell%20biology&source=all&per_page=10"
```

### PowerShell
```powershell
$query = "cell biology"
$url = "http://localhost:8000/api/assets/search?query=$([uri]::EscapeDataString($query))&source=all&per_page=10"
Invoke-RestMethod -Uri $url -Method Get | ConvertTo-Json -Depth 5
```

---

## Test 5: Generate AI Asset (POST Request)

### Command Prompt (curl)
```cmd
curl -X POST http://localhost:8000/api/assets/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\":\"Educational diagram of photosynthesis\",\"type\":\"image\",\"subject\":\"Biology\",\"style\":\"educational\"}"
```

### PowerShell
```powershell
$body = @{
    prompt = "Educational diagram of photosynthesis"
    type = "image"
    subject = "Biology"
    style = "educational"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/assets/generate" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body | ConvertTo-Json -Depth 5
```

### Expected Response
```json
{
  "asset_id": "gen_Education",
  "asset_url": "https://placeholder.com/generated.png",
  "status": "processing",
  "message": "Asset generation started. Check back in a few minutes."
}
```

---

## Test 6: Test Frontend UI

1. Open `asset_search.html` in browser:
   ```
   file:///C:/Users/hp/Documents/Akulearn_docs/public/asset_search.html
   ```

2. Make sure FastAPI server is running:
   ```cmd
   cd C:\Users\hp\Documents\Akulearn_docs
   myenv\Scripts\activate.bat
   uvicorn src.backend.api.learning:app --reload --host 127.0.0.1 --port 8000
   ```

3. Test search:
   - Enter query: "photosynthesis"
   - Select source: "All Sources"
   - Click "Search"

---

## Postman Collection (Import This)

```json
{
  "info": {
    "name": "Akulearn Asset Manager API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/api/assets/health",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "assets", "health"]
        }
      }
    },
    {
      "name": "Search Images",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/api/assets/search?query=photosynthesis&source=all&per_page=10",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "assets", "search"],
          "query": [
            {"key": "query", "value": "photosynthesis"},
            {"key": "source", "value": "all"},
            {"key": "per_page", "value": "10"}
          ]
        }
      }
    },
    {
      "name": "Generate Asset",
      "request": {
        "method": "POST",
        "header": [
          {"key": "Content-Type", "value": "application/json"}
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"prompt\": \"Educational diagram of photosynthesis\",\n  \"type\": \"image\",\n  \"subject\": \"Biology\",\n  \"style\": \"educational\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/assets/generate",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "assets", "generate"]
        }
      }
    }
  ]
}
```

Save this as `Akulearn_Asset_Manager.postman_collection.json` and import into Postman.

---

## Troubleshooting

### Issue: Connection Refused
**Solution**: Make sure FastAPI server is running:
```cmd
cd C:\Users\hp\Documents\Akulearn_docs
myenv\Scripts\activate.bat
uvicorn src.backend.api.learning:app --reload
```

### Issue: "No images found or API keys not configured"
**Solution**: Add API keys to `.env` file:
```env
UNSPLASH_ACCESS_KEY=your_key_here
PEXELS_API_KEY=your_key_here
```

### Issue: CORS Error in Browser
**Solution**: FastAPI should have CORS enabled (already configured in learning.py)

### Issue: Module Not Found
**Solution**: Install dependencies:
```cmd
myenv\Scripts\activate.bat
pip install aiohttp replicate openai pillow supabase
```

---

## API Documentation

Once server is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

Look for "Asset Manager" section in the documentation.

---

## Next Steps

1. ✅ Test health endpoint (no keys needed)
2. 🔑 Get API keys from:
   - Unsplash: https://unsplash.com/developers
   - Pexels: https://www.pexels.com/api/
   - Replicate: https://replicate.com/account/api-tokens
   - OpenAI: https://platform.openai.com/api-keys
3. ✅ Add keys to `.env` file
4. ✅ Test search endpoints
5. ✅ Test frontend UI
6. ✅ Integrate into main Akulearn platform

---

**Created**: February 2, 2026
**Last Updated**: February 2, 2026
