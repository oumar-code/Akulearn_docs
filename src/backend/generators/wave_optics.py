import json
import logging
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import trimesh

logger = logging.getLogger(__name__)


class WaveOpticsGenerator:
    """Generator for Wave and Optics educational models (Priority #6)
    Models:
    - wave_types.glb: transverse vs longitudinal waves
    - electromagnetic_spectrum.glb: EM spectrum bands
    - reflection_mirrors.glb: plane, concave, convex mirrors with rays
    - refraction_lenses.glb: convex and concave lenses with rays
    - total_internal_reflection.glb: fiber optic TIR demonstration
    - prism_dispersion.glb: prism with dispersion rays
    """

    def __init__(self, output_dir: Path = None) -> None:
        self.output_dir = Path(output_dir or "generated_assets/wave_optics")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.colors = {
            "ray": [255, 50, 50, 255],
            "mirror": [180, 180, 200, 255],
            "lens": [150, 200, 255, 180],  # semi-transparent feel
            "fiber": [200, 200, 255, 200],
            "spectrum": [200, 200, 200, 255],
            "prism": [170, 170, 220, 180],
            "wave": [100, 200, 255, 255],
        }

    # ---------- helpers ----------
    def _save_glb(self, mesh: trimesh.Trimesh, filename: str) -> Dict[str, Any]:
        path = self.output_dir / filename
        scene = trimesh.Scene(mesh)
        scene.export(path)
        size_kb = path.stat().st_size / 1024 if path.exists() else 0
        return {
            "name": filename.replace('.glb', ''),
            "filepath": str(path),
            "size_kb": round(size_kb, 2),
        }

    def _create_arrow(self, start: np.ndarray, end: np.ndarray, color: List[int] = None) -> trimesh.Trimesh:
        """Create a simple arrow (cylinder shaft + cone head) from start to end."""
        color = color or self.colors["ray"]
        start = np.array(start, dtype=float)
        end = np.array(end, dtype=float)
        vec = end - start
        length = np.linalg.norm(vec)
        if length < 1e-6:
            vec = np.array([0, 0, 1.0])
            length = 1.0
        direction = vec / length

        # shaft
        shaft = trimesh.creation.cylinder(radius=0.02, height=length * 0.8, sections=24)
        shaft.visual.vertex_colors = color
        # head
        head = trimesh.creation.cone(radius=0.06, height=length * 0.2, sections=24)
        head.visual.vertex_colors = color

        # align along +Z then rotate to direction
        axis = np.cross([0, 0, 1.0], direction)
        angle = np.arccos(np.clip(np.dot([0, 0, 1.0], direction), -1.0, 1.0))
        if np.linalg.norm(axis) > 1e-6 and angle > 1e-6:
            R = trimesh.transformations.rotation_matrix(angle, axis)
            shaft.apply_transform(R)
            head.apply_transform(R)

        # position
        shaft.apply_translation(start)
        head.apply_translation(start + direction * length * 0.8)

        return trimesh.util.concatenate([shaft, head])

    # ---------- models ----------
    def generate_wave_types(self) -> Dict[str, Any]:
        """Transverse vs longitudinal waves using spheres along paths and arrows."""
        meshes = []
        # transverse: sine-like path in X-Z plane
        t = np.linspace(0, 2 * np.pi, 32)
        x = t
        z = 0.4 * np.sin(t)
        for xi, zi in zip(x, z):
            s = trimesh.creation.icosphere(subdivisions=2, radius=0.05)
            s.apply_translation([xi, 0.0, zi])
            s.visual.vertex_colors = self.colors["wave"]
            meshes.append(s)
        # longitudinal: spheres along X with compressions
        x2 = np.linspace(0, 2 * np.pi, 32)
        density = 0.5 + 0.5 * np.sin(x2)
        position = 0.0
        for i in range(len(x2)):
            s = trimesh.creation.icosphere(subdivisions=2, radius=0.05)
            s.apply_translation([position, -0.5, 0.0])
            s.visual.vertex_colors = [100, 255, 150, 255]
            meshes.append(s)
            position += 0.12 * density[i]

        # arrows indicating direction of propagation
        meshes.append(self._create_arrow([0, 0.0, 0], [6.5, 0.0, 0]))
        meshes.append(self._create_arrow([0, -0.5, 0], [6.5, -0.5, 0], [100, 255, 150, 255]))

        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "wave_types.glb")
        meta.update({
            "description": "Transverse (sine-like) and longitudinal (compressions) wave comparison",
            "curriculum": ["phy_010"],
        })
        return meta

    def generate_electromagnetic_spectrum(self) -> Dict[str, Any]:
        """EM spectrum as colored bars with gradient ordering."""
        meshes = []
        bands = [
            ("radio", [150, 0, 150, 255]),
            ("microwave", [120, 0, 200, 255]),
            ("infrared", [255, 100, 100, 255]),
            ("visible", [255, 255, 100, 255]),
            ("ultraviolet", [100, 100, 255, 255]),
            ("xray", [100, 200, 255, 255]),
            ("gamma", [150, 255, 255, 255]),
        ]
        x = 0.0
        for name, color in bands:
            bar = trimesh.creation.box(extents=[1.2, 0.15, 0.05])
            bar.apply_translation([x, 0.0, 0.0])
            bar.visual.vertex_colors = color
            meshes.append(bar)
            x += 1.4
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "electromagnetic_spectrum.glb")
        meta.update({
            "description": "Electromagnetic spectrum bands (radio → gamma) as colored bars",
            "curriculum": ["phy_011"],
        })
        return meta

    def generate_reflection_mirrors(self) -> Dict[str, Any]:
        """Plane, concave, convex mirrors with incident/reflected rays."""
        meshes = []
        # plane mirror
        plane = trimesh.creation.box(extents=[2.0, 1.2, 0.05])
        plane.apply_translation([-2.5, 0.0, 0.0])
        plane.visual.vertex_colors = self.colors["mirror"]
        meshes.append(plane)
        meshes.append(self._create_arrow([-3.5, 0.3, 0.5], [-2.5, 0.3, 0.05]))
        meshes.append(self._create_arrow([-2.5, 0.3, 0.05], [-1.5, 0.3, -0.5]))

        # concave mirror (approx as inward-curved thin cylinder segment)
        concave = trimesh.creation.cylinder(radius=0.6, height=0.05, sections=48)
        concave.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
        concave.apply_translation([0.0, 0.0, 0.0])
        concave.visual.vertex_colors = self.colors["mirror"]
        meshes.append(concave)
        meshes.append(self._create_arrow([-1.0, -0.3, 0.5], [0.0, -0.3, 0.0]))
        meshes.append(self._create_arrow([0.0, -0.3, 0.0], [1.0, -0.1, -0.4]))

        # convex mirror (outward-curved thin cylinder segment)
        convex = concave.copy()
        convex.apply_translation([3.0, 0.0, 0.0])
        meshes.append(convex)
        meshes.append(self._create_arrow([2.0, 0.4, 0.5], [3.0, 0.4, 0.0]))
        meshes.append(self._create_arrow([3.0, 0.4, 0.0], [4.0, 0.6, 0.5]))

        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "reflection_mirrors.glb")
        meta.update({
            "description": "Plane, concave and convex mirrors with incident/reflected rays",
            "curriculum": ["phy_011"],
        })
        return meta

    def generate_refraction_lenses(self) -> Dict[str, Any]:
        """Convex and concave lenses with refracted rays (approx)."""
        meshes = []
        # convex lens: two discs close together
        lens1 = trimesh.creation.cylinder(radius=0.6, height=0.2, sections=48)
        lens1.apply_translation([-1.5, 0.0, 0.0])
        lens1.visual.vertex_colors = self.colors["lens"]
        meshes.append(lens1)
        meshes.append(self._create_arrow([-3.0, 0.0, 0.0], [-1.5, 0.0, 0.0]))
        meshes.append(self._create_arrow([-1.5, 0.0, 0.0], [0.0, -0.2, 0.3]))

        # concave lens: smaller radius, suggest divergence
        lens2 = trimesh.creation.cylinder(radius=0.5, height=0.2, sections=48)
        lens2.apply_translation([1.5, 0.0, 0.0])
        lens2.visual.vertex_colors = self.colors["lens"]
        meshes.append(lens2)
        meshes.append(self._create_arrow([0.0, 0.0, 0.0], [1.5, 0.0, 0.0]))
        meshes.append(self._create_arrow([1.5, 0.0, 0.0], [3.0, 0.2, -0.3]))

        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "refraction_lenses.glb")
        meta.update({
            "description": "Convex and concave lenses with approximated refracted rays",
            "curriculum": ["phy_011"],
        })
        return meta

    def generate_total_internal_reflection(self) -> Dict[str, Any]:
        """Fiber optic cable with internal reflection arrows."""
        meshes = []
        fiber = trimesh.creation.cylinder(radius=0.4, height=6.0, sections=48)
        fiber.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
        fiber.apply_translation([0.0, -0.4, 0.0])
        fiber.visual.vertex_colors = self.colors["fiber"]
        meshes.append(fiber)
        # internal zig arrows
        meshes.append(self._create_arrow([-2.5, -0.4, -0.2], [-1.5, -0.4, 0.2]))
        meshes.append(self._create_arrow([-1.5, -0.4, 0.2], [-0.5, -0.4, -0.2]))
        meshes.append(self._create_arrow([-0.5, -0.4, -0.2], [0.5, -0.4, 0.2]))
        meshes.append(self._create_arrow([0.5, -0.4, 0.2], [1.5, -0.4, -0.2]))
        meshes.append(self._create_arrow([1.5, -0.4, -0.2], [2.5, -0.4, 0.2]))

        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "total_internal_reflection.glb")
        meta.update({
            "description": "Fiber optic cable demonstrating total internal reflection",
            "curriculum": ["phy_011"],
        })
        return meta

    def generate_prism_dispersion(self) -> Dict[str, Any]:
        """Triangular prism (simplified box) with dispersion rays (rainbow)."""
        meshes = []
        prism = trimesh.creation.box(extents=[1.2, 1.0, 0.8])
        prism.apply_translation([0.0, 0.0, 0.0])
        prism.visual.vertex_colors = self.colors["prism"]
        meshes.append(prism)

        # incident ray
        meshes.append(self._create_arrow([-1.5, 0.0, 0.2], [-0.6, 0.0, 0.1]))
        # dispersed rays (approx colors)
        colors = [
            [255, 0, 0, 255],
            [255, 165, 0, 255],
            [255, 255, 0, 255],
            [0, 128, 0, 255],
            [0, 0, 255, 255],
            [75, 0, 130, 255],
            [148, 0, 211, 255],
        ]
        angles = np.linspace(-0.2, 0.3, len(colors))
        for i, col in enumerate(colors):
            end = [1.5, angles[i], -0.2 + 0.1 * i]
            meshes.append(self._create_arrow([0.6, 0.0, 0.0], end, col))

        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "prism_dispersion.glb")
        meta.update({
            "description": "Prism dispersion with incident ray and rainbow-colored exit rays",
            "curriculum": ["phy_011"],
        })
        return meta

    # ---------- batches ----------
    def generate_all_models(self) -> List[Dict[str, Any]]:
        logger.info("🌊 Generating all wave & optics models...")
        models = [
            self.generate_wave_types(),
            self.generate_electromagnetic_spectrum(),
            self.generate_reflection_mirrors(),
            self.generate_refraction_lenses(),
            self.generate_total_internal_reflection(),
            self.generate_prism_dispersion(),
        ]
        self.generate_manifest(models)
        logger.info(f"✅ Generated {len(models)} wave & optics models")
        return models

    def generate_manifest(self, models: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_size = sum(m.get("size_kb", 0) for m in models)
        manifest = {
            "models": models,
            "total_models": len(models),
            "total_size_kb": round(total_size, 2),
            "curriculum_alignment": {
                "phy_010": "Wave Types and Properties",
                "phy_011": "Optics: Reflection, Refraction, Spectrum",
            },
            "output_dir": str(self.output_dir),
        }
        path = self.output_dir / "wave_optics_manifest.json"
        with open(path, "w") as f:
            json.dump(manifest, f, indent=2)
        return manifest


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description="Wave & Optics Models Generator")
    parser.add_argument("--model", choices=[
        "all", "wave_types", "electromagnetic_spectrum", "reflection_mirrors",
        "refraction_lenses", "total_internal_reflection", "prism_dispersion"
    ], default="all")
    args = parser.parse_args()

    gen = WaveOpticsGenerator()
    if args.model == "all":
        gen.generate_all_models()
        print("📋 Manifest created: wave_optics_manifest.json")
    else:
        func = getattr(gen, f"generate_{args.model}")
        meta = func()
        print(f"✅ Generated: {meta['name']}.glb → {meta['size_kb']} KB")
