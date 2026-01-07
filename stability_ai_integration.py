"""
Stability AI Integration for Akulearn - Educational Image Generation
Uses Dream Studio API (Free Tier) to generate diagrams and illustrations
"""

import os
import requests
import base64
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StabilityAIGenerator:
    """Generate educational images using Stability AI Dream Studio API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Stability AI client
        
        Args:
            api_key: Stability AI API key (defaults to env var STABILITY_API_KEY)
        """
        self.api_key = api_key or os.getenv("STABILITY_API_KEY")
        if not self.api_key:
            raise ValueError("STABILITY_API_KEY not found. Get one from https://dreamstudio.ai/account")
        
        self.base_url = "https://api.stability.ai/v1"
        self.engine_id = "stable-diffusion-v1-6"  # Free tier compatible
        
    def generate_educational_image(
        self,
        prompt: str,
        subject: str,
        output_dir: str = "generated_content/diagrams",
        width: int = 512,
        height: int = 512,
        cfg_scale: float = 7.0,
        steps: int = 30,
        style: str = "educational"
    ) -> Optional[Dict[str, Any]]:
        """
        Generate an educational image from text prompt
        
        Args:
            prompt: Description of the image to generate
            subject: Subject area (Math, Physics, Chemistry, etc.)
            output_dir: Directory to save generated images
            width: Image width (512, 768, or 1024)
            height: Image height (512, 768, or 1024)
            cfg_scale: Prompt strength (7-15 recommended)
            steps: Number of diffusion steps (20-50, more = better quality)
            style: Visual style preset
            
        Returns:
            Dict with image path and metadata, or None if failed
        """
        # Enhance prompt for educational content
        enhanced_prompt = self._enhance_educational_prompt(prompt, subject, style)
        
        logger.info(f"🎨 Generating {subject} diagram: {prompt[:50]}...")
        
        try:
            response = requests.post(
                f"{self.base_url}/generation/{self.engine_id}/text-to-image",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "text_prompts": [
                        {
                            "text": enhanced_prompt,
                            "weight": 1
                        },
                        {
                            "text": "blurry, low quality, distorted, ugly, watermark",
                            "weight": -1  # Negative prompt
                        }
                    ],
                    "cfg_scale": cfg_scale,
                    "height": height,
                    "width": width,
                    "steps": steps,
                    "samples": 1
                }
            )
            
            if response.status_code != 200:
                logger.error(f"❌ API error: {response.status_code} - {response.text}")
                return None
            
            data = response.json()
            
            # Save image
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{subject.lower()}_{timestamp}.png"
            filepath = os.path.join(output_dir, filename)
            
            # Decode and save base64 image
            image_data = data["artifacts"][0]["base64"]
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(image_data))
            
            logger.info(f"✅ Saved to: {filepath}")
            
            return {
                "filepath": filepath,
                "prompt": prompt,
                "enhanced_prompt": enhanced_prompt,
                "subject": subject,
                "width": width,
                "height": height,
                "generated_at": datetime.now().isoformat(),
                "seed": data["artifacts"][0].get("seed")
            }
            
        except Exception as e:
            logger.error(f"❌ Generation failed: {str(e)}")
            return None
    
    def _enhance_educational_prompt(self, prompt: str, subject: str, style: str) -> str:
        """Enhance prompt with educational styling and subject context"""
        
        style_presets = {
            "educational": "clean diagram, educational illustration, textbook style, clear labels, professional",
            "scientific": "scientific diagram, technical illustration, detailed, accurate, labeled",
            "simple": "simple diagram, minimalist, clear, easy to understand, basic",
            "detailed": "detailed illustration, comprehensive diagram, annotated, informative"
        }
        
        style_suffix = style_presets.get(style, style_presets["educational"])
        
        subject_contexts = {
            "Mathematics": "mathematical diagram, geometric illustration, clear notation",
            "Physics": "physics diagram, scientific illustration, forces and motion",
            "Chemistry": "chemistry diagram, molecular structure, chemical bonds",
            "Biology": "biology diagram, anatomical illustration, life science",
            "Geography": "geographical illustration, map diagram, terrain features",
            "Economics": "economic chart, business diagram, graphs and data"
        }
        
        subject_context = subject_contexts.get(subject, "educational diagram")
        
        return f"{prompt}, {subject_context}, {style_suffix}, white background, high quality, 4k"
    
    def generate_batch_images(
        self,
        prompts: List[Dict[str, str]],
        output_dir: str = "generated_content/diagrams"
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple images in batch
        
        Args:
            prompts: List of dicts with 'prompt', 'subject', and optional 'style'
            output_dir: Output directory
            
        Returns:
            List of generation results
        """
        results = []
        
        for idx, item in enumerate(prompts, 1):
            logger.info(f"[{idx}/{len(prompts)}] Generating...")
            
            result = self.generate_educational_image(
                prompt=item["prompt"],
                subject=item["subject"],
                output_dir=output_dir,
                style=item.get("style", "educational")
            )
            
            if result:
                results.append(result)
        
        logger.info(f"\n✅ Generated {len(results)}/{len(prompts)} images")
        return results
    
    def check_credits(self) -> Dict[str, Any]:
        """Check remaining API credits"""
        try:
            response = requests.get(
                f"{self.base_url}/user/balance",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": response.text}
        except Exception as e:
            return {"error": str(e)}


def create_lesson_visuals(lesson_data: Dict[str, Any], api_key: Optional[str] = None) -> List[str]:
    """
    Generate visual aids for a lesson
    
    Args:
        lesson_data: Lesson dict with subject, topic, and content
        api_key: Stability AI API key
        
    Returns:
        List of generated image paths
    """
    generator = StabilityAIGenerator(api_key=api_key)
    
    subject = lesson_data.get("subject", "General")
    topic = lesson_data.get("topic", "")
    
    # Generate key concept illustrations
    prompts = [
        {
            "prompt": f"Diagram illustrating {topic}",
            "subject": subject,
            "style": "educational"
        }
    ]
    
    results = generator.generate_batch_images(prompts)
    return [r["filepath"] for r in results]


if __name__ == "__main__":
    # Test the integration
    print("\n" + "="*70)
    print("🎨 STABILITY AI DREAM STUDIO - Educational Image Generation")
    print("="*70)
    
    # Check for API key
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        print("\n⚠️  STABILITY_API_KEY not found in environment!")
        print("Get your free API key from: https://dreamstudio.ai/account")
        print("\nAdd to .env file:")
        print("STABILITY_API_KEY=your_key_here")
        exit(1)
    
    generator = StabilityAIGenerator(api_key=api_key)
    
    # Check credits
    print("\n📊 Checking API credits...")
    credits = generator.check_credits()
    print(f"Credits: {json.dumps(credits, indent=2)}")
    
    # Test generation with sample educational prompts
    print("\n🎨 Generating sample educational images...")
    
    test_prompts = [
        {
            "prompt": "Quadratic function parabola with vertex and axis of symmetry",
            "subject": "Mathematics",
            "style": "educational"
        },
        {
            "prompt": "Newton's laws of motion diagram with forces and acceleration",
            "subject": "Physics",
            "style": "scientific"
        },
        {
            "prompt": "Periodic table with element groups highlighted",
            "subject": "Chemistry",
            "style": "simple"
        }
    ]
    
    results = generator.generate_batch_images(test_prompts)
    
    print("\n" + "="*70)
    print(f"✅ Generated {len(results)} images")
    for r in results:
        print(f"   - {r['filepath']}")
    print("="*70 + "\n")
