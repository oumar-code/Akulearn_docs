# Graphics Generation - Quick Reference

## 🚀 Quick Start

### Install Everything
```bash
pip install matplotlib plotly kaleido Pillow vpython py3Dmol trimesh pyglet moderngl manim rdkit-pypi biopython nglview open3d
```

### Generate All Assets
```bash
cd src/backend
python -c "from generators.asset_generator_manager import AssetGeneratorManager; m = AssetGeneratorManager(); m.generate_all_priority_assets()"
```

### Find Generated Files
```
generated_assets/
├── math_diagrams/           (PNG files)
├── geometric_shapes/        (GLB + STL files)
├── simulations/             (HTML5 interactive)
└── assets_manifest.json     (Index)
```

---

## 📊 What You Get

| Type | Count | Format | Location |
|------|-------|--------|----------|
| **Math Diagrams** | 6 | PNG 300dpi | `math_diagrams/` |
| **3D Shapes** | 7 | GLB/STL | `geometric_shapes/` |
| **Simulations** | 3 | HTML5 | `simulations/` |
| **Chemistry** | 19 | Metadata | Ready for RDKit |

---

## 🔧 Generators Available

### 1. Math Diagrams
```python
from src.backend.generators.math_diagrams import MathDiagramGenerator
gen = MathDiagramGenerator()

# Available methods:
gen.generate_trigonometric_functions()     # sin, cos, tan
gen.generate_quadratic_function()           # parabola with vertex
gen.generate_circle_theorem()               # inscribed angles
gen.generate_histogram()                    # frequency distribution
gen.generate_box_plot()                     # dataset comparison
gen.generate_scatter_plot()                 # correlation
gen.generate_all_basic_diagrams()          # all 6 at once
```

### 2. 3D Shapes
```python
from src.backend.generators.shape_3d_generator import Shape3DGenerator
gen = Shape3DGenerator()

# Available methods:
gen.generate_cube(2.0)                      # cube
gen.generate_sphere(1.5)                    # sphere
gen.generate_cylinder(1.0, 3.0)             # cylinder
gen.generate_cone(1.0, 2.5)                 # cone
gen.generate_pyramid(2.0, 3.0)              # pyramid
gen.generate_prism(6, 1.0, 2.0)             # hexagonal prism
gen.generate_all_basic_shapes()             # all 7 at once
```

### 3. Physics Simulations
```python
from src.backend.generators.physics_simulations import PhysicsSimulationGenerator
gen = PhysicsSimulationGenerator()

# Available methods:
gen.generate_pendulum_simulation()          # SHM
gen.generate_projectile_motion_simulation() # ballistics
gen.generate_wave_simulation()              # wave propagation
gen.generate_all_simulations()              # all 3 at once
```

### 4. Chemistry Models
```python
from src.backend.generators.chemistry_models import ChemistryModelGenerator
gen = ChemistryModelGenerator()

# Available methods:
gen.generate_hydrocarbons()                 # CH4, C2H6, benzene, etc.
gen.generate_common_molecules()             # H2O, CO2, acids, etc.
gen.generate_inorganic_molecules()          # salts, oxides, etc.
gen.generate_all_priority_molecules()       # all 19 at once
```

### 5. Central Manager
```python
from src.backend.generators.asset_generator_manager import AssetGeneratorManager
manager = AssetGeneratorManager()

# Usage:
manager.generate_all_priority_assets()           # Everything
manager.generate_for_lesson({
    "subject": "Mathematics",
    "topic": "Trigonometry",
    "grade_level": "SS2"
})  # Subject-specific

manager.generate_subject_pack("Chemistry", "SS1")  # Subject pack
```

---

## 📚 Usage Examples

### Example 1: Math Lesson Assets
```python
lesson = {
    "subject": "Mathematics",
    "topic": "Circle Theorems",
    "grade_level": "SS2"
}
assets = manager.generate_for_lesson(lesson)
# Returns: {"math_diagrams": ["path/to/diagram.png"], ...}
```

### Example 2: Physics Lesson Assets
```python
lesson = {
    "subject": "Physics",
    "topic": "Simple Harmonic Motion",
    "grade_level": "SS3"
}
assets = manager.generate_for_lesson(lesson)
# Returns: {"simulations": ["path/to/simulation.html"], ...}
```

### Example 3: Full Curriculum Pack
```python
all_assets = manager.generate_all_priority_assets()
# Generates 35+ assets across all categories
# Saves manifest to: generated_assets/assets_manifest.json
```

---

## 🎯 Via Skills System

### Execute Skill
```bash
python src/backend/akulearn_skills.py execute graphics_diagram_generator \
    --subject "Mathematics" \
    --topic "Quadratic Equations" \
    --asset_type "2d_diagram"
```

### List Skill Info
```bash
python src/backend/akulearn_skills.py show graphics_diagram_generator
```

---

## 📁 File Locations

```
Project Root/
├── src/backend/generators/
│   ├── __init__.py
│   ├── math_diagrams.py              ← 2D math visualizations
│   ├── shape_3d_generator.py         ← 3D geometric models
│   ├── chemistry_models.py           ← Molecular structures
│   ├── physics_simulations.py        ← Interactive simulations
│   └── asset_generator_manager.py    ← Central coordinator
│
├── src/backend/skills/instructions/
│   └── graphics_generation_instructions.md  ← Full documentation
│
├── src/backend/skills/
│   └── skill_definitions.json        ← Includes graphics_diagram_generator
│
├── generated_assets/
│   ├── math_diagrams/                ← Output: 6 PNG files
│   ├── geometric_shapes/             ← Output: 7 GLB + 7 STL files
│   ├── simulations/                  ← Output: 3 HTML5 files
│   ├── molecules/                    ← Output: Fallback metadata
│   └── assets_manifest.json          ← Index of all assets
│
└── test files:
    ├── test_graphics_generators.py
    └── run_comprehensive_graphics_test.py
```

---

## 🔍 Troubleshooting

### RDKit Not Available
```
⚠️ Chemistry models generator will use fallback mode.
```
**Fix**: `pip install rdkit-pypi`

### Matplotlib Import Error
```
ERROR: Failed to import matplotlib
```
**Fix**: `pip install matplotlib numpy scipy`

### Generated Files Missing
**Check**: Is `generated_assets/` directory writable?
```bash
mkdir -p generated_assets/{math_diagrams,geometric_shapes,simulations,molecules}
```

---

## 📈 Performance

- **Quick test**: ~1-2 seconds per generator
- **Full suite**: ~5-10 seconds for all 35 assets
- **File sizes**: Math (50-200KB), 3D (1-4KB), Simulations (3-6KB)

---

## ✅ What's Included

- ✅ 6 Mathematical diagrams
- ✅ 7 3D geometric shapes (GLB format for AR/VR)
- ✅ 3 Interactive physics simulations
- ✅ 19 Chemistry molecules (fallback mode)
- ✅ Manifest system for asset tracking
- ✅ Skills system integration
- ✅ Comprehensive documentation
- ✅ CLI interface
- ✅ Python API

---

## 🎓 Next: RDKit Integration

For full chemistry support:
```bash
pip install rdkit-pypi

# Then regenerate:
python -c "from generators.chemistry_models import ChemistryModelGenerator; gen = ChemistryModelGenerator(); gen.generate_all_priority_molecules()"
```

This will create:
- 3D molecular MOL files
- Structure images (with/without H atoms)
- Molecular property calculations
- Metadata JSON

---

## 📞 Support

- **Documentation**: `src/backend/skills/instructions/graphics_generation_instructions.md`
- **Full Report**: `GRAPHICS_IMPLEMENTATION_COMPLETE.md`
- **Strategy**: `GRAPHICS_GENERATION_STRATEGY.md`

**Status**: ✅ Production Ready
