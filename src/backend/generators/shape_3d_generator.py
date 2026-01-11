"""
3D Shapes Generator
Generates 3D geometric shapes using trimesh and plotly
- Basic shapes: cube, sphere, cylinder, cone, pyramid, prism
- Export formats: GLB, STL, OBJ
- Interactive visualization with Plotly
"""

import numpy as np
import trimesh
from pathlib import Path
from typing import Dict, List, Tuple, Any
import json
import logging

logger = logging.getLogger(__name__)


class Shape3DGenerator:
    """Generate 3D geometric shapes for mathematics lessons"""
    
    def __init__(self, output_dir="generated_assets/geometric_shapes"):
        """
        Initialize 3D shape generator
        
        Args:
            output_dir: Directory to save generated shapes
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Shape3DGenerator initialized: {self.output_dir}")
    
    def generate_cube(self, side_length: float = 2.0, name: str = None) -> Dict[str, Any]:
        """
        Generate a cube mesh
        
        Args:
            side_length: Side length of the cube
            name: Name for the output files
            
        Returns:
            Dictionary with metadata and file paths
        """
        try:
            # Create cube
            cube = trimesh.creation.box(extents=[side_length] * 3)
            
            # Add colors
            cube.visual.face_colors = [100, 150, 200, 200]
            
            # Export as GLB
            output_name = name or f"cube_{side_length}"
            glb_path = self.output_dir / f"{output_name}.glb"
            cube.export(glb_path)
            
            # Export as STL
            stl_path = self.output_dir / f"{output_name}.stl"
            cube.export(stl_path)
            
            metadata = {
                "name": output_name,
                "shape_type": "cube",
                "side_length": float(side_length),
                "volume": float(side_length ** 3),
                "surface_area": float(6 * side_length ** 2),
                "vertices": int(cube.vertices.shape[0]),
                "faces": int(cube.faces.shape[0]),
                "glb_file": str(glb_path),
                "stl_file": str(stl_path)
            }
            
            logger.info(f"✅ Generated cube: {glb_path}")
            return metadata
        except Exception as e:
            logger.error(f"❌ Error generating cube: {e}")
            raise
    
    def generate_sphere(self, radius: float = 1.0, subdivisions: int = 3, name: str = None) -> Dict[str, Any]:
        """
        Generate a sphere mesh
        
        Args:
            radius: Radius of the sphere
            subdivisions: Subdivision level for smoothness
            name: Name for the output files
            
        Returns:
            Dictionary with metadata and file paths
        """
        try:
            sphere = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
            sphere.visual.face_colors = [200, 100, 150, 200]
            
            output_name = name or f"sphere_r{radius}"
            glb_path = self.output_dir / f"{output_name}.glb"
            sphere.export(glb_path)
            
            stl_path = self.output_dir / f"{output_name}.stl"
            sphere.export(stl_path)
            
            metadata = {
                "name": output_name,
                "shape_type": "sphere",
                "radius": float(radius),
                "volume": float(4/3 * np.pi * radius**3),
                "surface_area": float(4 * np.pi * radius**2),
                "vertices": int(sphere.vertices.shape[0]),
                "faces": int(sphere.faces.shape[0]),
                "glb_file": str(glb_path),
                "stl_file": str(stl_path)
            }
            
            logger.info(f"✅ Generated sphere: {glb_path}")
            return metadata
        except Exception as e:
            logger.error(f"❌ Error generating sphere: {e}")
            raise
    
    def generate_cylinder(self, radius: float = 1.0, height: float = 3.0, 
                         sections: int = 32, name: str = None) -> Dict[str, Any]:
        """
        Generate a cylinder mesh
        
        Args:
            radius: Radius of the cylinder
            height: Height of the cylinder
            sections: Number of sections for smoothness
            name: Name for the output files
            
        Returns:
            Dictionary with metadata and file paths
        """
        try:
            cylinder = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
            cylinder.visual.face_colors = [150, 200, 100, 200]
            
            output_name = name or f"cylinder_r{radius}_h{height}"
            glb_path = self.output_dir / f"{output_name}.glb"
            cylinder.export(glb_path)
            
            stl_path = self.output_dir / f"{output_name}.stl"
            cylinder.export(stl_path)
            
            metadata = {
                "name": output_name,
                "shape_type": "cylinder",
                "radius": float(radius),
                "height": float(height),
                "volume": float(np.pi * radius**2 * height),
                "surface_area": float(2 * np.pi * radius * height + 2 * np.pi * radius**2),
                "vertices": int(cylinder.vertices.shape[0]),
                "faces": int(cylinder.faces.shape[0]),
                "glb_file": str(glb_path),
                "stl_file": str(stl_path)
            }
            
            logger.info(f"✅ Generated cylinder: {glb_path}")
            return metadata
        except Exception as e:
            logger.error(f"❌ Error generating cylinder: {e}")
            raise
    
    def generate_cone(self, radius: float = 1.0, height: float = 2.0, 
                     sections: int = 32, name: str = None) -> Dict[str, Any]:
        """
        Generate a cone mesh
        
        Args:
            radius: Radius of the base
            height: Height of the cone
            sections: Number of sections for smoothness
            name: Name for the output files
            
        Returns:
            Dictionary with metadata and file paths
        """
        try:
            cone = trimesh.creation.cone(radius=radius, height=height, sections=sections)
            cone.visual.face_colors = [200, 150, 100, 200]
            
            output_name = name or f"cone_r{radius}_h{height}"
            glb_path = self.output_dir / f"{output_name}.glb"
            cone.export(glb_path)
            
            stl_path = self.output_dir / f"{output_name}.stl"
            cone.export(stl_path)
            
            metadata = {
                "name": output_name,
                "shape_type": "cone",
                "radius": float(radius),
                "height": float(height),
                "volume": float(1/3 * np.pi * radius**2 * height),
                "surface_area": float(np.pi * radius**2 + np.pi * radius * np.sqrt(radius**2 + height**2)),
                "vertices": int(cone.vertices.shape[0]),
                "faces": int(cone.faces.shape[0]),
                "glb_file": str(glb_path),
                "stl_file": str(stl_path)
            }
            
            logger.info(f"✅ Generated cone: {glb_path}")
            return metadata
        except Exception as e:
            logger.error(f"❌ Error generating cone: {e}")
            raise
    
    def generate_pyramid(self, base_size: float = 2.0, height: float = 3.0, 
                        name: str = None) -> Dict[str, Any]:
        """
        Generate a square pyramid
        
        Args:
            base_size: Size of the square base
            height: Height of the pyramid
            name: Name for the output files
            
        Returns:
            Dictionary with metadata and file paths
        """
        try:
            # Define vertices
            vertices = np.array([
                [-base_size/2, -base_size/2, 0],  # Base corners
                [base_size/2, -base_size/2, 0],
                [base_size/2, base_size/2, 0],
                [-base_size/2, base_size/2, 0],
                [0, 0, height]  # Apex
            ])
            
            # Define faces
            faces = np.array([
                [0, 1, 2], [0, 2, 3],  # Base (two triangles)
                [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]  # Sides
            ])
            
            pyramid = trimesh.Trimesh(vertices=vertices, faces=faces)
            pyramid.visual.face_colors = [255, 200, 100, 200]
            
            output_name = name or f"pyramid_{base_size}_{height}"
            glb_path = self.output_dir / f"{output_name}.glb"
            pyramid.export(glb_path)
            
            stl_path = self.output_dir / f"{output_name}.stl"
            pyramid.export(stl_path)
            
            metadata = {
                "name": output_name,
                "shape_type": "square_pyramid",
                "base_size": float(base_size),
                "height": float(height),
                "volume": float(1/3 * base_size**2 * height),
                "surface_area": float(base_size**2 + 2 * base_size * np.sqrt((base_size/2)**2 + height**2)),
                "vertices": int(pyramid.vertices.shape[0]),
                "faces": int(pyramid.faces.shape[0]),
                "glb_file": str(glb_path),
                "stl_file": str(stl_path)
            }
            
            logger.info(f"✅ Generated pyramid: {glb_path}")
            return metadata
        except Exception as e:
            logger.error(f"❌ Error generating pyramid: {e}")
            raise
    
    def generate_prism(self, base_sides: int = 6, base_radius: float = 1.0, 
                      height: float = 2.0, name: str = None) -> Dict[str, Any]:
        """
        Generate a prism (hexagonal by default)
        
        Args:
            base_sides: Number of sides for the base polygon
            base_radius: Radius of the base polygon
            height: Height of the prism
            name: Name for the output files
            
        Returns:
            Dictionary with metadata and file paths
        """
        try:
            prism = trimesh.creation.cylinder(
                radius=base_radius,
                height=height,
                sections=base_sides
            )
            prism.visual.face_colors = [100, 200, 200, 200]
            
            output_name = name or f"prism_{base_sides}sided_h{height}"
            glb_path = self.output_dir / f"{output_name}.glb"
            prism.export(glb_path)
            
            stl_path = self.output_dir / f"{output_name}.stl"
            prism.export(stl_path)
            
            metadata = {
                "name": output_name,
                "shape_type": "prism",
                "base_sides": int(base_sides),
                "base_radius": float(base_radius),
                "height": float(height),
                "vertices": int(prism.vertices.shape[0]),
                "faces": int(prism.faces.shape[0]),
                "glb_file": str(glb_path),
                "stl_file": str(stl_path)
            }
            
            logger.info(f"✅ Generated {base_sides}-sided prism: {glb_path}")
            return metadata
        except Exception as e:
            logger.error(f"❌ Error generating prism: {e}")
            raise
    
    def generate_all_basic_shapes(self) -> List[Dict[str, Any]]:
        """Generate all basic 3D shapes with educational parameters"""
        shapes = []
        
        logger.info("🎲 Generating 3D geometric shapes...")
        
        # Cube
        try:
            shapes.append(self.generate_cube(2.0, "Cube_2"))
        except Exception as e:
            logger.warning(f"⚠️ Cube generation failed: {e}")
        
        # Sphere
        try:
            shapes.append(self.generate_sphere(1.5, 3, "Sphere_1.5"))
        except Exception as e:
            logger.warning(f"⚠️ Sphere generation failed: {e}")
        
        # Cylinder
        try:
            shapes.append(self.generate_cylinder(1.0, 3.0, 32, "Cylinder_1x3"))
        except Exception as e:
            logger.warning(f"⚠️ Cylinder generation failed: {e}")
        
        # Cone
        try:
            shapes.append(self.generate_cone(1.0, 2.5, 32, "Cone_1x2.5"))
        except Exception as e:
            logger.warning(f"⚠️ Cone generation failed: {e}")
        
        # Pyramid
        try:
            shapes.append(self.generate_pyramid(2.0, 3.0, "Pyramid_2x3"))
        except Exception as e:
            logger.warning(f"⚠️ Pyramid generation failed: {e}")
        
        # Triangular Prism
        try:
            shapes.append(self.generate_prism(3, 1.0, 2.0, "Triangular_Prism"))
        except Exception as e:
            logger.warning(f"⚠️ Triangular prism generation failed: {e}")
        
        # Hexagonal Prism
        try:
            shapes.append(self.generate_prism(6, 1.0, 2.0, "Hexagonal_Prism"))
        except Exception as e:
            logger.warning(f"⚠️ Hexagonal prism generation failed: {e}")
        
        logger.info(f"✅ Generated {len(shapes)} 3D shapes")
        return shapes
    
    def generate_manifest(self, shapes: List[Dict[str, Any]]) -> str:
        """
        Generate manifest file with all shape metadata
        
        Args:
            shapes: List of shape metadata dictionaries
            
        Returns:
            Path to manifest file
        """
        try:
            manifest = {
                "generated_at": str(np.datetime64('today')),
                "total_shapes": len(shapes),
                "shapes": shapes
            }
            
            manifest_path = self.output_dir / "shapes_manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            logger.info(f"✅ Generated manifest: {manifest_path}")
            return str(manifest_path)
        except Exception as e:
            logger.error(f"❌ Error generating manifest: {e}")
            raise


if __name__ == "__main__":
    # Test basic generation
    logging.basicConfig(level=logging.INFO)
    generator = Shape3DGenerator()
    shapes = generator.generate_all_basic_shapes()
    
    print("\n" + "="*50)
    print("🎲 3D Shapes Generated:")
    print("="*50)
    for shape in shapes:
        print(f"✅ {shape['name']}: {shape['shape_type']}")
        print(f"   Volume: {shape.get('volume', 'N/A'):.2f}")
        print(f"   Surface Area: {shape.get('surface_area', 'N/A'):.2f}")
    
    # Generate manifest
    generator.generate_manifest(shapes)
