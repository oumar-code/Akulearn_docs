import json
import logging
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import trimesh

logger = logging.getLogger(__name__)


class EarthSpaceGenerator:
    """Generator for Earth and Space educational models (Priority #9)
    Models:
    - earth_layers.glb: crust, mantle, outer core, inner core with cross-section
    - tectonic_plates.glb: continental and oceanic plates with boundaries
    - volcano.glb: cross-section with magma chamber and eruption
    - water_cycle.glb: evaporation, condensation, precipitation, collection
    - rock_cycle.glb: igneous, sedimentary, metamorphic transformations
    - moon_phases.glb: 8 lunar phases showing illumination
    """

    def __init__(self, output_dir: Path = None) -> None:
        self.output_dir = Path(output_dir or "generated_assets/earth_space")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.colors = {
            "crust": [180, 100, 50, 255],
            "mantle": [220, 150, 80, 255],
            "outer_core": [255, 200, 100, 255],
            "inner_core": [255, 150, 50, 255],
            "water": [50, 100, 200, 255],
            "cloud": [200, 200, 200, 255],
            "rock_igneous": [120, 80, 60, 255],
            "rock_sedimentary": [160, 140, 100, 255],
            "rock_metamorphic": [100, 100, 120, 255],
            "magma": [255, 100, 0, 255],
            "plate": [150, 150, 150, 200],
            "boundary": [255, 0, 0, 255],
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

    def _create_sphere(self, center, radius, color, subdivisions=3):
        """Helper to create colored sphere."""
        sphere = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
        sphere.apply_translation(center)
        sphere.visual.vertex_colors = color
        return sphere

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

    # ---------- models ----------
    def generate_earth_layers(self) -> Dict[str, Any]:
        """Earth cross-section showing crust, mantle, outer core, inner core."""
        meshes = []
        
        # Inner core (solid, very hot)
        inner_core = self._create_sphere([0, 0, 0], 1.0, self.colors["inner_core"], 2)
        meshes.append(inner_core)
        
        # Outer core (liquid iron/nickel)
        outer_core = self._create_sphere([0, 0, 0], 2.2, self.colors["outer_core"], 2)
        meshes.append(outer_core)
        
        # Mantle (hot rock)
        mantle = self._create_sphere([0, 0, 0], 4.0, self.colors["mantle"], 3)
        meshes.append(mantle)
        
        # Crust (thin outer layer)
        crust = self._create_sphere([0, 0, 0], 4.3, self.colors["crust"], 3)
        meshes.append(crust)
        
        # Slice to show cross-section - remove front half
        # Create a cutting plane at x=0
        for mesh in meshes:
            # Get vertices
            vertices = mesh.vertices
            # Find vertices with x > -0.1 (keep back half, remove front)
            mask = vertices[:, 0] < 0.1
            if mask.any():
                # Adjust transparency to show internal structure
                mesh.visual.vertex_colors[:, 3] = 200
        
        # Add labels/zones
        # Crust zone (thin)
        crust_zone = trimesh.creation.box(extents=[0.5, 4.0, 4.0])
        crust_zone.apply_translation([4.15, 0, 0])
        crust_zone.visual.vertex_colors = [200, 100, 50, 50]
        meshes.append(crust_zone)
        
        # Mantle zone
        mantle_zone = trimesh.creation.box(extents=[1.8, 4.0, 4.0])
        mantle_zone.apply_translation([2.6, 0, 0])
        mantle_zone.visual.vertex_colors = [220, 150, 80, 30]
        meshes.append(mantle_zone)
        
        # Layer boundaries (rings for clarity)
        for radius, color in [(1.0, [255, 150, 50, 100]), (2.2, [255, 200, 100, 100]), 
                               (4.0, [220, 150, 80, 100])]:
            ring = trimesh.creation.cylinder(radius=radius, height=0.1, sections=64)
            ring.apply_translation([0, 0, 0])
            ring.visual.vertex_colors = color
            meshes.append(ring)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "earth_layers.glb")
        meta.update({
            "description": "Earth cross-section showing crust, mantle, outer core, and inner core with layer boundaries",
            "curriculum": ["geol_001", "phys_012"],
        })
        return meta

    def generate_tectonic_plates(self) -> Dict[str, Any]:
        """Continental and oceanic tectonic plates with boundaries."""
        meshes = []
        
        # Base sphere (Earth surface)
        earth = self._create_sphere([0, 0, 0], 3.0, [100, 150, 100, 100], 3)
        meshes.append(earth)
        
        # Plate 1 (North American)
        plate1 = trimesh.creation.box(extents=[2.0, 3.5, 0.2])
        plate1.apply_translation([-1.5, 1.0, 3.0])
        plate1.visual.vertex_colors = self.colors["plate"]
        meshes.append(plate1)
        
        # Plate 2 (Eurasian)
        plate2 = trimesh.creation.box(extents=[2.5, 2.0, 0.2])
        plate2.apply_translation([0.5, 2.0, 3.0])
        plate2.visual.vertex_colors = [160, 160, 160, 200]
        meshes.append(plate2)
        
        # Plate 3 (African)
        plate3 = trimesh.creation.box(extents=[1.8, 2.5, 0.2])
        plate3.apply_translation([0, -1.5, 3.0])
        plate3.visual.vertex_colors = [140, 140, 140, 200]
        meshes.append(plate3)
        
        # Plate 4 (Pacific)
        plate4 = trimesh.creation.box(extents=[2.2, 2.0, 0.2])
        plate4.apply_translation([-3.0, 0, 3.0])
        plate4.visual.vertex_colors = [150, 150, 150, 200]
        meshes.append(plate4)
        
        # Convergent boundary (collision) - red zones
        boundary1 = trimesh.creation.box(extents=[0.15, 1.5, 0.3])
        boundary1.apply_translation([-0.5, 2.5, 3.1])
        boundary1.visual.vertex_colors = self.colors["boundary"]
        meshes.append(boundary1)
        
        # Divergent boundary (spreading) - red zones
        boundary2 = trimesh.creation.box(extents=[0.15, 2.0, 0.3])
        boundary2.apply_translation([0.3, 0, 3.1])
        boundary2.visual.vertex_colors = self.colors["boundary"]
        meshes.append(boundary2)
        
        # Transform boundary (sliding)
        boundary3 = trimesh.creation.box(extents=[0.15, 1.0, 0.3])
        boundary3.apply_translation([-2.5, -0.5, 3.1])
        boundary3.visual.vertex_colors = self.colors["boundary"]
        meshes.append(boundary3)
        
        # Mountain range indication
        mountain = trimesh.creation.cylinder(radius=0.3, height=0.8, sections=16)
        mountain.apply_translation([-0.5, 2.5, 3.4])
        mountain.visual.vertex_colors = [100, 100, 100, 255]
        meshes.append(mountain)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "tectonic_plates.glb")
        meta.update({
            "description": "Tectonic plates showing continental/oceanic boundaries, collision zones, spreading centers, and transform faults",
            "curriculum": ["geol_002"],
        })
        return meta

    def generate_volcano(self) -> Dict[str, Any]:
        """Volcano cross-section with magma chamber and eruption cone."""
        meshes = []
        
        # Base plate
        base = trimesh.creation.box(extents=[6.0, 6.0, 0.5])
        base.apply_translation([0, 0, -0.5])
        base.visual.vertex_colors = self.colors["crust"]
        meshes.append(base)
        
        # Magma chamber (beneath surface)
        chamber = self._create_sphere([0, 0, -2.0], 1.2, self.colors["magma"], 2)
        meshes.append(chamber)
        
        # Volcanic pipe (conduit from chamber to surface)
        pipe = self._create_cylinder([0, 0, -2.0], [0, 0, 1.5], 0.35, self.colors["magma"])
        if pipe:
            meshes.append(pipe)
        
        # Volcanic cone (mountain shape)
        cone = trimesh.creation.cone(radius=2.0, height=3.0, sections=32)
        cone.apply_translation([0, 0, 1.5])
        cone.visual.vertex_colors = [100, 80, 60, 255]
        meshes.append(cone)
        
        # Crater (top opening)
        crater = trimesh.creation.cylinder(radius=0.6, height=0.3, sections=32)
        crater.apply_translation([0, 0, 3.0])
        crater.visual.vertex_colors = [50, 30, 20, 255]
        meshes.append(crater)
        
        # Lava flow
        lava1 = trimesh.creation.cylinder(radius=0.3, height=2.0, sections=16)
        lava1.apply_transform(trimesh.transformations.rotation_matrix(np.radians(20), [0, 1, 0]))
        lava1.apply_translation([1.2, 0, 0.5])
        lava1.visual.vertex_colors = self.colors["magma"]
        meshes.append(lava1)
        
        lava2 = trimesh.creation.cylinder(radius=0.3, height=2.0, sections=16)
        lava2.apply_transform(trimesh.transformations.rotation_matrix(np.radians(-20), [0, 1, 0]))
        lava2.apply_translation([-1.2, 0, 0.5])
        lava2.visual.vertex_colors = self.colors["magma"]
        meshes.append(lava2)
        
        # Eruption plume (ash column)
        plume1 = self._create_sphere([0, 0, 3.5], 0.8, self.colors["cloud"], 2)
        meshes.append(plume1)
        plume2 = self._create_sphere([0.2, 0.2, 4.2], 0.6, self.colors["cloud"], 2)
        meshes.append(plume2)
        plume3 = self._create_sphere([-0.2, -0.2, 4.8], 0.5, self.colors["cloud"], 2)
        meshes.append(plume3)
        
        # Section cut (show internal structure)
        section = trimesh.creation.box(extents=[0.2, 6.0, 4.0])
        section.apply_translation([0, 0, 0])
        section.visual.vertex_colors = [0, 0, 0, 0]  # Transparent
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "volcano.glb")
        meta.update({
            "description": "Volcano cross-section showing magma chamber, pipe, eruption cone, lava flows, and ash plume",
            "curriculum": ["geol_003"],
        })
        return meta

    def generate_water_cycle(self) -> Dict[str, Any]:
        """Water cycle showing evaporation, condensation, precipitation, collection."""
        meshes = []
        
        # Ground/Ocean
        ground = trimesh.creation.box(extents=[8.0, 1.0, 0.5])
        ground.apply_translation([0, -0.5, -0.5])
        ground.visual.vertex_colors = [100, 100, 100, 255]
        meshes.append(ground)
        
        # Water body
        water = trimesh.creation.box(extents=[4.0, 0.8, 0.3])
        water.apply_translation([-2.0, -0.5, 0])
        water.visual.vertex_colors = self.colors["water"]
        meshes.append(water)
        
        # Mountains
        mountain1 = trimesh.creation.cone(radius=1.2, height=3.0, sections=32)
        mountain1.apply_translation([2.5, 0, 1.5])
        mountain1.visual.vertex_colors = [120, 100, 80, 255]
        meshes.append(mountain1)
        
        mountain2 = trimesh.creation.cone(radius=1.0, height=2.5, sections=32)
        mountain2.apply_translation([4.0, 0, 1.25])
        mountain2.visual.vertex_colors = [130, 110, 90, 255]
        meshes.append(mountain2)
        
        # Sun (evaporation source)
        sun = self._create_sphere([-3.0, 4.0, 0], 0.8, [255, 255, 0, 255], 2)
        meshes.append(sun)
        
        # Evaporation arrows (water vapor rising)
        for i in range(3):
            x = -3.0 + i * 0.5
            arrow_cyl = self._create_cylinder([x, 1.0, 0], [x, 2.5, 0], 0.08, [100, 200, 255, 150])
            if arrow_cyl:
                meshes.append(arrow_cyl)
        
        # Clouds (condensation)
        cloud1 = self._create_sphere([-1.0, 3.5, 0], 0.6, self.colors["cloud"], 2)
        meshes.append(cloud1)
        cloud2 = self._create_sphere([0.2, 3.6, 0], 0.5, self.colors["cloud"], 2)
        meshes.append(cloud2)
        cloud3 = self._create_sphere([-0.4, 3.8, 0], 0.4, self.colors["cloud"], 2)
        meshes.append(cloud3)
        
        cloud4 = self._create_sphere([3.0, 3.3, 0], 0.7, self.colors["cloud"], 2)
        meshes.append(cloud4)
        cloud5 = self._create_sphere([3.8, 3.4, 0], 0.6, self.colors["cloud"], 2)
        meshes.append(cloud5)
        
        # Precipitation (rain)
        for i in range(8):
            x = 2.5 + i * 0.3
            rain = self._create_cylinder([x, 3.0, 0], [x, 2.0, 0], 0.05, [50, 100, 200, 200])
            if rain:
                meshes.append(rain)
        
        # Collection/Runoff arrows
        for i in range(2):
            x = 3.0 + i * 0.4
            runoff = self._create_cylinder([x, 1.0, 0], [x - 1.0, 0.5, 0], 0.08, [50, 100, 200, 150])
            if runoff:
                meshes.append(runoff)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "water_cycle.glb")
        meta.update({
            "description": "Water cycle showing sun, evaporation, condensation in clouds, precipitation, and collection in ocean",
            "curriculum": ["geog_001", "env_001"],
        })
        return meta

    def generate_rock_cycle(self) -> Dict[str, Any]:
        """Rock cycle showing transformations between igneous, sedimentary, metamorphic."""
        meshes = []
        
        # Igneous rock (formed from magma/lava)
        igneous = trimesh.creation.box(extents=[1.2, 1.2, 0.8])
        igneous.apply_translation([-2.5, 1.5, 0])
        igneous.visual.vertex_colors = self.colors["rock_igneous"]
        meshes.append(igneous)
        
        # Weathering/Erosion arrow to sediment
        arrow1 = self._create_cylinder([-2.5, 0.8, 0], [-1.5, 0.2, 0], 0.12, [255, 100, 0, 200])
        if arrow1:
            meshes.append(arrow1)
        
        # Sedimentary rock (compacted sediment)
        sedimentary = trimesh.creation.box(extents=[1.2, 1.2, 0.8])
        sedimentary.apply_translation([-0.5, -1.0, 0])
        sedimentary.visual.vertex_colors = self.colors["rock_sedimentary"]
        meshes.append(sedimentary)
        
        # Heat/Pressure arrow to metamorphic
        arrow2 = self._create_cylinder([0.5, -0.5, 0], [1.5, 0.5, 0], 0.12, [255, 150, 0, 200])
        if arrow2:
            meshes.append(arrow2)
        
        # Metamorphic rock (heated/pressurized)
        metamorphic = trimesh.creation.box(extents=[1.2, 1.2, 0.8])
        metamorphic.apply_translation([2.5, 1.5, 0])
        metamorphic.visual.vertex_colors = self.colors["rock_metamorphic"]
        meshes.append(metamorphic)
        
        # Melting arrow back to igneous
        arrow3 = self._create_cylinder([2.0, 2.2, 0], [-2.0, 2.2, 0], 0.12, [255, 200, 0, 200])
        if arrow3:
            meshes.append(arrow3)
        
        # Heat source indicator
        heat = self._create_sphere([3.5, 2.8, 0], 0.4, [255, 100, 0, 255], 2)
        meshes.append(heat)
        
        # Magma chamber (bottom)
        magma_chamber = self._create_sphere([-2.5, -2.5, 0], 0.8, self.colors["magma"], 2)
        meshes.append(magma_chamber)
        
        # Uplift/Exhumation label indicator
        uplift = trimesh.creation.cylinder(radius=0.3, height=2.0, sections=16)
        uplift.apply_translation([2.5, -1.0, 0])
        uplift.visual.vertex_colors = [200, 100, 100, 150]
        meshes.append(uplift)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "rock_cycle.glb")
        meta.update({
            "description": "Rock cycle showing transformations between igneous, sedimentary, and metamorphic rocks with processes",
            "curriculum": ["geol_004"],
        })
        return meta

    def generate_moon_phases(self) -> Dict[str, Any]:
        """Eight lunar phases showing illumination from Sun."""
        meshes = []
        
        # Sun position (far left)
        sun = self._create_sphere([-7.0, 0, 0], 0.6, [255, 255, 0, 255], 2)
        meshes.append(sun)
        
        # Phase spacing
        phase_x = [-5.0, -3.0, -1.0, 1.0, 3.0, 5.0, 7.0, 9.0]
        phase_names = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
                       "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]
        
        for i, x_pos in enumerate(phase_x):
            # Moon sphere
            moon = self._create_sphere([x_pos, 0, 0], 0.4, [200, 200, 200, 255], 2)
            meshes.append(moon)
            
            # Illuminated side indicator (sphere showing lit portion)
            # Calculate illumination based on phase
            illumination_fraction = (i + 1) / 8.0
            if i <= 3:  # Waxing phases
                ill_color = [255, 255, 100, 200]
            else:  # Waning phases
                ill_color = [255, 200, 100, 200]
            
            illum = self._create_sphere([x_pos + 0.15, 0, 0.2], 0.35, ill_color, 2)
            meshes.append(illum)
            
            # Shadow (dark side)
            shadow = self._create_sphere([x_pos - 0.15, 0, 0.2], 0.35, [50, 50, 50, 200], 2)
            meshes.append(shadow)
        
        # Orbital path
        angles = np.linspace(0, 2 * np.pi, 100)
        for j in range(len(angles) - 1):
            x1 = 2.0 * np.cos(angles[j])
            x2 = 2.0 * np.cos(angles[j + 1])
            line = self._create_cylinder([x1, 1.0, -0.5], [x2, 1.0, -0.5], 0.05, [100, 100, 100, 100])
            if line:
                meshes.append(line)
        
        # Earth position
        earth = self._create_sphere([0, 0, 0], 0.3, [50, 100, 200, 255], 2)
        meshes.append(earth)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "moon_phases.glb")
        meta.update({
            "description": "Eight lunar phases showing illumination from Sun's perspective: new, waxing, full, waning",
            "curriculum": ["astro_001"],
        })
        return meta

    # ---------- batches ----------
    def generate_all_models(self) -> List[Dict[str, Any]]:
        logger.info("🌍 Generating all earth and space models...")
        models = [
            self.generate_earth_layers(),
            self.generate_tectonic_plates(),
            self.generate_volcano(),
            self.generate_water_cycle(),
            self.generate_rock_cycle(),
            self.generate_moon_phases(),
        ]
        self.generate_manifest(models)
        logger.info(f"✅ Generated {len(models)} earth and space models")
        return models

    def generate_manifest(self, models: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_size = sum(m.get("size_kb", 0) for m in models)
        manifest = {
            "models": models,
            "total_models": len(models),
            "total_size_kb": round(total_size, 2),
            "curriculum_alignment": {
                "geol_001": "Earth Structure and Layers",
                "geol_002": "Plate Tectonics",
                "geol_003": "Volcanism and Earthquakes",
                "geol_004": "Rock Cycle",
                "geog_001": "Water Cycle and Weather",
                "astro_001": "Lunar Phases",
                "env_001": "Environmental Processes",
                "phys_012": "Planetary Science",
            },
            "output_dir": str(self.output_dir),
        }
        path = self.output_dir / "earth_space_manifest.json"
        with open(path, "w") as f:
            json.dump(manifest, f, indent=2)
        return manifest


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description="Earth and Space Models Generator")
    parser.add_argument("--model", choices=[
        "all", "earth_layers", "tectonic_plates", "volcano",
        "water_cycle", "rock_cycle", "moon_phases"
    ], default="all")
    args = parser.parse_args()

    gen = EarthSpaceGenerator()
    if args.model == "all":
        gen.generate_all_models()
        print("📋 Manifest created: earth_space_manifest.json")
    else:
        func = getattr(gen, f"generate_{args.model}")
        meta = func()
        print(f"✅ Generated: {meta['name']}.glb → {meta['size_kb']} KB")
