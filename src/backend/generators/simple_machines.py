import json
import logging
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import trimesh

logger = logging.getLogger(__name__)


class SimpleMachinesGenerator:
    """Generator for Simple Machines educational models (Priority #8)
    Models:
    - lever_types.glb: first, second, third class levers with force vectors
    - pulley_systems.glb: fixed, movable, compound pulleys
    - inclined_plane.glb: ramp with force components
    - wheel_and_axle.glb: complete mechanism with mechanical advantage
    - wedge_screw.glb: wedge and screw demonstrations
    - gear_systems.glb: simple gear trains showing motion transfer
    """

    def __init__(self, output_dir: Path = None) -> None:
        self.output_dir = Path(output_dir or "generated_assets/simple_machines")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.colors = {
            "fulcrum": [100, 100, 100, 255],
            "lever_bar": [150, 100, 50, 255],
            "load": [200, 50, 50, 255],
            "effort": [50, 100, 200, 255],
            "force_arrow": [255, 0, 0, 255],
            "rope": [139, 90, 43, 255],
            "pulley": [150, 150, 150, 255],
            "plane": [100, 150, 100, 255],
            "wheel": [80, 80, 80, 255],
            "axle": [50, 50, 50, 255],
            "wedge": [200, 150, 100, 255],
            "screw": [100, 100, 150, 255],
            "gear": [180, 180, 180, 255],
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

    def _create_arrow(self, start, end, color, radius=0.1):
        """Create arrow for force vector visualization."""
        vec = np.array(end) - np.array(start)
        length = np.linalg.norm(vec)
        if length < 1e-6:
            return None
        direction = vec / length
        
        # Shaft
        shaft = trimesh.creation.cylinder(radius=radius, height=length * 0.7, sections=16)
        z_axis = np.array([0, 0, 1])
        axis = np.cross(z_axis, direction)
        if np.linalg.norm(axis) > 1e-6:
            angle = np.arccos(np.clip(np.dot(z_axis, direction), -1.0, 1.0))
            R = trimesh.transformations.rotation_matrix(angle, axis)
            shaft.apply_transform(R)
        shaft.apply_translation(start + direction * (length * 0.35))
        shaft.visual.vertex_colors = color
        
        # Cone head
        cone = trimesh.creation.cone(radius=radius * 2.5, height=length * 0.3, sections=16)
        cone.apply_translation([0, 0, length * 0.15])
        if np.linalg.norm(axis) > 1e-6:
            cone.apply_transform(R)
        cone.apply_translation(start + direction * (length * 0.85))
        cone.visual.vertex_colors = color
        
        return trimesh.util.concatenate([shaft, cone])

    def _create_cylinder(self, start, end, radius, color, sections=16):
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

    def _create_box(self, center, extents, color):
        """Helper to create colored box."""
        box = trimesh.creation.box(extents=extents)
        box.apply_translation(center)
        box.visual.vertex_colors = color
        return box

    def _create_sphere(self, center, radius, color, subdivisions=2):
        """Helper to create colored sphere."""
        sphere = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
        sphere.apply_translation(center)
        sphere.visual.vertex_colors = color
        return sphere

    # ---------- models ----------
    def generate_lever_types(self) -> Dict[str, Any]:
        """Three types of levers with fulcrum, load, effort visualization."""
        meshes = []
        spacing = 5.0
        
        # First class lever (fulcrum in middle)
        # Lever bar
        bar1 = self._create_box([0, 0, 0], [4.0, 0.3, 0.3], self.colors["lever_bar"])
        meshes.append(bar1)
        # Fulcrum (triangle)
        fulcrum1 = trimesh.creation.cone(radius=0.4, height=0.8, sections=3)
        fulcrum1.apply_translation([0, 0, -0.6])
        fulcrum1.visual.vertex_colors = self.colors["fulcrum"]
        meshes.append(fulcrum1)
        # Load (left)
        load1 = self._create_box([-1.5, 0, 0.5], [0.5, 0.5, 0.5], self.colors["load"])
        meshes.append(load1)
        # Effort (right)
        effort1 = self._create_box([1.5, 0, 0.5], [0.5, 0.5, 0.5], self.colors["effort"])
        meshes.append(effort1)
        # Force arrows
        load_arrow1 = self._create_arrow([-1.5, 0, 0.5], [-1.5, 0, -1.0], self.colors["force_arrow"], 0.08)
        effort_arrow1 = self._create_arrow([1.5, 0, 1.5], [1.5, 0, 0.5], self.colors["force_arrow"], 0.08)
        if load_arrow1:
            meshes.append(load_arrow1)
        if effort_arrow1:
            meshes.append(effort_arrow1)
        
        # Second class lever (load in middle)
        # Lever bar
        bar2 = self._create_box([spacing, 0, 0], [4.0, 0.3, 0.3], self.colors["lever_bar"])
        meshes.append(bar2)
        # Fulcrum (left end)
        fulcrum2 = trimesh.creation.cone(radius=0.4, height=0.8, sections=3)
        fulcrum2.apply_translation([spacing - 2.0, 0, -0.6])
        fulcrum2.visual.vertex_colors = self.colors["fulcrum"]
        meshes.append(fulcrum2)
        # Load (middle)
        load2 = self._create_box([spacing, 0, 0.5], [0.5, 0.5, 0.5], self.colors["load"])
        meshes.append(load2)
        # Effort (right end)
        effort2 = self._create_box([spacing + 2.0, 0, 0.5], [0.5, 0.5, 0.5], self.colors["effort"])
        meshes.append(effort2)
        # Force arrows
        load_arrow2 = self._create_arrow([spacing, 0, 0.5], [spacing, 0, -1.0], self.colors["force_arrow"], 0.08)
        effort_arrow2 = self._create_arrow([spacing + 2.0, 0, 1.5], [spacing + 2.0, 0, 0.5], self.colors["force_arrow"], 0.08)
        if load_arrow2:
            meshes.append(load_arrow2)
        if effort_arrow2:
            meshes.append(effort_arrow2)
        
        # Third class lever (effort in middle)
        # Lever bar
        bar3 = self._create_box([spacing * 2, 0, 0], [4.0, 0.3, 0.3], self.colors["lever_bar"])
        meshes.append(bar3)
        # Fulcrum (left end)
        fulcrum3 = trimesh.creation.cone(radius=0.4, height=0.8, sections=3)
        fulcrum3.apply_translation([spacing * 2 - 2.0, 0, -0.6])
        fulcrum3.visual.vertex_colors = self.colors["fulcrum"]
        meshes.append(fulcrum3)
        # Effort (middle)
        effort3 = self._create_box([spacing * 2, 0, 0.5], [0.5, 0.5, 0.5], self.colors["effort"])
        meshes.append(effort3)
        # Load (right end)
        load3 = self._create_box([spacing * 2 + 2.0, 0, 0.5], [0.5, 0.5, 0.5], self.colors["load"])
        meshes.append(load3)
        # Force arrows
        effort_arrow3 = self._create_arrow([spacing * 2, 0, 1.5], [spacing * 2, 0, 0.5], self.colors["force_arrow"], 0.08)
        load_arrow3 = self._create_arrow([spacing * 2 + 2.0, 0, 0.5], [spacing * 2 + 2.0, 0, -1.0], self.colors["force_arrow"], 0.08)
        if effort_arrow3:
            meshes.append(effort_arrow3)
        if load_arrow3:
            meshes.append(load_arrow3)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "lever_types.glb")
        meta.update({
            "description": "Three classes of levers: first (fulcrum middle), second (load middle), third (effort middle) with force vectors",
            "curriculum": ["phy_004"],
        })
        return meta

    def generate_pulley_systems(self) -> Dict[str, Any]:
        """Fixed, movable, and compound pulley systems."""
        meshes = []
        spacing = 4.0
        
        # Fixed pulley (left)
        # Support beam
        beam1 = self._create_box([0, 0, 3.0], [0.3, 0.3, 1.0], self.colors["fulcrum"])
        meshes.append(beam1)
        # Pulley wheel
        pulley1 = trimesh.creation.cylinder(radius=0.8, height=0.2, sections=32)
        pulley1.apply_translation([0, 0, 2.5])
        pulley1.visual.vertex_colors = self.colors["pulley"]
        meshes.append(pulley1)
        # Rope
        rope1a = self._create_cylinder([0.8, 0, 2.5], [0.8, 0, 0.5], 0.05, self.colors["rope"])
        rope1b = self._create_cylinder([-0.8, 0, 2.5], [-0.8, 0, 1.0], 0.05, self.colors["rope"])
        if rope1a:
            meshes.append(rope1a)
        if rope1b:
            meshes.append(rope1b)
        # Load
        load1 = self._create_box([0.8, 0, 0.3], [0.5, 0.5, 0.5], self.colors["load"])
        meshes.append(load1)
        # Effort indicator
        effort1 = self._create_box([-0.8, 0, 0.8], [0.3, 0.3, 0.3], self.colors["effort"])
        meshes.append(effort1)
        
        # Movable pulley (middle)
        # Support beam
        beam2 = self._create_box([spacing, 0, 3.0], [0.3, 0.3, 1.0], self.colors["fulcrum"])
        meshes.append(beam2)
        # Upper pulley (fixed)
        pulley2a = trimesh.creation.cylinder(radius=0.6, height=0.2, sections=32)
        pulley2a.apply_translation([spacing, 0, 2.5])
        pulley2a.visual.vertex_colors = self.colors["pulley"]
        meshes.append(pulley2a)
        # Lower pulley (movable)
        pulley2b = trimesh.creation.cylinder(radius=0.6, height=0.2, sections=32)
        pulley2b.apply_translation([spacing, 0, 1.5])
        pulley2b.visual.vertex_colors = self.colors["pulley"]
        meshes.append(pulley2b)
        # Rope
        rope2a = self._create_cylinder([spacing - 0.6, 0, 2.5], [spacing - 0.6, 0, 1.5], 0.05, self.colors["rope"])
        rope2b = self._create_cylinder([spacing + 0.6, 0, 2.5], [spacing + 0.6, 0, 0.5], 0.05, self.colors["rope"])
        if rope2a:
            meshes.append(rope2a)
        if rope2b:
            meshes.append(rope2b)
        # Load
        load2 = self._create_box([spacing, 0, 1.0], [0.5, 0.5, 0.5], self.colors["load"])
        meshes.append(load2)
        # Effort indicator
        effort2 = self._create_box([spacing + 0.6, 0, 0.3], [0.3, 0.3, 0.3], self.colors["effort"])
        meshes.append(effort2)
        
        # Compound pulley (right)
        # Support beam
        beam3 = self._create_box([spacing * 2, 0, 3.0], [0.3, 0.3, 1.0], self.colors["fulcrum"])
        meshes.append(beam3)
        # Upper pulley
        pulley3a = trimesh.creation.cylinder(radius=0.5, height=0.2, sections=32)
        pulley3a.apply_translation([spacing * 2, 0, 2.5])
        pulley3a.visual.vertex_colors = self.colors["pulley"]
        meshes.append(pulley3a)
        # Middle pulley
        pulley3b = trimesh.creation.cylinder(radius=0.5, height=0.2, sections=32)
        pulley3b.apply_translation([spacing * 2, 0, 1.8])
        pulley3b.visual.vertex_colors = self.colors["pulley"]
        meshes.append(pulley3b)
        # Lower pulley
        pulley3c = trimesh.creation.cylinder(radius=0.5, height=0.2, sections=32)
        pulley3c.apply_translation([spacing * 2, 0, 1.1])
        pulley3c.visual.vertex_colors = self.colors["pulley"]
        meshes.append(pulley3c)
        # Rope segments
        rope3a = self._create_cylinder([spacing * 2 - 0.5, 0, 2.5], [spacing * 2 - 0.5, 0, 1.8], 0.05, self.colors["rope"])
        rope3b = self._create_cylinder([spacing * 2 + 0.5, 0, 1.8], [spacing * 2 + 0.5, 0, 1.1], 0.05, self.colors["rope"])
        if rope3a:
            meshes.append(rope3a)
        if rope3b:
            meshes.append(rope3b)
        # Load
        load3 = self._create_box([spacing * 2, 0, 0.6], [0.5, 0.5, 0.5], self.colors["load"])
        meshes.append(load3)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "pulley_systems.glb")
        meta.update({
            "description": "Three pulley systems: fixed pulley (left), movable pulley (middle), compound pulley (right) showing mechanical advantage",
            "curriculum": ["phy_004"],
        })
        return meta

    def generate_inclined_plane(self) -> Dict[str, Any]:
        """Inclined plane with force components and mechanical advantage."""
        meshes = []
        
        # Inclined plane
        plane = trimesh.creation.box(extents=[6.0, 3.0, 0.3])
        # Rotate to create incline (30 degrees)
        angle = np.radians(30)
        R = trimesh.transformations.rotation_matrix(angle, [0, 1, 0])
        plane.apply_transform(R)
        plane.apply_translation([0, 0, 1.5])
        plane.visual.vertex_colors = self.colors["plane"]
        meshes.append(plane)
        
        # Ground
        ground = self._create_box([0, 0, -0.2], [8.0, 3.0, 0.3], [100, 80, 60, 255])
        meshes.append(ground)
        
        # Object on incline
        obj_pos = [-1.5, 0, 2.5]
        obj = self._create_box(obj_pos, [0.8, 0.8, 0.8], self.colors["load"])
        meshes.append(obj)
        
        # Force vectors
        # Weight (downward)
        weight_arrow = self._create_arrow(obj_pos, [obj_pos[0], obj_pos[1], obj_pos[2] - 2.0], [255, 0, 0, 255], 0.1)
        if weight_arrow:
            meshes.append(weight_arrow)
        
        # Normal force (perpendicular to plane)
        normal_arrow = self._create_arrow(obj_pos, [obj_pos[0] + 1.0, obj_pos[1], obj_pos[2] + 1.2], [0, 255, 0, 255], 0.1)
        if normal_arrow:
            meshes.append(normal_arrow)
        
        # Parallel component (along plane)
        parallel_arrow = self._create_arrow(obj_pos, [obj_pos[0] - 1.5, obj_pos[1], obj_pos[2] - 0.8], [0, 0, 255, 255], 0.1)
        if parallel_arrow:
            meshes.append(parallel_arrow)
        
        # Support structures
        support1 = self._create_box([2.5, 0, 0.8], [0.3, 3.0, 1.6], self.colors["fulcrum"])
        meshes.append(support1)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "inclined_plane.glb")
        meta.update({
            "description": "Inclined plane with object showing weight, normal force, and parallel force components",
            "curriculum": ["phy_004"],
        })
        return meta

    def generate_wheel_and_axle(self) -> Dict[str, Any]:
        """Wheel and axle mechanism demonstrating mechanical advantage."""
        meshes = []
        
        # Axle (central cylinder)
        axle = trimesh.creation.cylinder(radius=0.3, height=3.0, sections=32)
        axle.apply_translation([0, 0, 0])
        axle.visual.vertex_colors = self.colors["axle"]
        meshes.append(axle)
        
        # Large wheel on left
        wheel1 = trimesh.creation.cylinder(radius=2.0, height=0.3, sections=64)
        wheel1.apply_translation([0, 0, -1.2])
        wheel1.visual.vertex_colors = self.colors["wheel"]
        meshes.append(wheel1)
        
        # Spokes for large wheel
        for i in range(8):
            angle = 2 * np.pi * i / 8
            x = 1.0 * np.cos(angle)
            y = 1.0 * np.sin(angle)
            spoke = self._create_cylinder([0, 0, -1.2], [x, y, -1.2], 0.08, [100, 100, 100, 255])
            if spoke:
                meshes.append(spoke)
        
        # Small wheel on right
        wheel2 = trimesh.creation.cylinder(radius=1.2, height=0.3, sections=64)
        wheel2.apply_translation([0, 0, 1.2])
        wheel2.visual.vertex_colors = self.colors["wheel"]
        meshes.append(wheel2)
        
        # Spokes for small wheel
        for i in range(6):
            angle = 2 * np.pi * i / 6
            x = 0.6 * np.cos(angle)
            y = 0.6 * np.sin(angle)
            spoke = self._create_cylinder([0, 0, 1.2], [x, y, 1.2], 0.08, [100, 100, 100, 255])
            if spoke:
                meshes.append(spoke)
        
        # Handle on large wheel
        handle = self._create_cylinder([2.0, 0, -1.2], [2.5, 0, -1.2], 0.12, self.colors["effort"])
        if handle:
            meshes.append(handle)
        handle_grip = self._create_sphere([2.5, 0, -1.2], 0.2, self.colors["effort"], 2)
        meshes.append(handle_grip)
        
        # Load rope on small wheel
        rope = self._create_cylinder([0, -1.2, 1.2], [0, -1.2, -1.5], 0.08, self.colors["rope"])
        if rope:
            meshes.append(rope)
        
        # Load weight
        load = self._create_box([0, -1.2, -2.0], [0.6, 0.6, 0.8], self.colors["load"])
        meshes.append(load)
        
        # Support frame
        support1 = self._create_box([0, 0, -2.0], [0.2, 3.0, 0.2], self.colors["fulcrum"])
        support2 = self._create_box([0, 1.5, -1.0], [0.2, 0.2, 2.0], self.colors["fulcrum"])
        support3 = self._create_box([0, -1.5, -1.0], [0.2, 0.2, 2.0], self.colors["fulcrum"])
        meshes.extend([support1, support2, support3])
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "wheel_and_axle.glb")
        meta.update({
            "description": "Wheel and axle mechanism with large wheel, small axle, handle, and load demonstrating mechanical advantage",
            "curriculum": ["phy_004"],
        })
        return meta

    def generate_wedge_screw(self) -> Dict[str, Any]:
        """Wedge and screw demonstrations showing force multiplication."""
        meshes = []
        
        # Wedge (left side)
        # Base block to split
        block = self._create_box([-3.0, 0, 0.5], [2.0, 1.5, 1.0], [150, 120, 90, 255])
        meshes.append(block)
        
        # Wedge shape (triangular prism)
        wedge_vertices = np.array([
            [-3.0, -0.8, 0.0], [-3.0, 0.8, 0.0],  # base back
            [-3.0, -0.8, 1.0], [-3.0, 0.8, 1.0],  # base front
            [-4.5, 0.0, 0.0], [-4.5, 0.0, 1.0],   # tip
        ])
        wedge_faces = np.array([
            [0, 1, 3], [0, 3, 2],  # base
            [4, 0, 2], [4, 2, 5],  # left side
            [1, 4, 5], [1, 5, 3],  # right side
            [0, 4, 1],  # back
            [2, 3, 5],  # front
        ])
        wedge = trimesh.Trimesh(vertices=wedge_vertices, faces=wedge_faces)
        wedge.visual.vertex_colors = self.colors["wedge"]
        meshes.append(wedge)
        
        # Force arrow on wedge
        wedge_force = self._create_arrow([-4.5, 0, 0.5], [-3.5, 0, 0.5], self.colors["effort"], 0.08)
        if wedge_force:
            meshes.append(wedge_force)
        
        # Screw (right side)
        # Screw shaft
        shaft = trimesh.creation.cylinder(radius=0.3, height=3.5, sections=32)
        shaft.apply_translation([3.0, 0, 1.75])
        shaft.visual.vertex_colors = self.colors["screw"]
        meshes.append(shaft)
        
        # Screw threads (helical ridges)
        num_threads = 12
        for i in range(num_threads):
            angle = 2 * np.pi * i / 4  # 3 full rotations
            z = 0.2 + i * 0.28
            x = 3.0 + 0.5 * np.cos(angle)
            y = 0.5 * np.sin(angle)
            thread = trimesh.creation.cylinder(radius=0.15, height=0.15, sections=16)
            R = trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0])
            thread.apply_transform(R)
            thread.apply_translation([x, y, z])
            thread.visual.vertex_colors = [120, 120, 180, 255]
            meshes.append(thread)
        
        # Screw head
        head = trimesh.creation.cylinder(radius=0.6, height=0.3, sections=32)
        head.apply_translation([3.0, 0, 3.6])
        head.visual.vertex_colors = [80, 80, 120, 255]
        meshes.append(head)
        
        # Wood block being screwed
        wood = self._create_box([3.0, 0, 0.5], [2.0, 2.0, 1.0], [150, 120, 90, 255])
        meshes.append(wood)
        
        # Base platform
        platform = self._create_box([0, 0, -0.3], [10.0, 3.0, 0.3], [100, 80, 60, 255])
        meshes.append(platform)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "wedge_screw.glb")
        meta.update({
            "description": "Wedge (left) splitting block and screw (right) with helical threads showing inclined plane principle",
            "curriculum": ["phy_004"],
        })
        return meta

    def generate_gear_systems(self) -> Dict[str, Any]:
        """Simple gear train showing motion and force transfer."""
        meshes = []
        
        # Base plate
        base = self._create_box([0, 0, -0.3], [8.0, 4.0, 0.3], [80, 80, 80, 255])
        meshes.append(base)
        
        # First gear (large, driver)
        gear1 = trimesh.creation.cylinder(radius=1.5, height=0.4, sections=32)
        gear1.apply_translation([-2.5, 0, 0.2])
        gear1.visual.vertex_colors = self.colors["gear"]
        meshes.append(gear1)
        
        # Gear teeth for first gear
        for i in range(16):
            angle = 2 * np.pi * i / 16
            x = -2.5 + 1.7 * np.cos(angle)
            y = 1.7 * np.sin(angle)
            tooth = trimesh.creation.box(extents=[0.2, 0.3, 0.5])
            tooth.apply_translation([x, y, 0.2])
            tooth.visual.vertex_colors = [160, 160, 160, 255]
            meshes.append(tooth)
        
        # Second gear (small, driven)
        gear2 = trimesh.creation.cylinder(radius=0.8, height=0.4, sections=32)
        gear2.apply_translation([0, 0, 0.2])
        gear2.visual.vertex_colors = self.colors["gear"]
        meshes.append(gear2)
        
        # Gear teeth for second gear
        for i in range(10):
            angle = 2 * np.pi * i / 10
            x = 1.0 * np.cos(angle)
            y = 1.0 * np.sin(angle)
            tooth = trimesh.creation.box(extents=[0.15, 0.25, 0.5])
            tooth.apply_translation([x, y, 0.2])
            tooth.visual.vertex_colors = [160, 160, 160, 255]
            meshes.append(tooth)
        
        # Third gear (medium)
        gear3 = trimesh.creation.cylinder(radius=1.2, height=0.4, sections=32)
        gear3.apply_translation([2.5, 0, 0.2])
        gear3.visual.vertex_colors = self.colors["gear"]
        meshes.append(gear3)
        
        # Gear teeth for third gear
        for i in range(14):
            angle = 2 * np.pi * i / 14
            x = 2.5 + 1.4 * np.cos(angle)
            y = 1.4 * np.sin(angle)
            tooth = trimesh.creation.box(extents=[0.18, 0.28, 0.5])
            tooth.apply_translation([x, y, 0.2])
            tooth.visual.vertex_colors = [160, 160, 160, 255]
            meshes.append(tooth)
        
        # Axles
        axle1 = trimesh.creation.cylinder(radius=0.15, height=1.0, sections=16)
        axle1.apply_translation([-2.5, 0, -0.3])
        axle1.visual.vertex_colors = [50, 50, 50, 255]
        meshes.append(axle1)
        
        axle2 = trimesh.creation.cylinder(radius=0.12, height=1.0, sections=16)
        axle2.apply_translation([0, 0, -0.3])
        axle2.visual.vertex_colors = [50, 50, 50, 255]
        meshes.append(axle2)
        
        axle3 = trimesh.creation.cylinder(radius=0.14, height=1.0, sections=16)
        axle3.apply_translation([2.5, 0, -0.3])
        axle3.visual.vertex_colors = [50, 50, 50, 255]
        meshes.append(axle3)
        
        # Rotation direction arrows
        arrow1 = self._create_arrow([-2.5, 1.8, 0.2], [-1.5, 1.8, 0.2], [255, 0, 0, 255], 0.08)
        arrow2 = self._create_arrow([0, -1.2, 0.2], [1.0, -1.2, 0.2], [0, 255, 0, 255], 0.08)
        arrow3 = self._create_arrow([2.5, 1.6, 0.2], [3.5, 1.6, 0.2], [255, 0, 0, 255], 0.08)
        
        if arrow1:
            meshes.append(arrow1)
        if arrow2:
            meshes.append(arrow2)
        if arrow3:
            meshes.append(arrow3)
        
        combined = trimesh.util.concatenate(meshes)
        meta = self._save_glb(combined, "gear_systems.glb")
        meta.update({
            "description": "Simple gear train with three gears showing motion transfer, speed ratios, and direction changes",
            "curriculum": ["phy_004"],
        })
        return meta

    # ---------- batches ----------
    def generate_all_models(self) -> List[Dict[str, Any]]:
        logger.info("🔧 Generating all simple machines models...")
        models = [
            self.generate_lever_types(),
            self.generate_pulley_systems(),
            self.generate_inclined_plane(),
            self.generate_wheel_and_axle(),
            self.generate_wedge_screw(),
            self.generate_gear_systems(),
        ]
        self.generate_manifest(models)
        logger.info(f"✅ Generated {len(models)} simple machines models")
        return models

    def generate_manifest(self, models: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_size = sum(m.get("size_kb", 0) for m in models)
        manifest = {
            "models": models,
            "total_models": len(models),
            "total_size_kb": round(total_size, 2),
            "curriculum_alignment": {
                "phy_004": "Simple Machines and Mechanical Advantage",
            },
            "output_dir": str(self.output_dir),
        }
        path = self.output_dir / "simple_machines_manifest.json"
        with open(path, "w") as f:
            json.dump(manifest, f, indent=2)
        return manifest


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description="Simple Machines Models Generator")
    parser.add_argument("--model", choices=[
        "all", "lever_types", "pulley_systems", "inclined_plane",
        "wheel_and_axle", "wedge_screw", "gear_systems"
    ], default="all")
    args = parser.parse_args()

    gen = SimpleMachinesGenerator()
    if args.model == "all":
        gen.generate_all_models()
        print("📋 Manifest created: simple_machines_manifest.json")
    else:
        func = getattr(gen, f"generate_{args.model}")
        meta = func()
        print(f"✅ Generated: {meta['name']}.glb → {meta['size_kb']} KB")
