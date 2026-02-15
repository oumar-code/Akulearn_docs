#!/usr/bin/env python3
"""
Process image_queue/nerdc_queue.json and generate images for each queued item
using Stable Diffusion XL via stable_image_client. Skips completed items.
Updates both the queue file (status) and connected_stack/backend/content_data.json
with an `image` field containing path, prompt, and timestamp.
"""

import json
from pathlib import Path
from datetime import datetime
import time

QUEUE_FILE = Path("image_queue/nerdc_queue.json")
BACKEND_CONTENT = Path("connected_stack/backend/content_data.json")
IMAGES_DIR = Path("generated_images")


def load_json(path: Path, default):
    try:
        return json.load(path.open("r", encoding="utf-8"))
    except FileNotFoundError:
        return default


def save_json(path: Path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    IMAGES_DIR.mkdir(exist_ok=True)

    queue = load_json(QUEUE_FILE, [])
    backend = load_json(BACKEND_CONTENT, {"content": [], "progress": {}})

    # Build index by id for backend content
    idx = {item.get("id"): i for i, item in enumerate(backend.get("content", []))}

    # Import image generator lazily
    try:
        from stable_image_client import generate_image
    except ImportError as e:
        print(f"ERROR: {e}. Ensure stable_image_client.py is present and dependencies installed.")
        return

    updated = 0
    for item in queue:
        if item.get("status") == "done":
            continue
        content_id = item.get("id")
        prompt = item.get("prompt")
        if not content_id or content_id not in idx:
            item["status"] = "skipped"
            item["reason"] = "not_found_in_backend"
            continue

        # Skip if backend already has image
        backend_item = backend["content"][idx[content_id]]
        if backend_item.get("image"):
            item["status"] = "skipped"
            item["reason"] = "already_has_image"
            continue

        # Generate
        print(f"Generating image for: {backend_item.get('subject')} > {backend_item.get('title')}")
        try:
            # let generate_image pick a filename
            _, out_path = generate_image(prompt)

            backend_item["image"] = {
                "path": out_path,
                "prompt": prompt,
                "generated_at": datetime.now().isoformat()
            }
            item["status"] = "done"
            item["completed_at"] = datetime.now().isoformat()
            updated += 1

            # gentle pacing
            time.sleep(3)
        except Exception as e:
            item["status"] = "error"
            item["error"] = str(e)[:200]
            print(f"ERROR: {e}")

    # Save updates
    save_json(QUEUE_FILE, queue)
    save_json(BACKEND_CONTENT, backend)

    print(f"Completed: {updated} images. Queue saved: {QUEUE_FILE}")


if __name__ == "__main__":
    main()
