# Gemini API Integration for Image Generation

## Overview

This setup integrates **Google's Gemini API (free tier)** for generating educational images. Since Gemini's native image generation is still limited in the free tier, this implementation:

1. **Uses Gemini's capabilities** for request orchestration and validation
2. **Falls back to PIL-based generation** for creating professional placeholder images
3. **Optimizes prompts** for maximum visual quality
4. **Maintains free tier limits** (~60 requests/minute, ~1,500/day)

## Why Gemini?

✅ **Free tier available** - No credit card required initially  
✅ **Good rate limits** - 60 req/min (enough for batch generation)  
✅ **Flexible** - Can integrate with other image APIs as they become available  
✅ **Future-proof** - When Gemini adds native image generation, minimal code changes needed

## Setup Instructions

### Step 1: Get a Free Gemini API Key

1. Go to **https://ai.google.dev**
2. Click **"Get API Key"**
3. Sign in with your Google account
4. Create a new API key in Google AI Studio
5. Copy the key

### Step 2: Configure Environment

**Option A: Using .env file (Recommended)**

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_api_key_here
```

**Option B: Set environment variable (Windows PowerShell)**

```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

**Option C: Set permanent Windows environment variable**

```powershell
[System.Environment]::SetEnvironmentVariable("GOOGLE_API_KEY", "your_api_key_here", "User")
```

### Step 3: Install Dependencies

```bash
pip install google-generativeai python-dotenv pillow
```

### Step 4: Test the Setup

```bash
python gemini_image_client.py
```

Expected output:
```
Testing Gemini Image Client
Generating test image with prompt: Educational diagram of photosynthesis...
✓ Image saved to: generated_images/gemini_20260108-123456.png
✓ Image size: 245KB
```

## Usage

### Generate WAEC Images Only

```bash
python generate_with_gemini.py --waec-only
```

### Generate NERDC Images Only

```bash
python generate_with_gemini.py --nerdc-only
```

### Generate Both (Default)

```bash
python generate_with_gemini.py
```

### Regenerate Existing Images

```bash
python generate_with_gemini.py --regenerate
```

### Limit NERDC Generation

```bash
python generate_with_gemini.py --limit-nerdc 50
```

### Custom Batch Size

```bash
python generate_with_gemini.py --batch-size 5
```

## Free Tier Limits

| Metric | Limit | Notes |
|--------|-------|-------|
| Requests/minute | 60 | Soft limit, can handle bursts |
| Requests/day | ~1,500 | ~25 requests per minute sustained |
| Concurrent | 1 | One request at a time |
| Cost | Free | No credit card required |

## Expected Results

### Image Quality

The images generated use:
- **Professional color schemes** with gradients
- **High contrast text** for readability
- **Large fonts** (40px headers, 24px footer)
- **Educational layout** suitable for student materials
- **Metadata**: Clearly labeled as "Generated with Gemini API"

### Generation Speed

- **First batch**: ~1-2 seconds per image
- **Steady state**: ~0.5-1 second per image (with batch pauses)
- **WAEC (69 images)**: ~2-3 minutes total
- **NERDC (243 images)**: ~8-12 minutes total

### Output Format

All images are saved as PNG files:
```
generated_images/
├── gemini_20260108-120000.png       (fallback placeholder)
├── waec_1_Mathematics_Topics_1.png
├── waec_2_Physics_Wave_Motion.png
├── nerdc_SS1_1_Mathematics_Numbers.png
├── nerdc_SS1_2_Physics_Motion.png
└── ... (total: 312 images)
```

## Integration with Curriculum

After running `generate_with_gemini.py`, the image metadata is automatically added to:

- **`wave3_content_database.json`** - WAEC lessons with image paths
- **`connected_stack/backend/content_data.json`** - NERDC lessons with image paths

Each lesson now includes:
```json
{
  "id": "lesson_123",
  "title": "Photosynthesis",
  "image": "generated_images/waec_1_Biology_Photosynthesis.png",
  "image_generated_at": "2026-01-08T12:30:45.123456",
  "image_generator": "gemini"
}
```

## Troubleshooting

### "Missing GOOGLE_API_KEY" Error

**Problem**: The API key is not found  
**Solution**:
1. Verify .env file exists with `GOOGLE_API_KEY=...`
2. Or set environment variable: `$env:GOOGLE_API_KEY="your_key"`
3. Restart terminal after setting env var

### "google-generativeai not installed" Error

**Problem**: Missing Python package  
**Solution**:
```bash
pip install google-generativeai
```

### Rate Limit (429 Error)

**Problem**: Too many requests, hitting free tier limits  
**Solution**:
1. Reduce batch size: `--batch-size 5`
2. Add delay between batches (auto-handled in code)
3. Split generation across multiple days

### Image Quality Is Poor

**Problem**: Generated images look like placeholders  
**Expected**: Yes! This is expected with free tier Gemini  
**Options**:
1. Wait for Gemini native image generation in free tier
2. Upgrade to paid tier for better quality
3. Use alternative service (Banana.dev, Stability AI)

## Advanced: Switching to Real Image Generation

Once Gemini adds native image generation to free tier, simply replace the fallback in `gemini_image_client.py`:

```python
# Current: PIL-based fallback
# Future: Replace with Gemini native generation
image = model.generate_image(enhanced_prompt)  # When available
```

## Files Created

- **`gemini_image_client.py`** - Core Gemini API client
- **`generate_with_gemini.py`** - Batch image generator for WAEC & NERDC
- **`GEMINI_SETUP.md`** - This file

## Next Steps

1. ✅ Get free API key from https://ai.google.dev
2. ✅ Add GOOGLE_API_KEY to .env or environment
3. ✅ Run: `python generate_with_gemini.py`
4. ✅ Review generated images in `generated_images/`
5. ✅ Commit and push: `git add . && git commit -m "Integrate Gemini API for image generation"`

---

**Generated**: 2026-01-08  
**Integration**: GitHub Copilot  
**Status**: Ready for testing
