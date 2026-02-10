import json
import logging
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import trimesh

logger = logging.getLogger(__name__)


class CellBiologyGenerator:
    """Generator for Cell Biology educational models (Priority #7)
    Models:
    - animal_cell.glb: complete animal cell with all major organelles
    - plant_vs_animal_cell.glb: side-by-side comparison
    - mitochondria.glb: powerhouse with cristae structure
    - cell_membrane.glb: phospholipid bilayer with proteins
    - nucleus.glb: nuclear membrane and chromatin
    - cell_division.glb: mitosis stages (prophase, metaphase, anaphase, telophase)
    """

    def __init__(self, output_dir: Path = None) -> None:
        self.output_dir = Path(output_dir or "generated_assets/cell_biology")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.colors = {
            "nucleus": [200, 100, 100, 255],
            "mitochondria": [255, 150, 0, 255],
            "er": [150, 200, 150, 255],
            "golgi": [150, 150, 200, 255],
            "ribosome": [255, 200, 100, 255],
            "lysosome": [200, 150, 255, 255],
            "membrane": [200, 200, 200, 200],
            "protein": [100, 150, 255, 255],
            "cell_wall": [100, 100, 100, 255],
            "chloroplast": [50, 200, 50, 255],
            "chromatin": [255, 100, 100, 255],
            "centriole": [200, 200, 100, 255],
        }

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

    def _create_sphere(self, center, radius, color, subdivisions=2):
        """Helper to create colored sphere at position."""
        s = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
        s.apply_translation(center)
        s.visual.vertex_colors = color
        return s

    def _create_cylinder(self, start, end, radius, color, sections=16):
        """Helper to create cylinder between two points."""
        cyl = trimesh.creation.cylinder(radius=radius, height=1.0, sections=sections)
        vec = np.array(end) - np.array(start)
        length = np.linalg.norm(vec)
        if length < 1e-6:
            return None
        direction = vec / length
        axis = np.cross([0, 0, 1.0], direction)
        if np.linalg.norm(axis) > 1e-6:
            angle = np.arccos(np.clip(np.dot([0, 0, 1.0], direction), -1.0, 1.0))
            R = trimesh.transformations.rotation_matrix(angle, axis)
            cyl.apply_transform(R)
        cyl.apply_translation(start)
        cyl.visual.vertex_colors = color
        return cyl

    # ---------- models ----------
    def generate_animal_cell(self) -> Dict[str, Any]:
        """Complete animal cell with major organelles."""
        meshes = []
        
        # Cell membrane (outer sphere)
        cell = trimesh.creation.icosphere(subdivisions=3, radius=5.0)
        cell.visual.vertex_colors = self.colors["membrane"]
        meshes.append(cell)

        # Nucleus (large central sphere)
        nucleus = self._create_sphere([0, 0, 0], 1.5, self.colors["nucleus"], 2)
        meshes.append(nucleus)
        
        # Chromatin inside nucleus (small spheres)
        for i in range(8):
            angle = 2 * np.pi * i / 8
            x = 0.5 * np.cos(angle)
            z = 0.5 * np.sin(angle)
            chromatin = self._create_sphere([x, 0, z], 0.2, self.colors["chromatin"], 1)
            meshes.append(chromatin)

        # Mitochondria (small elongated)
        mito_positions = [[-2, 2, 1], [2, 2, -1], [-1, -2, 2], [1, -2, -1]]
        for pos in mito_positions:
            mito = trimesh.creation.cylinder(radius=0.3, height=1.2, sections=16)
            mito.apply_translation(pos)
            mito.visual.vertex_colors = self.colors["mitochondria"]
            meshes.append(mito)

        # Endoplasmic reticulum (rough, wavy)
        er_points = [[-3, 1, 0], [-2, 1.5, 0.5], [-1, 1, 1], [0, 1.5, 0.5]]
        for i in range(len(er_points) - 1):
            cyl = self._create_cylinder(er_points[i], er_points[i+1], 0.2, self.colors["er"])
            if cyl is not None:
                meshes.append(cyl)

        # Golgi apparatus (stack of discs)
        for i in range(4):
            disc = trimesh.creation.cylinder(radius=0.8, height=0.15, sections=20)
            disc.apply_translation([2, -1 + i*0.3, 1])
            disc.visual.vertex_colors = self.colors["golgi"]
            meshes.append(disc)

        # Ribosomes (small dots)
        for i in range(12):
            angle = 2 * np.pi * i / 12
            x = 3.5 * np.cos(angle)
            z = 3.5 * np.sin(angle)
            y = np.random.uniform(-1, 1)
            rib = self._create_sphere([x, y, z], 0.15, self.colors["ribosome"], 1)
            meshes.append(rib)

        # Lysosomes (small spheres)
        for i in range(6):
            lys = self._create_sphere(np.random.uniform(-3, 3, 3), 0.3, self.colors["lysosome"], 1)
            meshes.append(lys)

        # Centrioles (pair of cylinders)
        cent1 = self._create_cylinder([-0.5, -1.5, 0], [0.5, -1.5, 0], 0.1, self.colors["centriole"])
        cent2 = self._create_cylinder([0, -1.0, -0.5], [0, -2.0, 0.5], 0.1, self.colors["centriole"])
        if cent1 is not None:
            meshes.append(cent1)
        if cent2 is not None:
            meshes.append(cent2)

        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "animal_cell.glb")
        meta.update({
            "description": "Complete animal cell with nucleus, mitochondria, ER, Golgi, ribosomes, lysosomes, centrioles",
            "curriculum": ["bio_001"],
        })
        return meta

    def generate_plant_vs_animal_cell(self) -> Dict[str, Any]:
        """Side-by-side animal (left) and plant (right) cell comparison."""
        meshes = []
        
        # Animal cell (left side)
        animal_cell = trimesh.creation.icosphere(subdivisions=3, radius=4.0)
        animal_cell.apply_translation([-5.5, 0, 0])
        animal_cell.visual.vertex_colors = self.colors["membrane"]
        meshes.append(animal_cell)

        # Animal nucleus
        nucleus_a = self._create_sphere([-5.5, 0, 0], 1.2, self.colors["nucleus"], 2)
        meshes.append(nucleus_a)

        # Animal mitochondria
        mito_a = trimesh.creation.cylinder(radius=0.25, height=0.8, sections=16)
        mito_a.apply_translation([-7, 0.5, 0])
        mito_a.visual.vertex_colors = self.colors["mitochondria"]
        meshes.append(mito_a)

        # Plant cell (right side) - with cell wall
        wall = trimesh.creation.box(extents=[8.5, 8.5, 0.3])
        wall.apply_translation([5.5, 0, -2.1])
        wall.visual.vertex_colors = self.colors["cell_wall"]
        meshes.append(wall)

        plant_cell = trimesh.creation.icosphere(subdivisions=3, radius=4.0)
        plant_cell.apply_translation([5.5, 0, 0])
        plant_cell.visual.vertex_colors = self.colors["membrane"]
        meshes.append(plant_cell)

        # Plant nucleus
        nucleus_p = self._create_sphere([5.5, 0, 0], 1.2, self.colors["nucleus"], 2)
        meshes.append(nucleus_p)

        # Plant chloroplast (multiple large organelles)
        for i in range(3):
            angle = 2 * np.pi * i / 3
            x = 5.5 + 2.0 * np.cos(angle)
            z = 2.0 * np.sin(angle)
            chloro = self._create_sphere([x, 0, z], 0.8, self.colors["chloroplast"], 2)
            meshes.append(chloro)

        # Plant mitochondria
        mito_p = trimesh.creation.cylinder(radius=0.25, height=0.8, sections=16)
        mito_p.apply_translation([7, 0.5, 0])
        mito_p.visual.vertex_colors = self.colors["mitochondria"]
        meshes.append(mito_p)

        # Large vacuole in plant
        vacuole = trimesh.creation.icosphere(subdivisions=2, radius=2.5)
        vacuole.apply_translation([5.5, 0, 0])
        vacuole.visual.vertex_colors = [150, 200, 150, 180]
        meshes.append(vacuole)

        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "plant_vs_animal_cell.glb")
        meta.update({
            "description": "Side-by-side comparison: animal cell (left) vs plant cell (right) with cell wall, chloroplasts, large vacuole",
            "curriculum": ["bio_001"],
        })
        return meta

    def generate_mitochondria(self) -> Dict[str, Any]:
        """Mitochondria with cristae structure."""
        meshes = []
        
        # Outer membrane (ellipsoid)
        outer = trimesh.creation.cylinder(radius=1.2, height=3.0, sections=32)
        outer.visual.vertex_colors = self.colors["mitochondria"]
        meshes.append(outer)

        # Inner membrane (smaller cylinder inside)
        inner = trimesh.creation.cylinder(radius=0.8, height=2.5, sections=32)
        inner.apply_translation([0, 0, 0.2])
        inner.visual.vertex_colors = [255, 180, 50, 255]
        meshes.append(inner)

        # Cristae (thin internal folds)
        for i in range(6):
            z_pos = -1.0 + i * 0.4
            crista = trimesh.creation.cylinder(radius=0.1, height=1.5, sections=16)
            crista.apply_translation([0.5 * np.cos(i), 0.5 * np.sin(i), z_pos])
            crista.visual.vertex_colors = [255, 200, 100, 255]
            meshes.append(crista)

        # Matrix (inner space indicator - spheres)
        for i in range(10):
            matrix_particle = self._create_sphere(np.random.uniform(-0.8, 0.8, 3), 0.1, [255, 220, 150, 200], 1)
            meshes.append(matrix_particle)

        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "mitochondria.glb")
        meta.update({
            "description": "Mitochondria cross-section showing outer/inner membranes, cristae, and matrix",
            "curriculum": ["bio_001"],
        })
        return meta

    def generate_cell_membrane(self) -> Dict[str, Any]:
        """Phospholipid bilayer with embedded proteins."""
        meshes = []
        
        # Base plane (membrane cross-section)
        base = trimesh.creation.box(extents=[6.0, 0.2, 2.0])
        base.visual.vertex_colors = self.colors["membrane"]
        meshes.append(base)

        # Phospholipid heads (spheres on both sides)
        for i in range(10):
            x = -2.5 + i * 0.6
            # Outer head
            head_out = self._create_sphere([x, 0.15, 0], 0.2, [200, 100, 100, 255], 1)
            meshes.append(head_out)
            # Inner head
            head_in = self._create_sphere([x, -0.15, 0], 0.2, [200, 100, 100, 255], 1)
            meshes.append(head_in)
            # Tail (thin lines)
            tail = self._create_cylinder([x, 0.12, 0], [x, -0.12, 0], 0.05, [200, 200, 200, 255])
            if tail is not None:
                meshes.append(tail)

        # Membrane proteins (embedded cylinders)
        protein_positions = [
            [-2.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [-1.0, 0.0, -0.8],
            [1.0, 0.0, 0.8],
        ]
        for pos in protein_positions:
            protein = trimesh.creation.cylinder(radius=0.3, height=0.5, sections=16)
            protein.apply_translation(pos)
            protein.visual.vertex_colors = self.colors["protein"]
            meshes.append(protein)

        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "cell_membrane.glb")
        meta.update({
            "description": "Phospholipid bilayer with heads, tails, and embedded protein molecules",
            "curriculum": ["bio_001"],
        })
        return meta

    def generate_nucleus(self) -> Dict[str, Any]:
        """Nucleus with nuclear membrane and chromatin."""
        meshes = []
        
        # Nuclear envelope (outer sphere)
        envelope = trimesh.creation.icosphere(subdivisions=3, radius=2.0)
        envelope.visual.vertex_colors = self.colors["nucleus"]
        meshes.append(envelope)

        # Nuclear pores (small holes - represented by circles)
        for i in range(12):
            angle_phi = np.pi * i / 6
            angle_theta = 2 * np.pi * np.random.random()
            x = 2.0 * np.sin(angle_phi) * np.cos(angle_theta)
            y = 2.0 * np.sin(angle_phi) * np.sin(angle_theta)
            z = 2.0 * np.cos(angle_phi)
            pore = self._create_sphere([x, y, z], 0.15, [100, 100, 100, 150], 1)
            meshes.append(pore)

        # Chromatin (fibrous DNA structure - cylinders and spheres)
        for i in range(20):
            angle = 2 * np.pi * i / 20
            x = 1.0 * np.cos(angle)
            y = 0.5 * np.sin(angle)
            z = np.random.uniform(-1.0, 1.0)
            chromatin = self._create_sphere([x, y, z], 0.15, self.colors["chromatin"], 1)
            meshes.append(chromatin)

        # Nucleolus (dense central region)
        nucleolus = self._create_sphere([0, 0, 0], 0.7, [255, 150, 100, 255], 2)
        meshes.append(nucleolus)

        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "nucleus.glb")
        meta.update({
            "description": "Nucleus showing nuclear envelope with pores, chromatin, and nucleolus",
            "curriculum": ["bio_001"],
        })
        return meta

    def generate_cell_division(self) -> Dict[str, Any]:
        """Mitosis stages: prophase, metaphase, anaphase, telophase."""
        meshes = []
        stage_spacing = 3.5

        stages = [
            ("Prophase", 0, [
                ("chromatin", [-1, 0, -1], 0.2),
                ("chromatin", [0, 0, 0], 0.2),
                ("chromatin", [1, 0, 1], 0.2),
                ("centriole", [-1.5, 0, 0], 0.15),
                ("centriole", [1.5, 0, 0], 0.15),
            ]),
            ("Metaphase", stage_spacing, [
                ("chromatin", [-0.5, 0, 0], 0.2),
                ("chromatin", [0, 0, 0.5], 0.2),
                ("chromatin", [0.5, 0, 0], 0.2),
                ("centriole", [-1.5, 0, 0], 0.15),
                ("centriole", [1.5, 0, 0], 0.15),
            ]),
            ("Anaphase", 2 * stage_spacing, [
                ("chromatin", [-1, 0, -0.5], 0.15),
                ("chromatin", [1, 0, 0.5], 0.15),
                ("chromatin", [-0.5, 0, -1], 0.15),
                ("chromatin", [0.5, 0, 1], 0.15),
                ("centriole", [-1.5, 0, 0], 0.15),
                ("centriole", [1.5, 0, 0], 0.15),
            ]),
            ("Telophase", 3 * stage_spacing, [
                ("nucleus", [-1.5, 0, 0], 0.6),
                ("nucleus", [1.5, 0, 0], 0.6),
                ("centriole", [-2.0, 0, 0], 0.1),
                ("centriole", [2.0, 0, 0], 0.1),
            ]),
        ]

        for stage_name, x_offset, components in stages:
            for comp_type, pos, radius in components:
                color = self.colors.get(comp_type, [100, 100, 100, 255])
                sphere = self._create_sphere(
                    [pos[0] + x_offset, pos[1], pos[2]], 
                    radius, 
                    color, 
                    1
                )
                meshes.append(sphere)
            
            # Stage outline (small box)
            outline = trimesh.creation.box(extents=[2.0, 2.0, 0.05])
            outline.apply_translation([x_offset, 0, -1.2])
            outline.visual.vertex_colors = [100, 100, 100, 100]
            meshes.append(outline)

        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "cell_division.glb")
        meta.update({
            "description": "Mitosis stages: Prophase, Metaphase, Anaphase, Telophase showing chromosome movement and cytokinesis",
            "curriculum": ["bio_001"],
        })
        return meta

    # ---------- batches ----------
    def generate_all_models(self) -> List[Dict[str, Any]]:
        logger.info("🧬 Generating all cell biology models...")
        models = [
            self.generate_animal_cell(),
            self.generate_plant_vs_animal_cell(),
            self.generate_mitochondria(),
            self.generate_cell_membrane(),
            self.generate_nucleus(),
            self.generate_cell_division(),
        ]
        self.generate_manifest(models)
        logger.info(f"✅ Generated {len(models)} cell biology models")
        return models

    def generate_manifest(self, models: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_size = sum(m.get("size_kb", 0) for m in models)
        manifest = {
            "models": models,
            "total_models": len(models),
            "total_size_kb": round(total_size, 2),
            "curriculum_alignment": {
                "bio_001": "Cell Biology: Structure and Function",
            },
            "output_dir": str(self.output_dir),
        }
        path = self.output_dir / "cell_biology_manifest.json"
        with open(path, "w") as f:
            json.dump(manifest, f, indent=2)
        return manifest


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description="Cell Biology Models Generator")
    parser.add_argument("--model", choices=[
        "all", "animal_cell", "plant_vs_animal_cell", "mitochondria",
        "cell_membrane", "nucleus", "cell_division"
    ], default="all")
    args = parser.parse_args()

    gen = CellBiologyGenerator()
    if args.model == "all":
        gen.generate_all_models()
        print("📋 Manifest created: cell_biology_manifest.json")
    else:
        func = getattr(gen, f"generate_{args.model}")
        meta = func()
        print(f"✅ Generated: {meta['name']}.glb → {meta['size_kb']} KB")
