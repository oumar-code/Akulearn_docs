"""
Mathematical Functions 3D Model Generator - Priority #12

Generates 6 interactive mathematical function visualization models for Nigerian secondary education (math_012, math_013).
Supports calculus, algebra, and trigonometry concepts for SS2/SS3 mathematics.

Models:
1. 3d_graphs.glb - Parabola, cubic, and polynomial functions
2. polynomial_functions.glb - Roots, extrema, and behavior analysis
3. trigonometric_surfaces.glb - Sine, cosine, tangent wave visualizations
4. surface_of_revolution.glb - Rotated curves creating 3D surfaces
5. volume_integration.glb - Area under curve visualization for integration
6. tangent_planes.glb - Partial derivatives and tangent plane concepts

Educational Focus: Advanced mathematics visualization for calculus and algebra
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
import trimesh

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class MathematicalFunctionsModelGenerator:
    """Generates 6 mathematical function visualization models for advanced secondary mathematics."""

    def __init__(self):
        """Initialize the generator."""
        self.output_dir = Path('generated_assets/mathematical_functions')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("📐 Mathematical Functions Generator initialized")

    def _create_sphere(self, center: Tuple[float, float, float], radius: float, color: Tuple[int, int, int], subdivisions: int = 2) -> trimesh.Trimesh:
        """Create a sphere primitive."""
        sphere = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
        sphere.apply_translation(center)
        sphere.visual.vertex_colors = color
        return sphere

    def _create_cylinder(self, start: Tuple[float, float, float], end: Tuple[float, float, float], radius: float, color: Tuple[int, int, int], sections: int = 16) -> trimesh.Trimesh:
        """Create a cylinder between two points."""
        height = np.linalg.norm(np.array(end) - np.array(start))
        cyl = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
        direction = np.array(end) - np.array(start)
        if height > 0:
            direction = direction / height
        up = np.array([0, 0, 1])
        if abs(np.dot(direction, up)) > 0.99:
            up = np.array([1, 0, 0])
        right = np.cross(direction, up)
        right = right / np.linalg.norm(right)
        actual_up = np.cross(right, direction)
        rotation_matrix = np.column_stack([right, actual_up, direction])
        transform = np.eye(4)
        transform[:3, :3] = rotation_matrix
        cyl.apply_transform(transform)
        mid_point = (np.array(start) + np.array(end)) / 2
        cyl.apply_translation(mid_point)
        cyl.visual.vertex_colors = color
        return cyl

    def _create_box(self, center: Tuple[float, float, float], extents: Tuple[float, float, float], color: Tuple[int, int, int]) -> trimesh.Trimesh:
        """Create a box primitive."""
        box = trimesh.creation.box(extents=extents)
        box.apply_translation(center)
        box.visual.vertex_colors = color
        return box

    def _create_surface_mesh(self, x_range: Tuple[float, float], y_range: Tuple[float, float], func, color: Tuple[int, int, int], resolution: int = 20) -> trimesh.Trimesh:
        """Create a surface mesh from a function z = f(x, y)."""
        x = np.linspace(x_range[0], x_range[1], resolution)
        y = np.linspace(y_range[0], y_range[1], resolution)
        X, Y = np.meshgrid(x, y)
        Z = func(X, Y)
        
        vertices = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
        
        # Create triangles
        faces = []
        for i in range(resolution - 1):
            for j in range(resolution - 1):
                v0 = i * resolution + j
                v1 = v0 + 1
                v2 = (i + 1) * resolution + j
                v3 = v2 + 1
                faces.append([v0, v1, v2])
                faces.append([v1, v3, v2])
        
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        mesh.visual.vertex_colors = color
        return mesh

    def generate_3d_graphs(self) -> str:
        """Generate 3D polynomial function graphs."""
        logger.info("📍 Generating 3D polynomial graphs...")
        meshes = []

        # Parabola: z = x^2 + y^2
        def parabola(x, y):
            return x**2 + y**2
        parabola_mesh = self._create_surface_mesh((-2, 2), (-2, 2), parabola, (100, 200, 255), resolution=25)
        meshes.append(parabola_mesh)

        # Axes for reference
        x_axis = self._create_cylinder((0, 0, 0), (3, 0, 0), 0.1, (255, 0, 0))
        y_axis = self._create_cylinder((0, 0, 0), (0, 3, 0), 0.1, (0, 255, 0))
        z_axis = self._create_cylinder((0, 0, 0), (0, 0, 5), 0.1, (0, 0, 255))
        meshes.extend([x_axis, y_axis, z_axis])

        # Origin marker
        origin = self._create_sphere((0, 0, 0), 0.2, (255, 255, 255))
        meshes.append(origin)

        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        file_path = self.output_dir / '3d_graphs.glb'
        combined.export(file_path)
        file_size = file_path.stat().st_size / 1024
        logger.info(f"✅ 3d_graphs.glb created ({file_size:.2f} KB)")
        return str(file_path)

    def generate_polynomial_functions(self) -> str:
        """Generate polynomial functions with roots and extrema."""
        logger.info("📍 Generating polynomial functions...")
        meshes = []

        # Cubic function: z = x^3 - 3x (showing roots and extrema)
        def cubic(x, y):
            return x**3 - 3*x + 0.1*y

        cubic_mesh = self._create_surface_mesh((-3, 3), (-2, 2), cubic, (200, 100, 255), resolution=25)
        meshes.append(cubic_mesh)

        # Mark roots (where function crosses x-axis, y=0)
        # Roots approximately at -1.7, 0, 1.7
        roots = [-1.732, 0, 1.732]
        for root in roots:
            root_marker = self._create_sphere((root, 0, 0), 0.3, (255, 255, 0))
            meshes.append(root_marker)

        # Mark extrema (local max/min)
        # For x^3 - 3x, extrema at x = ±1
        extrema = [-1, 1]
        for ext_x in extrema:
            ext_z = ext_x**3 - 3*ext_x
            extrema_marker = self._create_sphere((ext_x, 0, ext_z), 0.3, (255, 100, 100))
            meshes.append(extrema_marker)

        # Axes
        x_axis = self._create_cylinder((-3, 0, 0), (3, 0, 0), 0.08, (255, 0, 0))
        z_axis = self._create_cylinder((0, 0, -5), (0, 0, 5), 0.08, (0, 0, 255))
        meshes.extend([x_axis, z_axis])

        # Origin
        origin = self._create_sphere((0, 0, 0), 0.2, (255, 255, 255))
        meshes.append(origin)

        combined = trimesh.util.concatenate(meshes)
        file_path = self.output_dir / 'polynomial_functions.glb'
        combined.export(file_path)
        file_size = file_path.stat().st_size / 1024
        logger.info(f"✅ polynomial_functions.glb created ({file_size:.2f} KB)")
        return str(file_path)

    def generate_trigonometric_surfaces(self) -> str:
        """Generate trigonometric function surfaces."""
        logger.info("📍 Generating trigonometric surfaces...")
        meshes = []

        # Sine wave surface: z = sin(x) * cos(y)
        def trig_surface(x, y):
            return np.sin(x * np.pi) * np.cos(y * np.pi)

        trig_mesh = self._create_surface_mesh((-2, 2), (-2, 2), trig_surface, (100, 255, 200), resolution=30)
        meshes.append(trig_mesh)

        # Axes
        x_axis = self._create_cylinder((-2, 0, 0), (2, 0, 0), 0.08, (255, 0, 0))
        y_axis = self._create_cylinder((0, -2, 0), (0, 2, 0), 0.08, (0, 255, 0))
        z_axis = self._create_cylinder((0, 0, -1.5), (0, 0, 1.5), 0.08, (0, 0, 255))
        meshes.extend([x_axis, y_axis, z_axis])

        # Origin
        origin = self._create_sphere((0, 0, 0), 0.15, (255, 255, 255))
        meshes.append(origin)

        # Mark critical points (maxima and minima)
        critical_points = [(0, 0), (0, 1), (0, -1)]
        for cp_x, cp_y in critical_points:
            cp_z = np.sin(cp_x * np.pi) * np.cos(cp_y * np.pi)
            cp_marker = self._create_sphere((cp_x, cp_y, cp_z), 0.15, (255, 150, 100))
            meshes.append(cp_marker)

        combined = trimesh.util.concatenate(meshes)
        file_path = self.output_dir / 'trigonometric_surfaces.glb'
        combined.export(file_path)
        file_size = file_path.stat().st_size / 1024
        logger.info(f"✅ trigonometric_surfaces.glb created ({file_size:.2f} KB)")
        return str(file_path)

    def generate_surface_of_revolution(self) -> str:
        """Generate surface of revolution (rotating curve around axis)."""
        logger.info("📍 Generating surface of revolution...")
        meshes = []

        # Profile curve: y = e^(-x^2) (Gaussian curve)
        # Rotated around z-axis
        x_vals = np.linspace(-2, 2, 30)
        theta_vals = np.linspace(0, 2*np.pi, 30)
        
        vertices = []
        for x in x_vals:
            y = np.exp(-(x**2))
            for theta in theta_vals:
                x_rev = y * np.cos(theta)
                y_rev = y * np.sin(theta)
                z_rev = x
                vertices.append([x_rev, y_rev, z_rev])
        
        # Create faces
        faces = []
        for i in range(len(x_vals) - 1):
            for j in range(len(theta_vals) - 1):
                v0 = i * len(theta_vals) + j
                v1 = v0 + 1
                v2 = (i + 1) * len(theta_vals) + j
                v3 = v2 + 1
                faces.append([v0, v1, v2])
                faces.append([v1, v3, v2])
        
        surface = trimesh.Trimesh(vertices=np.array(vertices), faces=faces)
        surface.visual.vertex_colors = (100, 255, 150)
        meshes.append(surface)

        # Central axis
        z_axis = self._create_cylinder((0, 0, -2.5), (0, 0, 2.5), 0.08, (200, 200, 200))
        meshes.append(z_axis)

        # Origin marker
        origin = self._create_sphere((0, 0, 0), 0.15, (255, 255, 100))
        meshes.append(origin)

        combined = trimesh.util.concatenate(meshes)
        file_path = self.output_dir / 'surface_of_revolution.glb'
        combined.export(file_path)
        file_size = file_path.stat().st_size / 1024
        logger.info(f"✅ surface_of_revolution.glb created ({file_size:.2f} KB)")
        return str(file_path)

    def generate_volume_integration(self) -> str:
        """Generate volume under a curve (integration visualization)."""
        logger.info("📍 Generating volume integration...")
        meshes = []

        # Function: z = 1 - x^2 (parabola opening downward)
        def integration_func(x, y):
            return max(0, 1 - x**2)

        # Create surface
        resolution = 25
        x = np.linspace(-1.2, 1.2, resolution)
        y = np.linspace(0, 1, resolution)
        
        vertices = []
        for xi in x:
            for yi in y:
                z = max(0, 1 - xi**2)
                vertices.append([xi, yi, z])
                # Also add base points at z=0
                vertices.append([xi, yi, 0])
        
        # Create faces for the volume
        faces = []
        for i in range(len(x) - 1):
            for j in range(len(y) - 1):
                # Top surface
                v0 = (i * len(y) + j) * 2
                v1 = v0 + 2
                v2 = ((i + 1) * len(y) + j) * 2
                v3 = v2 + 2
                faces.append([v0, v1, v2])
                faces.append([v1, v3, v2])
                
                # Side faces
                v_base0 = v0 + 1
                v_base1 = v0 + 3
                v_base2 = v0 + len(y)*2 + 1
                v_base3 = v0 + len(y)*2 + 3
                faces.append([v_base0, v_base2, v_base1])
                faces.append([v_base1, v_base2, v_base3])

        volume = trimesh.Trimesh(vertices=np.array(vertices), faces=faces)
        volume.visual.vertex_colors = (150, 150, 255)
        meshes.append(volume)

        # Function curve visualization (edge)
        for i in range(len(x) - 1):
            x1, x2 = x[i], x[i+1]
            z1 = max(0, 1 - x1**2)
            z2 = max(0, 1 - x2**2)
            edge = self._create_cylinder((x1, 0.5, z1), (x2, 0.5, z2), 0.05, (255, 100, 100))
            meshes.append(edge)

        # Axes
        x_axis = self._create_cylinder((-1.5, 0, 0), (1.5, 0, 0), 0.08, (255, 0, 0))
        y_axis = self._create_cylinder((0, 0, 0), (0, 1.2, 0), 0.08, (0, 255, 0))
        z_axis = self._create_cylinder((0, 0, 0), (0, 0, 1.2), 0.08, (0, 0, 255))
        meshes.extend([x_axis, y_axis, z_axis])

        # Origin
        origin = self._create_sphere((0, 0, 0), 0.15, (255, 255, 255))
        meshes.append(origin)

        combined = trimesh.util.concatenate(meshes)
        file_path = self.output_dir / 'volume_integration.glb'
        combined.export(file_path)
        file_size = file_path.stat().st_size / 1024
        logger.info(f"✅ volume_integration.glb created ({file_size:.2f} KB)")
        return str(file_path)

    def generate_tangent_planes(self) -> str:
        """Generate tangent planes for partial derivative visualization."""
        logger.info("📍 Generating tangent planes...")
        meshes = []

        # Surface: z = x^2 + y^2 (paraboloid)
        def surface_func(x, y):
            return x**2 + y**2

        paraboloid = self._create_surface_mesh((-2, 2), (-2, 2), surface_func, (100, 200, 100), resolution=20)
        meshes.append(paraboloid)

        # Tangent plane at point (1, 1, 2)
        # For z = x^2 + y^2, at (1,1): dz/dx = 2x = 2, dz/dy = 2y = 2
        # Tangent plane: z - 2 = 2(x - 1) + 2(y - 1) = 2x + 2y - 4
        tangent_vertices = [
            [-1, -1, -4],  # Corner 1
            [3, -1, 2],    # Corner 2
            [-1, 3, 2],    # Corner 3
            [3, 3, 8],     # Corner 4
        ]
        tangent_faces = [[0, 1, 2], [1, 3, 2]]
        tangent_plane = trimesh.Trimesh(vertices=tangent_vertices, faces=tangent_faces)
        tangent_plane.visual.vertex_colors = (255, 100, 100)
        meshes.append(tangent_plane)

        # Point of tangency
        tangency_point = self._create_sphere((1, 1, 2), 0.2, (255, 255, 0))
        meshes.append(tangency_point)

        # Partial derivative vectors at tangency point
        # ∇f = (2x, 2y) = (2, 2) at (1, 1)
        dx_vector = self._create_cylinder((1, 1, 2), (2, 1, 2), 0.1, (255, 0, 0))
        dy_vector = self._create_cylinder((1, 1, 2), (1, 2, 2), 0.1, (0, 255, 0))
        meshes.extend([dx_vector, dy_vector])

        # Axes
        x_axis = self._create_cylinder((-2, 0, 0), (3, 0, 0), 0.08, (200, 0, 0))
        y_axis = self._create_cylinder((0, -2, 0), (0, 3, 0), 0.08, (0, 200, 0))
        z_axis = self._create_cylinder((0, 0, 0), (0, 0, 8), 0.08, (0, 0, 200))
        meshes.extend([x_axis, y_axis, z_axis])

        # Origin
        origin = self._create_sphere((0, 0, 0), 0.15, (255, 255, 255))
        meshes.append(origin)

        combined = trimesh.util.concatenate(meshes)
        file_path = self.output_dir / 'tangent_planes.glb'
        combined.export(file_path)
        file_size = file_path.stat().st_size / 1024
        logger.info(f"✅ tangent_planes.glb created ({file_size:.2f} KB)")
        return str(file_path)

    def generate_all_models(self) -> Dict[str, str]:
        """Generate all mathematical function models and return file paths."""
        logger.info("📐 Generating all mathematical function models...")

        models = {
            '3d_graphs': self.generate_3d_graphs(),
            'polynomial_functions': self.generate_polynomial_functions(),
            'trigonometric_surfaces': self.generate_trigonometric_surfaces(),
            'surface_of_revolution': self.generate_surface_of_revolution(),
            'volume_integration': self.generate_volume_integration(),
            'tangent_planes': self.generate_tangent_planes(),
        }

        # Generate manifest
        self.generate_manifest()

        return models

    def generate_manifest(self) -> None:
        """Generate manifest with metadata for all mathematical function models."""
        manifest = {
            "priority": 12,
            "category": "Mathematical Functions & Calculus",
            "curriculum_topics": ["math_012", "math_013"],
            "grade_levels": ["SS2", "SS3"],
            "total_models": 6,
            "models": [
                {
                    "id": "3d_graphs",
                    "name": "3D Polynomial Graphs",
                    "filename": "3d_graphs.glb",
                    "description": "3D visualization of parabola and polynomial functions with coordinate axes",
                    "mathematical_concept": "Polynomial functions, quadratic surfaces, coordinate geometry",
                    "curriculum_alignment": "math_012, math_013 - Functions and Calculus",
                    "educational_value": "Visualize polynomial behavior in 3D space, understand surface geometry"
                },
                {
                    "id": "polynomial_functions",
                    "name": "Polynomial Functions with Roots & Extrema",
                    "filename": "polynomial_functions.glb",
                    "description": "Cubic polynomial showing roots (zeros) and extrema (local max/min)",
                    "mathematical_concept": ["Polynomial roots", "Critical points", "Local extrema", "First derivative"],
                    "curriculum_alignment": "math_012 - Polynomial Analysis",
                    "educational_value": "Understand relationship between roots, extrema, and derivative"
                },
                {
                    "id": "trigonometric_surfaces",
                    "name": "Trigonometric Function Surfaces",
                    "filename": "trigonometric_surfaces.glb",
                    "description": "3D surface of sin(x)*cos(y) showing wave behavior in 2D parameter space",
                    "mathematical_concept": ["Trigonometric functions", "Wave properties", "Periodic behavior", "Critical points"],
                    "curriculum_alignment": "math_012 - Trigonometric Functions",
                    "educational_value": "Visualize periodic behavior and critical points in trigonometric surfaces"
                },
                {
                    "id": "surface_of_revolution",
                    "name": "Surface of Revolution",
                    "filename": "surface_of_revolution.glb",
                    "description": "Gaussian curve rotated around central axis creating symmetric 3D shape",
                    "mathematical_concept": ["Solids of revolution", "Rotation transformations", "Symmetry", "Volume calculation"],
                    "curriculum_alignment": "math_013 - Calculus",
                    "educational_value": "Understand how 2D curves create 3D volumes through rotation"
                },
                {
                    "id": "volume_integration",
                    "name": "Volume Under Curves (Integration)",
                    "filename": "volume_integration.glb",
                    "description": "3D representation of area under curve z=1-x² and corresponding volume",
                    "mathematical_concept": ["Integration", "Area under curves", "Volume calculation", "Definite integrals"],
                    "curriculum_alignment": "math_013 - Integration",
                    "educational_value": "Visualize abstract concept of integration as area/volume accumulation"
                },
                {
                    "id": "tangent_planes",
                    "name": "Tangent Planes & Partial Derivatives",
                    "filename": "tangent_planes.glb",
                    "description": "Paraboloid with tangent plane at point showing partial derivative vectors",
                    "mathematical_concept": ["Partial derivatives", "Gradient vectors", "Tangent planes", "Multivariable calculus"],
                    "curriculum_alignment": "math_013 - Multivariable Calculus",
                    "educational_value": "Visualize how partial derivatives define tangent planes to surfaces"
                }
            ],
            "total_file_size_kb": None,
            "file_format": "glb",
            "target_platform": "WebAR, VR headsets, Mobile AR",
            "mathematical_concepts": [
                "Functions and Relations",
                "Polynomial Analysis",
                "Trigonometric Functions",
                "Limits and Continuity",
                "Differentiation",
                "Integration",
                "Multivariable Calculus",
                "Coordinate Geometry",
                "Transformations"
            ],
            "lesson_routing_keywords": {
                "polynomial": ["3d graphs", "parabola", "cubic", "polynomial function", "quadratic", "degree"],
                "roots_extrema": ["roots", "zeros", "critical points", "extrema", "maximum", "minimum", "turning point"],
                "trigonometry": ["trigonometric surface", "sine wave", "cosine", "periodic", "amplitude", "frequency"],
                "revolution": ["surface of revolution", "solid of revolution", "rotation", "axis", "symmetry", "cone", "sphere"],
                "integration": ["integration", "area under curve", "volume", "accumulation", "definite integral", "Riemann sum"],
                "calculus": ["derivative", "tangent", "partial derivative", "gradient", "multivariable", "critical point"],
                "geometry": ["3d graph", "surface", "coordinate system", "coordinate geometry", "spatial reasoning", "projection"]
            }
        }

        manifest_path = self.output_dir / 'mathematical_functions_manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        logger.info(f"📋 Manifest created: {manifest_path}")


def main():
    """Generate all mathematical function models."""
    generator = MathematicalFunctionsModelGenerator()
    models = generator.generate_all_models()

    print("\n✅ Generated 6 Mathematical Functions models:")
    for model_name, model_path in models.items():
        file_size = Path(model_path).stat().st_size / 1024
        print(f"  - {model_name}.glb: {file_size:.2f} KB")

    # Calculate total
    total_size = sum(Path(path).stat().st_size for path in models.values()) / 1024
    print(f"\nTotal: {total_size:.2f} KB")


if __name__ == '__main__':
    main()
