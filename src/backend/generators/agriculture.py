import json
import logging
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import trimesh

logger = logging.getLogger(__name__)


class AgricultureModelGenerator:
    """Generator for Agricultural Science educational models (Priority #10)
    Models:
    - soil_layers.glb: topsoil, subsoil, bedrock with organic matter
    - crop_growth_stages.glb: maize/rice growth from seed to harvest
    - livestock_anatomy.glb: cow, goat, chicken digestive systems
    - farm_tools_3d.glb: hoe, cutlass, plough, harrow (Nigerian tools)
    - irrigation_systems.glb: drip, sprinkler, surface irrigation
    - greenhouse.glb: modern greenhouse structure with plants
    """

    def __init__(self, output_dir: Path = None) -> None:
        self.output_dir = Path(output_dir or "generated_assets/agriculture")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.colors = {
            "topsoil": [101, 67, 33, 255],
            "subsoil": [139, 90, 43, 255],
            "bedrock": [169, 169, 169, 255],
            "organic": [60, 40, 20, 255],
            "plant_green": [34, 139, 34, 255],
            "seed": [139, 90, 43, 255],
            "root": [160, 82, 45, 255],
            "stem": [50, 205, 50, 255],
            "leaf": [0, 128, 0, 255],
            "grain": [255, 215, 0, 255],
            "cow": [160, 82, 45, 255],
            "goat": [210, 180, 140, 255],
            "chicken": [255, 255, 255, 255],
            "metal": [192, 192, 192, 255],
            "wood": [139, 69, 19, 255],
            "water": [30, 144, 255, 255],
            "pipe": [105, 105, 105, 255],
            "glass": [173, 216, 230, 200],
            "frame": [100, 100, 100, 255],
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

    def _create_box(self, center, extents, color):
        """Helper to create colored box."""
        box = trimesh.creation.box(extents=extents)
        box.apply_translation(center)
        box.visual.vertex_colors = color
        return box

    def _create_cylinder(self, start, end, radius, color, sections=32):
        """Helper to create cylinder between two points."""
        cyl = trimesh.creation.cylinder(radius=radius, height=1.0, sections=sections)
        vec = np.array(end) - np.array(start)
        length = np.linalg.norm(vec)
        if length < 1e-6:
            return None
        direction = vec / length
        cyl.apply_scale([1, 1, length])
        axis = np.cross([0, 0, 1.0], direction)
        if np.linalg.norm(axis) > 1e-6:
            angle = np.arccos(np.clip(np.dot([0, 0, 1.0], direction), -1.0, 1.0))
            R = trimesh.transformations.rotation_matrix(angle, axis)
            cyl.apply_transform(R)
        cyl.apply_translation(start)
        cyl.visual.vertex_colors = color
        return cyl

    def _create_sphere(self, center, radius, color, subdivisions=2):
        """Helper to create colored sphere."""
        sphere = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
        sphere.apply_translation(center)
        sphere.visual.vertex_colors = color
        return sphere

    def _create_cone(self, height, radius, color, position=[0, 0, 0]):
        """Helper to create colored cone."""
        cone = trimesh.creation.cone(radius=radius, height=height, sections=32)
        cone.apply_translation(position)
        cone.visual.vertex_colors = color
        return cone

    # ---------- models ----------
    def generate_soil_layers(self) -> Dict[str, Any]:
        """Soil profile showing topsoil, subsoil, and bedrock layers."""
        meshes = []
        
        # Bedrock layer (bottom, hardest layer)
        bedrock = self._create_box([0, 0, -3.0], [8.0, 8.0, 2.0], self.colors["bedrock"])
        meshes.append(bedrock)
        
        # Subsoil layer (middle, less organic matter)
        subsoil = self._create_box([0, 0, -1.2], [8.0, 8.0, 1.6], self.colors["subsoil"])
        meshes.append(subsoil)
        
        # Topsoil layer (top, rich in organic matter)
        topsoil = self._create_box([0, 0, 0.2], [8.0, 8.0, 1.2], self.colors["topsoil"])
        meshes.append(topsoil)
        
        # Organic matter particles in topsoil
        for i in range(15):
            x = np.random.uniform(-3.5, 3.5)
            y = np.random.uniform(-3.5, 3.5)
            z = np.random.uniform(-0.2, 0.6)
            organic = self._create_sphere([x, y, z], 0.12, self.colors["organic"], 1)
            meshes.append(organic)
        
        # Plant roots penetrating layers
        for i in range(5):
            x = np.random.uniform(-3.0, 3.0)
            y = np.random.uniform(-3.0, 3.0)
            root = self._create_cylinder([x, y, 0.8], [x + np.random.uniform(-0.3, 0.3), 
                                                        y + np.random.uniform(-0.3, 0.3), -1.5], 
                                        0.05, self.colors["root"])
            if root:
                meshes.append(root)
        
        # Layer labels (zones)
        # Topsoil zone indicator
        topsoil_label = self._create_box([4.5, 0, 0.2], [0.8, 1.5, 0.8], [101, 67, 33, 100])
        meshes.append(topsoil_label)
        
        # Subsoil zone indicator
        subsoil_label = self._create_box([4.5, 0, -1.2], [0.8, 1.5, 1.2], [139, 90, 43, 100])
        meshes.append(subsoil_label)
        
        # Bedrock zone indicator
        bedrock_label = self._create_box([4.5, 0, -3.0], [0.8, 1.5, 1.5], [169, 169, 169, 100])
        meshes.append(bedrock_label)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "soil_layers.glb")
        meta.update({
            "description": "Soil profile showing topsoil (organic-rich), subsoil, and bedrock layers with plant roots",
            "curriculum": ["agr_002"],
        })
        return meta

    def generate_crop_growth_stages(self) -> Dict[str, Any]:
        """Maize/rice growth stages from seed to harvest."""
        meshes = []
        
        # Ground base
        ground = self._create_box([0, 0, -0.3], [12.0, 4.0, 0.6], self.colors["topsoil"])
        meshes.append(ground)
        
        # Stage 1: Seed (far left)
        seed = self._create_sphere([-5.0, 0, 0.2], 0.2, self.colors["seed"], 1)
        meshes.append(seed)
        
        # Stage 2: Germination (small sprout)
        germination_root = self._create_cylinder([-3.5, 0, 0], [-3.5, 0, -0.4], 0.05, self.colors["root"])
        if germination_root:
            meshes.append(germination_root)
        germination_stem = self._create_cylinder([-3.5, 0, 0], [-3.5, 0, 0.5], 0.06, self.colors["stem"])
        if germination_stem:
            meshes.append(germination_stem)
        
        # Stage 3: Seedling (2 leaves)
        seedling_stem = self._create_cylinder([-2.0, 0, 0], [-2.0, 0, 1.2], 0.08, self.colors["stem"])
        if seedling_stem:
            meshes.append(seedling_stem)
        leaf1 = self._create_box([-2.0, -0.6, 0.8], [0.1, 1.2, 0.4], self.colors["leaf"])
        meshes.append(leaf1)
        leaf2 = self._create_box([-2.0, 0.6, 1.0], [0.1, 1.0, 0.3], self.colors["leaf"])
        meshes.append(leaf2)
        
        # Stage 4: Vegetative growth (multiple leaves)
        veg_stem = self._create_cylinder([-0.5, 0, 0], [-0.5, 0, 2.0], 0.12, self.colors["stem"])
        if veg_stem:
            meshes.append(veg_stem)
        for i, height in enumerate([0.8, 1.2, 1.6]):
            leaf = self._create_box([-0.5, -0.8 if i % 2 == 0 else 0.8, height], 
                                   [0.1, 1.5, 0.5], self.colors["leaf"])
            meshes.append(leaf)
        
        # Stage 5: Flowering/Tasseling
        flower_stem = self._create_cylinder([1.0, 0, 0], [1.0, 0, 2.8], 0.14, self.colors["stem"])
        if flower_stem:
            meshes.append(flower_stem)
        # Tassel (flower at top)
        tassel = self._create_cone(0.6, 0.3, [255, 255, 100, 255], [1.0, 0, 3.2])
        meshes.append(tassel)
        for i in range(4):
            leaf = self._create_box([1.0, -1.0 if i % 2 == 0 else 1.0, 1.0 + i * 0.6], 
                                   [0.1, 1.8, 0.6], self.colors["leaf"])
            meshes.append(leaf)
        
        # Stage 6: Grain formation
        grain_stem = self._create_cylinder([2.5, 0, 0], [2.5, 0, 2.5], 0.14, self.colors["stem"])
        if grain_stem:
            meshes.append(grain_stem)
        # Ear of corn/rice head
        ear = self._create_cylinder([2.5, 0.5, 2.0], [2.5, 0.5, 2.8], 0.15, self.colors["grain"])
        if ear:
            meshes.append(ear)
        for i in range(4):
            leaf = self._create_box([2.5, -1.0 if i % 2 == 0 else 1.0, 0.8 + i * 0.5], 
                                   [0.1, 1.6, 0.5], self.colors["leaf"])
            meshes.append(leaf)
        
        # Stage 7: Mature harvest-ready
        mature_stem = self._create_cylinder([4.0, 0, 0], [4.0, 0, 2.3], 0.14, [139, 115, 85, 255])
        if mature_stem:
            meshes.append(mature_stem)
        # Mature ear (ready to harvest)
        mature_ear = self._create_cylinder([4.0, 0.6, 1.8], [4.0, 0.6, 2.8], 0.18, self.colors["grain"])
        if mature_ear:
            meshes.append(mature_ear)
        for i in range(3):
            leaf = self._create_box([4.0, -0.8 if i % 2 == 0 else 0.8, 0.8 + i * 0.5], 
                                   [0.1, 1.4, 0.4], [154, 205, 50, 255])
            meshes.append(leaf)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "crop_growth_stages.glb")
        meta.update({
            "description": "Maize/rice growth stages: seed, germination, seedling, vegetative, flowering, grain formation, harvest",
            "curriculum": ["agr_003"],
        })
        return meta

    def generate_livestock_anatomy(self) -> Dict[str, Any]:
        """Simplified digestive systems of cow, goat, and chicken."""
        meshes = []
        
        # COW (left side)
        # Body
        cow_body = self._create_box([-4.0, 0, 1.0], [2.0, 1.2, 1.0], self.colors["cow"])
        meshes.append(cow_body)
        # Head
        cow_head = self._create_box([-5.2, 0, 1.2], [0.8, 0.8, 0.6], self.colors["cow"])
        meshes.append(cow_head)
        # Legs
        for x_offset in [-0.6, 0.6]:
            leg = self._create_cylinder([-4.0 + x_offset, 0, 0.5], [-4.0 + x_offset, 0, -0.5], 0.15, self.colors["cow"])
            if leg:
                meshes.append(leg)
        # Rumen (large stomach chamber)
        rumen = self._create_sphere([-4.0, 0, 0.8], 0.5, [200, 100, 100, 200], 2)
        meshes.append(rumen)
        # Intestines
        intestine = self._create_cylinder([-3.5, 0, 0.6], [-3.0, 0, 0.4], 0.12, [255, 182, 193, 200])
        if intestine:
            meshes.append(intestine)
        
        # GOAT (center)
        # Body
        goat_body = self._create_box([0, 0, 0.8], [1.5, 0.9, 0.8], self.colors["goat"])
        meshes.append(goat_body)
        # Head
        goat_head = self._create_box([-1.0, 0, 1.0], [0.6, 0.6, 0.5], self.colors["goat"])
        meshes.append(goat_head)
        # Legs
        for x_offset in [-0.4, 0.4]:
            leg = self._create_cylinder([0 + x_offset, 0, 0.4], [0 + x_offset, 0, -0.4], 0.12, self.colors["goat"])
            if leg:
                meshes.append(leg)
        # Stomach system (smaller rumen)
        stomach = self._create_sphere([0, 0, 0.6], 0.35, [200, 100, 100, 200], 2)
        meshes.append(stomach)
        # Intestines
        intestine = self._create_cylinder([0.3, 0, 0.5], [0.6, 0, 0.3], 0.1, [255, 182, 193, 200])
        if intestine:
            meshes.append(intestine)
        
        # CHICKEN (right side)
        # Body
        chicken_body = self._create_sphere([4.0, 0, 0.8], 0.6, self.colors["chicken"], 2)
        meshes.append(chicken_body)
        # Head
        chicken_head = self._create_sphere([4.5, 0, 1.2], 0.3, self.colors["chicken"], 1)
        meshes.append(chicken_head)
        # Beak
        beak = self._create_cone(0.2, 0.1, [255, 200, 0, 255], [4.7, 0, 1.2])
        meshes.append(beak)
        # Legs
        for y_offset in [-0.3, 0.3]:
            leg = self._create_cylinder([4.0, y_offset, 0.5], [4.0, y_offset, -0.2], 0.08, [255, 200, 0, 255])
            if leg:
                meshes.append(leg)
        # Crop (food storage)
        crop = self._create_sphere([4.3, 0, 1.0], 0.2, [255, 220, 200, 200], 1)
        meshes.append(crop)
        # Gizzard (grinding organ)
        gizzard = self._create_sphere([4.0, 0, 0.5], 0.25, [200, 100, 100, 200], 1)
        meshes.append(gizzard)
        # Intestines
        intestine = self._create_cylinder([3.8, 0, 0.4], [3.5, 0, 0.2], 0.08, [255, 182, 193, 200])
        if intestine:
            meshes.append(intestine)
        
        # Ground platform
        ground = self._create_box([0, 0, -0.8], [12.0, 4.0, 0.6], [139, 90, 43, 255])
        meshes.append(ground)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "livestock_anatomy.glb")
        meta.update({
            "description": "Livestock digestive systems: cow (ruminant with rumen), goat (smaller ruminant), chicken (crop and gizzard)",
            "curriculum": ["agr_004"],
        })
        return meta

    def generate_farm_tools_3d(self) -> Dict[str, Any]:
        """Traditional Nigerian farm tools: hoe, cutlass, plough, harrow."""
        meshes = []
        
        # HOE (left)
        # Handle
        hoe_handle = self._create_cylinder([-6.0, 0, 0], [-6.0, 0, 2.5], 0.08, self.colors["wood"])
        if hoe_handle:
            meshes.append(hoe_handle)
        # Blade
        hoe_blade = self._create_box([-6.0, 0.3, 0.2], [0.1, 0.6, 0.4], self.colors["metal"])
        meshes.append(hoe_blade)
        
        # CUTLASS/MACHETE (center-left)
        # Handle
        cutlass_handle = self._create_cylinder([-3.0, 0, 0.5], [-3.0, 0, 1.2], 0.08, self.colors["wood"])
        if cutlass_handle:
            meshes.append(cutlass_handle)
        # Blade (curved)
        cutlass_blade = self._create_box([-3.0, 0.5, 0.8], [0.08, 1.0, 0.3], self.colors["metal"])
        meshes.append(cutlass_blade)
        
        # PLOUGH (center-right)
        # Beam (horizontal)
        plough_beam = self._create_cylinder([1.0, 0, 1.0], [2.5, 0, 1.0], 0.12, self.colors["wood"])
        if plough_beam:
            meshes.append(plough_beam)
        # Handles (two vertical)
        plough_handle1 = self._create_cylinder([2.0, -0.4, 1.0], [2.0, -0.4, 2.0], 0.08, self.colors["wood"])
        if plough_handle1:
            meshes.append(plough_handle1)
        plough_handle2 = self._create_cylinder([2.0, 0.4, 1.0], [2.0, 0.4, 2.0], 0.08, self.colors["wood"])
        if plough_handle2:
            meshes.append(plough_handle2)
        # Ploughshare (blade that cuts soil)
        ploughshare = self._create_box([1.2, 0, 0.5], [0.15, 0.8, 0.6], self.colors["metal"])
        meshes.append(ploughshare)
        
        # HARROW (right - toothed frame)
        # Frame (rectangular)
        harrow_frame1 = self._create_cylinder([5.0, -0.8, 0.5], [5.0, 0.8, 0.5], 0.08, self.colors["wood"])
        if harrow_frame1:
            meshes.append(harrow_frame1)
        harrow_frame2 = self._create_cylinder([4.5, -0.8, 0.5], [4.5, 0.8, 0.5], 0.08, self.colors["wood"])
        if harrow_frame2:
            meshes.append(harrow_frame2)
        harrow_frame3 = self._create_cylinder([4.5, -0.8, 0.5], [5.0, -0.8, 0.5], 0.08, self.colors["wood"])
        if harrow_frame3:
            meshes.append(harrow_frame3)
        harrow_frame4 = self._create_cylinder([4.5, 0.8, 0.5], [5.0, 0.8, 0.5], 0.08, self.colors["wood"])
        if harrow_frame4:
            meshes.append(harrow_frame4)
        # Teeth (metal spikes)
        for x in [4.6, 4.75, 4.9]:
            for y in [-0.6, -0.2, 0.2, 0.6]:
                tooth = self._create_cylinder([x, y, 0.5], [x, y, -0.3], 0.05, self.colors["metal"])
                if tooth:
                    meshes.append(tooth)
        
        # Ground base
        ground = self._create_box([0, 0, -0.8], [14.0, 4.0, 0.6], self.colors["topsoil"])
        meshes.append(ground)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "farm_tools_3d.glb")
        meta.update({
            "description": "Traditional Nigerian farm tools: hoe (weeding), cutlass (clearing), plough (tilling), harrow (breaking soil)",
            "curriculum": ["agr_002"],
        })
        return meta

    def generate_irrigation_systems(self) -> Dict[str, Any]:
        """Three irrigation methods: drip, sprinkler, surface."""
        meshes = []
        
        # Ground field
        ground = self._create_box([0, 0, -0.3], [12.0, 8.0, 0.6], self.colors["topsoil"])
        meshes.append(ground)
        
        # DRIP IRRIGATION (left section)
        # Main water line
        main_line = self._create_cylinder([-5.0, -3.0, 0.1], [-5.0, 3.0, 0.1], 0.08, self.colors["pipe"])
        if main_line:
            meshes.append(main_line)
        # Drip lines (lateral)
        for y in [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]:
            drip_line = self._create_cylinder([-5.0, y, 0.1], [-3.5, y, 0.1], 0.04, self.colors["pipe"])
            if drip_line:
                meshes.append(drip_line)
            # Water droplets
            for x in np.arange(-4.8, -3.5, 0.4):
                droplet = self._create_sphere([x, y, 0], 0.05, self.colors["water"], 1)
                meshes.append(droplet)
        # Plants receiving water
        for i in range(6):
            plant = self._create_cylinder([-4.2, -2.5 + i, 0], [-4.2, -2.5 + i, 0.6], 0.06, self.colors["plant_green"])
            if plant:
                meshes.append(plant)
        
        # SPRINKLER IRRIGATION (center section)
        # Sprinkler posts
        for x in [-1.0, 0, 1.0]:
            post = self._create_cylinder([x, 0, 0], [x, 0, 2.0], 0.08, self.colors["metal"])
            if post:
                meshes.append(post)
            # Sprinkler head
            head = self._create_sphere([x, 0, 2.2], 0.15, self.colors["metal"], 1)
            meshes.append(head)
            # Water spray (arc pattern)
            for angle in np.linspace(0, 2 * np.pi, 12):
                spray_x = x + 1.5 * np.cos(angle)
                spray_y = 1.5 * np.sin(angle)
                spray = self._create_cylinder([x, 0, 2.2], [spray_x, spray_y, 1.5], 0.03, self.colors["water"])
                if spray:
                    meshes.append(spray)
        # Crops under sprinklers
        for x in np.arange(-1.5, 1.5, 0.4):
            for y in np.arange(-1.5, 1.5, 0.4):
                crop = self._create_cylinder([x, y, 0], [x, y, 0.5], 0.05, self.colors["plant_green"])
                if crop:
                    meshes.append(crop)
        
        # SURFACE IRRIGATION (right section - furrow)
        # Water channels (furrows)
        for y in [-2.0, -1.0, 0, 1.0, 2.0]:
            furrow = self._create_box([4.5, y, -0.1], [2.0, 0.3, 0.3], self.colors["water"])
            meshes.append(furrow)
            # Ridge with crops
            if y < 2.0:
                ridge_y = y + 0.5
                for x in np.arange(3.5, 5.5, 0.3):
                    crop = self._create_cylinder([x, ridge_y, 0], [x, ridge_y, 0.4], 0.05, self.colors["plant_green"])
                    if crop:
                        meshes.append(crop)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "irrigation_systems.glb")
        meta.update({
            "description": "Three irrigation methods: drip (efficient, targeted), sprinkler (overhead spray), surface (furrow channels)",
            "curriculum": ["agr_003"],
        })
        return meta

    def generate_greenhouse(self) -> Dict[str, Any]:
        """Modern greenhouse structure with plants and climate control."""
        meshes = []
        
        # Ground/floor
        floor = self._create_box([0, 0, -0.2], [8.0, 6.0, 0.4], [100, 100, 100, 255])
        meshes.append(floor)
        
        # Frame structure (metal/wood)
        # Vertical posts (corners and middle)
        for x in [-3.5, 0, 3.5]:
            for y in [-2.5, 2.5]:
                post = self._create_cylinder([x, y, 0], [x, y, 3.5], 0.1, self.colors["frame"])
                if post:
                    meshes.append(post)
        
        # Horizontal beams (top)
        for y in [-2.5, 2.5]:
            beam = self._create_cylinder([-3.5, y, 3.5], [3.5, y, 3.5], 0.1, self.colors["frame"])
            if beam:
                meshes.append(beam)
        for x in [-3.5, 0, 3.5]:
            beam = self._create_cylinder([x, -2.5, 3.5], [x, 2.5, 3.5], 0.1, self.colors["frame"])
            if beam:
                meshes.append(beam)
        
        # Roof (arched/peaked)
        # Peak beam
        peak = self._create_cylinder([-3.5, 0, 4.5], [3.5, 0, 4.5], 0.1, self.colors["frame"])
        if peak:
            meshes.append(peak)
        # Sloped roof supports
        for x in [-3.5, -1.5, 0.5, 2.5]:
            slope1 = self._create_cylinder([x, -2.5, 3.5], [x + 1.0, 0, 4.5], 0.08, self.colors["frame"])
            if slope1:
                meshes.append(slope1)
            slope2 = self._create_cylinder([x + 1.0, 0, 4.5], [x + 1.0, 2.5, 3.5], 0.08, self.colors["frame"])
            if slope2:
                meshes.append(slope2)
        
        # Glass/plastic panels (transparent walls and roof)
        # Side walls
        wall1 = self._create_box([-3.5, 0, 1.75], [0.1, 5.0, 3.5], self.colors["glass"])
        meshes.append(wall1)
        wall2 = self._create_box([3.5, 0, 1.75], [0.1, 5.0, 3.5], self.colors["glass"])
        meshes.append(wall2)
        # End walls
        wall3 = self._create_box([0, -2.5, 1.75], [7.0, 0.1, 3.5], self.colors["glass"])
        meshes.append(wall3)
        wall4 = self._create_box([0, 2.5, 1.75], [7.0, 0.1, 3.5], self.colors["glass"])
        meshes.append(wall4)
        # Roof panels
        roof1 = self._create_box([0, -1.25, 4.0], [7.0, 2.5, 0.1], self.colors["glass"])
        meshes.append(roof1)
        roof2 = self._create_box([0, 1.25, 4.0], [7.0, 2.5, 0.1], self.colors["glass"])
        meshes.append(roof2)
        
        # Plants inside (rows of crops)
        for x in np.arange(-3.0, 3.5, 1.0):
            for y in np.arange(-2.0, 2.5, 0.8):
                # Pot
                pot = self._create_cylinder([x, y, 0], [x, y, 0.3], 0.15, [139, 69, 19, 255])
                if pot:
                    meshes.append(pot)
                # Plant stem
                stem = self._create_cylinder([x, y, 0.3], [x, y, 1.2], 0.05, self.colors["stem"])
                if stem:
                    meshes.append(stem)
                # Leaves
                leaf1 = self._create_box([x, y - 0.3, 0.8], [0.05, 0.5, 0.2], self.colors["leaf"])
                meshes.append(leaf1)
                leaf2 = self._create_box([x, y + 0.3, 1.0], [0.05, 0.4, 0.2], self.colors["leaf"])
                meshes.append(leaf2)
        
        # Ventilation fan (on side wall)
        fan = self._create_sphere([-3.4, 1.5, 2.5], 0.3, [200, 200, 200, 255], 1)
        meshes.append(fan)
        
        # Irrigation pipes overhead
        overhead_pipe = self._create_cylinder([-3.0, 0, 3.0], [3.0, 0, 3.0], 0.06, self.colors["pipe"])
        if overhead_pipe:
            meshes.append(overhead_pipe)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "greenhouse.glb")
        meta.update({
            "description": "Modern greenhouse with transparent walls/roof, metal frame, potted plants, ventilation, and irrigation",
            "curriculum": ["agr_003"],
        })
        return meta

    # ---------- batches ----------
    def generate_all_models(self) -> List[Dict[str, Any]]:
        logger.info("🌾 Generating all agricultural models...")
        models = [
            self.generate_soil_layers(),
            self.generate_crop_growth_stages(),
            self.generate_livestock_anatomy(),
            self.generate_farm_tools_3d(),
            self.generate_irrigation_systems(),
            self.generate_greenhouse(),
        ]
        self.generate_manifest(models)
        logger.info(f"✅ Generated {len(models)} agricultural models")
        return models

    def generate_manifest(self, models: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_size = sum(m.get("size_kb", 0) for m in models)
        manifest = {
            "models": models,
            "total_models": len(models),
            "total_size_kb": round(total_size, 2),
            "curriculum_alignment": {
                "agr_002": "Soil Science and Farm Tools",
                "agr_003": "Crop Production and Irrigation",
                "agr_004": "Livestock Management",
            },
            "nigerian_context": {
                "crops": "Maize, rice (major Nigerian staples)",
                "livestock": "Cow, goat, chicken (common Nigerian livestock)",
                "tools": "Traditional Nigerian farming implements",
                "relevance": "Vocational training for agriculture sector",
            },
            "output_dir": str(self.output_dir),
        }
        path = self.output_dir / "agriculture_manifest.json"
        with open(path, "w") as f:
            json.dump(manifest, f, indent=2)
        return manifest


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description="Agricultural Models Generator")
    parser.add_argument("--model", choices=[
        "all", "soil_layers", "crop_growth_stages", "livestock_anatomy",
        "farm_tools_3d", "irrigation_systems", "greenhouse"
    ], default="all")
    args = parser.parse_args()

    gen = AgricultureModelGenerator()
    if args.model == "all":
        gen.generate_all_models()
        print("📋 Manifest created: agriculture_manifest.json")
    else:
        func = getattr(gen, f"generate_{args.model}")
        meta = func()
        print(f"✅ Generated: {meta['name']}.glb → {meta['size_kb']} KB")
