"""
Geometric 3D Shapes Generator
Priority #5: Mathematics Geometric Models for Nigerian Education System

Generates 8 foundational 3D shape models for mathematics curriculum:
- Cube, Cuboid, Cylinder, Cone, Sphere, Pyramid
- Prisms (triangular, hexagonal)
- Composite solids (combined shapes)

All models optimized for AR/VR and curriculum-aligned for WAEC/NECO standards.
"""

import trimesh
import numpy as np
from pathlib import Path
import json
import logging
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeometricShapeGenerator:
    """Generator for geometric 3D shape models for mathematics"""
    
    def __init__(self, output_dir: str = "generated_assets/geometric_shapes"):
        """
        Initialize the geometric shape generator
        
        Args:
            output_dir: Directory to save generated models
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"GeometricShapeGenerator initialized. Output: {self.output_dir}")
        
        # Color scheme for shapes (educational, distinct colors)
        self.shape_colors = {
            'cube': [255, 100, 100, 255],        # Red
            'cuboid': [100, 150, 255, 255],      # Blue
            'cylinder': [100, 255, 100, 255],    # Green
            'cone': [255, 200, 100, 255],        # Orange
            'sphere': [200, 100, 255, 255],      # Purple
            'pyramid': [255, 255, 100, 255],     # Yellow
            'prism': [100, 255, 200, 255],       # Cyan
            'composite': [255, 150, 200, 255],   # Pink
            'edge': [50, 50, 50, 255],           # Dark gray for edges
            'label': [255, 255, 255, 255],       # White for labels
        }
    
    def _add_edge_highlights(self, mesh: trimesh.Trimesh) -> List[trimesh.Trimesh]:
        """Add thin cylinders along edges for educational clarity"""
        edge_meshes = []
        edges = mesh.edges_unique
        
        # Sample every 3rd edge to avoid clutter
        for i, edge in enumerate(edges[::3]):
            if i > 15:  # Limit to 15 edge highlights
                break
            v1 = mesh.vertices[edge[0]]
            v2 = mesh.vertices[edge[1]]
            
            direction = v2 - v1
            length = np.linalg.norm(direction)
            
            if length < 0.01:  # Skip very small edges
                continue
            
            edge_cyl = trimesh.creation.cylinder(radius=0.02, height=length)
            edge_cyl.visual.vertex_colors = self.shape_colors['edge']
            
            # Rotate and position
            direction_norm = direction / length
            z_axis = np.array([0, 0, 1])
            
            if not np.allclose(direction_norm, z_axis):
                rot_axis = np.cross(z_axis, direction_norm)
                rot_norm = np.linalg.norm(rot_axis)
                if rot_norm > 1e-8:
                    rot_axis = rot_axis / rot_norm
                    angle = np.arccos(np.clip(np.dot(z_axis, direction_norm), -1.0, 1.0))
                    R = trimesh.transformations.rotation_matrix(angle, rot_axis, point=[0, 0, 0])
                    edge_cyl.apply_transform(R)
            
            midpoint = (v1 + v2) / 2
            edge_cyl.apply_translation(midpoint)
            edge_meshes.append(edge_cyl)
        
        return edge_meshes
    
    def generate_cube(self, size: float = 2.0) -> Dict[str, any]:
        """Generate a cube with edge highlights"""
        logger.info("Generating cube...")
        
        # Create cube
        cube = trimesh.creation.box(extents=[size, size, size])
        cube.visual.vertex_colors = self.shape_colors['cube']
        
        # Add edge highlights
        edges = self._add_edge_highlights(cube)
        
        # Combine
        all_meshes = [cube] + edges
        combined = trimesh.util.concatenate(all_meshes)
        
        # Save
        output_path = self.output_dir / "cube.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: cube.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'cube.glb',
            'filepath': str(output_path),
            'model': 'Cube',
            'dimensions': f'{size}x{size}x{size}',
            'properties': ['6 faces', '12 edges', '8 vertices', 'All edges equal'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Regular hexahedron with all faces being squares of equal size'
        }
    
    def generate_cuboid(self, length: float = 3.0, width: float = 2.0, height: float = 1.5) -> Dict[str, any]:
        """Generate a rectangular cuboid"""
        logger.info("Generating cuboid...")
        
        cuboid = trimesh.creation.box(extents=[length, width, height])
        cuboid.visual.vertex_colors = self.shape_colors['cuboid']
        
        edges = self._add_edge_highlights(cuboid)
        
        combined = trimesh.util.concatenate([cuboid] + edges)
        
        output_path = self.output_dir / "cuboid.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: cuboid.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'cuboid.glb',
            'filepath': str(output_path),
            'model': 'Cuboid (Rectangular Prism)',
            'dimensions': f'{length}x{width}x{height}',
            'properties': ['6 rectangular faces', '12 edges', '8 vertices'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Rectangular box with length, width, and height all different'
        }
    
    def generate_cylinder(self, radius: float = 1.0, height: float = 3.0) -> Dict[str, any]:
        """Generate a cylinder"""
        logger.info("Generating cylinder...")
        
        cylinder = trimesh.creation.cylinder(radius=radius, height=height)
        cylinder.visual.vertex_colors = self.shape_colors['cylinder']
        
        output_path = self.output_dir / "cylinder.glb"
        cylinder.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: cylinder.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'cylinder.glb',
            'filepath': str(output_path),
            'model': 'Cylinder',
            'dimensions': f'r={radius}, h={height}',
            'properties': ['2 circular bases', '1 curved surface', f'Volume=πr²h'],
            'vertices': len(cylinder.vertices),
            'faces': len(cylinder.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Right circular cylinder with parallel circular bases'
        }
    
    def generate_cone(self, radius: float = 1.0, height: float = 2.5) -> Dict[str, any]:
        """Generate a cone"""
        logger.info("Generating cone...")
        
        cone = trimesh.creation.cone(radius=radius, height=height)
        cone.visual.vertex_colors = self.shape_colors['cone']
        
        output_path = self.output_dir / "cone.glb"
        cone.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: cone.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'cone.glb',
            'filepath': str(output_path),
            'model': 'Cone',
            'dimensions': f'r={radius}, h={height}',
            'properties': ['1 circular base', '1 apex', 'Curved lateral surface', f'Volume=⅓πr²h'],
            'vertices': len(cone.vertices),
            'faces': len(cone.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Right circular cone with apex directly above center of base'
        }
    
    def generate_sphere(self, radius: float = 1.5) -> Dict[str, any]:
        """Generate a sphere"""
        logger.info("Generating sphere...")
        
        sphere = trimesh.creation.icosphere(subdivisions=3, radius=radius)
        sphere.visual.vertex_colors = self.shape_colors['sphere']
        
        output_path = self.output_dir / "sphere.glb"
        sphere.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: sphere.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'sphere.glb',
            'filepath': str(output_path),
            'model': 'Sphere',
            'dimensions': f'r={radius}',
            'properties': ['Perfect curved surface', 'All points equidistant from center', f'Volume=⁴⁄₃πr³'],
            'vertices': len(sphere.vertices),
            'faces': len(sphere.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Perfect sphere with all surface points at equal radius from center'
        }
    
    def generate_pyramid(self, base_size: float = 2.0, height: float = 3.0) -> Dict[str, any]:
        """Generate a square pyramid"""
        logger.info("Generating pyramid...")
        
        # Create vertices: 4 base corners + 1 apex
        half_base = base_size / 2
        vertices = np.array([
            [-half_base, -half_base, 0],  # Base corners
            [half_base, -half_base, 0],
            [half_base, half_base, 0],
            [-half_base, half_base, 0],
            [0, 0, height]  # Apex
        ])
        
        # Define faces
        faces = np.array([
            [0, 1, 2], [0, 2, 3],  # Base (2 triangles)
            [0, 1, 4],  # Side faces
            [1, 2, 4],
            [2, 3, 4],
            [3, 0, 4]
        ])
        
        pyramid = trimesh.Trimesh(vertices=vertices, faces=faces)
        pyramid.visual.vertex_colors = self.shape_colors['pyramid']
        
        edges = self._add_edge_highlights(pyramid)
        combined = trimesh.util.concatenate([pyramid] + edges)
        
        output_path = self.output_dir / "pyramid.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: pyramid.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'pyramid.glb',
            'filepath': str(output_path),
            'model': 'Square Pyramid',
            'dimensions': f'base={base_size}x{base_size}, h={height}',
            'properties': ['Square base', '4 triangular faces', '1 apex', f'Volume=⅓×base²×h'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Square-based pyramid with apex directly above base center'
        }
    
    def generate_prisms(self) -> Dict[str, any]:
        """Generate triangular and hexagonal prisms side by side"""
        logger.info("Generating prisms...")
        
        meshes = []
        
        # Triangular prism
        height = 3.0
        base_radius = 1.0
        tri_prism = trimesh.creation.cylinder(radius=base_radius, height=height, sections=3)
        tri_prism.visual.vertex_colors = self.shape_colors['prism']
        tri_prism.apply_translation([-2.5, 0, 0])
        meshes.append(tri_prism)
        
        # Hexagonal prism
        hex_prism = trimesh.creation.cylinder(radius=base_radius, height=height, sections=6)
        hex_prism.visual.vertex_colors = self.shape_colors['prism']
        hex_prism.apply_translation([2.5, 0, 0])
        meshes.append(hex_prism)
        
        combined = trimesh.util.concatenate(meshes)
        
        output_path = self.output_dir / "prisms.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: prisms.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'prisms.glb',
            'filepath': str(output_path),
            'model': 'Prisms Collection',
            'dimensions': f'height={height}',
            'properties': ['Triangular prism (3 sides)', 'Hexagonal prism (6 sides)', 'Uniform cross-sections'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Prisms with polygonal bases and parallel edges'
        }
    
    def generate_composite_solids(self) -> Dict[str, any]:
        """Generate composite shapes (cylinder on cube, hemisphere on cylinder)"""
        logger.info("Generating composite solids...")
        
        meshes = []
        
        # Example 1: Cylinder on top of cube
        cube_size = 1.5
        cube = trimesh.creation.box(extents=[cube_size, cube_size, cube_size])
        cube.apply_translation([0, 0, -cube_size/2])
        cube.visual.vertex_colors = self.shape_colors['cube']
        meshes.append(cube)
        
        cyl_radius = 0.6
        cyl_height = 1.5
        cylinder = trimesh.creation.cylinder(radius=cyl_radius, height=cyl_height)
        cylinder.apply_translation([0, 0, cube_size/2 + cyl_height/2])
        cylinder.visual.vertex_colors = self.shape_colors['cylinder']
        meshes.append(cylinder)
        
        # Example 2: Cone on cylinder (positioned beside first composite)
        base_cyl = trimesh.creation.cylinder(radius=0.8, height=2.0)
        base_cyl.apply_translation([3.5, 0, -1.0])
        base_cyl.visual.vertex_colors = self.shape_colors['cylinder']
        meshes.append(base_cyl)
        
        top_cone = trimesh.creation.cone(radius=0.8, height=1.5)
        top_cone.apply_translation([3.5, 0, 0.75])
        top_cone.visual.vertex_colors = self.shape_colors['cone']
        meshes.append(top_cone)
        
        combined = trimesh.util.concatenate(meshes)
        
        output_path = self.output_dir / "composite_solids.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: composite_solids.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'composite_solids.glb',
            'filepath': str(output_path),
            'model': 'Composite Solids',
            'dimensions': 'Various',
            'properties': ['Cylinder on cube', 'Cone on cylinder', 'Combined volume calculations'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Combined shapes requiring addition of volumes and surface areas'
        }
    
    def generate_all_shapes(self) -> List[Dict[str, any]]:
        """Generate all 8 geometric shape models"""
        logger.info("📐 Generating all geometric shapes...")
        
        models = []
        models.append(self.generate_cube())
        models.append(self.generate_cuboid())
        models.append(self.generate_cylinder())
        models.append(self.generate_cone())
        models.append(self.generate_sphere())
        models.append(self.generate_pyramid())
        models.append(self.generate_prisms())
        models.append(self.generate_composite_solids())
        
        logger.info(f"✅ Generated {len(models)} geometric shapes")
        
        return models
    
    def generate_manifest(self, models: List[Dict[str, any]]) -> str:
        """Generate manifest file for all geometric shapes"""
        manifest = {
            "collection": "Geometric 3D Shapes",
            "priority": 5,
            "exam_weight": "High",
            "subject": "Mathematics",
            "topic_codes": ["math_008", "math_009"],
            "grade_levels": ["JSS1", "JSS2", "JSS3", "SS1", "SS2", "SS3"],
            "curriculum_standards": ["WAEC", "NECO"],
            "total_models": len(models),
            "models": []
        }
        
        for model in models:
            manifest["models"].append({
                "filename": model['filename'],
                "filepath": model['filepath'],
                "model": model['model'],
                "dimensions": model['dimensions'],
                "properties": model['properties'],
                "exam_topics": ["math_008", "math_009"],
                "grade_levels": ["JSS1", "JSS2", "JSS3", "SS1", "SS2", "SS3"],
                "vertices": model['vertices'],
                "faces": model['faces'],
                "file_size_kb": model['file_size_kb'],
                "educational_notes": model['educational_notes'],
                "ar_ready": True,
                "curriculum_standard": ["WAEC", "NECO"]
            })
        
        manifest_path = self.output_dir / "geometric_shapes_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"📋 Manifest created: {manifest_path}")
        return str(manifest_path)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate geometric 3D shape models')
    parser.add_argument('--model', type=str, default='all',
                       choices=['all', 'cube', 'cuboid', 'cylinder', 'cone', 
                               'sphere', 'pyramid', 'prisms', 'composite'],
                       help='Which model to generate')
    
    args = parser.parse_args()
    
    generator = GeometricShapeGenerator()
    
    if args.model == 'all':
        models = generator.generate_all_shapes()
        generator.generate_manifest(models)
        
        total_size = sum(m['file_size_kb'] for m in models)
        print(f"\n📊 Generation Statistics:")
        print(f"   Models: {len(models)}")
        print(f"   Total Size: {total_size:.2f} KB")
        print(f"   Shapes: {', '.join(m['model'] for m in models)}")
    else:
        model_map = {
            'cube': generator.generate_cube,
            'cuboid': generator.generate_cuboid,
            'cylinder': generator.generate_cylinder,
            'cone': generator.generate_cone,
            'sphere': generator.generate_sphere,
            'pyramid': generator.generate_pyramid,
            'prisms': generator.generate_prisms,
            'composite': generator.generate_composite_solids,
        }
        
        result = model_map[args.model]()
        print(f"\n✅ Generated: {result['filename']} ({result['file_size_kb']:.2f} KB)")
