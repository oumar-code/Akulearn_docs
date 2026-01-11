# Graphics and Shapes Generation Strategy

## Executive Summary

This document outlines a comprehensive strategy for generating educational graphics, diagrams, and 3D shapes using Python libraries to support the Akulearn curriculum. We'll leverage existing infrastructure and extend it with specialized tools for 2D/3D visualizations.

---

## Current State Analysis

### ✅ Already Implemented
1. **Phase 3 Diagrams** (100 SVG diagrams)
   - Venn diagrams, flowcharts, circuits, chemical reactions
   - Using: SVG generation, matplotlib
   
2. **Phase 2 Graphs** (70 files)
   - Mathematical graphs, charts, statistical visualizations
   - Using: matplotlib, custom SVG generators

3. **Image Generation**
   - Lesson images via Stable Diffusion/Gemini
   - Tools: `batch_image_generator.py`, `stable_image_client.py`

### 🎯 Gaps Identified

Based on curriculum analysis and 3D assets priority plan:

1. **3D Models** - Biological, chemical, physical structures
2. **Interactive Animations** - Process visualizations
3. **Mathematical 3D Shapes** - Geometry visualization
4. **Scientific Simulations** - Physics/chemistry processes
5. **Anatomical Diagrams** - Biology systems
6. **Molecular Structures** - 3D chemistry models
7. **Geographic/Topographic** - Nigerian maps, terrain

---

## Python Libraries Selection

### Tier 1: Production-Ready (Install Now)

#### **matplotlib** ✅ (Already in use)
```bash
pip install matplotlib
```
**Use Cases:**
- 2D graphs, charts, plots
- Statistical visualizations
- Function plotting
- Data representation

**Examples:**
- Trigonometric functions
- Statistical distributions
- Coordinate geometry
- Data trends

---

#### **plotly** ✅ (Already in use)
```bash
pip install plotly kaleido
```
**Use Cases:**
- Interactive 3D plots
- Dynamic visualizations
- WebGL-based graphics
- Dashboard charts

**Examples:**
- 3D surface plots
- Interactive molecular structures
- Animated process diagrams
- Data exploration tools

---

#### **Pillow (PIL)** ✅ (Already in use)
```bash
pip install Pillow
```
**Use Cases:**
- Image manipulation
- Diagram composition
- Text overlays
- Image processing

**Examples:**
- Adding labels to diagrams
- Combining multiple images
- Creating infographics
- Image optimization

---

#### **VPython**
```bash
pip install vpython
```
**Use Cases:**
- 3D physics simulations
- Interactive 3D models
- Motion visualization
- Force diagrams

**Examples:**
- Projectile motion
- Circular motion
- Simple harmonic motion
- Electric field visualization

**Priority Models:**
- Pendulum motion
- Spring systems
- Planetary orbits
- Wave propagation

---

#### **py3Dmol**
```bash
pip install py3Dmol
```
**Use Cases:**
- Molecular visualization
- Chemical structures
- Protein models
- Interactive 3D chemistry

**Examples:**
- Hydrocarbon molecules
- DNA structure
- Amino acids
- Chemical bonds

**Priority Models:**
- Water (H₂O), methane (CH₄)
- Benzene ring
- DNA double helix
- Protein structures

---

### Tier 2: Specialized Libraries

#### **trimesh**
```bash
pip install trimesh
```
**Use Cases:**
- 3D mesh manipulation
- GLB/STL file creation
- Geometric operations
- 3D model processing

**Priority Shapes:**
- Cube, sphere, cylinder, cone
- Prisms, pyramids
- Composite solids
- Frustums

---

#### **pyglet + moderngl**
```bash
pip install pyglet moderngl
```
**Use Cases:**
- OpenGL rendering
- High-performance 3D
- Real-time rendering
- Complex visualizations

**Priority Applications:**
- Interactive 3D viewers
- Real-time simulations
- AR/VR content preparation
- Performance-critical renders

---

#### **manim (Mathematical Animation Engine)**
```bash
pip install manim
```
**Use Cases:**
- Mathematical animations
- Concept visualization
- Educational videos
- Process demonstrations

**Priority Animations:**
- Geometric transformations
- Calculus concepts (limits, derivatives)
- Trigonometric functions
- Algebraic operations

---

#### **RDKit**
```bash
pip install rdkit-pypi
```
**Use Cases:**
- Advanced chemistry
- Molecular structures
- Chemical reactions
- Drug design visualization

**Priority Structures:**
- Organic compounds
- Functional groups
- Reaction mechanisms
- 3D molecular conformations

---

#### **Biopython + nglview**
```bash
pip install biopython nglview
```
**Use Cases:**
- Biological structures
- DNA/RNA visualization
- Protein modeling
- Sequence analysis

**Priority Models:**
- DNA structure
- Protein folding
- Cell components
- Biological processes

---

### Tier 3: Advanced (Future Consideration)

#### **Blender Python API (bpy)**
**Use Cases:**
- Professional 3D modeling
- Animation rendering
- Complex scenes
- High-quality assets

**Note:** Requires Blender installation

#### **Open3D**
```bash
pip install open3d
```
**Use Cases:**
- Point cloud processing
- 3D reconstruction
- Mesh operations
- Computer vision

---

## Implementation Strategy

### Phase 1: 2D Graphics Enhancement (Weeks 1-4)

#### **Goal:** Generate all 2D educational diagrams

#### **Libraries:** matplotlib, plotly, Pillow

#### **Deliverables:**

**1. Mathematics Diagrams**
```python
# File: src/backend/generators/math_diagrams.py
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

class MathDiagramGenerator:
    """Generate mathematical diagrams for lessons"""
    
    def __init__(self, output_dir="generated_assets/math_diagrams"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_trigonometric_functions(self):
        """Generate sine, cosine, tangent graphs"""
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        x = np.linspace(-2*np.pi, 2*np.pi, 1000)
        
        # Sine wave
        axes[0].plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
        axes[0].grid(True, alpha=0.3)
        axes[0].axhline(y=0, color='k', linewidth=0.5)
        axes[0].axvline(x=0, color='k', linewidth=0.5)
        axes[0].set_ylabel('y', fontsize=12)
        axes[0].set_title('Sine Function', fontsize=14, fontweight='bold')
        axes[0].legend()
        
        # Cosine wave
        axes[1].plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
        axes[1].grid(True, alpha=0.3)
        axes[1].axhline(y=0, color='k', linewidth=0.5)
        axes[1].axvline(x=0, color='k', linewidth=0.5)
        axes[1].set_ylabel('y', fontsize=12)
        axes[1].set_title('Cosine Function', fontsize=14, fontweight='bold')
        axes[1].legend()
        
        # Tangent wave
        axes[2].plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
        axes[2].set_ylim(-5, 5)
        axes[2].grid(True, alpha=0.3)
        axes[2].axhline(y=0, color='k', linewidth=0.5)
        axes[2].axvline(x=0, color='k', linewidth=0.5)
        axes[2].set_xlabel('x (radians)', fontsize=12)
        axes[2].set_ylabel('y', fontsize=12)
        axes[2].set_title('Tangent Function', fontsize=14, fontweight='bold')
        axes[2].legend()
        
        plt.tight_layout()
        output_path = self.output_dir / "trigonometric_functions.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def generate_quadratic_function(self, a=1, b=0, c=0):
        """Generate parabola for quadratic equations"""
        x = np.linspace(-10, 10, 500)
        y = a * x**2 + b * x + c
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(x, y, 'b-', linewidth=2, label=f'y = {a}x² + {b}x + {c}')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        
        # Mark vertex
        vertex_x = -b / (2*a)
        vertex_y = a * vertex_x**2 + b * vertex_x + c
        ax.plot(vertex_x, vertex_y, 'ro', markersize=10, label=f'Vertex ({vertex_x:.2f}, {vertex_y:.2f})')
        
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title('Quadratic Function', fontsize=14, fontweight='bold')
        ax.legend()
        
        output_path = self.output_dir / f"quadratic_{a}_{b}_{c}.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def generate_circle_theorem(self):
        """Generate circle with angle properties"""
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Draw circle
        circle = plt.Circle((0, 0), 5, fill=False, color='blue', linewidth=2)
        ax.add_patch(circle)
        
        # Draw inscribed angle
        angles = [0, 60, 180]  # degrees
        points = [(5*np.cos(np.radians(a)), 5*np.sin(np.radians(a))) for a in angles]
        
        # Draw triangle
        triangle = plt.Polygon(points, fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(triangle)
        
        # Mark points
        for i, point in enumerate(points):
            ax.plot(point[0], point[1], 'ro', markersize=8)
            ax.text(point[0]*1.15, point[1]*1.15, f'P{i+1}', fontsize=12, ha='center')
        
        # Mark center
        ax.plot(0, 0, 'ko', markersize=8)
        ax.text(0.3, 0.3, 'O', fontsize=12)
        
        ax.set_xlim(-7, 7)
        ax.set_ylim(-7, 7)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('Circle Theorem - Inscribed Angle', fontsize=14, fontweight='bold')
        
        output_path = self.output_dir / "circle_theorem.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
```

**2. Statistical Diagrams**
```python
def generate_histogram(self, data, bins=10, title="Frequency Distribution"):
    """Generate histogram for statistics lessons"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(data, bins=bins, edgecolor='black', alpha=0.7, color='skyblue')
    ax.set_xlabel('Value', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add mean line
    mean_val = np.mean(data)
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
    ax.legend()
    
    output_path = self.output_dir / f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return str(output_path)

def generate_box_plot(self, datasets, labels, title="Box Plot Comparison"):
    """Generate box plot for data analysis"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bp = ax.boxplot(datasets, labels=labels, patch_artist=True)
    
    # Color boxes
    colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    ax.set_ylabel('Values', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    output_path = self.output_dir / f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return str(output_path)
```

---

### Phase 2: 3D Shapes and Models (Weeks 5-8)

#### **Goal:** Generate 3D geometric shapes and basic models

#### **Libraries:** trimesh, plotly, vpython

#### **Deliverables:**

**1. Geometric 3D Shapes**
```python
# File: src/backend/generators/shape_3d_generator.py
import trimesh
import numpy as np
from pathlib import Path
import plotly.graph_objects as go

class Shape3DGenerator:
    """Generate 3D geometric shapes for mathematics lessons"""
    
    def __init__(self, output_dir="content/ar_assets/geometric_shapes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_cube(self, side_length=2.0):
        """Generate a cube mesh"""
        # Create cube
        cube = trimesh.creation.box(extents=[side_length] * 3)
        
        # Add colors
        cube.visual.face_colors = [100, 150, 200, 200]
        
        # Export as GLB
        output_path = self.output_dir / f"cube_{side_length}.glb"
        cube.export(output_path)
        
        return str(output_path)
    
    def generate_sphere(self, radius=1.0, subdivisions=3):
        """Generate a sphere mesh"""
        sphere = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
        sphere.visual.face_colors = [200, 100, 150, 200]
        
        output_path = self.output_dir / f"sphere_r{radius}.glb"
        sphere.export(output_path)
        
        return str(output_path)
    
    def generate_cylinder(self, radius=1.0, height=3.0, sections=32):
        """Generate a cylinder mesh"""
        cylinder = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
        cylinder.visual.face_colors = [150, 200, 100, 200]
        
        output_path = self.output_dir / f"cylinder_r{radius}_h{height}.glb"
        cylinder.export(output_path)
        
        return str(output_path)
    
    def generate_cone(self, radius=1.0, height=2.0, sections=32):
        """Generate a cone mesh"""
        cone = trimesh.creation.cone(radius=radius, height=height, sections=sections)
        cone.visual.face_colors = [200, 150, 100, 200]
        
        output_path = self.output_dir / f"cone_r{radius}_h{height}.glb"
        cone.export(output_path)
        
        return str(output_path)
    
    def generate_pyramid(self, base_size=2.0, height=3.0):
        """Generate a square pyramid"""
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
            [0, 1, 2], [0, 2, 3],  # Base
            [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]  # Sides
        ])
        
        pyramid = trimesh.Trimesh(vertices=vertices, faces=faces)
        pyramid.visual.face_colors = [255, 200, 100, 200]
        
        output_path = self.output_dir / f"pyramid_{base_size}_{height}.glb"
        pyramid.export(output_path)
        
        return str(output_path)
    
    def generate_prism(self, base_sides=6, base_radius=1.0, height=2.0):
        """Generate a prism (hexagonal by default)"""
        prism = trimesh.creation.cylinder(
            radius=base_radius,
            height=height,
            sections=base_sides
        )
        prism.visual.face_colors = [100, 200, 200, 200]
        
        output_path = self.output_dir / f"prism_{base_sides}sided_h{height}.glb"
        prism.export(output_path)
        
        return str(output_path)
    
    def generate_all_basic_shapes(self):
        """Generate all basic 3D shapes"""
        shapes = []
        
        shapes.append(("Cube", self.generate_cube(2.0)))
        shapes.append(("Sphere", self.generate_sphere(1.0)))
        shapes.append(("Cylinder", self.generate_cylinder(1.0, 3.0)))
        shapes.append(("Cone", self.generate_cone(1.0, 2.0)))
        shapes.append(("Pyramid", self.generate_pyramid(2.0, 3.0)))
        shapes.append(("Hexagonal Prism", self.generate_prism(6, 1.0, 2.0)))
        shapes.append(("Triangular Prism", self.generate_prism(3, 1.0, 2.0)))
        
        return shapes
```

**2. Interactive 3D Visualizations**
```python
def generate_interactive_3d_plot(self, func_type='surface'):
    """Generate interactive 3D plots using Plotly"""
    if func_type == 'surface':
        # Create surface plot
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(np.sqrt(X**2 + Y**2))
        
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
        fig.update_layout(
            title='3D Surface Plot: z = sin(√(x² + y²))',
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z'
            ),
            width=800,
            height=800
        )
        
        output_path = self.output_dir / "interactive_surface.html"
        fig.write_html(output_path)
        
        return str(output_path)
```

---

### Phase 3: Scientific Visualizations (Weeks 9-12)

#### **Goal:** Generate chemistry, physics, and biology visualizations

#### **Libraries:** py3Dmol, vpython, RDKit, Biopython

#### **Deliverables:**

**1. Chemistry Molecular Structures**
```python
# File: src/backend/generators/chemistry_models.py
from rdkit import Chem
from rdkit.Chem import AllChem, Draw
import py3Dmol
import json
from pathlib import Path

class ChemistryModelGenerator:
    """Generate 3D molecular structures for chemistry lessons"""
    
    def __init__(self, output_dir="content/ar_assets/molecules"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_molecule_3d(self, smiles, name):
        """Generate 3D model from SMILES notation"""
        # Create molecule from SMILES
        mol = Chem.MolFromSmiles(smiles)
        
        if mol is None:
            raise ValueError(f"Invalid SMILES: {smiles}")
        
        # Add hydrogens and generate 3D coordinates
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=42)
        AllChem.MMFFOptimizeMolecule(mol)
        
        # Export to MOL format
        mol_block = Chem.MolToMolBlock(mol)
        
        # Save MOL file
        mol_path = self.output_dir / f"{name}.mol"
        with open(mol_path, 'w') as f:
            f.write(mol_block)
        
        # Generate 2D structure image
        img = Draw.MolToImage(mol, size=(400, 400))
        img_path = self.output_dir / f"{name}_2d.png"
        img.save(img_path)
        
        # Create metadata
        metadata = {
            "name": name,
            "smiles": smiles,
            "mol_file": str(mol_path),
            "image_2d": str(img_path),
            "formula": Chem.rdMolDescriptors.CalcMolFormula(mol),
            "molecular_weight": Chem.rdMolDescriptors.CalcExactMolWt(mol),
            "num_atoms": mol.GetNumAtoms(),
            "num_bonds": mol.GetNumBonds()
        }
        
        metadata_path = self.output_dir / f"{name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return metadata
    
    def generate_hydrocarbons(self):
        """Generate common hydrocarbon molecules"""
        hydrocarbons = [
            ("C", "methane"),
            ("CC", "ethane"),
            ("CCC", "propane"),
            ("CCCC", "butane"),
            ("C=C", "ethene"),
            ("C=CC", "propene"),
            ("c1ccccc1", "benzene"),
        ]
        
        generated = []
        for smiles, name in hydrocarbons:
            try:
                metadata = self.generate_molecule_3d(smiles, name)
                generated.append(metadata)
                print(f"✅ Generated {name}")
            except Exception as e:
                print(f"❌ Failed {name}: {e}")
        
        return generated
    
    def generate_common_molecules(self):
        """Generate common molecules for chemistry lessons"""
        molecules = [
            ("O", "water"),
            ("O=C=O", "carbon_dioxide"),
            ("N#N", "nitrogen"),
            ("[O-][N+](=O)c1ccccc1", "nitrobenzene"),
            ("CC(=O)O", "acetic_acid"),
            ("C(C(=O)O)N", "glycine"),
            ("c1ccc(cc1)O", "phenol"),
        ]
        
        generated = []
        for smiles, name in molecules:
            try:
                metadata = self.generate_molecule_3d(smiles, name)
                generated.append(metadata)
                print(f"✅ Generated {name}")
            except Exception as e:
                print(f"❌ Failed {name}: {e}")
        
        return generated
```

**2. Physics Simulations**
```python
# File: src/backend/generators/physics_simulations.py
from vpython import *
import json
from pathlib import Path

class PhysicsSimulationGenerator:
    """Generate physics simulations and animations"""
    
    def __init__(self, output_dir="content/simulations/physics"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_pendulum_html(self):
        """Generate simple harmonic motion pendulum"""
        html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple Pendulum Simulation</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
    <style>
        body { margin: 0; padding: 20px; font-family: Arial; }
        canvas { border: 1px solid #ddd; }
        .controls { margin-top: 10px; }
    </style>
</head>
<body>
    <h2>Simple Pendulum - Simple Harmonic Motion</h2>
    <div id="canvas-container"></div>
    <div class="controls">
        <label>Length: <input type="range" id="length" min="100" max="300" value="200" /></label>
        <label>Angle: <input type="range" id="angle" min="10" max="90" value="45" /></label>
        <button onclick="reset()">Reset</button>
    </div>
    
    <script>
        let angle, angleV = 0, angleA = 0;
        let length = 200;
        const gravity = 0.5;
        const damping = 0.995;
        
        function setup() {
            createCanvas(800, 600).parent('canvas-container');
            angle = PI / 4;
        }
        
        function draw() {
            background(240);
            translate(width / 2, 50);
            
            // Physics
            angleA = (-gravity / length) * sin(angle);
            angleV += angleA;
            angleV *= damping;
            angle += angleV;
            
            // Draw rod
            let bobX = length * sin(angle);
            let bobY = length * cos(angle);
            stroke(0);
            strokeWeight(2);
            line(0, 0, bobX, bobY);
            
            // Draw bob
            fill(200, 50, 50);
            ellipse(bobX, bobY, 40, 40);
            
            // Draw pivot
            fill(100);
            ellipse(0, 0, 10, 10);
            
            // Display info
            fill(0);
            noStroke();
            text(`Angle: ${(angle * 180 / PI).toFixed(1)}°`, -380, 550);
            text(`Length: ${length}px`, -380, 570);
        }
        
        function reset() {
            length = document.getElementById('length').value;
            angle = radians(document.getElementById('angle').value);
            angleV = 0;
        }
    </script>
</body>
</html>
        '''
        
        output_path = self.output_dir / "pendulum_simulation.html"
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return str(output_path)
```

---

### Phase 4: Biology and Anatomy (Weeks 13-16)

#### **Goal:** Generate biological structures and anatomical models

#### **Libraries:** trimesh, Biopython, custom modeling

**Priority Models:**
1. Human digestive system
2. Circulatory system (heart, blood vessels)
3. Respiratory system (lungs)
4. Plant cell structure
5. DNA helix

**Strategy:** 
- Use trimesh for basic organ shapes
- Create custom meshes for complex structures
- Export to GLB for AR/VR compatibility

---

## Integration Plan

### **Step 1: Create Unified Generator Interface**

```python
# File: src/backend/generators/asset_generator_manager.py
from typing import List, Dict, Any
from pathlib import Path
import json

class AssetGeneratorManager:
    """Central manager for all asset generation"""
    
    def __init__(self):
        self.generators = {}
        self.register_generators()
    
    def register_generators(self):
        """Register all available generators"""
        from .math_diagrams import MathDiagramGenerator
        from .shape_3d_generator import Shape3DGenerator
        from .chemistry_models import ChemistryModelGenerator
        from .physics_simulations import PhysicsSimulationGenerator
        
        self.generators['math_2d'] = MathDiagramGenerator()
        self.generators['shapes_3d'] = Shape3DGenerator()
        self.generators['chemistry'] = ChemistryModelGenerator()
        self.generators['physics'] = PhysicsSimulationGenerator()
    
    def generate_for_lesson(self, lesson: Dict[str, Any]) -> List[str]:
        """Generate all applicable assets for a lesson"""
        subject = lesson.get('subject', '').lower()
        topic = lesson.get('topic', '').lower()
        generated_assets = []
        
        # Mathematics
        if subject == 'mathematics':
            if 'trigonometry' in topic:
                asset_path = self.generators['math_2d'].generate_trigonometric_functions()
                generated_assets.append(asset_path)
            elif 'quadratic' in topic:
                asset_path = self.generators['math_2d'].generate_quadratic_function()
                generated_assets.append(asset_path)
        
        # Chemistry
        elif subject == 'chemistry':
            if 'hydrocarbon' in topic or 'organic' in topic:
                assets = self.generators['chemistry'].generate_hydrocarbons()
                generated_assets.extend([a['mol_file'] for a in assets])
        
        # Physics
        elif subject == 'physics':
            if 'motion' in topic or 'pendulum' in topic:
                asset_path = self.generators['physics'].generate_pendulum_html()
                generated_assets.append(asset_path)
        
        return generated_assets
    
    def generate_all_priority_assets(self):
        """Generate all high-priority assets from 3D Assets Priority Plan"""
        results = {
            'geometric_shapes': [],
            'chemistry_molecules': [],
            'physics_simulations': []
        }
        
        # Generate geometric shapes
        print("🎨 Generating geometric shapes...")
        shapes = self.generators['shapes_3d'].generate_all_basic_shapes()
        results['geometric_shapes'] = shapes
        
        # Generate chemistry molecules
        print("⚗️ Generating chemistry molecules...")
        hydrocarbons = self.generators['chemistry'].generate_hydrocarbons()
        molecules = self.generators['chemistry'].generate_common_molecules()
        results['chemistry_molecules'] = hydrocarbons + molecules
        
        # Generate physics simulations
        print("🔬 Generating physics simulations...")
        pendulum = self.generators['physics'].generate_pendulum_html()
        results['physics_simulations'] = [pendulum]
        
        # Save manifest
        manifest_path = Path("generated_assets/graphics_manifest.json")
        with open(manifest_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Generated {sum(len(v) for v in results.values())} assets")
        print(f"📄 Manifest saved: {manifest_path}")
        
        return results
```

### **Step 2: Add to Skills System**

Update `skill_definitions.json`:
```json
{
  "graphics_generator": {
    "id": "graphics_generator",
    "name": "Graphics and Shapes Generator",
    "description": "Generate 2D diagrams, 3D models, and scientific visualizations for lessons",
    "category": "content_generation",
    "complexity": "medium",
    "required_context": ["subject", "topic", "asset_type"],
    "optional_context": ["dimensions", "style", "format"],
    "tools": ["src/backend/generators/asset_generator_manager.py"],
    "output_format": "asset_manifest",
    "estimated_duration": "2-10 minutes",
    "dependencies": [],
    "instruction_template": "graphics_generation_instructions.md"
  }
}
```

---

## Installation Script

```python
# File: install_graphics_libraries.py
import subprocess
import sys

def install_packages():
    """Install all required graphics libraries"""
    
    packages = [
        # Tier 1: Production-Ready
        "matplotlib",
        "plotly",
        "kaleido",  # For plotly static exports
        "Pillow",
        "vpython",
        "py3Dmol",
        
        # Tier 2: Specialized
        "trimesh",
        "pyglet",
        "moderngl",
        "manim",
        "rdkit-pypi",
        "biopython",
        "nglview",
        
        # Tier 3: Advanced (optional)
        # "open3d",  # Uncomment if needed
    ]
    
    print("📦 Installing graphics and 3D libraries...\n")
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed\n")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}\n")
    
    print("✅ Installation complete!")
    print("\nVerifying installations...")
    
    # Verify imports
    imports_to_test = {
        "matplotlib": "matplotlib.pyplot",
        "plotly": "plotly.graph_objects",
        "PIL": "Pillow",
        "vpython": "vpython",
        "py3Dmol": "py3Dmol",
        "trimesh": "trimesh",
    }
    
    for module_name, package_name in imports_to_test.items():
        try:
            __import__(module_name)
            print(f"✅ {package_name} ready")
        except ImportError:
            print(f"❌ {package_name} not available")

if __name__ == "__main__":
    install_packages()
```

---

## Usage Examples

### Generate All Priority Assets
```bash
python src/backend/generators/asset_generator_manager.py
```

### Generate for Specific Subject
```python
from src.backend.generators.asset_generator_manager import AssetGeneratorManager

manager = AssetGeneratorManager()

# Generate mathematics assets
lesson = {
    "subject": "Mathematics",
    "topic": "Trigonometry",
    "grade_level": "SS2"
}

assets = manager.generate_for_lesson(lesson)
print(f"Generated {len(assets)} assets")
```

### Use with Skills System
```bash
python src/backend/akulearn_skills.py execute graphics_generator \
    --subject Mathematics \
    --topic "Quadratic Equations" \
    --asset_type "2d_diagram"
```

---

## Output Structure

```
generated_assets/
├── math_diagrams/
│   ├── trigonometric_functions.png
│   ├── quadratic_1_0_0.png
│   ├── circle_theorem.png
│   └── ...
├── geometric_shapes/ (GLB files)
│   ├── cube_2.0.glb
│   ├── sphere_r1.0.glb
│   ├── cylinder_r1.0_h3.0.glb
│   └── ...
├── molecules/
│   ├── methane.mol
│   ├── methane_2d.png
│   ├── methane_metadata.json
│   └── ...
├── simulations/
│   ├── pendulum_simulation.html
│   ├── projectile_motion.html
│   └── ...
└── graphics_manifest.json
```

---

## Quality Standards

### For 2D Graphics
- **Resolution:** Minimum 300 DPI
- **Format:** PNG with transparency
- **Size:** Optimized < 500KB
- **Labels:** Clear, readable, Nigerian English

### For 3D Models
- **Format:** GLB (binary glTF)
- **Polygon Count:** < 50,000 triangles
- **File Size:** < 5MB
- **Texture Resolution:** 1024x1024 max
- **Features:** Labeled parts, proper scaling

### For Animations
- **Format:** HTML5/WebGL or MP4
- **Duration:** 30-120 seconds
- **FPS:** 30fps minimum
- **Controls:** Play/pause, speed control

---

## Performance Optimization

1. **Lazy Loading:** Generate on-demand
2. **Caching:** Cache generated assets
3. **CDN Delivery:** Serve from CDN
4. **Progressive Loading:** Load low-res first
5. **Batch Generation:** Generate in batches

---

## Monitoring and Metrics

```python
class AssetGenerationMetrics:
    """Track asset generation performance"""
    
    def __init__(self):
        self.generation_times = {}
        self.success_rates = {}
        self.file_sizes = {}
    
    def track_generation(self, asset_type, duration, success, file_size):
        if asset_type not in self.generation_times:
            self.generation_times[asset_type] = []
            self.success_rates[asset_type] = []
            self.file_sizes[asset_type] = []
        
        self.generation_times[asset_type].append(duration)
        self.success_rates[asset_type].append(1 if success else 0)
        self.file_sizes[asset_type].append(file_size)
    
    def get_report(self):
        report = {}
        for asset_type in self.generation_times:
            report[asset_type] = {
                "avg_time": np.mean(self.generation_times[asset_type]),
                "success_rate": np.mean(self.success_rates[asset_type]) * 100,
                "avg_size_mb": np.mean(self.file_sizes[asset_type]) / 1024 / 1024
            }
        return report
```

---

## Next Steps

1. **Week 1:** Install libraries and test basic generation
2. **Week 2:** Implement math diagrams generator
3. **Week 3:** Implement 3D shapes generator
4. **Week 4:** Integrate with skills system
5. **Week 5-8:** Chemistry and physics visualizations
6. **Week 9-12:** Biology models
7. **Week 13-16:** Full curriculum coverage

---

## Success Criteria

- [ ] All Tier 1 libraries installed and tested
- [ ] 50+ 2D diagrams generated for mathematics
- [ ] 15+ 3D geometric shapes in GLB format
- [ ] 20+ chemistry molecules modeled
- [ ] 10+ physics simulations created
- [ ] Integration with skills system complete
- [ ] API endpoints for asset retrieval functional
- [ ] Documentation and examples complete
- [ ] Performance benchmarks met

---

**Last Updated:** January 11, 2026  
**Status:** Strategy Approved - Ready for Implementation  
**Next Review:** Weekly during implementation
