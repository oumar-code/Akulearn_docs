"""
Akulearn Graphics and Shapes Generator Package
Provides unified interface for generating educational graphics, diagrams, and 3D models
"""

__version__ = "1.0.0"

from .math_diagrams import MathDiagramGenerator
from .shape_3d_generator import Shape3DGenerator
from .chemistry_models import ChemistryModelGenerator
from .physics_simulations import PhysicsSimulationGenerator
from .biology_models import BiologyModelGenerator
from .plant_models import PlantModelGenerator
from .molecular_models import MolecularModelGenerator
from .circuit_models import CircuitModelGenerator
from .geometric_shapes import GeometricShapeGenerator
from .wave_optics import WaveOpticsGenerator
from .cell_biology import CellBiologyGenerator
from .simple_machines import SimpleMachinesGenerator
from .earth_space import EarthSpaceGenerator
from .agriculture import AgricultureModelGenerator
from .asset_generator_manager import AssetGeneratorManager

__all__ = [
    'MathDiagramGenerator',
    'Shape3DGenerator', 
    'ChemistryModelGenerator',
    'PhysicsSimulationGenerator',
    'BiologyModelGenerator',
    'PlantModelGenerator',
    'MolecularModelGenerator',
    'CircuitModelGenerator',
    'GeometricShapeGenerator',
    'WaveOpticsGenerator',
    'CellBiologyGenerator',
    'SimpleMachinesGenerator',    'EarthSpaceGenerator',    "AssetGeneratorManager",
]
