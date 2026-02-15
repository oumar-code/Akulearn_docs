# Priority #5: Geometric 3D Shapes (Mathematics)

Subject: Mathematics | Topic: math_008, math_009 | Grade: JSS1–SS3 | Exam Weight: High
Expected Output: generated_assets/geometric_shapes  
Total Models: ~8 (GLB, AR/VR-ready)

## Overview
Priority #5 from 3D_ASSETS_PRIORITY_PLAN.md focuses on foundational geometric 3D shapes essential for mathematics curriculum covering surface area, volume, and spatial reasoning across all secondary levels.

## Planned Models

| Model | Purpose | Components | Grade Level |
|-------|---------|-----------|-------------|
| **cube.glb** | Regular 3D cube | 8 vertices, 12 edges, 6 square faces | JSS1+ |
| **cuboid.glb** | Rectangular box | Dimensions varied, 8 vertices | JSS1+ |
| **cylinder.glb** | Circular solid | Circular bases, lateral surface | SS1+ |
| **cone.glb** | Circular pyramid | Apex, circular base, slant edge | SS1+ |
| **sphere.glb** | Perfect sphere | Smooth surface, radius indicators | JSS3+ |
| **pyramid.glb** | Square pyramid | Square base, triangular faces, apex | JSS2+ |
| **prisms.glb** | Triangular/hexagonal | Multiple prism types side-by-side | SS1+ |
| **composite_solids.glb** | Combined shapes | Cube + cylinder, hemisphere on cube | SS2+ |

## Curriculum Mapping
- **Subject**: Mathematics
- **Topics**: math_008 (Mensuration), math_009 (3D Geometry)
- **Grade Levels**: JSS1, JSS2, JSS3, SS1, SS2, SS3
- **Standards**: WAEC, NECO

## Integration Plan
- Register `GeometricShapeGenerator` in AssetGeneratorManager
- Add routing for "shape", "geometry", "cube", "prism", "pyramid", etc.
- Include surface area/volume annotations
- Support cross-grade curriculum coverage

## Technical Approach
- Use trimesh for mesh generation
- Add edge/vertex highlighting for educational visualization
- Include dimension labels (length, width, height, radius)
- All models under 500 KB for AR/VR optimization

## Testing Strategy
- Individual shape generation tests
- Integration with AssetGeneratorManager
- File verification and size optimization
- Cross-grade lesson routing

## Timeline
- Generator class: ~50–80 lines per shape method
- Total implementation: ~600–800 lines
- Expected build time: 30–45 minutes
- Testing: ~15 minutes

---

## Ready to Start?
Confirm to proceed with Priority #5 implementation.
