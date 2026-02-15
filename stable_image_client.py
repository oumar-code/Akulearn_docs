"""
Hugging Face Inference API client for Stable Diffusion XL using huggingface_hub.
- Uses the hosted model: stabilityai/stable-diffusion-xl-base-1.0
- Reads the token from the HUGGINGFACE_API_TOKEN environment variable.
- Auto-loads from .env file if present.
"""

import os
import time
import pathlib
from typing import Optional, Tuple

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load .env file if it exists
load_dotenv()

DEFAULT_TIMEOUT = 60  # seconds
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"


class StableImageClientError(Exception):
    """Raised when the Hugging Face inference API responds with an error."""


def _load_token() -> str:
    token = os.getenv("HUGGINGFACE_API_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
    if not token:
        raise StableImageClientError(
            "Missing HUGGINGFACE_API_TOKEN or HUGGINGFACE_TOKEN. Set it in your environment or .env file."
        )
    return token.strip()


def generate_image(
    prompt: str,
    *,
    negative_prompt: Optional[str] = None,
    guidance_scale: float = 7.5,
    num_inference_steps: int = 30,
    seed: Optional[int] = None,
    output_path: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> Tuple[bytes, str]:
    """
    Generate an image from a text prompt using the Hugging Face Inference API.

    Returns (image_bytes, saved_path)
    """

    token = _load_token()

    # Use the router via huggingface_hub with retries and an explicit timeout.
    client = InferenceClient(
        model=MODEL_ID,
        token=token,
        timeout=timeout,
    )

    try:
        image = client.text_to_image(
            prompt,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            seed=seed,
        )
        image_bytes = image.tobytes() if hasattr(image, "tobytes") else image
    except Exception as e:
        raise StableImageClientError(f"Image generation failed: {str(e)}")

    # Save image
    if output_path is None:
        ts = time.strftime("%Y%m%d-%H%M%S")
        output_dir = pathlib.Path("generated_images")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"sdxl_{ts}.png"
    else:
        output_path = pathlib.Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    if hasattr(image, 'save'):
        image.save(output_path)
    else:
        output_path.write_bytes(image_bytes)
    
    return image_bytes, str(output_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate an image via Hugging Face SDXL")
    parser.add_argument("prompt", help="Text prompt for Stable Diffusion XL")
    parser.add_argument("--negative", dest="negative", help="Negative prompt", default=None)
    parser.add_argument("--steps", dest="steps", type=int, default=30, help="Inference steps")
    parser.add_argument("--guidance", dest="guidance", type=float, default=7.5, help="Guidance scale")
    parser.add_argument("--seed", dest="seed", type=int, default=None, help="Random seed")
    parser.add_argument("--out", dest="out", default=None, help="Output image path")

    args = parser.parse_args()

    try:
        _, saved = generate_image(
            args.prompt,
            negative_prompt=args.negative,
            guidance_scale=args.guidance,
            num_inference_steps=args.steps,
            seed=args.seed,
            output_path=args.out,
        )
        print(f"✅ Image saved to {saved}")
    except StableImageClientError as exc:
        print(f"❌ {exc}")
