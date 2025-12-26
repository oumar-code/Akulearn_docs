#!/usr/bin/env python3
"""
Lesson Visual Assets Generator
Generates diagrams, illustrations, and infographics for lesson content
Uses Gemini Nano for text-to-diagram, Banana API for illustrations
"""

import json
import os
import requests
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not required; will use os.getenv directly
    pass


class AssetType(Enum):
    """Asset generation types"""
    DIAGRAM_FLOWCHART = "flowchart"
    DIAGRAM_NETWORK = "network"
    DIAGRAM_ARCHITECTURE = "architecture"
    ILLUSTRATION = "illustration"
    INFOGRAPHIC = "infographic"
    DIAGRAM_ASCII = "ascii"
    DIAGRAM_PLANTUML = "plantuml"


@dataclass
class AssetSpec:
    """Visual asset specification"""
    asset_id: str
    title: str
    type: AssetType
    description: str
    subject: str
    lesson: str
    context: str
    nigerian_context: bool = True
    prompt_override: Optional[str] = None


class GeminiNanoAdapter:
    """Wrapper for Gemini Nano API (diagram generation via text)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def generate_plantuml(self, description: str, diagram_type: str = "flowchart") -> str:
        """Generate PlantUML code from description via Gemini Nano"""
        prompt = f"""Generate PlantUML code for a {diagram_type}. 
        Description: {description}
        
        Return ONLY the PlantUML code block, no explanation.
        Use @startuml/@enduml markers.
        Make it educational and clear."""
        
        try:
            response = requests.post(
                f"{self.base_url}/gemini-nano:generateContent",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 1024,
                    }
                },
                headers={"x-goog-api-key": self.api_key}
            )
            response.raise_for_status()
            
            result = response.json()
            if "candidates" in result and result["candidates"]:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            return ""
        except Exception as e:
            print(f"❌ Gemini Nano error: {e}")
            return self._fallback_plantuml(diagram_type)
    
    def generate_graphviz(self, description: str) -> str:
        """Generate Graphviz DOT code for diagrams"""
        prompt = f"""Generate Graphviz DOT code for a network/system diagram.
        Description: {description}
        
        Return ONLY the DOT code, no explanation.
        Use digraph {{ ... }} format.
        Make nodes and labels clear."""
        
        try:
            response = requests.post(
                f"{self.base_url}/gemini-nano:generateContent",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1024}
                },
                headers={"x-goog-api-key": self.api_key}
            )
            response.raise_for_status()
            
            result = response.json()
            if "candidates" in result and result["candidates"]:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            return ""
        except Exception as e:
            print(f"❌ Graphviz generation error: {e}")
            return ""
    
    def generate_svg_ascii(self, description: str) -> str:
        """Generate ASCII diagram for quick reference"""
        prompt = f"""Create an ASCII art diagram (box drawing characters).
        Description: {description}
        
        Make it educational, use box drawing chars, max 20x30 chars.
        Return ONLY the ASCII art."""
        
        try:
            response = requests.post(
                f"{self.base_url}/gemini-nano:generateContent",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 512}
                },
                headers={"x-goog-api-key": self.api_key}
            )
            response.raise_for_status()
            
            result = response.json()
            if "candidates" in result and result["candidates"]:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            return ""
        except Exception as e:
            print(f"❌ ASCII diagram error: {e}")
            return ""
    
    @staticmethod
    def _fallback_plantuml(diagram_type: str) -> str:
        """Fallback PlantUML if API fails"""
        fallbacks = {
            "flowchart": """@startuml
start
:Input;
:Process;
:Output;
stop
@enduml""",
            "class": """@startuml
class Lesson {
  title
  content()
}
@enduml"""
        }
        return fallbacks.get(diagram_type, "")


class BananaAPIAdapter:
    """Wrapper for Banana API (illustration generation)"""
    
    def __init__(self, api_key: str, model: str = "stable-diffusion-v1-5"):
        self.api_key = api_key
        self.model = model
        self.endpoint = "https://api.banana.dev/start/v4"
    
    def generate_illustration(self, prompt: str, negative_prompt: str = "") -> Optional[bytes]:
        """Generate illustration from prompt"""
        
        # Enhance prompt with educational context
        enhanced_prompt = f"{prompt}. Educational illustration. High quality. Clear and detailed."
        
        try:
            payload = {
                "model_name": self.model,
                "task_name": "generate",
                "webhook": None,
                "startupToken": self.api_key,
                "modelInputs": {
                    "prompt": enhanced_prompt,
                    "negative_prompt": negative_prompt or "blurry, low quality, distorted",
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5,
                    "width": 768,
                    "height": 768,
                }
            }
            
            response = requests.post(self.endpoint, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            if result.get("processingStatus") == "SUCCESS" and "modelOutputs" in result:
                # Image is typically base64 encoded in response
                image_data = result["modelOutputs"].get("image", "")
                if image_data:
                    return base64.b64decode(image_data)
            return None
        except Exception as e:
            print(f"❌ Banana API error: {e}")
            return None


class AssetGenerator:
    """Main asset generation orchestrator"""
    
    def __init__(self, json_path: str, gemini_key: str = None, banana_key: str = None):
        self.json_path = json_path
        with open(json_path, 'r', encoding='utf-8') as f:
            self.lesson = json.load(f)
        
        self.gemini = GeminiNanoAdapter(gemini_key) if gemini_key else None
        self.banana = BananaAPIAdapter(banana_key) if banana_key else None
        
        # Setup output directories
        subject = self.lesson['metadata']['subject']
        level = self.lesson['metadata']['level']
        lesson_num = self.lesson['metadata']['lesson'].zfill(2)
        
        self.asset_dir = Path(f"content/ai_generated/assets/{subject}/{level}/lesson_{lesson_num}")
        self.rendered_dir = Path(f"content/ai_rendered/assets/{subject}/{level}/lesson_{lesson_num}")
        
        self.asset_dir.mkdir(parents=True, exist_ok=True)
        self.rendered_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all_assets(self) -> List[str]:
        """Generate all assets specified in lesson"""
        generated = []
        
        # Extract visual aids from lesson
        visual_aids = self.lesson.get('resources', {}).get('visual_aids', [])
        
        for aid in visual_aids:
            print(f"\n🎨 Generating: {aid['title']}")
            
            # Sanitize asset ID (remove special chars like /)
            asset_id = aid['title'].lower().replace(' ', '_').replace('/', '_')
            
            asset_spec = AssetSpec(
                asset_id=asset_id,
                title=aid['title'],
                type=self._infer_asset_type(aid),
                description=aid['description'],
                subject=self.lesson['metadata']['subject'],
                lesson=self.lesson['metadata']['lesson'],
                context=self.lesson['metadata']['lesson_title'],
            )
            
            result = self.generate_asset(asset_spec)
            if result:
                generated.append(result)
        
        return generated
    
    def generate_asset(self, spec: AssetSpec) -> Optional[str]:
        """Generate single asset based on spec"""
        
        if spec.type == AssetType.DIAGRAM_PLANTUML:
            return self._generate_plantuml_diagram(spec)
        elif spec.type == AssetType.DIAGRAM_NETWORK:
            return self._generate_network_diagram(spec)
        elif spec.type == AssetType.DIAGRAM_ARCHITECTURE:
            return self._generate_architecture_diagram(spec)
        elif spec.type == AssetType.ILLUSTRATION:
            return self._generate_illustration(spec)
        elif spec.type == AssetType.DIAGRAM_ASCII:
            return self._generate_ascii_diagram(spec)
        else:
            print(f"⚠️  Unknown asset type: {spec.type}")
            return None
    
    def _generate_plantuml_diagram(self, spec: AssetSpec) -> Optional[str]:
        """Generate flowchart/sequence diagram via PlantUML"""
        if not self.gemini:
            print(f"⚠️  Gemini Nano not configured, creating fallback PlantUML for: {spec.asset_id}")
            return self._save_fallback_plantuml(spec)
        
        plantuml_code = self.gemini.generate_plantuml(spec.description, "flowchart")
        
        if plantuml_code:
            output_path = self.asset_dir / f"{spec.asset_id}.plantuml"
            with open(output_path, 'w') as f:
                f.write(plantuml_code)
            print(f"✅ PlantUML saved: {output_path}")
            return str(output_path)
        return None
    
    def _save_fallback_plantuml(self, spec: AssetSpec) -> Optional[str]:
        """Save fallback PlantUML diagram"""
        fallback = """@startuml
title """ + spec.title.replace('"', "'") + """
start
:Process;
stop
@enduml"""
        
        output_path = self.asset_dir / f"{spec.asset_id}.plantuml"
        with open(output_path, 'w') as f:
            f.write(fallback)
        print(f"✅ Fallback PlantUML saved: {output_path}")
        return str(output_path)
    
    def _generate_network_diagram(self, spec: AssetSpec) -> Optional[str]:
        """Generate network diagram via Graphviz"""
        if not self.gemini:
            print(f"⚠️  Gemini Nano not configured, creating fallback Graphviz for: {spec.asset_id}")
            return self._save_fallback_graphviz(spec)
        
        # For Nigerian context, enhance description
        enhanced_desc = f"{spec.description}. Include Nigerian school network setup context if applicable."
        
        graphviz_code = self.gemini.generate_graphviz(enhanced_desc)
        
        if graphviz_code:
            output_path = self.asset_dir / f"{spec.asset_id}.dot"
            with open(output_path, 'w') as f:
                f.write(graphviz_code)
            print(f"✅ Graphviz saved: {output_path}")
            return str(output_path)
        return None
    
    def _save_fallback_graphviz(self, spec: AssetSpec) -> Optional[str]:
        """Save fallback Graphviz diagram"""
        fallback = """digraph G {
    rankdir=LR;
    node [shape=box];
    A [label="Input"];
    B [label="Process"];
    C [label="Output"];
    A -> B -> C;
}"""
        
        output_path = self.asset_dir / f"{spec.asset_id}.dot"
        with open(output_path, 'w') as f:
            f.write(fallback)
        print(f"✅ Fallback Graphviz saved: {output_path}")
        return str(output_path)
    
    def _generate_architecture_diagram(self, spec: AssetSpec) -> Optional[str]:
        """Generate system architecture diagram"""
        if not self.gemini:
            print(f"⚠️  Gemini Nano not configured, creating fallback architecture diagram for: {spec.asset_id}")
            return self._save_fallback_architecture(spec)
        
        plantuml_code = self.gemini.generate_plantuml(spec.description, "class")
        
        if plantuml_code:
            output_path = self.asset_dir / f"{spec.asset_id}.plantuml"
            with open(output_path, 'w') as f:
                f.write(plantuml_code)
            print(f"✅ Architecture diagram saved: {output_path}")
            return str(output_path)
        return None
    
    def _save_fallback_architecture(self, spec: AssetSpec) -> Optional[str]:
        """Save fallback architecture diagram"""
        fallback = """@startuml
class Component {
  property
  method()
}
@enduml"""
        
        output_path = self.asset_dir / f"{spec.asset_id}.plantuml"
        with open(output_path, 'w') as f:
            f.write(fallback)
        print(f"✅ Fallback architecture diagram saved: {output_path}")
        return str(output_path)
    
    def _generate_illustration(self, spec: AssetSpec) -> Optional[str]:
        """Generate illustration via Banana API"""
        if not self.banana:
            print("⚠️  Banana API not configured, skipping illustration")
            return None
        
        # Craft prompt for educational illustration
        prompt = f"{spec.description}. Nigerian education context. Subject: {spec.subject}. Lesson: {spec.context}."
        
        image_data = self.banana.generate_illustration(prompt)
        
        if image_data:
            output_path = self.rendered_dir / f"{spec.asset_id}.png"
            with open(output_path, 'wb') as f:
                f.write(image_data)
            print(f"✅ Illustration saved: {output_path}")
            return str(output_path)
        return None
    
    def _generate_ascii_diagram(self, spec: AssetSpec) -> Optional[str]:
        """Generate quick ASCII diagram"""
        if not self.gemini:
            print(f"⚠️  Gemini Nano not configured, creating fallback ASCII diagram for: {spec.asset_id}")
            return self._save_fallback_ascii(spec)
        
        ascii_art = self.gemini.generate_svg_ascii(spec.description)
        
        if ascii_art:
            output_path = self.asset_dir / f"{spec.asset_id}.txt"
            with open(output_path, 'w') as f:
                f.write(ascii_art)
            print(f"✅ ASCII diagram saved: {output_path}")
            return str(output_path)
        return None
    
    def _save_fallback_ascii(self, spec: AssetSpec) -> Optional[str]:
        """Save fallback ASCII diagram"""
        fallback = """+-----------+
| """ + spec.title[:11].ljust(11) + """|
+-----------+
| . Item 1  |
| . Item 2  |
| . Item 3  |
+-----------+"""
        
        output_path = self.asset_dir / f"{spec.asset_id}.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(fallback)
        print(f"✅ Fallback ASCII diagram saved: {output_path}")
        return str(output_path)
    
    @staticmethod
    def _infer_asset_type(aid: Dict[str, str]) -> AssetType:
        """Infer asset type from aid metadata"""
        type_str = aid.get('type', '').lower()
        description = aid.get('description', '').lower()
        
        if 'flowchart' in type_str or 'flowchart' in description or 'flow' in description:
            return AssetType.DIAGRAM_PLANTUML
        elif 'network' in type_str or 'network' in description:
            return AssetType.DIAGRAM_NETWORK
        elif 'architecture' in type_str or 'architecture' in description or 'diagram' in description:
            return AssetType.DIAGRAM_ARCHITECTURE
        elif 'illustration' in type_str or 'image' in type_str:
            return AssetType.ILLUSTRATION
        elif 'infographic' in type_str or 'chart' in description:
            return AssetType.INFOGRAPHIC
        elif 'ascii' in type_str:
            return AssetType.DIAGRAM_ASCII
        else:
            # Default to ASCII for quick reference
            return AssetType.DIAGRAM_ASCII


def batch_generate_assets(
    source_dir: str = "content/ai_generated/textbooks",
    gemini_key: str = None,
    banana_key: str = None
) -> Dict[str, List[str]]:
    """Batch generate assets for all lessons"""
    
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return {}
    
    json_files = list(source_path.rglob("lesson_*.json"))
    print(f"🔍 Found {len(json_files)} lessons to generate assets for\n")
    
    results = {}
    
    for json_file in json_files:
        try:
            print(f"📚 Processing: {json_file.relative_to(source_path)}")
            generator = AssetGenerator(str(json_file), gemini_key, banana_key)
            assets = generator.generate_all_assets()
            
            lesson_key = json_file.stem
            results[lesson_key] = assets
            
        except Exception as e:
            print(f"❌ Error processing {json_file}: {e}")
    
    print(f"\n✅ Asset generation complete: {sum(len(v) for v in results.values())} assets created")
    return results


if __name__ == "__main__":
    import sys
    
    # Load API keys from environment or .env file
    gemini_key = os.getenv("GEMINI_API_KEY")
    banana_key = os.getenv("BANANA_API_KEY")
    
    if len(sys.argv) > 1:
        # Generate assets for specific lesson
        json_path = sys.argv[1]
        print(f"🎨 Generating assets for: {json_path}\n")
        generator = AssetGenerator(json_path, gemini_key, banana_key)
        generator.generate_all_assets()
    else:
        # Batch generate for all lessons
        print("🚀 Batch generating assets for all lessons...\n")
        batch_generate_assets(
            "content/ai_generated/textbooks",
            gemini_key,
            banana_key
        )
