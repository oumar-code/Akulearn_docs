"""
Nigerian Cultural and Historical 3D Models Generator

Generates culturally significant 3D models representing Nigerian heritage, architecture,
government structures, and traditional crafts for social studies, history, and civic education.

Educational Focus:
- Nigerian traditional architecture and cultural heritage
- Government structures and civic institutions
- Historical monuments and national symbols
- Traditional crafts and artistic heritage
- Cultural artifacts and indigenous practices

Curriculum Alignment:
- soc_001: Nigerian Culture and Society (JSS1-JSS3)
- soc_002: Traditional Institutions (JSS2-SS1)
- soc_003: Cultural Heritage (SS1-SS2)
- hist_001: Nigerian History (SS1-SS3)
- gov_002: Government Structures (SS2-SS3)

Grade Levels: JSS1 through SS3
"""

import trimesh
import numpy as np
from pathlib import Path
import json
import logging
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NigerianCulturalModelsGenerator:
    """Generator for Nigerian cultural and historical 3D models"""
    
    def __init__(self, output_dir: str = "generated_assets/nigerian_cultural"):
        """
        Initialize the Nigerian Cultural Models Generator
        
        Args:
            output_dir: Directory to save generated GLB files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("🏛️ Nigerian Cultural Models Generator initialized")
    
    def _create_box(self, center: Tuple[float, float, float], 
                    dimensions: Tuple[float, float, float],
                    color: Tuple[int, int, int, int] = (139, 69, 19, 255)) -> trimesh.Trimesh:
        """Create a colored box (rectangular prism)"""
        box = trimesh.creation.box(extents=dimensions)
        box.apply_translation(center)
        box.visual.vertex_colors = color
        return box
    
    def _create_cylinder(self, center: Tuple[float, float, float],
                        radius: float, height: float,
                        color: Tuple[int, int, int, int] = (139, 69, 19, 255)) -> trimesh.Trimesh:
        """Create a colored cylinder"""
        cylinder = trimesh.creation.cylinder(radius=radius, height=height, sections=16)
        cylinder.apply_translation(center)
        cylinder.visual.vertex_colors = color
        return cylinder
    
    def _create_cone(self, center: Tuple[float, float, float],
                    radius: float, height: float,
                    color: Tuple[int, int, int, int] = (178, 34, 34, 255)) -> trimesh.Trimesh:
        """Create a colored cone"""
        cone = trimesh.creation.cone(radius=radius, height=height, sections=16)
        cone.apply_translation(center)
        cone.visual.vertex_colors = color
        return cone
    
    def _create_sphere(self, center: Tuple[float, float, float],
                      radius: float,
                      color: Tuple[int, int, int, int] = (255, 215, 0, 255)) -> trimesh.Trimesh:
        """Create a colored sphere"""
        sphere = trimesh.creation.icosphere(subdivisions=2, radius=radius)
        sphere.apply_translation(center)
        sphere.visual.vertex_colors = color
        return sphere
    
    def generate_traditional_architecture(self) -> str:
        """
        Generate traditional Nigerian architecture model (compound with huts)
        
        Features:
        - Circular mud huts with conical thatched roofs
        - Compound layout (multiple huts)
        - Traditional Yoruba/Hausa/Igbo architectural elements
        - Entrance structure
        
        Returns:
            Path to generated GLB file
        """
        logger.info("🏛️ Generating traditional Nigerian architecture...")
        
        meshes = []
        
        # Compound wall (circular perimeter)
        wall_segments = 24
        wall_radius = 5.0
        wall_height = 1.5
        wall_thickness = 0.3
        
        for i in range(wall_segments):
            angle1 = (i / wall_segments) * 2 * np.pi
            angle2 = ((i + 1) / wall_segments) * 2 * np.pi
            
            if i == 0:  # Leave gap for entrance
                continue
            
            x1 = wall_radius * np.cos(angle1)
            y1 = wall_radius * np.sin(angle1)
            x2 = wall_radius * np.cos(angle2)
            y2 = wall_radius * np.sin(angle2)
            
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            wall_segment = self._create_box(
                center=(mid_x, mid_y, wall_height/2),
                dimensions=(wall_thickness, 0.5, wall_height),
                color=(160, 120, 80, 255)  # Clay/mud color
            )
            meshes.append(wall_segment)
        
        # Main hut (center-right)
        main_hut_base = self._create_cylinder(
            center=(2, 0, 1.0),
            radius=1.5,
            height=2.0,
            color=(139, 90, 43, 255)  # Darker mud
        )
        meshes.append(main_hut_base)
        
        # Main hut roof (conical thatch)
        main_roof = self._create_cone(
            center=(2, 0, 2.8),
            radius=1.8,
            height=1.8,
            color=(210, 180, 140, 255)  # Thatch color
        )
        meshes.append(main_roof)
        
        # Secondary hut (left)
        secondary_hut = self._create_cylinder(
            center=(-1.5, -1.5, 0.8),
            radius=1.0,
            height=1.6,
            color=(139, 90, 43, 255)
        )
        meshes.append(secondary_hut)
        
        secondary_roof = self._create_cone(
            center=(-1.5, -1.5, 2.0),
            radius=1.3,
            height=1.4,
            color=(210, 180, 140, 255)
        )
        meshes.append(secondary_roof)
        
        # Storage hut (smaller, back)
        storage_hut = self._create_cylinder(
            center=(-1, 2, 0.6),
            radius=0.7,
            height=1.2,
            color=(139, 90, 43, 255)
        )
        meshes.append(storage_hut)
        
        storage_roof = self._create_cone(
            center=(-1, 2, 1.5),
            radius=0.9,
            height=1.0,
            color=(210, 180, 140, 255)
        )
        meshes.append(storage_roof)
        
        # Central meeting area (flat stone)
        meeting_area = self._create_cylinder(
            center=(0, 0, 0.05),
            radius=1.5,
            height=0.1,
            color=(128, 128, 128, 255)  # Stone gray
        )
        meshes.append(meeting_area)
        
        # Decorative elements (wooden posts)
        for angle in [np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4]:
            post_x = 1.2 * np.cos(angle)
            post_y = 1.2 * np.sin(angle)
            post = self._create_cylinder(
                center=(post_x, post_y, 0.4),
                radius=0.08,
                height=0.8,
                color=(101, 67, 33, 255)  # Dark wood
            )
            meshes.append(post)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Export
        output_path = self.output_dir / "traditional_architecture.glb"
        combined.export(output_path)
        
        file_size = output_path.stat().st_size / 1024
        logger.info(f"✅ traditional_architecture.glb created ({file_size:.2f} KB)")
        
        return str(output_path)
    
    def generate_national_monuments(self) -> str:
        """
        Generate Nigerian national monuments model
        
        Features:
        - Stylized representation of Nigerian flag monument
        - Eagle monument (national symbol)
        - Commemorative obelisk
        - Plaza base
        
        Returns:
            Path to generated GLB file
        """
        logger.info("🏛️ Generating national monuments...")
        
        meshes = []
        
        # Plaza base (large platform)
        plaza = self._create_box(
            center=(0, 0, 0.1),
            dimensions=(10, 10, 0.2),
            color=(200, 200, 200, 255)  # Light gray concrete
        )
        meshes.append(plaza)
        
        # Central obelisk
        obelisk_base = self._create_box(
            center=(0, 0, 1.5),
            dimensions=(0.8, 0.8, 3.0),
            color=(169, 169, 169, 255)  # Dark gray stone
        )
        meshes.append(obelisk_base)
        
        # Obelisk top (pyramid)
        obelisk_top = self._create_cone(
            center=(0, 0, 3.3),
            radius=0.5,
            height=0.8,
            color=(169, 169, 169, 255)
        )
        meshes.append(obelisk_top)
        
        # Eagle statue (on obelisk top)
        eagle_body = self._create_sphere(
            center=(0, 0, 4.0),
            radius=0.3,
            color=(0, 128, 0, 255)  # Green (Nigerian flag color)
        )
        meshes.append(eagle_body)
        
        # Eagle wings (simplified)
        left_wing = self._create_box(
            center=(-0.4, 0, 4.0),
            dimensions=(0.5, 0.1, 0.3),
            color=(0, 128, 0, 255)
        )
        meshes.append(left_wing)
        
        right_wing = self._create_box(
            center=(0.4, 0, 4.0),
            dimensions=(0.5, 0.1, 0.3),
            color=(0, 128, 0, 255)
        )
        meshes.append(right_wing)
        
        # Flag poles (left and right)
        for x_pos in [-3, 3]:
            # Pole
            pole = self._create_cylinder(
                center=(x_pos, 0, 2.5),
                radius=0.08,
                height=5.0,
                color=(192, 192, 192, 255)  # Silver
            )
            meshes.append(pole)
            
            # Green section (top)
            green_section = self._create_box(
                center=(x_pos + 0.3, 0, 4.3),
                dimensions=(0.5, 0.05, 0.8),
                color=(0, 128, 0, 255)  # Nigerian green
            )
            meshes.append(green_section)
            
            # White section (middle)
            white_section = self._create_box(
                center=(x_pos + 0.3, 0, 3.5),
                dimensions=(0.5, 0.05, 0.8),
                color=(255, 255, 255, 255)  # Nigerian white
            )
            meshes.append(white_section)
            
            # Green section (bottom)
            green_section2 = self._create_box(
                center=(x_pos + 0.3, 0, 2.7),
                dimensions=(0.5, 0.05, 0.8),
                color=(0, 128, 0, 255)
            )
            meshes.append(green_section2)
        
        # Commemorative plaques (4 corners)
        for x, y in [(-4, -4), (4, -4), (-4, 4), (4, 4)]:
            plaque = self._create_box(
                center=(x, y, 0.5),
                dimensions=(0.6, 0.1, 1.0),
                color=(184, 134, 11, 255)  # Bronze
            )
            meshes.append(plaque)
        
        # Decorative pillars (4 sides)
        for x, y in [(-2, -4.5), (2, -4.5), (-2, 4.5), (2, 4.5)]:
            pillar = self._create_cylinder(
                center=(x, y, 1.0),
                radius=0.2,
                height=2.0,
                color=(245, 245, 220, 255)  # Beige stone
            )
            meshes.append(pillar)
            
            pillar_top = self._create_sphere(
                center=(x, y, 2.2),
                radius=0.25,
                color=(245, 245, 220, 255)
            )
            meshes.append(pillar_top)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Export
        output_path = self.output_dir / "national_monuments.glb"
        combined.export(output_path)
        
        file_size = output_path.stat().st_size / 1024
        logger.info(f"✅ national_monuments.glb created ({file_size:.2f} KB)")
        
        return str(output_path)
    
    def generate_government_buildings(self) -> str:
        """
        Generate Nigerian government buildings model (National Assembly representation)
        
        Features:
        - Parliament chamber dome
        - Legislative wings
        - Administrative blocks
        - Front plaza
        
        Returns:
            Path to generated GLB file
        """
        logger.info("🏛️ Generating government buildings...")
        
        meshes = []
        
        # Front plaza
        plaza = self._create_box(
            center=(0, -3, 0.05),
            dimensions=(10, 4, 0.1),
            color=(180, 180, 180, 255)
        )
        meshes.append(plaza)
        
        # Central dome building
        dome_base = self._create_cylinder(
            center=(0, 0, 1.5),
            radius=2.0,
            height=3.0,
            color=(245, 245, 220, 255)  # Beige/cream
        )
        meshes.append(dome_base)
        
        # Dome roof (sphere segment)
        dome = self._create_sphere(
            center=(0, 0, 3.5),
            radius=2.2,
            color=(0, 128, 0, 255)  # Green dome
        )
        meshes.append(dome)
        
        # Dome finial (top ornament)
        finial = self._create_cone(
            center=(0, 0, 5.5),
            radius=0.3,
            height=0.6,
            color=(255, 215, 0, 255)  # Gold
        )
        meshes.append(finial)
        
        # Left legislative wing
        left_wing = self._create_box(
            center=(-3.5, 0, 1.0),
            dimensions=(3, 4, 2.0),
            color=(245, 245, 220, 255)
        )
        meshes.append(left_wing)
        
        # Left wing roof
        left_roof = self._create_box(
            center=(-3.5, 0, 2.2),
            dimensions=(3.2, 4.2, 0.3),
            color=(178, 34, 34, 255)  # Red roof
        )
        meshes.append(left_roof)
        
        # Right legislative wing
        right_wing = self._create_box(
            center=(3.5, 0, 1.0),
            dimensions=(3, 4, 2.0),
            color=(245, 245, 220, 255)
        )
        meshes.append(right_wing)
        
        # Right wing roof
        right_roof = self._create_box(
            center=(3.5, 0, 2.2),
            dimensions=(3.2, 4.2, 0.3),
            color=(178, 34, 34, 255)
        )
        meshes.append(right_roof)
        
        # Front entrance pillars (6 classical columns)
        for i in range(6):
            x_pos = -2.5 + i * 1.0
            pillar = self._create_cylinder(
                center=(x_pos, -2, 1.5),
                radius=0.15,
                height=3.0,
                color=(255, 255, 255, 255)  # White columns
            )
            meshes.append(pillar)
            
            # Capital (top of pillar)
            capital = self._create_box(
                center=(x_pos, -2, 3.2),
                dimensions=(0.3, 0.3, 0.2),
                color=(255, 255, 255, 255)
            )
            meshes.append(capital)
        
        # Front pediment (triangular top)
        pediment = self._create_cone(
            center=(0, -2, 3.7),
            radius=3.0,
            height=0.8,
            color=(245, 245, 220, 255)
        )
        # Rotate to be horizontal
        rotation = trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])
        pediment.apply_transform(rotation)
        meshes.append(pediment)
        
        # Nigerian coat of arms (simplified, front center)
        coat_of_arms = self._create_sphere(
            center=(0, -2.2, 2.5),
            radius=0.4,
            color=(0, 128, 0, 255)
        )
        meshes.append(coat_of_arms)
        
        # Shield elements
        shield_center = self._create_box(
            center=(0, -2.3, 2.5),
            dimensions=(0.3, 0.1, 0.6),
            color=(255, 255, 255, 255)
        )
        meshes.append(shield_center)
        
        # Front steps
        for i in range(3):
            step = self._create_box(
                center=(0, -2.5 - i*0.3, 0.1 + i*0.2),
                dimensions=(6, 0.3, 0.2),
                color=(200, 200, 200, 255)
            )
            meshes.append(step)
        
        # Side towers (administrative)
        for x_pos in [-5, 5]:
            tower = self._create_box(
                center=(x_pos, 1, 1.5),
                dimensions=(1.5, 1.5, 3.0),
                color=(245, 245, 220, 255)
            )
            meshes.append(tower)
            
            tower_roof = self._create_cone(
                center=(x_pos, 1, 3.5),
                radius=0.9,
                height=1.0,
                color=(178, 34, 34, 255)
            )
            meshes.append(tower_roof)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Export
        output_path = self.output_dir / "government_buildings.glb"
        combined.export(output_path)
        
        file_size = output_path.stat().st_size / 1024
        logger.info(f"✅ government_buildings.glb created ({file_size:.2f} KB)")
        
        return str(output_path)
    
    def generate_cultural_artifacts(self) -> str:
        """
        Generate traditional Nigerian cultural artifacts
        
        Features:
        - Benin bronze head
        - Talking drum (gangan)
        - Calabash
        - Traditional mask
        - Ceremonial staff
        
        Returns:
            Path to generated GLB file
        """
        logger.info("🏛️ Generating cultural artifacts...")
        
        meshes = []
        
        # Display base/platform
        base = self._create_box(
            center=(0, 0, 0.1),
            dimensions=(8, 6, 0.2),
            color=(139, 90, 43, 255)  # Wood
        )
        meshes.append(base)
        
        # 1. Benin Bronze Head (left front)
        head = self._create_sphere(
            center=(-2.5, -1.5, 0.8),
            radius=0.5,
            color=(184, 115, 51, 255)  # Bronze
        )
        meshes.append(head)
        
        # Head crown/headdress
        crown = self._create_cylinder(
            center=(-2.5, -1.5, 1.4),
            radius=0.45,
            height=0.4,
            color=(184, 115, 51, 255)
        )
        meshes.append(crown)
        
        # Crown details (beads)
        for i in range(8):
            angle = i * np.pi / 4
            bead_x = -2.5 + 0.5 * np.cos(angle)
            bead_y = -1.5 + 0.5 * np.sin(angle)
            bead = self._create_sphere(
                center=(bead_x, bead_y, 1.6),
                radius=0.08,
                color=(255, 215, 0, 255)  # Gold accents
            )
            meshes.append(bead)
        
        # Head pedestal
        pedestal = self._create_cylinder(
            center=(-2.5, -1.5, 0.3),
            radius=0.3,
            height=0.3,
            color=(139, 69, 19, 255)
        )
        meshes.append(pedestal)
        
        # 2. Talking Drum (center front)
        drum_body = self._create_cylinder(
            center=(0, -1.5, 0.6),
            radius=0.4,
            height=0.8,
            color=(160, 82, 45, 255)  # Sienna brown
        )
        meshes.append(drum_body)
        
        # Drum heads (top and bottom)
        drum_top = self._create_cylinder(
            center=(0, -1.5, 1.05),
            radius=0.42,
            height=0.05,
            color=(210, 180, 140, 255)  # Leather
        )
        meshes.append(drum_top)
        
        drum_bottom = self._create_cylinder(
            center=(0, -1.5, 0.15),
            radius=0.42,
            height=0.05,
            color=(210, 180, 140, 255)
        )
        meshes.append(drum_bottom)
        
        # Drum strings (simplified as vertical lines)
        for i in range(6):
            angle = i * np.pi / 3
            string_x = 0.4 * np.cos(angle)
            string_y = -1.5 + 0.4 * np.sin(angle)
            string = self._create_cylinder(
                center=(string_x, string_y, 0.6),
                radius=0.02,
                height=0.9,
                color=(139, 69, 19, 255)
            )
            meshes.append(string)
        
        # 3. Calabash (right front)
        calabash = self._create_sphere(
            center=(2.5, -1.5, 0.5),
            radius=0.5,
            color=(184, 134, 11, 255)  # Dark goldenrod
        )
        meshes.append(calabash)
        
        # Calabash opening (top)
        opening = self._create_cylinder(
            center=(2.5, -1.5, 0.9),
            radius=0.2,
            height=0.15,
            color=(139, 90, 43, 255)
        )
        meshes.append(opening)
        
        # 4. Traditional Mask (left back)
        mask_face = self._create_box(
            center=(-2.5, 1.5, 1.0),
            dimensions=(0.6, 0.2, 0.9),
            color=(101, 67, 33, 255)  # Dark wood
        )
        meshes.append(mask_face)
        
        # Mask eyes (white)
        left_eye = self._create_sphere(
            center=(-2.7, 1.4, 1.1),
            radius=0.08,
            color=(255, 255, 255, 255)
        )
        meshes.append(left_eye)
        
        right_eye = self._create_sphere(
            center=(-2.3, 1.4, 1.1),
            radius=0.08,
            color=(255, 255, 255, 255)
        )
        meshes.append(right_eye)
        
        # Mask mouth (red)
        mouth = self._create_box(
            center=(-2.5, 1.4, 0.7),
            dimensions=(0.3, 0.05, 0.1),
            color=(178, 34, 34, 255)
        )
        meshes.append(mouth)
        
        # Mask headdress (feathers)
        for i in range(3):
            feather = self._create_cone(
                center=(-2.5 + (i-1)*0.2, 1.5, 1.6),
                radius=0.08,
                height=0.4,
                color=(255, 69, 0, 255)  # Orange-red
            )
            meshes.append(feather)
        
        # 5. Ceremonial Staff (Opa) - right back
        staff = self._create_cylinder(
            center=(2.5, 1.5, 0.8),
            radius=0.06,
            height=1.6,
            color=(139, 69, 19, 255)  # Saddle brown
        )
        meshes.append(staff)
        
        # Staff head ornament
        staff_head = self._create_sphere(
            center=(2.5, 1.5, 1.7),
            radius=0.15,
            color=(255, 215, 0, 255)  # Gold
        )
        meshes.append(staff_head)
        
        # Staff decorative rings
        for z in [0.4, 0.8, 1.2]:
            ring = self._create_cylinder(
                center=(2.5, 1.5, z),
                radius=0.09,
                height=0.08,
                color=(184, 134, 11, 255)  # Bronze
            )
            meshes.append(ring)
        
        # Informational labels (small pedestals)
        for x, y in [(-2.5, -1.5), (0, -1.5), (2.5, -1.5), (-2.5, 1.5), (2.5, 1.5)]:
            label = self._create_box(
                center=(x, y - 0.5, 0.25),
                dimensions=(0.6, 0.2, 0.05),
                color=(255, 255, 255, 255)
            )
            meshes.append(label)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Export
        output_path = self.output_dir / "cultural_artifacts.glb"
        combined.export(output_path)
        
        file_size = output_path.stat().st_size / 1024
        logger.info(f"✅ cultural_artifacts.glb created ({file_size:.2f} KB)")
        
        return str(output_path)
    
    def generate_historical_sites(self) -> str:
        """
        Generate Nigerian historical sites (Ancient city walls representation)
        
        Features:
        - Ancient city walls (inspired by Benin/Kano walls)
        - Gate structures
        - Watchtowers
        - Moat/defensive features
        
        Returns:
            Path to generated GLB file
        """
        logger.info("🏛️ Generating historical sites...")
        
        meshes = []
        
        # Ground base
        ground = self._create_box(
            center=(0, 0, 0.05),
            dimensions=(12, 12, 0.1),
            color=(139, 90, 43, 255)  # Earth
        )
        meshes.append(ground)
        
        # City walls (rectangular perimeter)
        wall_height = 3.0
        wall_thickness = 0.5
        
        # North wall
        north_wall = self._create_box(
            center=(0, 5, wall_height/2),
            dimensions=(10, wall_thickness, wall_height),
            color=(139, 69, 19, 255)  # Mud brick
        )
        meshes.append(north_wall)
        
        # South wall
        south_wall = self._create_box(
            center=(0, -5, wall_height/2),
            dimensions=(10, wall_thickness, wall_height),
            color=(139, 69, 19, 255)
        )
        meshes.append(south_wall)
        
        # East wall
        east_wall = self._create_box(
            center=(5, 0, wall_height/2),
            dimensions=(wall_thickness, 10, wall_height),
            color=(139, 69, 19, 255)
        )
        meshes.append(east_wall)
        
        # West wall
        west_wall = self._create_box(
            center=(-5, 0, wall_height/2),
            dimensions=(wall_thickness, 10, wall_height),
            color=(139, 69, 19, 255)
        )
        meshes.append(west_wall)
        
        # Gate structure (south entrance)
        gate_left = self._create_box(
            center=(-1.5, -5, wall_height/2),
            dimensions=(1, wall_thickness + 0.2, wall_height),
            color=(101, 67, 33, 255)  # Darker
        )
        meshes.append(gate_left)
        
        gate_right = self._create_box(
            center=(1.5, -5, wall_height/2),
            dimensions=(1, wall_thickness + 0.2, wall_height),
            color=(101, 67, 33, 255)
        )
        meshes.append(gate_right)
        
        # Gate arch
        gate_arch = self._create_box(
            center=(0, -5, 2.5),
            dimensions=(3, wall_thickness + 0.3, 1),
            color=(101, 67, 33, 255)
        )
        meshes.append(gate_arch)
        
        # Watchtowers (4 corners)
        tower_positions = [(-5, -5), (5, -5), (-5, 5), (5, 5)]
        for x, y in tower_positions:
            # Tower base
            tower = self._create_cylinder(
                center=(x, y, 2.5),
                radius=0.8,
                height=5.0,
                color=(139, 69, 19, 255)
            )
            meshes.append(tower)
            
            # Tower roof (conical)
            tower_roof = self._create_cone(
                center=(x, y, 5.5),
                radius=1.0,
                height=1.2,
                color=(178, 34, 34, 255)  # Red clay
            )
            meshes.append(tower_roof)
            
            # Tower windows (4 directions)
            for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
                window_x = x + 0.85 * np.cos(angle)
                window_y = y + 0.85 * np.sin(angle)
                window = self._create_box(
                    center=(window_x, window_y, 4.0),
                    dimensions=(0.2, 0.1, 0.4),
                    color=(50, 50, 50, 255)  # Dark opening
                )
                meshes.append(window)
        
        # Battlements (crenellations on walls)
        battlement_spacing = 1.0
        battlement_size = 0.4
        
        # North wall battlements
        for i in range(10):
            x_pos = -4.5 + i * battlement_spacing
            battlement = self._create_box(
                center=(x_pos, 5, wall_height + 0.3),
                dimensions=(battlement_size, wall_thickness + 0.2, 0.6),
                color=(120, 60, 20, 255)
            )
            meshes.append(battlement)
        
        # South wall battlements (excluding gate)
        for i in range(10):
            x_pos = -4.5 + i * battlement_spacing
            if abs(x_pos) > 2:  # Skip gate area
                battlement = self._create_box(
                    center=(x_pos, -5, wall_height + 0.3),
                    dimensions=(battlement_size, wall_thickness + 0.2, 0.6),
                    color=(120, 60, 20, 255)
                )
                meshes.append(battlement)
        
        # Moat (simplified as ground depression)
        moat_segments = 16
        moat_radius = 6.5
        for i in range(moat_segments):
            angle = (i / moat_segments) * 2 * np.pi
            moat_x = moat_radius * np.cos(angle)
            moat_y = moat_radius * np.sin(angle)
            
            moat_section = self._create_cylinder(
                center=(moat_x, moat_y, -0.2),
                radius=0.4,
                height=0.3,
                color=(70, 130, 180, 255)  # Steel blue (water)
            )
            meshes.append(moat_section)
        
        # Historical marker (center)
        marker = self._create_cylinder(
            center=(0, 0, 0.5),
            radius=0.5,
            height=1.0,
            color=(128, 128, 128, 255)  # Stone gray
        )
        meshes.append(marker)
        
        # Marker plaque
        plaque = self._create_box(
            center=(0, 0.6, 0.8),
            dimensions=(0.8, 0.1, 0.4),
            color=(184, 134, 11, 255)  # Bronze
        )
        meshes.append(plaque)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Export
        output_path = self.output_dir / "historical_sites.glb"
        combined.export(output_path)
        
        file_size = output_path.stat().st_size / 1024
        logger.info(f"✅ historical_sites.glb created ({file_size:.2f} KB)")
        
        return str(output_path)
    
    def generate_traditional_crafts(self) -> str:
        """
        Generate traditional Nigerian crafts and tools
        
        Features:
        - Weaving loom
        - Pottery wheel with clay pot
        - Blacksmith anvil and tools
        - Leather working tools
        - Dyeing vats
        
        Returns:
            Path to generated GLB file
        """
        logger.info("🏛️ Generating traditional crafts...")
        
        meshes = []
        
        # Workshop base
        base = self._create_box(
            center=(0, 0, 0.1),
            dimensions=(10, 8, 0.2),
            color=(160, 120, 80, 255)  # Clay ground
        )
        meshes.append(base)
        
        # 1. Weaving Loom (left)
        # Loom frame
        loom_left = self._create_cylinder(
            center=(-3, -2, 1.0),
            radius=0.08,
            height=2.0,
            color=(101, 67, 33, 255)
        )
        meshes.append(loom_left)
        
        loom_right = self._create_cylinder(
            center=(-3, 0, 1.0),
            radius=0.08,
            height=2.0,
            color=(101, 67, 33, 255)
        )
        meshes.append(loom_right)
        
        # Loom crossbar (top)
        crossbar = self._create_cylinder(
            center=(-3, -1, 2.0),
            radius=0.06,
            height=2.0,
            color=(101, 67, 33, 255)
        )
        rotation = trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])
        crossbar.apply_transform(rotation)
        meshes.append(crossbar)
        
        # Fabric on loom (colorful)
        fabric = self._create_box(
            center=(-3, -1, 1.2),
            dimensions=(0.05, 1.5, 1.2),
            color=(255, 140, 0, 255)  # Orange fabric
        )
        meshes.append(fabric)
        
        # Woven pattern (stripes)
        for i in range(5):
            stripe = self._create_box(
                center=(-2.95, -1, 0.8 + i*0.3),
                dimensions=(0.06, 1.5, 0.1),
                color=(0, 128, 0, 255)  # Green stripes
            )
            meshes.append(stripe)
        
        # 2. Pottery Wheel and Pot (center-left)
        # Wheel base
        wheel_base = self._create_cylinder(
            center=(-1, -2, 0.3),
            radius=0.5,
            height=0.4,
            color=(101, 67, 33, 255)
        )
        meshes.append(wheel_base)
        
        # Wheel disk
        wheel_disk = self._create_cylinder(
            center=(-1, -2, 0.6),
            radius=0.6,
            height=0.08,
            color=(139, 90, 43, 255)
        )
        meshes.append(wheel_disk)
        
        # Clay pot on wheel
        pot_base = self._create_cylinder(
            center=(-1, -2, 0.75),
            radius=0.3,
            height=0.2,
            color=(160, 82, 45, 255)  # Clay
        )
        meshes.append(pot_base)
        
        pot_body = self._create_cylinder(
            center=(-1, -2, 1.0),
            radius=0.35,
            height=0.4,
            color=(160, 82, 45, 255)
        )
        meshes.append(pot_body)
        
        pot_neck = self._create_cylinder(
            center=(-1, -2, 1.3),
            radius=0.25,
            height=0.2,
            color=(160, 82, 45, 255)
        )
        meshes.append(pot_neck)
        
        # 3. Blacksmith Anvil and Tools (center-right)
        # Anvil base
        anvil_base = self._create_box(
            center=(1, -2, 0.5),
            dimensions=(0.6, 0.4, 0.8),
            color=(64, 64, 64, 255)  # Dark gray
        )
        meshes.append(anvil_base)
        
        # Anvil top
        anvil_top = self._create_box(
            center=(1, -2, 1.0),
            dimensions=(0.8, 0.5, 0.2),
            color=(169, 169, 169, 255)  # Light gray iron
        )
        meshes.append(anvil_top)
        
        # Anvil horn
        horn = self._create_cone(
            center=(1.5, -2, 1.1),
            radius=0.15,
            height=0.4,
            color=(169, 169, 169, 255)
        )
        rotation = trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0])
        horn.apply_transform(rotation)
        meshes.append(horn)
        
        # Hammer (on anvil)
        hammer_head = self._create_box(
            center=(0.8, -2, 1.2),
            dimensions=(0.3, 0.1, 0.1),
            color=(128, 128, 128, 255)
        )
        meshes.append(hammer_head)
        
        hammer_handle = self._create_cylinder(
            center=(0.8, -1.7, 1.2),
            radius=0.03,
            height=0.4,
            color=(139, 69, 19, 255)
        )
        rotation = trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])
        hammer_handle.apply_transform(rotation)
        meshes.append(hammer_handle)
        
        # 4. Leather Working Station (right)
        # Work bench
        bench = self._create_box(
            center=(3, -2, 0.6),
            dimensions=(1.5, 1.0, 0.3),
            color=(139, 90, 43, 255)
        )
        meshes.append(bench)
        
        # Bench legs
        for x, y in [(2.5, -2.3), (3.5, -2.3), (2.5, -1.7), (3.5, -1.7)]:
            leg = self._create_cylinder(
                center=(x, y, 0.3),
                radius=0.05,
                height=0.6,
                color=(101, 67, 33, 255)
            )
            meshes.append(leg)
        
        # Leather hide
        leather = self._create_box(
            center=(3, -2, 0.8),
            dimensions=(1.0, 0.8, 0.02),
            color=(139, 69, 19, 255)
        )
        meshes.append(leather)
        
        # Tools (awl, knife)
        awl = self._create_cylinder(
            center=(2.5, -2, 0.85),
            radius=0.02,
            height=0.3,
            color=(192, 192, 192, 255)
        )
        meshes.append(awl)
        
        knife = self._create_box(
            center=(3.5, -2, 0.85),
            dimensions=(0.3, 0.05, 0.02),
            color=(192, 192, 192, 255)
        )
        meshes.append(knife)
        
        # 5. Dyeing Vats (back)
        # Three vats with different colored dyes
        dye_colors = [
            (75, 0, 130, 255),    # Indigo
            (178, 34, 34, 255),   # Red
            (255, 215, 0, 255)    # Yellow
        ]
        
        for i, color in enumerate(dye_colors):
            x_pos = -2 + i * 2
            
            # Vat container
            vat = self._create_cylinder(
                center=(x_pos, 2, 0.5),
                radius=0.5,
                height=0.8,
                color=(101, 67, 33, 255)  # Wood
            )
            meshes.append(vat)
            
            # Dye liquid
            dye = self._create_cylinder(
                center=(x_pos, 2, 0.4),
                radius=0.45,
                height=0.6,
                color=color
            )
            meshes.append(dye)
            
            # Fabric dipping (partially submerged)
            fabric_dip = self._create_box(
                center=(x_pos, 2, 0.7),
                dimensions=(0.3, 0.05, 0.4),
                color=(255, 255, 255, 255)  # White fabric
            )
            meshes.append(fabric_dip)
        
        # Storage baskets
        for x in [-3.5, 3.5]:
            basket = self._create_cylinder(
                center=(x, 2, 0.3),
                radius=0.4,
                height=0.5,
                color=(210, 180, 140, 255)  # Tan woven
            )
            meshes.append(basket)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Export
        output_path = self.output_dir / "traditional_crafts.glb"
        combined.export(output_path)
        
        file_size = output_path.stat().st_size / 1024
        logger.info(f"✅ traditional_crafts.glb created ({file_size:.2f} KB)")
        
        return str(output_path)
    
    def generate_all_models(self) -> List[str]:
        """
        Generate all Nigerian cultural models
        
        Returns:
            List of paths to generated GLB files
        """
        logger.info("🏛️ Generating all Nigerian cultural models...")
        
        model_paths = []
        
        # Generate all models
        model_paths.append(self.generate_traditional_architecture())
        model_paths.append(self.generate_national_monuments())
        model_paths.append(self.generate_government_buildings())
        model_paths.append(self.generate_cultural_artifacts())
        model_paths.append(self.generate_historical_sites())
        model_paths.append(self.generate_traditional_crafts())
        
        # Generate manifest
        self.generate_manifest(model_paths)
        
        logger.info(f"✅ Generated {len(model_paths)} Nigerian cultural models")
        return model_paths
    
    def generate_manifest(self, model_paths: List[str]) -> str:
        """
        Generate a JSON manifest file with metadata about all models
        
        Args:
            model_paths: List of paths to generated model files
            
        Returns:
            Path to generated manifest file
        """
        manifest = {
            "generator": "NigerianCulturalModelsGenerator",
            "version": "1.0",
            "generated_date": "2026-01-13",
            "curriculum_topics": ["soc_001", "soc_002", "soc_003", "hist_001", "gov_002"],
            "grade_levels": ["JSS1", "JSS2", "JSS3", "SS1", "SS2", "SS3"],
            "total_models": len(model_paths),
            "models": []
        }
        
        for model_path in model_paths:
            path_obj = Path(model_path)
            file_size = path_obj.stat().st_size / 1024  # KB
            
            model_info = {
                "filename": path_obj.name,
                "path": str(path_obj),
                "size_kb": round(file_size, 2),
                "format": "GLB"
            }
            
            # Add specific metadata based on model type
            if "traditional_architecture" in path_obj.name:
                model_info.update({
                    "description": "Traditional Nigerian compound with circular huts and thatched roofs",
                    "cultural_significance": "Represents indigenous Yoruba/Hausa/Igbo architectural styles",
                    "topics": ["soc_001", "soc_002", "hist_001"]
                })
            elif "national_monuments" in path_obj.name:
                model_info.update({
                    "description": "Nigerian national monuments including flag, eagle, and commemorative structures",
                    "cultural_significance": "Symbols of Nigerian national identity and independence",
                    "topics": ["soc_001", "hist_001", "gov_002"]
                })
            elif "government_buildings" in path_obj.name:
                model_info.update({
                    "description": "National Assembly building with dome, legislative wings, and classical architecture",
                    "cultural_significance": "Seat of Nigerian democratic governance",
                    "topics": ["gov_002", "soc_003"]
                })
            elif "cultural_artifacts" in path_obj.name:
                model_info.update({
                    "description": "Traditional artifacts including Benin bronze, talking drum, calabash, mask, and staff",
                    "cultural_significance": "Represents Nigeria's rich artistic and cultural heritage",
                    "topics": ["soc_001", "soc_002", "hist_001"]
                })
            elif "historical_sites" in path_obj.name:
                model_info.update({
                    "description": "Ancient city walls with gates, watchtowers, and defensive features",
                    "cultural_significance": "Represents historical Nigerian cities like Benin and Kano",
                    "topics": ["hist_001", "soc_003"]
                })
            elif "traditional_crafts" in path_obj.name:
                model_info.update({
                    "description": "Traditional craft stations: weaving, pottery, blacksmithing, leather work, dyeing",
                    "cultural_significance": "Showcases indigenous Nigerian vocational skills and artisan traditions",
                    "topics": ["soc_001", "soc_002"]
                })
            
            manifest["models"].append(model_info)
        
        # Calculate total size
        manifest["total_size_kb"] = round(sum(m["size_kb"] for m in manifest["models"]), 2)
        
        # Save manifest
        manifest_path = self.output_dir / "nigerian_cultural_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📋 Manifest created: {manifest_path}")
        return str(manifest_path)


def main():
    """Main function to generate all Nigerian cultural models"""
    generator = NigerianCulturalModelsGenerator()
    
    print("\n" + "="*60)
    print("Nigerian Cultural and Historical 3D Models Generator")
    print("="*60 + "\n")
    
    # Generate all models
    model_paths = generator.generate_all_models()
    
    # Print summary
    print("\n" + "="*60)
    print("✅ Generated {} Nigerian Cultural models:".format(len(model_paths)))
    
    total_size = 0
    for path in model_paths:
        file_size = Path(path).stat().st_size / 1024
        total_size += file_size
        print(f"  - {Path(path).name}: {file_size:.2f} KB")
    
    print(f"\nTotal: {total_size:.2f} KB")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
