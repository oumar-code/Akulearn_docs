"""
Molecular and Atomic Structure 3D Model Generator
Priority #3: Chemistry Models for Nigerian Education System

Generates 8 molecular and atomic structure models for chemistry curriculum:
- Atomic models (H, C, O, N)
- Ionic bonding (NaCl)
- Covalent bonding (H2O, CO2, CH4)
- Metallic bonding structure
- Hydrocarbon series (CH4 to C4H10)
- Benzene ring
- Protein structure
- DNA helix

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


class MolecularModelGenerator:
    """Generator for molecular and atomic structure 3D models"""
    
    def __init__(self, output_dir: str = "generated_assets/molecular_models"):
        """
        Initialize the molecular model generator
        
        Args:
            output_dir: Directory to save generated models
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"MolecularModelGenerator initialized. Output: {self.output_dir}")
        
        # Color scheme for atoms (standard CPK coloring)
        self.atom_colors = {
            'hydrogen': [255, 255, 255, 255],    # White
            'carbon': [64, 64, 64, 255],         # Dark gray
            'oxygen': [255, 0, 0, 255],          # Red
            'nitrogen': [0, 0, 255, 255],        # Blue
            'phosphorus': [255, 165, 0, 255],    # Orange
            'sulfur': [255, 255, 0, 255],        # Yellow
            'electron': [0, 255, 255, 255],      # Cyan
            'bond': [200, 200, 200, 255],        # Light gray
        }
    
    def _create_sphere(self, radius: float, color: List[int], 
                      position: Tuple[float, float, float] = (0, 0, 0)) -> trimesh.Trimesh:
        """Create a sphere mesh"""
        sphere = trimesh.creation.icosphere(subdivisions=2, radius=radius)
        sphere.visual.vertex_colors = color
        sphere.apply_translation(position)
        return sphere
    
    def _create_cylinder(self, radius: float, height: float, color: List[int],
                        start: Tuple[float, float, float], 
                        end: Tuple[float, float, float]) -> trimesh.Trimesh:
        """Create a cylinder between two points (for bonds)"""
        cylinder = trimesh.creation.cylinder(radius=radius, height=height)
        cylinder.visual.vertex_colors = color
        
        # Calculate rotation to align with bond direction
        direction = np.array(end) - np.array(start)
        length = np.linalg.norm(direction)
        direction = direction / length
        
        # Default cylinder is along z-axis
        z_axis = np.array([0, 0, 1])
        
        if not np.allclose(direction, z_axis):
            rotation_axis = np.cross(z_axis, direction)
            rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
            angle = np.arccos(np.dot(z_axis, direction))
            
            rotation_matrix = trimesh.transformations.rotation_matrix(
                angle, rotation_axis, point=[0, 0, 0]
            )
            cylinder.apply_transform(rotation_matrix)
        
        # Position at midpoint
        midpoint = (np.array(start) + np.array(end)) / 2
        cylinder.apply_translation(midpoint)
        
        return cylinder
    
    def _create_torus(self, major_radius: float, minor_radius: float, 
                     color: List[int], position: Tuple[float, float, float] = (0, 0, 0)) -> trimesh.Trimesh:
        """Create a torus (for electron orbitals)"""
        torus = trimesh.creation.torus(major_radius=major_radius, minor_radius=minor_radius)
        torus.visual.vertex_colors = color
        torus.apply_translation(position)
        return torus
    
    def generate_atom_models(self) -> Dict[str, any]:
        """
        Generate atomic structure models for H, C, O, N
        Shows nucleus and electron shells
        """
        logger.info("Generating atomic models...")
        
        meshes = []
        
        # Atomic data: (protons, electron_shells)
        atoms = {
            'Hydrogen': (1, [1]),           # 1 proton, 1 electron in shell 1
            'Carbon': (6, [2, 4]),          # 6 protons, 2 in shell 1, 4 in shell 2
            'Oxygen': (8, [2, 6]),          # 8 protons, 2 in shell 1, 6 in shell 2
            'Nitrogen': (7, [2, 5]),        # 7 protons, 2 in shell 1, 5 in shell 2
        }
        
        x_offset = 0
        for atom_name, (protons, shells) in atoms.items():
            # Create nucleus (size proportional to protons)
            nucleus_radius = 0.3 + (protons * 0.05)
            nucleus = self._create_sphere(
                nucleus_radius, 
                self.atom_colors['carbon'],  # Dark color for nucleus
                (x_offset, 0, 0)
            )
            meshes.append(nucleus)
            
            # Create electron shells
            shell_radius = 1.0
            for shell_num, electron_count in enumerate(shells, 1):
                shell_radius = 1.0 + (shell_num * 0.8)
                
                # Create electrons in shell
                for i in range(electron_count):
                    angle = (2 * np.pi * i) / electron_count
                    electron_pos = (
                        x_offset + shell_radius * np.cos(angle),
                        shell_radius * np.sin(angle),
                        0
                    )
                    electron = self._create_sphere(0.15, self.atom_colors['electron'], electron_pos)
                    meshes.append(electron)
                
                # Create orbital ring (visual guide)
                orbital = self._create_torus(
                    shell_radius, 0.02, 
                    [100, 100, 255, 128],  # Translucent blue
                    (x_offset, 0, 0)
                )
                meshes.append(orbital)
            
            x_offset += 5.0  # Space between atoms
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "atom_models.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: atom_models.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'atom_models.glb',
            'filepath': str(output_path),
            'model': 'Atomic Structure Models',
            'atoms': ['Hydrogen', 'Carbon', 'Oxygen', 'Nitrogen'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Shows nucleus and electron shell configuration for common atoms'
        }
    
    def generate_ionic_bonding(self) -> Dict[str, any]:
        """
        Generate ionic bonding model (NaCl formation)
        Shows electron transfer from Na to Cl
        """
        logger.info("Generating ionic bonding model...")
        
        meshes = []
        
        # Sodium atom (Na) - loses 1 electron
        na_nucleus = self._create_sphere(0.5, [255, 200, 0, 255], (-3, 0, 0))  # Yellow-orange
        meshes.append(na_nucleus)
        
        # Sodium electrons (2, 8, 1 configuration)
        for i in range(11):
            if i < 2:
                shell_radius = 1.0
            elif i < 10:
                shell_radius = 1.8
            else:
                shell_radius = 2.6
            
            angle = (2 * np.pi * i) / max(2 if i < 2 else (8 if i < 10 else 1), 1)
            electron_pos = (
                -3 + shell_radius * np.cos(angle),
                shell_radius * np.sin(angle),
                0
            )
            electron = self._create_sphere(0.12, self.atom_colors['electron'], electron_pos)
            meshes.append(electron)
        
        # Chlorine atom (Cl) - gains 1 electron
        cl_nucleus = self._create_sphere(0.5, [0, 255, 0, 255], (3, 0, 0))  # Green
        meshes.append(cl_nucleus)
        
        # Chlorine electrons (2, 8, 7 configuration)
        for i in range(17):
            if i < 2:
                shell_radius = 1.0
            elif i < 10:
                shell_radius = 1.8
            else:
                shell_radius = 2.6
            
            angle = (2 * np.pi * i) / max(2 if i < 2 else (8 if i < 10 else 7), 1)
            electron_pos = (
                3 + shell_radius * np.cos(angle),
                shell_radius * np.sin(angle),
                0
            )
            electron = self._create_sphere(0.12, self.atom_colors['electron'], electron_pos)
            meshes.append(electron)
        
        # Electron being transferred (between atoms)
        transferred_electron = self._create_sphere(
            0.15, [255, 0, 255, 255],  # Magenta for visibility
            (0, 0, 0)
        )
        meshes.append(transferred_electron)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "ionic_bonding.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: ionic_bonding.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'ionic_bonding.glb',
            'filepath': str(output_path),
            'model': 'Ionic Bonding (NaCl Formation)',
            'components': ['Sodium atom', 'Chlorine atom', 'Electron transfer'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Shows electron transfer in ionic bond formation between Na and Cl'
        }
    
    def generate_covalent_bonding(self) -> Dict[str, any]:
        """
        Generate covalent bonding models (H2O, CO2, CH4)
        Shows shared electron pairs
        """
        logger.info("Generating covalent bonding models...")
        
        meshes = []
        
        # === Water (H2O) ===
        # Oxygen atom
        oxygen = self._create_sphere(0.6, self.atom_colors['oxygen'], (-6, 0, 0))
        meshes.append(oxygen)
        
        # Hydrogen atoms (bent structure, 104.5° angle)
        h1_pos = (-6 - 1.5 * np.cos(np.radians(52)), 1.5 * np.sin(np.radians(52)), 0)
        h2_pos = (-6 - 1.5 * np.cos(np.radians(52)), -1.5 * np.sin(np.radians(52)), 0)
        
        h1 = self._create_sphere(0.3, self.atom_colors['hydrogen'], h1_pos)
        h2 = self._create_sphere(0.3, self.atom_colors['hydrogen'], h2_pos)
        meshes.extend([h1, h2])
        
        # Covalent bonds (shared electrons)
        bond1 = self._create_cylinder(0.1, 1.5, self.atom_colors['bond'], (-6, 0, 0), h1_pos)
        bond2 = self._create_cylinder(0.1, 1.5, self.atom_colors['bond'], (-6, 0, 0), h2_pos)
        meshes.extend([bond1, bond2])
        
        # === Carbon Dioxide (CO2) ===
        # Carbon atom
        carbon = self._create_sphere(0.5, self.atom_colors['carbon'], (0, 0, 0))
        meshes.append(carbon)
        
        # Oxygen atoms (linear structure)
        o1 = self._create_sphere(0.6, self.atom_colors['oxygen'], (-2, 0, 0))
        o2 = self._create_sphere(0.6, self.atom_colors['oxygen'], (2, 0, 0))
        meshes.extend([o1, o2])
        
        # Double bonds (2 cylinders each)
        bond_co1a = self._create_cylinder(0.08, 2, self.atom_colors['bond'], (0, 0.15, 0), (-2, 0.15, 0))
        bond_co1b = self._create_cylinder(0.08, 2, self.atom_colors['bond'], (0, -0.15, 0), (-2, -0.15, 0))
        bond_co2a = self._create_cylinder(0.08, 2, self.atom_colors['bond'], (0, 0.15, 0), (2, 0.15, 0))
        bond_co2b = self._create_cylinder(0.08, 2, self.atom_colors['bond'], (0, -0.15, 0), (2, -0.15, 0))
        meshes.extend([bond_co1a, bond_co1b, bond_co2a, bond_co2b])
        
        # === Methane (CH4) ===
        # Carbon atom
        c_ch4 = self._create_sphere(0.5, self.atom_colors['carbon'], (6, 0, 0))
        meshes.append(c_ch4)
        
        # Hydrogen atoms (tetrahedral structure)
        tetrahedral_positions = [
            (6 + 1.2, 1.2, 0),
            (6 - 1.2, 1.2, 0),
            (6, -1.2, 1.2),
            (6, -1.2, -1.2),
        ]
        
        for h_pos in tetrahedral_positions:
            h = self._create_sphere(0.3, self.atom_colors['hydrogen'], h_pos)
            meshes.append(h)
            bond = self._create_cylinder(0.1, 1.2, self.atom_colors['bond'], (6, 0, 0), h_pos)
            meshes.append(bond)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "covalent_bonding.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: covalent_bonding.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'covalent_bonding.glb',
            'filepath': str(output_path),
            'model': 'Covalent Bonding (H2O, CO2, CH4)',
            'molecules': ['Water (H2O)', 'Carbon Dioxide (CO2)', 'Methane (CH4)'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Shows shared electron pairs in covalent bonds with different molecular geometries'
        }
    
    def generate_metallic_bonding(self) -> Dict[str, any]:
        """
        Generate metallic bonding lattice structure
        Shows delocalized electron sea
        """
        logger.info("Generating metallic bonding model...")
        
        meshes = []
        
        # Create metal lattice (4x4x4 cubic structure)
        lattice_spacing = 1.5
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    pos = (x * lattice_spacing, y * lattice_spacing, z * lattice_spacing)
                    atom = self._create_sphere(0.3, [192, 192, 192, 255], pos)  # Silver color
                    meshes.append(atom)
        
        # Create delocalized electrons (electron sea)
        np.random.seed(42)  # For reproducibility
        for _ in range(30):
            x = np.random.uniform(0, 3 * lattice_spacing)
            y = np.random.uniform(0, 3 * lattice_spacing)
            z = np.random.uniform(0, 3 * lattice_spacing)
            electron = self._create_sphere(0.1, self.atom_colors['electron'], (x, y, z))
            meshes.append(electron)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "metallic_bonding.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: metallic_bonding.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'metallic_bonding.glb',
            'filepath': str(output_path),
            'model': 'Metallic Bonding Structure',
            'components': ['Metal atoms (lattice)', 'Delocalized electrons'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Shows metal lattice structure with delocalized electron sea'
        }
    
    def generate_hydrocarbon_series(self) -> Dict[str, any]:
        """
        Generate hydrocarbon series (CH4, C2H6, C3H8, C4H10)
        Alkane series showing increasing chain length
        """
        logger.info("Generating hydrocarbon series...")
        
        meshes = []
        x_offset = 0
        
        hydrocarbons = [
            ('CH4', 1),   # Methane
            ('C2H6', 2),  # Ethane
            ('C3H8', 3),  # Propane
            ('C4H10', 4), # Butane
        ]
        
        for name, carbon_count in hydrocarbons:
            # Create carbon chain
            carbon_spacing = 1.5
            carbon_positions = []
            for i in range(carbon_count):
                c_pos = (x_offset + i * carbon_spacing, 0, 0)
                carbon_positions.append(c_pos)
                carbon = self._create_sphere(0.4, self.atom_colors['carbon'], c_pos)
                meshes.append(carbon)
                
                # Bonds between carbons
                if i > 0:
                    bond = self._create_cylinder(
                        0.1, carbon_spacing, self.atom_colors['bond'],
                        carbon_positions[i-1], c_pos
                    )
                    meshes.append(bond)
            
            # Add hydrogen atoms
            for i, c_pos in enumerate(carbon_positions):
                # Terminal carbons get 3 H, middle carbons get 2 H
                h_count = 3 if (i == 0 or i == carbon_count - 1) else 2
                
                for j in range(h_count):
                    if h_count == 3:
                        # Tetrahedral positions for terminal carbons
                        if i == 0:  # First carbon
                            h_positions = [
                                (c_pos[0] - 0.8, c_pos[1] + 0.8, c_pos[2]),
                                (c_pos[0], c_pos[1] - 0.8, c_pos[2] + 0.8),
                                (c_pos[0], c_pos[1] - 0.8, c_pos[2] - 0.8),
                            ]
                        else:  # Last carbon
                            h_positions = [
                                (c_pos[0] + 0.8, c_pos[1] + 0.8, c_pos[2]),
                                (c_pos[0], c_pos[1] - 0.8, c_pos[2] + 0.8),
                                (c_pos[0], c_pos[1] - 0.8, c_pos[2] - 0.8),
                            ]
                    else:  # Middle carbons get 2 H
                        h_positions = [
                            (c_pos[0], c_pos[1] + 0.8, c_pos[2] + 0.8),
                            (c_pos[0], c_pos[1] + 0.8, c_pos[2] - 0.8),
                        ]
                    
                    h_pos = h_positions[j]
                    hydrogen = self._create_sphere(0.25, self.atom_colors['hydrogen'], h_pos)
                    meshes.append(hydrogen)
                    
                    # C-H bond
                    bond = self._create_cylinder(0.08, 0.8, self.atom_colors['bond'], c_pos, h_pos)
                    meshes.append(bond)
            
            x_offset += (carbon_count + 1) * carbon_spacing + 2
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "hydrocarbon_series.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: hydrocarbon_series.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'hydrocarbon_series.glb',
            'filepath': str(output_path),
            'model': 'Hydrocarbon Series (Alkanes)',
            'molecules': ['Methane (CH4)', 'Ethane (C2H6)', 'Propane (C3H8)', 'Butane (C4H10)'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Shows increasing carbon chain length in alkane homologous series'
        }
    
    def generate_benzene_ring(self) -> Dict[str, any]:
        """
        Generate benzene ring structure (C6H6)
        Shows aromatic compound with resonance
        """
        logger.info("Generating benzene ring...")
        
        meshes = []
        
        # Create hexagonal ring of carbons
        ring_radius = 1.5
        carbon_positions = []
        for i in range(6):
            angle = (2 * np.pi * i) / 6
            c_pos = (ring_radius * np.cos(angle), ring_radius * np.sin(angle), 0)
            carbon_positions.append(c_pos)
            carbon = self._create_sphere(0.4, self.atom_colors['carbon'], c_pos)
            meshes.append(carbon)
        
        # Create C-C bonds (alternating single/double bonds shown as thick/thin)
        for i in range(6):
            next_i = (i + 1) % 6
            # Alternate bond thickness to show resonance
            thickness = 0.12 if i % 2 == 0 else 0.08
            bond = self._create_cylinder(
                thickness, 
                np.linalg.norm(np.array(carbon_positions[next_i]) - np.array(carbon_positions[i])),
                self.atom_colors['bond'],
                carbon_positions[i],
                carbon_positions[next_i]
            )
            meshes.append(bond)
        
        # Add hydrogen atoms (one per carbon, pointing outward)
        for i, c_pos in enumerate(carbon_positions):
            angle = (2 * np.pi * i) / 6
            h_pos = (
                (ring_radius + 0.8) * np.cos(angle),
                (ring_radius + 0.8) * np.sin(angle),
                0
            )
            hydrogen = self._create_sphere(0.25, self.atom_colors['hydrogen'], h_pos)
            meshes.append(hydrogen)
            
            # C-H bond
            bond = self._create_cylinder(0.08, 0.8, self.atom_colors['bond'], c_pos, h_pos)
            meshes.append(bond)
        
        # Add delocalized pi electron cloud (torus above and below ring)
        pi_cloud_top = trimesh.creation.cylinder(radius=ring_radius * 0.9, height=0.1)
        pi_cloud_top.visual.vertex_colors = [255, 200, 0, 100]  # Translucent yellow
        pi_cloud_top.apply_translation((0, 0, 0.5))
        meshes.append(pi_cloud_top)
        
        pi_cloud_bottom = trimesh.creation.cylinder(radius=ring_radius * 0.9, height=0.1)
        pi_cloud_bottom.visual.vertex_colors = [255, 200, 0, 100]
        pi_cloud_bottom.apply_translation((0, 0, -0.5))
        meshes.append(pi_cloud_bottom)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "benzene_ring.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: benzene_ring.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'benzene_ring.glb',
            'filepath': str(output_path),
            'model': 'Benzene Ring (C6H6)',
            'components': ['6 Carbon atoms', '6 Hydrogen atoms', 'Delocalized pi electrons'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Shows aromatic benzene structure with resonance and delocalized electrons'
        }
    
    def generate_protein_structure(self) -> Dict[str, any]:
        """
        Generate protein structure showing primary to quaternary structure
        Simplified representation with alpha helix
        """
        logger.info("Generating protein structure...")
        
        meshes = []
        
        # Primary structure (amino acid chain represented as connected spheres)
        amino_acid_count = 20
        for i in range(amino_acid_count):
            # Create spiral (alpha helix)
            t = i * 0.5
            radius = 1.5
            height = 0.3
            x = radius * np.cos(t)
            y = radius * np.sin(t)
            z = i * height
            
            # Amino acid (represented as sphere)
            color = [100 + (i * 5), 100, 200, 255]  # Gradient color
            amino_acid = self._create_sphere(0.3, color, (x, y, z))
            meshes.append(amino_acid)
            
            # Peptide bond to next amino acid
            if i < amino_acid_count - 1:
                next_t = (i + 1) * 0.5
                next_x = radius * np.cos(next_t)
                next_y = radius * np.sin(next_t)
                next_z = (i + 1) * height
                
                bond = self._create_cylinder(
                    0.1, 
                    np.sqrt((next_x - x)**2 + (next_y - y)**2 + (next_z - z)**2),
                    self.atom_colors['bond'],
                    (x, y, z),
                    (next_x, next_y, next_z)
                )
                meshes.append(bond)
        
        # Add secondary structure indicators (beta sheets as flat ribbons)
        sheet_y_offset = 5
        for i in range(5):
            for j in range(3):
                x = i * 0.8 - 2
                y = sheet_y_offset
                z = j * 0.5
                strand = trimesh.creation.box(extents=[0.3, 0.1, 1.5])
                strand.visual.vertex_colors = [200, 150, 100, 255]
                strand.apply_translation((x, y, z))
                meshes.append(strand)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "protein_structure.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: protein_structure.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'protein_structure.glb',
            'filepath': str(output_path),
            'model': 'Protein Structure',
            'components': ['Alpha helix', 'Beta sheet', 'Amino acid chain'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Shows protein secondary structures: alpha helix and beta sheets'
        }
    
    def generate_dna_helix(self) -> Dict[str, any]:
        """
        Generate DNA double helix structure
        Shows sugar-phosphate backbone and base pairs
        """
        logger.info("Generating DNA helix...")
        
        meshes = []
        
        # Parameters for double helix
        turns = 2
        points_per_turn = 10
        total_points = turns * points_per_turn
        radius = 1.5
        pitch = 3.0  # Height per turn
        
        strand1_positions = []
        strand2_positions = []
        
        # Create two strands
        for i in range(total_points):
            t = (2 * np.pi * i) / points_per_turn
            z = (pitch * i) / points_per_turn
            
            # Strand 1 (sugar-phosphate backbone)
            x1 = radius * np.cos(t)
            y1 = radius * np.sin(t)
            strand1_positions.append((x1, y1, z))
            backbone1 = self._create_sphere(0.25, self.atom_colors['phosphorus'], (x1, y1, z))
            meshes.append(backbone1)
            
            # Strand 2 (opposite side)
            x2 = radius * np.cos(t + np.pi)
            y2 = radius * np.sin(t + np.pi)
            strand2_positions.append((x2, y2, z))
            backbone2 = self._create_sphere(0.25, self.atom_colors['phosphorus'], (x2, y2, z))
            meshes.append(backbone2)
            
            # Connect backbones
            if i > 0:
                # Strand 1 connections
                bond1 = self._create_cylinder(
                    0.08,
                    np.linalg.norm(np.array(strand1_positions[i]) - np.array(strand1_positions[i-1])),
                    self.atom_colors['bond'],
                    strand1_positions[i-1],
                    strand1_positions[i]
                )
                meshes.append(bond1)
                
                # Strand 2 connections
                bond2 = self._create_cylinder(
                    0.08,
                    np.linalg.norm(np.array(strand2_positions[i]) - np.array(strand2_positions[i-1])),
                    self.atom_colors['bond'],
                    strand2_positions[i-1],
                    strand2_positions[i]
                )
                meshes.append(bond2)
            
            # Base pairs (connecting the two strands)
            # Alternate colors for different base pairs (A-T, G-C)
            if i % 2 == 0:
                base_color = [255, 0, 0, 255]  # Red (A-T)
            else:
                base_color = [0, 0, 255, 255]  # Blue (G-C)
            
            # Create base on strand 1
            base1_pos = ((x1 + x2) / 2 * 0.6, (y1 + y2) / 2 * 0.6, z)
            base1 = self._create_sphere(0.2, base_color, base1_pos)
            meshes.append(base1)
            
            # Create base on strand 2
            base2_pos = ((x1 + x2) / 2 * 1.4, (y1 + y2) / 2 * 1.4, z)
            base2 = self._create_sphere(0.2, base_color, base2_pos)
            meshes.append(base2)
            
            # Hydrogen bonds between bases
            h_bond = self._create_cylinder(
                0.06,
                np.linalg.norm(np.array(base2_pos) - np.array(base1_pos)),
                [200, 200, 0, 255],  # Yellow for H-bonds
                base1_pos,
                base2_pos
            )
            meshes.append(h_bond)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        
        # Save model
        output_path = self.output_dir / "dna_helix.glb"
        combined.export(str(output_path))
        
        file_size_kb = output_path.stat().st_size / 1024
        logger.info(f"✅ Generated: dna_helix.glb ({file_size_kb:.2f} KB)")
        
        return {
            'filename': 'dna_helix.glb',
            'filepath': str(output_path),
            'model': 'DNA Double Helix',
            'components': ['Sugar-phosphate backbone (2 strands)', 'Base pairs (A-T, G-C)', 'Hydrogen bonds'],
            'vertices': len(combined.vertices),
            'faces': len(combined.faces),
            'file_size_kb': file_size_kb,
            'educational_notes': 'Shows DNA double helix with complementary base pairing and hydrogen bonds'
        }
    
    def generate_all_molecular_models(self) -> List[Dict[str, any]]:
        """Generate all 8 molecular structure models"""
        logger.info("🧪 Generating all molecular structure models...")
        
        models = []
        models.append(self.generate_atom_models())
        models.append(self.generate_ionic_bonding())
        models.append(self.generate_covalent_bonding())
        models.append(self.generate_metallic_bonding())
        models.append(self.generate_hydrocarbon_series())
        models.append(self.generate_benzene_ring())
        models.append(self.generate_protein_structure())
        models.append(self.generate_dna_helix())
        
        logger.info(f"✅ Generated {len(models)} molecular models")
        
        return models
    
    def generate_manifest(self, models: List[Dict[str, any]]) -> str:
        """Generate manifest file for all molecular models"""
        manifest = {
            "collection": "Molecular and Atomic Structures",
            "priority": 3,
            "exam_weight": "Very High",
            "subject": "Chemistry",
            "topic_codes": ["chem_001", "chem_004"],
            "grade_levels": ["SS1", "SS2", "SS3"],
            "curriculum_standards": ["WAEC", "NECO"],
            "total_models": len(models),
            "models": []
        }
        
        for model in models:
            manifest["models"].append({
                "filename": model['filename'],
                "filepath": model['filepath'],
                "model": model['model'],
                "components": model.get('components', model.get('atoms', model.get('molecules', []))),
                "exam_topics": ["chem_001", "chem_004"],
                "grade_levels": ["SS1", "SS2", "SS3"],
                "vertices": model['vertices'],
                "faces": model['faces'],
                "file_size_kb": model['file_size_kb'],
                "educational_notes": model['educational_notes'],
                "ar_ready": True,
                "curriculum_standard": ["WAEC", "NECO"]
            })
        
        manifest_path = self.output_dir / "molecular_models_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"📋 Manifest created: {manifest_path}")
        return str(manifest_path)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate molecular structure 3D models')
    parser.add_argument('--model', type=str, default='all',
                       choices=['all', 'atoms', 'ionic', 'covalent', 'metallic', 
                               'hydrocarbons', 'benzene', 'protein', 'dna'],
                       help='Which model to generate')
    
    args = parser.parse_args()
    
    generator = MolecularModelGenerator()
    
    if args.model == 'all':
        models = generator.generate_all_molecular_models()
        generator.generate_manifest(models)
        
        total_size = sum(m['file_size_kb'] for m in models)
        print(f"\n📊 Generation Statistics:")
        print(f"   Models: {len(models)}")
        print(f"   Total Size: {total_size:.2f} KB")
        print(f"   Models: {', '.join(m['model'] for m in models)}")
    else:
        model_map = {
            'atoms': generator.generate_atom_models,
            'ionic': generator.generate_ionic_bonding,
            'covalent': generator.generate_covalent_bonding,
            'metallic': generator.generate_metallic_bonding,
            'hydrocarbons': generator.generate_hydrocarbon_series,
            'benzene': generator.generate_benzene_ring,
            'protein': generator.generate_protein_structure,
            'dna': generator.generate_dna_helix,
        }
        
        result = model_map[args.model]()
        print(f"\n✅ Generated: {result['filename']} ({result['file_size_kb']:.2f} KB)")
