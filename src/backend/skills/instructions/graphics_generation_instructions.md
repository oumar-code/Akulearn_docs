# Graphics and Diagrams Generation Instructions

## Overview
The Graphics & Diagrams Generator skill creates educational visual content including:
- **2D Mathematical Diagrams**: Trigonometric functions, quadratic equations, circle theorems, statistical plots
- **3D Geometric Shapes**: Cubes, spheres, cylinders, cones, pyramids, prisms (GLB format for AR/VR)
- **Chemistry Models**: Molecular structures, chemical compounds (requires RDKit)
- **Physics Simulations**: Interactive simulations (pendulum, projectile motion, waves)

## When to Use

### Subject-Specific Generation
- **Mathematics**: Generate diagrams for algebra, geometry, trigonometry, statistics
- **Chemistry**: Generate molecular models and structure diagrams
- **Physics**: Create interactive physics simulations and visualizations
- **Biology**: Future support for anatomical structures and 3D cell models

### Asset Types
| Type | Description | Format | Subjects |
|------|-------------|--------|----------|
| Math Diagrams | 2D function plots, geometric shapes | PNG 300dpi | Mathematics |
| 3D Shapes | Geometric solids for visualization | GLB/STL | Mathematics, Physics |
| Molecules | Atomic/molecular structures | MOL/PNG | Chemistry |
| Simulations | Interactive physics/motion sims | HTML5/WebGL | Physics |

## Setup Requirements

### Install Graphics Libraries
```bash
# Core graphics libraries
pip install matplotlib plotly kaleido Pillow

# 3D graphics
pip install trimesh vpython py3Dmol

# Optional: Advanced features
pip install rdkit-pypi biopython nglview
```

### Directory Structure
```
generated_assets/
├── math_diagrams/          # 2D mathematical plots
├── geometric_shapes/       # 3D GLB/STL models
├── molecules/              # Chemistry structure files
├── simulations/            # HTML5 interactive sims
└── assets_manifest.json    # Manifest of all assets
```

## Usage Examples

### 1. Generate Mathematics Diagrams

#### Trigonometric Functions
```python
from src.backend.generators.math_diagrams import MathDiagramGenerator

gen = MathDiagramGenerator()
path = gen.generate_trigonometric_functions()
# Outputs: trigonometric_functions.png
```

#### Quadratic Equations
```python
# Generate y = ax² + bx + c
path = gen.generate_quadratic_function(a=1, b=-2, c=1)
# Shows vertex, x-intercepts, and axis of symmetry
```

#### Circle Theorems
```python
path = gen.generate_circle_theorem()
# Shows inscribed angle and central angle relationships
```

#### Statistical Plots
```python
# Histogram
path = gen.generate_histogram(title="Age Distribution")

# Box plot
path = gen.generate_box_plot(
    datasets=[data1, data2, data3],
    labels=["Group A", "Group B", "Group C"]
)

# Scatter plot with trend line
path = gen.generate_scatter_plot()
```

### 2. Generate 3D Geometric Shapes

```python
from src.backend.generators.shape_3d_generator import Shape3DGenerator

gen = Shape3DGenerator()

# Generate basic shapes
cube_meta = gen.generate_cube(side_length=2.0)
sphere_meta = gen.generate_sphere(radius=1.5)
cylinder_meta = gen.generate_cylinder(radius=1.0, height=3.0)
cone_meta = gen.generate_cone(radius=1.0, height=2.5)
pyramid_meta = gen.generate_pyramid(base_size=2.0, height=3.0)

# Generate all shapes at once
shapes = gen.generate_all_basic_shapes()
manifest_path = gen.generate_manifest(shapes)
```

**Output Files:**
- `.glb` - Binary glTF (for AR/VR rendering)
- `.stl` - Stereolithography (for 3D printing)

### 3. Generate Chemistry Molecules

```python
from src.backend.generators.chemistry_models import ChemistryModelGenerator

gen = ChemistryModelGenerator()

# Generate common molecules
molecules = gen.generate_all_priority_molecules()
# Categories: hydrocarbons, common_molecules, inorganic_molecules

# Generate specific category
hydrocarbons = gen.generate_hydrocarbons()
# Returns: methane, ethane, propane, butane, ethene, propene, ethyne, benzene
```

**Output Files:**
- `.mol` - 3D molecular structure file
- `*_2d.png` - 2D structure diagram
- `*_2d_clean.png` - 2D without hydrogens
- `*_metadata.json` - Molecular properties

### 4. Generate Physics Simulations

```python
from src.backend.generators.physics_simulations import PhysicsSimulationGenerator

gen = PhysicsSimulationGenerator()

# Generate interactive HTML simulations
pendulum_path = gen.generate_pendulum_simulation()
projectile_path = gen.generate_projectile_motion_simulation()
wave_path = gen.generate_wave_simulation()

# All simulations support:
# - Interactive parameters (angle, velocity, damping)
# - Real-time visualization
# - Physical calculations
# - Data display (energy, period, trajectory)
```

### 5. Use Asset Manager for Curriculum Integration

```python
from src.backend.generators.asset_generator_manager import AssetGeneratorManager

manager = AssetGeneratorManager()

# Generate assets for specific lesson
lesson = {
    "subject": "Mathematics",
    "topic": "Trigonometry",
    "grade_level": "SS2"
}
assets = manager.generate_for_lesson(lesson)
# Returns: math_diagrams, 3d_shapes, molecules, simulations

# Generate all priority assets
all_assets = manager.generate_all_priority_assets()

# Generate subject-specific pack
math_pack = manager.generate_subject_pack("Mathematics", "SS2")
chem_pack = manager.generate_subject_pack("Chemistry", "SS1")
```

## Integration with Skills System

### Execute via CLI
```bash
# Generate all priority assets
python src/backend/akulearn_skills.py execute graphics_diagram_generator \
    --subject "Mathematics" \
    --topic "Quadratic Equations" \
    --asset_type "2d_diagram"

# Generate subject pack
python src/backend/generators/asset_generator_manager.py \
    --action generate_pack \
    --subject Chemistry \
    --grade SS1
```

### Execute in Code
```python
from src.backend.skills.skill_orchestrator import SkillOrchestrator

orchestrator = SkillOrchestrator()
result = orchestrator.execute_skill(
    "graphics_diagram_generator",
    {
        "subject": "Physics",
        "topic": "Simple Harmonic Motion",
        "grade_level": "SS3"
    }
)
```

## Output Manifest Structure

```json
{
  "version": "1.0.0",
  "created_at": "2026-01-11T15:30:00",
  "updated_at": "2026-01-11T15:45:00",
  "total_assets": 42,
  "categories": {
    "math_diagrams": [
      {
        "trigonometric": "generated_assets/math_diagrams/trigonometric_functions.png",
        "quadratic": "generated_assets/math_diagrams/quadratic_1_0_0.png"
      }
    ],
    "3d_shapes": [
      {
        "name": "Cube_2",
        "shape_type": "cube",
        "glb_file": "generated_assets/geometric_shapes/Cube_2.glb",
        "volume": 8.0,
        "surface_area": 24.0
      }
    ],
    "molecules": [
      {
        "name": "methane",
        "formula": "CH4",
        "mol_file": "generated_assets/molecules/methane.mol"
      }
    ],
    "simulations": [
      "generated_assets/simulations/simple_pendulum.html"
    ]
  }
}
```

## Quality Standards

### 2D Graphics
- Resolution: Minimum 300 DPI
- Format: PNG with transparency
- File size: < 500KB
- Labels: Clear, readable fonts

### 3D Models
- Format: GLB (binary glTF)
- Polygon count: < 50,000 triangles
- File size: < 5MB
- Centered at origin
- Proper scaling

### Interactive Simulations
- Format: HTML5/WebGL
- Duration: 30-120 seconds
- FPS: 30fps minimum
- Controls: Intuitive UI

## Performance Tips

1. **Batch Generation**: Generate multiple assets at once
2. **Caching**: Check manifest before regenerating
3. **Lazy Loading**: Generate on-demand for lessons
4. **Optimization**: Use lower polygon counts for web
5. **Progressive Enhancement**: Start with low-res previews

## Troubleshooting

### RDKit Not Available
```
⚠️ Chemistry models generator will use fallback mode
```
**Solution**: Install RDKit for full chemistry support
```bash
pip install rdkit-pypi
```

### Matplotlib Rendering Issues
**Solution**: Use non-interactive backend
```python
import matplotlib
matplotlib.use('Agg')
```

### Large File Generation Times
**Solution**: Generate in batches or use simpler complexity options

## Success Criteria

- ✅ All requested diagrams generated successfully
- ✅ 3D models in GLB format with correct properties
- ✅ Molecular structures with metadata
- ✅ Interactive simulations with proper physics
- ✅ Manifest file created and updated
- ✅ Integration with skills system working
- ✅ All assets properly cataloged

## Next Steps

1. Generate all priority assets for curriculum coverage
2. Integrate with lesson content in LMS
3. Create preview tiles for asset browser
4. Add to student learning materials
5. Monitor usage and collect feedback
6. Expand to additional subjects and topics

---

**Last Updated**: January 11, 2026  
**Status**: Production Ready  
**Supported Subjects**: Mathematics, Chemistry, Physics, Biology (planned)
