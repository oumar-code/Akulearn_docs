"""
Circuit and Electrical Component 3D Model Generator
Priority #4: Physics Circuit Models for Nigerian Education System

Generates 6 circuit and electrical component models for physics curriculum:
- Series circuit
- Parallel circuit
- Circuit components (battery, resistor, capacitor, LED)
- Transformer (step-up/step-down)
- Electric motor (DC motor)
- Generator (AC generator)

All models are optimized for AR/VR and curriculum-aligned for WAEC/NECO standards.
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


class CircuitModelGenerator:
    """Generator for circuit and electrical component 3D models"""
    
    def __init__(self, output_dir: str = "generated_assets/circuit_models"):
        """
        Initialize the circuit model generator
        
        Args:
            output_dir: Directory to save generated models
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"CircuitModelGenerator initialized. Output: {self.output_dir}")
        
        # Color scheme for electrical components
        self.component_colors = {
            'wire': [255, 165, 0, 255],         # Orange (copper wire)
            'battery': [64, 64, 64, 255],       # Dark gray (battery casing)
            'battery_terminal': [192, 192, 192, 255],  # Silver (terminals)
            'resistor': [139, 69, 19, 255],     # Brown (resistor body)
            'resistor_bands': [255, 0, 0, 255], # Red (resistance bands)
            'bulb_base': [192, 192, 192, 255],  # Silver
            'bulb_glass': [255, 255, 200, 200], # Translucent yellow
            'capacitor': [0, 0, 255, 255],      # Blue
            'led': [255, 0, 0, 255],            # Red LED
            'coil': [255, 140, 0, 255],         # Copper coil
            'iron_core': [128, 128, 128, 255],  # Gray iron
            'magnet': [200, 0, 0, 255],         # Red magnet
            'current_arrow': [0, 200, 0, 255],  # Green arrow for current direction
            'voltage_arrow': [255, 0, 0, 255],  # Red arrow for voltage indicator
        }
    
    def _create_cylinder(self, radius: float, height: float, color: List[int],
                        position: Tuple[float, float, float] = (0, 0, 0)) -> trimesh.Trimesh:
        """Create a cylinder mesh"""
        cylinder = trimesh.creation.cylinder(radius=radius, height=height)
        cylinder.visual.vertex_colors = color
        cylinder.apply_translation(position)
        return cylinder
    
    def _create_box(self, extents: Tuple[float, float, float], color: List[int],
                   position: Tuple[float, float, float] = (0, 0, 0)) -> trimesh.Trimesh:
        """Create a box mesh"""
        box = trimesh.creation.box(extents=extents)
        box.visual.vertex_colors = color
        box.apply_translation(position)
        return box
    
    def _create_sphere(self, radius: float, color: List[int],
                      position: Tuple[float, float, float] = (0, 0, 0)) -> trimesh.Trimesh:
        """Create a sphere mesh"""
        sphere = trimesh.creation.icosphere(subdivisions=2, radius=radius)
        sphere.visual.vertex_colors = color
        sphere.apply_translation(position)
        return sphere
    
    def _create_wire(self, start: Tuple[float, float, float], 
                    end: Tuple[float, float, float], radius: float = 0.05) -> trimesh.Trimesh:
        """Create a wire (cylinder) between two points"""
        direction = np.array(end) - np.array(start)
        length = np.linalg.norm(direction)
        
        wire = trimesh.creation.cylinder(radius=radius, height=length)
        wire.visual.vertex_colors = self.component_colors['wire']
        
        # Rotate to align with direction
        direction = direction / length
        z_axis = np.array([0, 0, 1])
        
        if not np.allclose(direction, z_axis):
            rotation_axis = np.cross(z_axis, direction)
            norm = np.linalg.norm(rotation_axis)
            if norm > 1e-8:
                rotation_axis = rotation_axis / norm
                angle = np.arccos(np.dot(z_axis, direction))
                rotation_matrix = trimesh.transformations.rotation_matrix(angle, rotation_axis, point=[0, 0, 0])
                wire.apply_transform(rotation_matrix)
        else:
            angle = 0.0
        
        # Position at midpoint
        midpoint = (np.array(start) + np.array(end)) / 2
        wire.apply_translation(midpoint)
        
        return wire

    def _create_arrow(self, start: Tuple[float, float, float], end: Tuple[float, float, float], 
                      color: List[int], shaft_radius: float = 0.04, head_radius: float = 0.12, head_length: float = 0.3) -> trimesh.Trimesh:
        """Create an arrow from start to end (shaft + cone head)"""
        start_v = np.array(start, dtype=float)
        end_v = np.array(end, dtype=float)
        direction = end_v - start_v
        length = float(np.linalg.norm(direction))
        if length < 1e-6:
            # Fallback to small vertical arrow
            end_v = start_v + np.array([0, 0, 1.0])
            direction = end_v - start_v
            length = 1.0
        dir_unit = direction / length

        # Shaft length excludes head
        shaft_length = max(length - head_length, 0.05)
        shaft = trimesh.creation.cylinder(radius=shaft_radius, height=shaft_length)
        shaft.visual.vertex_colors = color

        # Head (cone)
        head = trimesh.creation.cone(radius=head_radius, height=head_length)
        head.visual.vertex_colors = color

        # Align both along direction
        z_axis = np.array([0, 0, 1.0])
        if not np.allclose(dir_unit, z_axis):
            rot_axis = np.cross(z_axis, dir_unit)
            rot_norm = np.linalg.norm(rot_axis)
            if rot_norm > 1e-8:
                rot_axis = rot_axis / rot_norm
                angle = np.arccos(np.clip(np.dot(z_axis, dir_unit), -1.0, 1.0))
                R = trimesh.transformations.rotation_matrix(angle, rot_axis, point=[0, 0, 0])
                shaft.apply_transform(R)
                head.apply_transform(R)

        # Position: shaft centered along start->(end-head), head at end
        shaft_mid = start_v + dir_unit * (shaft_length / 2.0)
        shaft.apply_translation(shaft_mid)

        head_base = end_v - dir_unit * (head_length / 2.0)
        head.apply_translation(head_base)

        return trimesh.util.concatenate([shaft, head])
    
    def _create_battery(self, position: Tuple[float, float, float]) -> List[trimesh.Trimesh]:
        """Create a battery component"""
        meshes = []
        
        # Battery body (2 cells)
        for i in range(2):
            cell = self._create_cylinder(
                0.3, 1.0, self.component_colors['battery'],
                (position[0] + i * 0.6, position[1], position[2])
            )
            meshes.append(cell)
        
        # Positive terminal
        pos_terminal = self._create_cylinder(
            0.15, 0.2, self.component_colors['battery_terminal'],
            (position[0] + 0.6, position[1], position[2] + 0.6)
        )
        meshes.append(pos_terminal)
        
        # Negative terminal
        neg_terminal = self._create_cylinder(
            0.15, 0.1, self.component_colors['battery_terminal'],
            (position[0], position[1], position[2] - 0.55)
        )
        meshes.append(neg_terminal)
        
        return meshes
    
    def _create_resistor(self, position: Tuple[float, float, float]) -> List[trimesh.Trimesh]:
        """Create a resistor component"""
        meshes = []
        
        # Resistor body
        body = self._create_cylinder(
            0.15, 0.8, self.component_colors['resistor'],
            position
        )
        meshes.append(body)
        
        # Color bands
        for i in range(3):
            band = self._create_cylinder(
                0.16, 0.05, self.component_colors['resistor_bands'],
                (position[0], position[1], position[2] - 0.25 + i * 0.25)
            )
            meshes.append(band)
        
        # Wire leads
        lead1 = self._create_cylinder(
            0.03, 0.4, self.component_colors['wire'],
            (position[0], position[1], position[2] + 0.6)
        )
        lead2 = self._create_cylinder(
            0.03, 0.4, self.component_colors['wire'],
            (position[0], position[1], position[2] - 0.6)
        )
        meshes.extend([lead1, lead2])
        
        return meshes
    
    def _create_bulb(self, position: Tuple[float, float, float]) -> List[trimesh.Trimesh]:
        """Create a light bulb component"""
        meshes = []
        
        # Glass bulb
        bulb = self._create_sphere(
            0.4, self.component_colors['bulb_glass'],
            position
        )
        meshes.append(bulb)
        
        # Base
        base = self._create_cylinder(
            0.25, 0.3, self.component_colors['bulb_base'],
            (position[0], position[1], position[2] - 0.5)
        )
        meshes.append(base)
        
        # Filament (small helix inside)
        for i in range(5):
            filament_part = self._create_sphere(
                0.05, [255, 200, 0, 255],
                (position[0], position[1], position[2] - 0.2 + i * 0.1)
            )
            meshes.append(filament_part)
        
        return meshes
    
    def generate_series_circuit(self) -> Dict[str, any]:
        """
        Generate a series circuit model
        Shows battery, 3 bulbs, and connecting wires in series
        """
        logger.info("Generating series circuit...")
        
        meshes = []
        
        # Circuit layout positions
        battery_pos = (0, 0, 0)
        bulb1_pos = (3, 0, 0)
        bulb2_pos = (3, 0, 3)
        bulb3_pos = (0, 0, 3)
        
        # Create components
        battery_meshes = self._create_battery(battery_pos)
        meshes.extend(battery_meshes)
        
        bulb1_meshes = self._create_bulb(bulb1_pos)
        meshes.extend(bulb1_meshes)
        
        bulb2_meshes = self._create_bulb(bulb2_pos)
        meshes.extend(bulb2_meshes)
        
        bulb3_meshes = self._create_bulb(bulb3_pos)
        meshes.extend(bulb3_meshes)
        
        # Connect with wires (series: battery → bulb1 → bulb2 → bulb3 → battery)
        wire1 = self._create_wire((0.6, 0, 0.6), (3, 0, -0.5))  # Battery to bulb1
        wire2 = self._create_wire((3, 0, 0.5), (3, 0, 2.5))     # Bulb1 to bulb2
        wire3 = self._create_wire((3, 0, 3.5), (0, 0, 3.5))     # Bulb2 to bulb3
        wire4 = self._create_wire((0, 0, 2.5), (0, 0, -0.5))    # Bulb3 to battery
        
        meshes.extend([wire1, wire2, wire3, wire4])

        # AR labels: current direction arrows along the path
        try:
            curr_arrow1 = self._create_arrow((0.6, 0, 0.6), (3.0, 0, 0.0), self.component_colors['current_arrow'])
            curr_arrow2 = self._create_arrow((3.0, 0, 0.5), (3.0, 0, 2.5), self.component_colors['current_arrow'])
            curr_arrow3 = self._create_arrow((3.0, 0, 3.5), (0.0, 0, 3.5), self.component_colors['current_arrow'])
            curr_arrow4 = self._create_arrow((0.0, 0, 2.5), (0.0, 0, 0.0), self.component_colors['current_arrow'])
            meshes.extend([curr_arrow1, curr_arrow2, curr_arrow3, curr_arrow4])
        except Exception as e:
            logger.warning(f"⚠️ Failed to add current arrows: {e}")

        # Voltage indicator arrows near battery terminals
        try:
            v_plus = self._create_arrow((0.6, 0, 0.9), (0.6, 0, 1.3), self.component_colors['voltage_arrow'])
            v_minus = self._create_arrow((0.0, 0, -0.9), (0.0, 0, -1.3), self.component_colors['voltage_arrow'])
            meshes.extend([v_plus, v_minus])
        except Exception as e:
            logger.warning(f"⚠️ Failed to add voltage arrows: {e}")
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "series_circuit.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: series_circuit.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'series_circuit.glb',
            'filepath': str(output_path),
            'model': 'Series Circuit',
            'components': ['Battery', '3 Light bulbs', 'Connecting wires'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Shows series circuit where current flows through single path, same current through all components'
        }
    
    def generate_parallel_circuit(self) -> Dict[str, any]:
        """
        Generate a parallel circuit model
        Shows battery with 3 bulbs in parallel branches
        """
        logger.info("Generating parallel circuit...")
        
        meshes = []
        
        # Circuit layout
        battery_pos = (0, 0, 1.5)
        bulb1_pos = (3, 0, 0)
        bulb2_pos = (3, 0, 1.5)
        bulb3_pos = (3, 0, 3)
        
        # Create components
        battery_meshes = self._create_battery(battery_pos)
        meshes.extend(battery_meshes)
        
        bulb1_meshes = self._create_bulb(bulb1_pos)
        meshes.extend(bulb1_meshes)
        
        bulb2_meshes = self._create_bulb(bulb2_pos)
        meshes.extend(bulb2_meshes)
        
        bulb3_meshes = self._create_bulb(bulb3_pos)
        meshes.extend(bulb3_meshes)
        
        # Junction points
        junction_left = (1.5, 0, 1.5)
        junction_right = (4.5, 0, 1.5)
        
        # Wires from battery to left junction
        wire_bat_junc = self._create_wire((0.6, 0, 1.5), junction_left)
        meshes.append(wire_bat_junc)
        
        # Parallel branches from left junction to bulbs
        wire_junc_b1 = self._create_wire(junction_left, (3, 0, -0.5))
        wire_junc_b2 = self._create_wire(junction_left, (3, 0, 1.0))
        wire_junc_b3 = self._create_wire(junction_left, (3, 0, 2.5))
        meshes.extend([wire_junc_b1, wire_junc_b2, wire_junc_b3])
        
        # Return wires from bulbs to right junction
        wire_b1_junc = self._create_wire((3, 0, 0.5), junction_right)
        wire_b2_junc = self._create_wire((3, 0, 2.0), junction_right)
        wire_b3_junc = self._create_wire((3, 0, 3.5), junction_right)
        meshes.extend([wire_b1_junc, wire_b2_junc, wire_b3_junc])
        
        # Wire from right junction back to battery
        wire_junc_bat = self._create_wire(junction_right, (0, 0, 1.5))
        meshes.append(wire_junc_bat)
        
        # Junction indicators (small spheres)
        junc_left_marker = self._create_sphere(0.1, [255, 255, 0, 255], junction_left)
        junc_right_marker = self._create_sphere(0.1, [255, 255, 0, 255], junction_right)
        meshes.extend([junc_left_marker, junc_right_marker])

        # AR labels: current arrows on each branch
        try:
            curr_a = self._create_arrow(junction_left, (3.0, 0, 0.0), self.component_colors['current_arrow'])
            curr_b = self._create_arrow(junction_left, (3.0, 0, 1.5), self.component_colors['current_arrow'])
            curr_c = self._create_arrow(junction_left, (3.0, 0, 3.0), self.component_colors['current_arrow'])
            meshes.extend([curr_a, curr_b, curr_c])
        except Exception as e:
            logger.warning(f"⚠️ Failed to add branch current arrows: {e}")

        # Voltage indicator arrows across battery (same across branches)
        try:
            v1 = self._create_arrow((0.6, 0, 1.8), (0.6, 0, 2.2), self.component_colors['voltage_arrow'])
            v2 = self._create_arrow((0.6, 0, 1.2), (0.6, 0, 0.8), self.component_colors['voltage_arrow'])
            meshes.extend([v1, v2])
        except Exception as e:
            logger.warning(f"⚠️ Failed to add voltage arrows: {e}")
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "parallel_circuit.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: parallel_circuit.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'parallel_circuit.glb',
            'filepath': str(output_path),
            'model': 'Parallel Circuit',
            'components': ['Battery', '3 Light bulbs (parallel)', 'Junction points', 'Connecting wires'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Shows parallel circuit with multiple paths, same voltage across all branches'
        }
    
    def generate_circuit_components(self) -> Dict[str, any]:
        """
        Generate individual circuit components library
        Shows battery, resistor, capacitor, LED separately
        """
        logger.info("Generating circuit components...")
        
        meshes = []
        
        # Layout positions for component library
        x_offset = 0
        spacing = 2.5
        
        # Battery
        battery_meshes = self._create_battery((x_offset, 0, 0))
        meshes.extend(battery_meshes)
        x_offset += spacing
        
        # Resistor
        resistor_meshes = self._create_resistor((x_offset, 0, 0))
        meshes.extend(resistor_meshes)
        x_offset += spacing
        
        # Capacitor
        cap_plate1 = self._create_cylinder(0.3, 0.05, self.component_colors['capacitor'], (x_offset, 0, 0.3))
        cap_plate2 = self._create_cylinder(0.3, 0.05, self.component_colors['capacitor'], (x_offset, 0, -0.3))
        cap_lead1 = self._create_cylinder(0.03, 0.4, self.component_colors['wire'], (x_offset, 0, 0.6))
        cap_lead2 = self._create_cylinder(0.03, 0.4, self.component_colors['wire'], (x_offset, 0, -0.6))
        meshes.extend([cap_plate1, cap_plate2, cap_lead1, cap_lead2])
        x_offset += spacing
        
        # LED
        led_dome = self._create_sphere(0.3, self.component_colors['led'], (x_offset, 0, 0.2))
        led_base = self._create_cylinder(0.2, 0.3, [64, 64, 64, 255], (x_offset, 0, -0.3))
        led_anode = self._create_cylinder(0.03, 0.5, self.component_colors['wire'], (x_offset + 0.1, 0, -0.7))
        led_cathode = self._create_cylinder(0.03, 0.5, self.component_colors['wire'], (x_offset - 0.1, 0, -0.7))
        meshes.extend([led_dome, led_base, led_anode, led_cathode])
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "circuit_components.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: circuit_components.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'circuit_components.glb',
            'filepath': str(output_path),
            'model': 'Circuit Components Library',
            'components': ['Battery', 'Resistor', 'Capacitor', 'LED'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Individual circuit components for identification and circuit building exercises'
        }
    
    def generate_transformer(self) -> Dict[str, any]:
        """
        Generate a transformer model
        Shows primary and secondary coils with iron core
        """
        logger.info("Generating transformer...")
        
        meshes = []
        
        # Iron core (rectangular)
        core = self._create_box((0.5, 2.0, 3.0), self.component_colors['iron_core'], (0, 0, 0))
        meshes.append(core)
        
        # Primary coil (left side, more turns)
        primary_turns = 10
        for i in range(primary_turns):
            z = -1.2 + (i * 0.25)
            coil_ring = trimesh.creation.torus(major_radius=0.8, minor_radius=0.08)
            coil_ring.visual.vertex_colors = self.component_colors['coil']
            # Rotate to vertical
            rotation = trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])
            coil_ring.apply_transform(rotation)
            coil_ring.apply_translation((-0.8, 0, z))
            meshes.append(coil_ring)
        
        # Secondary coil (right side, fewer turns)
        secondary_turns = 5
        for i in range(secondary_turns):
            z = -0.6 + (i * 0.25)
            coil_ring = trimesh.creation.torus(major_radius=0.8, minor_radius=0.08)
            coil_ring.visual.vertex_colors = self.component_colors['coil']
            # Rotate to vertical
            rotation = trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])
            coil_ring.apply_transform(rotation)
            coil_ring.apply_translation((0.8, 0, z))
            meshes.append(coil_ring)
        
        # Input/output terminals
        input1 = self._create_cylinder(0.08, 0.3, self.component_colors['battery_terminal'], (-1.5, 0, -1.2))
        input2 = self._create_cylinder(0.08, 0.3, self.component_colors['battery_terminal'], (-1.5, 0, 1.5))
        output1 = self._create_cylinder(0.08, 0.3, self.component_colors['battery_terminal'], (1.5, 0, -0.6))
        output2 = self._create_cylinder(0.08, 0.3, self.component_colors['battery_terminal'], (1.5, 0, 1.0))
        meshes.extend([input1, input2, output1, output2])
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "transformer.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: transformer.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'transformer.glb',
            'filepath': str(output_path),
            'model': 'Transformer',
            'components': ['Iron core', 'Primary coil (10 turns)', 'Secondary coil (5 turns)', 'Terminals'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Step-down transformer with primary (more turns) and secondary (fewer turns) coils'
        }
    
    def generate_electric_motor(self) -> Dict[str, any]:
        """
        Generate a DC electric motor model
        Shows armature, brushes, and magnets
        """
        logger.info("Generating electric motor...")
        
        meshes = []
        
        # Outer casing
        casing = self._create_cylinder(1.5, 3.0, [128, 128, 128, 255], (0, 0, 0))
        meshes.append(casing)
        
        # Magnets (permanent magnets on sides)
        magnet_north = self._create_box((0.3, 2.5, 0.8), self.component_colors['magnet'], (-1.0, 0, 0))
        magnet_south = self._create_box((0.3, 2.5, 0.8), [0, 0, 200, 255], (1.0, 0, 0))  # Blue for south
        meshes.extend([magnet_north, magnet_south])
        
        # Armature (rotating coil)
        armature_core = self._create_cylinder(0.3, 1.5, self.component_colors['iron_core'], (0, 0, 0))
        meshes.append(armature_core)
        
        # Armature coils
        for i in range(4):
            angle = (np.pi / 2) * i
            x = 0.5 * np.cos(angle)
            z = 0.5 * np.sin(angle)
            coil = self._create_box((0.2, 1.5, 0.1), self.component_colors['coil'], (x, 0, z))
            meshes.append(coil)
        
        # Commutator (split ring)
        comm1 = trimesh.creation.annulus(r_min=0.35, r_max=0.45, height=0.3)
        comm1.visual.vertex_colors = self.component_colors['battery_terminal']
        comm1.apply_translation((0, -1.2, 0))
        meshes.append(comm1)
        
        # Brushes
        brush1 = self._create_box((0.15, 0.4, 0.15), [64, 64, 64, 255], (0.5, -1.2, 0))
        brush2 = self._create_box((0.15, 0.4, 0.15), [64, 64, 64, 255], (-0.5, -1.2, 0))
        meshes.extend([brush1, brush2])
        
        # Shaft
        shaft = self._create_cylinder(0.1, 4.0, self.component_colors['battery_terminal'], (0, 0, 0))
        rotation = trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])
        shaft.apply_transform(rotation)
        meshes.append(shaft)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "electric_motor.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: electric_motor.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'electric_motor.glb',
            'filepath': str(output_path),
            'model': 'DC Electric Motor',
            'components': ['Armature coil', 'Permanent magnets', 'Commutator', 'Brushes', 'Shaft'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'DC motor showing electromagnetic induction principles and torque generation'
        }
    
    def generate_generator(self) -> Dict[str, any]:
        """
        Generate an AC generator model
        Shows rotating armature and slip rings
        """
        logger.info("Generating AC generator...")
        
        meshes = []
        
        # Outer casing
        casing = self._create_cylinder(1.5, 3.0, [128, 128, 128, 255], (0, 0, 0))
        meshes.append(casing)
        
        # Permanent magnets
        magnet_north = self._create_box((0.3, 2.5, 0.8), self.component_colors['magnet'], (-1.0, 0, 0))
        magnet_south = self._create_box((0.3, 2.5, 0.8), [0, 0, 200, 255], (1.0, 0, 0))
        meshes.extend([magnet_north, magnet_south])
        
        # Rotating armature coil
        armature = self._create_box((1.2, 0.1, 0.8), self.component_colors['coil'], (0, 0, 0))
        meshes.append(armature)
        
        # Slip rings (continuous rings for AC output)
        slip_ring1 = trimesh.creation.annulus(r_min=0.35, r_max=0.45, height=0.2)
        slip_ring1.visual.vertex_colors = self.component_colors['battery_terminal']
        slip_ring1.apply_translation((0, -1.3, 0))
        meshes.append(slip_ring1)
        
        slip_ring2 = trimesh.creation.annulus(r_min=0.35, r_max=0.45, height=0.2)
        slip_ring2.visual.vertex_colors = self.component_colors['battery_terminal']
        slip_ring2.apply_translation((0, -1.6, 0))
        meshes.append(slip_ring2)
        
        # Brushes touching slip rings
        brush1 = self._create_box((0.15, 0.4, 0.15), [64, 64, 64, 255], (0.5, -1.3, 0))
        brush2 = self._create_box((0.15, 0.4, 0.15), [64, 64, 64, 255], (0.5, -1.6, 0))
        meshes.extend([brush1, brush2])
        
        # Rotating shaft
        shaft = self._create_cylinder(0.1, 4.0, self.component_colors['battery_terminal'], (0, 0, 0))
        rotation = trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])
        shaft.apply_transform(rotation)
        meshes.append(shaft)
        
        # Output terminals
        output1 = self._create_cylinder(0.08, 0.4, self.component_colors['wire'], (1.0, -1.3, 0))
        output2 = self._create_cylinder(0.08, 0.4, self.component_colors['wire'], (1.0, -1.6, 0))
        meshes.extend([output1, output2])
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "generator.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: generator.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'generator.glb',
            'filepath': str(output_path),
            'model': 'AC Generator',
            'components': ['Rotating armature', 'Permanent magnets', 'Slip rings', 'Brushes', 'Shaft'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'AC generator showing electromagnetic induction and alternating current production'
        }
    
    def generate_all_circuit_models(self) -> List[Dict[str, any]]:
        """Generate all 6 circuit models"""
        logger.info("⚡ Generating all circuit models...")
        
        models = []
        models.append(self.generate_series_circuit())
        models.append(self.generate_parallel_circuit())
        models.append(self.generate_circuit_components())
        models.append(self.generate_transformer())
        models.append(self.generate_electric_motor())
        models.append(self.generate_generator())
        
        logger.info(f"✅ Generated {len(models)} circuit models")
        
        return models
    
    def generate_manifest(self, models: List[Dict[str, any]]) -> str:
        """Generate manifest file for all circuit models"""
        manifest = {
            "collection": "Circuit and Electrical Components",
            "priority": 4,
            "exam_weight": "Very High",
            "subject": "Physics",
            "topic_code": "phy_008",
            "grade_levels": ["SS2", "SS3"],
            "curriculum_standards": ["WAEC", "NECO"],
            "total_models": len(models),
            "models": []
        }
        
        for model in models:
            manifest["models"].append({
                "filename": model['filename'],
                "filepath": model['filepath'],
                "model": model['model'],
                "components": model['components'],
                "exam_topics": ["phy_008"],
                "grade_levels": ["SS2", "SS3"],
                "vertices": model['vertices'],
                "faces": model['faces'],
                "file_size_kb": model['file_size_kb'],
                "educational_notes": model['educational_notes'],
                "ar_ready": True,
                "curriculum_standard": ["WAEC", "NECO"]
            })
        
        manifest_path = self.output_dir / "circuit_models_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"📋 Manifest created: {manifest_path}")
        return str(manifest_path)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate circuit 3D models')
    parser.add_argument('--model', type=str, default='all',
                       choices=['all', 'series', 'parallel', 'components', 
                               'transformer', 'motor', 'generator'],
                       help='Which model to generate')
    
    args = parser.parse_args()
    
    generator = CircuitModelGenerator()
    
    if args.model == 'all':
        models = generator.generate_all_circuit_models()
        generator.generate_manifest(models)
        
        total_size = sum(m['file_size_kb'] for m in models)
        print(f"\n📊 Generation Statistics:")
        print(f"   Models: {len(models)}")
        print(f"   Total Size: {total_size:.2f} KB")
        print(f"   Models: {', '.join(m['model'] for m in models)}")
    else:
        model_map = {
            'series': generator.generate_series_circuit,
            'parallel': generator.generate_parallel_circuit,
            'components': generator.generate_circuit_components,
            'transformer': generator.generate_transformer,
            'motor': generator.generate_electric_motor,
            'generator': generator.generate_generator,
        }
        
        result = model_map[args.model]()
        print(f"\n✅ Generated: {result['filename']} ({result['file_size_kb']:.2f} KB)")
