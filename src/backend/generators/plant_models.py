"""
Plant 3D Model Generator
Generates detailed plant anatomy and photosynthesis models

Priority #2 from 3D_ASSETS_PRIORITY_PLAN.md:
- Very high exam weight biology topic (bio_002)
- 5 plant models for JSS3/SS1
- GLB format for AR/VR integration
"""

import numpy as np
import trimesh
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlantModelGenerator:
    """
    Generates 3D plant anatomy and photosynthesis models for educational content
    Focus: Plant biology for WAEC/NECO curriculum (bio_002)
    """
    
    def __init__(self, output_dir: str = "generated_assets/plant_models"):
        """
        Initialize the plant model generator
        
        Args:
            output_dir: Directory to save generated 3D models
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generated_models = []
        logger.info(f"PlantModelGenerator initialized. Output: {self.output_dir}")
    
    def _create_basic_mesh(self, shape: str, dimensions: Tuple[float, ...], 
                          color: Tuple[int, int, int, int]) -> trimesh.Trimesh:
        """Create basic mesh shapes with color"""
        if shape == 'sphere':
            mesh = trimesh.creation.icosphere(subdivisions=3, radius=dimensions[0])
        elif shape == 'cylinder':
            mesh = trimesh.creation.cylinder(radius=dimensions[0], height=dimensions[1], sections=32)
        elif shape == 'ellipsoid':
            mesh = trimesh.creation.icosphere(subdivisions=3, radius=1.0)
            mesh.apply_scale(dimensions)
        elif shape == 'box':
            mesh = trimesh.creation.box(extents=dimensions)
        else:
            mesh = trimesh.creation.box(extents=[1, 1, 1])
        
        mesh.visual.vertex_colors = color
        return mesh
    
    def _combine_meshes(self, meshes: List[trimesh.Trimesh], 
                       positions: List[Tuple[float, float, float]]) -> trimesh.Trimesh:
        """Combine multiple meshes at specified positions"""
        positioned_meshes = []
        for mesh, pos in zip(meshes, positions):
            mesh_copy = mesh.copy()
            mesh_copy.apply_translation(pos)
            positioned_meshes.append(mesh_copy)
        
        return trimesh.util.concatenate(positioned_meshes)
    
    def generate_plant_cell(self) -> Dict:
        """
        Generate detailed plant cell model with organelles
        Components: cell wall, cell membrane, nucleus, chloroplasts, vacuole, mitochondria
        """
        logger.info("Generating plant cell model...")
        
        # Colors
        color_cell_wall = (144, 238, 144, 255)    # Light green (cellulose)
        color_membrane = (255, 192, 203, 255)     # Pink
        color_nucleus = (255, 165, 0, 255)        # Orange
        color_chloroplast = (34, 139, 34, 255)    # Forest green
        color_vacuole = (173, 255, 47, 255)       # Green-yellow
        color_mitochondria = (139, 69, 19, 255)   # Brown
        
        # Create organelles
        cell_wall = self._create_basic_mesh('box', (4.0, 4.0, 3.0), color_cell_wall)
        cell_membrane = self._create_basic_mesh('box', (3.8, 3.8, 2.8), color_membrane)
        nucleus = self._create_basic_mesh('sphere', (0.8,), color_nucleus)
        vacuole = self._create_basic_mesh('ellipsoid', (1.8, 1.5, 1.5), color_vacuole)
        
        # Chloroplasts (multiple)
        chloroplasts = [
            self._create_basic_mesh('ellipsoid', (0.5, 0.6, 0.4), color_chloroplast),
            self._create_basic_mesh('ellipsoid', (0.5, 0.6, 0.4), color_chloroplast),
            self._create_basic_mesh('ellipsoid', (0.5, 0.6, 0.4), color_chloroplast),
            self._create_basic_mesh('ellipsoid', (0.5, 0.6, 0.4), color_chloroplast)
        ]
        
        # Mitochondria
        mitochondria = [
            self._create_basic_mesh('ellipsoid', (0.3, 0.4, 0.3), color_mitochondria),
            self._create_basic_mesh('ellipsoid', (0.3, 0.4, 0.3), color_mitochondria)
        ]
        
        # Position organelles
        all_meshes = [cell_wall, cell_membrane, nucleus, vacuole] + chloroplasts + mitochondria
        positions = [
            (0, 0, 0),      # cell wall (center)
            (0, 0, 0),      # cell membrane
            (0.5, 0.5, 0),  # nucleus
            (-0.5, 0, -0.5),# vacuole (large, center)
            (1.2, 1.0, 0),  # chloroplast 1
            (-1.2, 1.0, 0), # chloroplast 2
            (1.0, -0.8, 0.5),# chloroplast 3
            (-0.8, -1.0, -0.5),# chloroplast 4
            (0.5, -0.5, 0.8),# mitochondria 1
            (-0.6, 0.3, -0.6) # mitochondria 2
        ]
        
        plant_cell = self._combine_meshes(all_meshes, positions)
        
        # Save
        filename = "plant_cell.glb"
        filepath = self.output_dir / filename
        plant_cell.export(str(filepath))
        
        metadata = {
            "filename": filename,
            "filepath": str(filepath),
            "model": "Plant Cell",
            "components": ["Cell Wall", "Cell Membrane", "Nucleus", "Chloroplasts", "Vacuole", "Mitochondria"],
            "exam_topics": ["bio_002"],
            "grade_levels": ["JSS3", "SS1"],
            "vertices": len(plant_cell.vertices),
            "faces": len(plant_cell.faces),
            "file_size_kb": round(filepath.stat().st_size / 1024, 2),
            "educational_notes": "Detailed plant cell showing all major organelles and their positions",
            "ar_ready": True,
            "curriculum_standard": ["WAEC", "NECO"]
        }
        
        self.generated_models.append(metadata)
        logger.info(f"✅ Generated: {filename} ({metadata['file_size_kb']} KB)")
        return metadata
    
    def generate_leaf_structure(self) -> Dict:
        """
        Generate leaf cross-section model
        Components: upper epidermis, palisade mesophyll, spongy mesophyll, stomata, lower epidermis
        """
        logger.info("Generating leaf structure model...")
        
        # Colors
        color_epidermis = (255, 255, 200, 255)     # Light yellow
        color_palisade = (0, 200, 100, 255)        # Teal
        color_spongy = (100, 200, 150, 255)        # Light teal
        color_stoma = (100, 100, 100, 255)         # Gray
        color_vein = (139, 69, 19, 255)            # Brown (vascular tissue)
        
        # Create leaf layers (cross-section view)
        upper_epidermis = self._create_basic_mesh('box', (5.0, 0.4, 0.5), color_epidermis)
        palisade_mesophyll = self._create_basic_mesh('box', (5.0, 1.2, 0.5), color_palisade)
        spongy_mesophyll = self._create_basic_mesh('box', (5.0, 1.0, 0.5), color_spongy)
        lower_epidermis = self._create_basic_mesh('box', (5.0, 0.4, 0.5), color_epidermis)
        
        # Vascular bundle (vein)
        vein = self._create_basic_mesh('box', (5.0, 0.3, 0.8), color_vein)
        
        # Stomata (on lower epidermis)
        stomata = [
            self._create_basic_mesh('ellipsoid', (0.3, 0.2, 0.1), color_stoma),
            self._create_basic_mesh('ellipsoid', (0.3, 0.2, 0.1), color_stoma),
            self._create_basic_mesh('ellipsoid', (0.3, 0.2, 0.1), color_stoma)
        ]
        
        # Position layers (cross-section)
        all_meshes = [upper_epidermis, palisade_mesophyll, spongy_mesophyll, lower_epidermis, vein] + stomata
        positions = [
            (0, 2.0, 0),    # upper epidermis
            (0, 1.2, 0),    # palisade mesophyll
            (0, 0, 0),      # spongy mesophyll (center)
            (0, -1.2, 0),   # lower epidermis
            (0, 0.2, 0.5),  # vein
            (1.5, -1.3, 0), # stoma 1
            (0, -1.3, 0),   # stoma 2
            (-1.5, -1.3, 0) # stoma 3
        ]
        
        leaf_structure = self._combine_meshes(all_meshes, positions)
        
        # Save
        filename = "leaf_structure.glb"
        filepath = self.output_dir / filename
        leaf_structure.export(str(filepath))
        
        metadata = {
            "filename": filename,
            "filepath": str(filepath),
            "model": "Leaf Structure (Cross-Section)",
            "components": ["Upper Epidermis", "Palisade Mesophyll", "Spongy Mesophyll", "Lower Epidermis", "Stomata", "Vein"],
            "exam_topics": ["bio_002"],
            "grade_levels": ["JSS3", "SS1"],
            "vertices": len(leaf_structure.vertices),
            "faces": len(leaf_structure.faces),
            "file_size_kb": round(filepath.stat().st_size / 1024, 2),
            "educational_notes": "Leaf cross-section showing tissue layers and stomata for gas exchange",
            "ar_ready": True,
            "curriculum_standard": ["WAEC", "NECO"]
        }
        
        self.generated_models.append(metadata)
        logger.info(f"✅ Generated: {filename} ({metadata['file_size_kb']} KB)")
        return metadata
    
    def generate_root_system(self) -> Dict:
        """
        Generate root system model
        Components: tap root (main), lateral roots, root hairs, fibrous root alternative
        """
        logger.info("Generating root system model...")
        
        # Colors
        color_main_root = (139, 69, 19, 255)       # Brown
        color_lateral = (160, 82, 45, 255)         # Sienna
        color_root_hair = (210, 105, 30, 255)      # Chocolate
        color_rootlet = (180, 82, 45, 255)         # Lighter brown
        
        # Create tap root system
        main_root = self._create_basic_mesh('cylinder', (0.6, 6.0), color_main_root)
        
        # Lateral roots
        lateral_roots = [
            self._create_basic_mesh('cylinder', (0.3, 2.0), color_lateral),
            self._create_basic_mesh('cylinder', (0.3, 2.2), color_lateral),
            self._create_basic_mesh('cylinder', (0.3, 1.8), color_lateral),
            self._create_basic_mesh('cylinder', (0.3, 2.1), color_lateral)
        ]
        
        # Root hairs (simplified)
        root_hairs = [
            self._create_basic_mesh('cylinder', (0.1, 0.8), color_root_hair),
            self._create_basic_mesh('cylinder', (0.1, 0.7), color_root_hair),
            self._create_basic_mesh('cylinder', (0.1, 0.9), color_root_hair)
        ]
        
        # Fibrous roots (alternative showing)
        fibrous_roots = [
            self._create_basic_mesh('cylinder', (0.3, 3.0), color_rootlet),
            self._create_basic_mesh('cylinder', (0.3, 2.8), color_rootlet),
            self._create_basic_mesh('cylinder', (0.3, 3.2), color_rootlet)
        ]
        
        # Position root system
        all_meshes = [main_root] + lateral_roots + root_hairs + fibrous_roots
        positions = [
            (0, 0, 0),      # main tap root
            (1.0, -2.0, 0), # lateral root 1
            (-1.2, -1.5, 0),# lateral root 2
            (0.8, -3.5, 0), # lateral root 3
            (-0.9, -2.8, 0),# lateral root 4
            (0.3, -4.5, 0), # root hair 1
            (-0.4, -4.8, 0),# root hair 2
            (0.2, -5.2, 0), # root hair 3
            (2.5, 0.5, 0),  # fibrous root 1 (shown beside)
            (3.2, -1.0, 0), # fibrous root 2
            (2.8, -2.2, 0)  # fibrous root 3
        ]
        
        root_system = self._combine_meshes(all_meshes, positions)
        
        # Save
        filename = "root_system.glb"
        filepath = self.output_dir / filename
        root_system.export(str(filepath))
        
        metadata = {
            "filename": filename,
            "filepath": str(filepath),
            "model": "Root System",
            "components": ["Tap Root", "Lateral Roots", "Root Hairs", "Fibrous Roots (shown for comparison)"],
            "exam_topics": ["bio_002"],
            "grade_levels": ["JSS3", "SS1"],
            "vertices": len(root_system.vertices),
            "faces": len(root_system.faces),
            "file_size_kb": round(filepath.stat().st_size / 1024, 2),
            "educational_notes": "Shows both tap root (with laterals) and fibrous root systems for comparison",
            "ar_ready": True,
            "curriculum_standard": ["WAEC", "NECO"]
        }
        
        self.generated_models.append(metadata)
        logger.info(f"✅ Generated: {filename} ({metadata['file_size_kb']} KB)")
        return metadata
    
    def generate_flower_structure(self) -> Dict:
        """
        Generate flower structure model
        Components: sepal, petal, stamen (anther, filament), pistil (stigma, style, ovary)
        """
        logger.info("Generating flower structure model...")
        
        # Colors
        color_sepal = (34, 139, 34, 255)          # Dark green
        color_petal = (255, 105, 180, 255)        # Hot pink
        color_stamen = (255, 215, 0, 255)         # Gold
        color_anther = (255, 140, 0, 255)         # Dark orange
        color_pistil = (138, 43, 226, 255)        # Blue violet
        color_ovary = (186, 85, 211, 255)         # Medium orchid
        
        # Create flower parts
        # Sepals (green leafy parts)
        sepals = [
            self._create_basic_mesh('ellipsoid', (0.5, 0.8, 0.2), color_sepal),
            self._create_basic_mesh('ellipsoid', (0.5, 0.8, 0.2), color_sepal),
            self._create_basic_mesh('ellipsoid', (0.5, 0.8, 0.2), color_sepal),
            self._create_basic_mesh('ellipsoid', (0.5, 0.8, 0.2), color_sepal)
        ]
        
        # Petals (colored)
        petals = [
            self._create_basic_mesh('ellipsoid', (0.6, 1.0, 0.2), color_petal),
            self._create_basic_mesh('ellipsoid', (0.6, 1.0, 0.2), color_petal),
            self._create_basic_mesh('ellipsoid', (0.6, 1.0, 0.2), color_petal),
            self._create_basic_mesh('ellipsoid', (0.6, 1.0, 0.2), color_petal)
        ]
        
        # Stamens (male)
        filaments = [
            self._create_basic_mesh('cylinder', (0.2, 1.2), color_stamen),
            self._create_basic_mesh('cylinder', (0.2, 1.2), color_stamen),
            self._create_basic_mesh('cylinder', (0.2, 1.2), color_stamen)
        ]
        
        anthers = [
            self._create_basic_mesh('box', (0.3, 0.3, 0.3), color_anther),
            self._create_basic_mesh('box', (0.3, 0.3, 0.3), color_anther),
            self._create_basic_mesh('box', (0.3, 0.3, 0.3), color_anther)
        ]
        
        # Pistil (female)
        style = self._create_basic_mesh('cylinder', (0.15, 1.0), color_pistil)
        stigma = self._create_basic_mesh('sphere', (0.3,), color_anther)
        ovary = self._create_basic_mesh('sphere', (0.5,), color_ovary)
        
        # Position flower parts (center = receptacle)
        all_meshes = sepals + petals + filaments + anthers + [style, stigma, ovary]
        positions = [
            # Sepals (outer)
            (0.8, 0, 0),    (0, 0.8, 0),    (-0.8, 0, 0),   (0, -0.8, 0),
            # Petals (between sepals)
            (0.6, 0.6, 0),  (-0.6, 0.6, 0), (-0.6, -0.6, 0), (0.6, -0.6, 0),
            # Filaments
            (0.3, 0.3, 0),  (-0.3, 0.3, 0), (0, -0.4, 0),
            # Anthers (on top of filaments)
            (0.3, 1.4, 0),  (-0.3, 1.4, 0), (0, 1.0, 0),
            # Pistil (center)
            (0, 0, 0.3),    (0, 0.9, 0.3),  (0, -0.2, -0.3)
        ]
        
        flower = self._combine_meshes(all_meshes, positions)
        
        # Save
        filename = "flower_structure.glb"
        filepath = self.output_dir / filename
        flower.export(str(filepath))
        
        metadata = {
            "filename": filename,
            "filepath": str(filepath),
            "model": "Flower Structure",
            "components": ["Sepal", "Petal", "Stamen (Anther, Filament)", "Pistil (Stigma, Style, Ovary)"],
            "exam_topics": ["bio_002"],
            "grade_levels": ["JSS3", "SS1"],
            "vertices": len(flower.vertices),
            "faces": len(flower.faces),
            "file_size_kb": round(filepath.stat().st_size / 1024, 2),
            "educational_notes": "Complete flower anatomy showing male and female reproductive parts",
            "ar_ready": True,
            "curriculum_standard": ["WAEC", "NECO"],
            "nigerian_context": "Typical Nigerian flower structure"
        }
        
        self.generated_models.append(metadata)
        logger.info(f"✅ Generated: {filename} ({metadata['file_size_kb']} KB)")
        return metadata
    
    def generate_photosynthesis_process(self) -> Dict:
        """
        Generate photosynthesis process model
        Components: chloroplast, thylakoid, stroma, light reactions, dark reactions
        """
        logger.info("Generating photosynthesis process model...")
        
        # Colors
        color_chloroplast = (34, 139, 34, 255)    # Dark green
        color_thylakoid = (0, 255, 127, 255)      # Spring green
        color_stroma = (144, 238, 144, 255)       # Light green
        color_light_react = (255, 215, 0, 255)    # Gold (light reactions)
        color_dark_react = (255, 105, 180, 255)   # Hot pink (dark reactions/Calvin cycle)
        color_molecule = (100, 149, 237, 255)     # Cornflower (molecules)
        
        # Create chloroplast structure
        chloroplast_outer = self._create_basic_mesh('ellipsoid', (2.0, 2.5, 1.5), color_chloroplast)
        
        # Thylakoid stacks (grana)
        thylakoids = [
            self._create_basic_mesh('box', (1.5, 0.2, 0.3), color_thylakoid),
            self._create_basic_mesh('box', (1.5, 0.2, 0.3), color_thylakoid),
            self._create_basic_mesh('box', (1.5, 0.2, 0.3), color_thylakoid),
            self._create_basic_mesh('box', (1.5, 0.2, 0.3), color_thylakoid)
        ]
        
        # Light reaction zone
        light_reactions = [
            self._create_basic_mesh('sphere', (0.4,), color_light_react),
            self._create_basic_mesh('sphere', (0.4,), color_light_react)
        ]
        
        # Dark reaction zone (Calvin cycle)
        dark_reactions = [
            self._create_basic_mesh('sphere', (0.5,), color_dark_react),
            self._create_basic_mesh('sphere', (0.5,), color_dark_react),
            self._create_basic_mesh('sphere', (0.5,), color_dark_react)
        ]
        
        # Molecule representations
        molecules = [
            self._create_basic_mesh('sphere', (0.3,), color_molecule),  # CO2
            self._create_basic_mesh('sphere', (0.3,), color_molecule),  # H2O
            self._create_basic_mesh('sphere', (0.3,), color_molecule)   # Glucose
        ]
        
        # Position components
        all_meshes = [chloroplast_outer] + thylakoids + light_reactions + dark_reactions + molecules
        positions = [
            (0, 0, 0),      # chloroplast outer membrane
            # Thylakoids
            (0.5, 0.8, -0.3), (-0.5, 0.6, -0.3), (0.5, 0.2, 0.2), (-0.5, -0.2, 0.2),
            # Light reactions
            (-1.0, 1.0, -0.5), (1.0, 1.0, -0.5),
            # Dark reactions (Calvin cycle in stroma)
            (-0.8, -0.8, 0), (0, -1.0, 0), (0.8, -0.8, 0),
            # Input/Output molecules
            (-1.5, 0, 0.5),   # CO2 input
            (1.5, 0, 0.5),    # H2O input (from roots)
            (0, -1.5, 0)      # Glucose output
        ]
        
        photosynthesis = self._combine_meshes(all_meshes, positions)
        
        # Save
        filename = "photosynthesis_process.glb"
        filepath = self.output_dir / filename
        photosynthesis.export(str(filepath))
        
        metadata = {
            "filename": filename,
            "filepath": str(filepath),
            "model": "Photosynthesis Process",
            "components": ["Chloroplast", "Thylakoid (Light Reactions)", "Stroma (Dark Reactions/Calvin Cycle)", "Molecules (CO2, H2O, Glucose)"],
            "exam_topics": ["bio_002"],
            "grade_levels": ["SS1"],
            "vertices": len(photosynthesis.vertices),
            "faces": len(photosynthesis.faces),
            "file_size_kb": round(filepath.stat().st_size / 1024, 2),
            "educational_notes": "Chloroplast showing light reactions in thylakoids and dark reactions in stroma",
            "ar_ready": True,
            "curriculum_standard": ["WAEC", "NECO"],
            "animation_ready": "Light reactions vs dark reactions separation"
        }
        
        self.generated_models.append(metadata)
        logger.info(f"✅ Generated: {filename} ({metadata['file_size_kb']} KB)")
        return metadata
    
    def generate_all_plant_models(self) -> List[Dict]:
        """Generate all 5 priority plant models"""
        logger.info("="*70)
        logger.info("🌱 GENERATING PRIORITY #2: PLANT ANATOMY AND PHOTOSYNTHESIS")
        logger.info("="*70)
        
        models = [
            self.generate_plant_cell(),
            self.generate_leaf_structure(),
            self.generate_root_system(),
            self.generate_flower_structure(),
            self.generate_photosynthesis_process()
        ]
        
        logger.info("="*70)
        logger.info(f"✅ Generated {len(models)} plant models")
        logger.info("="*70)
        
        return models
    
    def generate_manifest(self) -> str:
        """Generate JSON manifest of all plant models"""
        manifest = {
            "collection": "Plant Anatomy and Photosynthesis",
            "priority": 2,
            "exam_weight": "Very High",
            "subject": "Biology",
            "topic_code": "bio_002",
            "grade_levels": ["JSS3", "SS1"],
            "curriculum_standards": ["WAEC", "NECO"],
            "total_models": len(self.generated_models),
            "models": self.generated_models,
            "ar_vr_ready": True,
            "file_format": "GLB (glTF 2.0 binary)",
            "generated_date": "2026-01-11"
        }
        
        manifest_path = self.output_dir / "plant_models_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"📄 Manifest saved: {manifest_path}")
        return str(manifest_path)
    
    def get_statistics(self) -> Dict:
        """Get generation statistics"""
        total_vertices = sum(m['vertices'] for m in self.generated_models)
        total_faces = sum(m['faces'] for m in self.generated_models)
        total_size = sum(m['file_size_kb'] for m in self.generated_models)
        
        return {
            "total_models": len(self.generated_models),
            "total_vertices": total_vertices,
            "total_faces": total_faces,
            "total_size_kb": round(total_size, 2),
            "average_size_kb": round(total_size / len(self.generated_models), 2) if self.generated_models else 0,
            "models": [m['model'] for m in self.generated_models]
        }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate plant 3D models")
    parser.add_argument('--output', default='generated_assets/plant_models',
                       help='Output directory for models')
    parser.add_argument('--model', choices=['plant_cell', 'leaf', 'root', 'flower', 'photosynthesis', 'all'],
                       default='all', help='Which model to generate')
    
    args = parser.parse_args()
    
    generator = PlantModelGenerator(args.output)
    
    if args.model == 'all':
        generator.generate_all_plant_models()
    else:
        method_map = {
            'plant_cell': 'generate_plant_cell',
            'leaf': 'generate_leaf_structure',
            'root': 'generate_root_system',
            'flower': 'generate_flower_structure',
            'photosynthesis': 'generate_photosynthesis_process'
        }
        if args.model in method_map:
            getattr(generator, method_map[args.model])()
    
    generator.generate_manifest()
    
    stats = generator.get_statistics()
    print(f"\n📊 Generation Statistics:")
    print(f"   Models: {stats['total_models']}")
    print(f"   Total Size: {stats['total_size_kb']} KB")
    print(f"   Models: {', '.join(stats['models'])}")
