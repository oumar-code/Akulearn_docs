"""
Akulearn Graphics and Shapes Generator Package
Provides unified interface for generating educational graphics, diagrams, and 3D models
"""

__version__ = "1.0.0"

from .math_diagrams import MathDiagramGenerator
from .shape_3d_generator import Shape3DGenerator
from .chemistry_models import ChemistryModelGenerator
from .physics_simulations import PhysicsSimulationGenerator
from .asset_generator_manager import AssetGeneratorManager

__all__ = [
    "MathDiagramGenerator",
    "Shape3DGenerator",
    "ChemistryModelGenerator",
    "PhysicsSimulationGenerator",
    "AssetGeneratorManager",
]
