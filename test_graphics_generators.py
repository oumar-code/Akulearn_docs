#!/usr/bin/env python
"""Quick test script for graphics generators"""

import sys
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path.cwd()))

print("="*60)
print("🧪 Testing Graphics Generators")
print("="*60)

# Test 1: Math Diagrams
print("\n1️⃣ Testing Math Diagrams...")
try:
    from src.backend.generators.math_diagrams import MathDiagramGenerator
    gen = MathDiagramGenerator()
    print("   ✅ Math generator initialized")
    path = gen.generate_trigonometric_functions()
    print(f"   ✅ Trigonometric functions: {Path(path).name}")
except Exception as e:
    print(f"   ❌ Math test failed: {e}")

# Test 2: 3D Shapes
print("\n2️⃣ Testing 3D Shapes...")
try:
    from src.backend.generators.shape_3d_generator import Shape3DGenerator
    gen = Shape3DGenerator()
    print("   ✅ 3D generator initialized")
    meta = gen.generate_cube(2.0, "test_cube")
    print(f"   ✅ Generated cube: {meta['name']}")
except Exception as e:
    print(f"   ❌ 3D test failed: {e}")

# Test 3: Chemistry Models
print("\n3️⃣ Testing Chemistry Models...")
try:
    from src.backend.generators.chemistry_models import ChemistryModelGenerator
    gen = ChemistryModelGenerator()
    print("   ✅ Chemistry generator initialized")
    if gen.rdkit_available:
        mols = gen.generate_hydrocarbons()
        print(f"   ✅ Generated {len(mols)} hydrocarbons")
    else:
        print("   ⚠️ RDKit not available (fallback mode)")
except Exception as e:
    print(f"   ❌ Chemistry test failed: {e}")

# Test 4: Physics Simulations
print("\n4️⃣ Testing Physics Simulations...")
try:
    from src.backend.generators.physics_simulations import PhysicsSimulationGenerator
    gen = PhysicsSimulationGenerator()
    print("   ✅ Physics generator initialized")
    path = gen.generate_pendulum_simulation()
    print(f"   ✅ Pendulum simulation: {Path(path).name}")
except Exception as e:
    print(f"   ❌ Physics test failed: {e}")

# Test 5: Asset Manager
print("\n5️⃣ Testing Asset Manager...")
try:
    from src.backend.generators.asset_generator_manager import AssetGeneratorManager
    manager = AssetGeneratorManager()
    print("   ✅ Asset manager initialized")
    print(f"   ✅ Registered generators: {list(manager.generators.keys())}")
except Exception as e:
    print(f"   ❌ Asset manager test failed: {e}")

print("\n" + "="*60)
print("✅ All tests completed!")
print("="*60)
