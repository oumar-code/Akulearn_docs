"""
Unified Asset Generator Manager
Central coordinator for all graphics, 3D models, and visualization generation
Integrates with Akulearn skills system for curriculum-aware generation
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

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
from .reproductive_systems import ReproductiveSystemsModelGenerator
from .mathematical_functions import MathematicalFunctionsModelGenerator
from .nigerian_cultural import NigerianCulturalModelsGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssetGeneratorManager:
    """Central manager for all asset generation"""
    
    def __init__(self, workspace_root: Optional[str] = None):
        """
        Initialize asset generator manager
        
        Args:
            workspace_root: Root workspace directory
        """
        self.workspace_root = workspace_root or str(Path.cwd())
        self.generators = {}
        self.register_generators()
        
        # Assets manifest
        self.manifest_path = Path(self.workspace_root) / "generated_assets" / "assets_manifest.json"
        self.manifest = self._load_manifest()
        
        logger.info(f"AssetGeneratorManager initialized")
    
    def register_generators(self):
        """Register all available generators"""
        try:
            self.generators['math_2d'] = MathDiagramGenerator()
            logger.info("✅ Math diagram generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register math generator: {e}")
        
        try:
            self.generators['shapes_3d'] = Shape3DGenerator()
            logger.info("✅ 3D shape generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register 3D shape generator: {e}")
        
        try:
            self.generators['chemistry'] = ChemistryModelGenerator()
            logger.info("✅ Chemistry model generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register chemistry generator: {e}")
        
        try:
            self.generators['physics'] = PhysicsSimulationGenerator()
            logger.info("✅ Physics simulation generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register physics generator: {e}")
        
        try:
            self.generators['biology'] = BiologyModelGenerator()
            logger.info("✅ Biology model generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register biology generator: {e}")
        
        try:
            self.generators['plants'] = PlantModelGenerator()
            logger.info("✅ Plant model generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register plant generator: {e}")
        
        try:
            self.generators['molecular'] = MolecularModelGenerator()
            logger.info("✅ Molecular model generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register molecular generator: {e}")
        
        try:
            self.generators['circuits'] = CircuitModelGenerator()
            logger.info("✅ Circuit model generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register circuit generator: {e}")
        
        try:
            self.generators['geometry'] = GeometricShapeGenerator()
            logger.info("✅ Geometric shape generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register geometric shape generator: {e}")
        
        try:
            self.generators['optics'] = WaveOpticsGenerator()
            logger.info("✅ Wave & Optics generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register wave/optics generator: {e}")
        
        try:
            self.generators['cells'] = CellBiologyGenerator()
            logger.info("✅ Cell Biology generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register cell biology generator: {e}")
        
        try:
            self.generators['machines'] = SimpleMachinesGenerator()
            logger.info("✅ Simple Machines generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register simple machines generator: {e}")
        
        try:
            self.generators['space'] = EarthSpaceGenerator()
            logger.info("✅ Earth & Space generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register earth/space generator: {e}")
        
        try:
            self.generators['agriculture'] = AgricultureModelGenerator()
            logger.info("✅ Agriculture generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register agriculture generator: {e}")
        
        try:
            self.generators['reproductive_systems'] = ReproductiveSystemsModelGenerator()
            logger.info("✅ Reproductive Systems generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register reproductive systems generator: {e}")
        
        try:
            self.generators['mathematical_functions'] = MathematicalFunctionsModelGenerator()
            logger.info("✅ Mathematical Functions generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register mathematical functions generator: {e}")
        
        try:
            self.generators['nigerian_cultural'] = NigerianCulturalModelsGenerator()
            logger.info("✅ Nigerian Cultural Models generator registered")
        except Exception as e:
            logger.warning(f"⚠️ Failed to register nigerian cultural generator: {e}")
    
    def _load_manifest(self) -> Dict[str, Any]:
        """Load existing manifest or create new one"""
        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"⚠️ Failed to load manifest: {e}")
        
        return {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "total_assets": 0,
            "categories": {
                "math_diagrams": [],
                "3d_shapes": [],
                "molecules": [],
                "simulations": []
            }
        }
    
    def _save_manifest(self):
        """Save manifest to disk"""
        try:
            self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.manifest_path, 'w') as f:
                json.dump(self.manifest, f, indent=2)
            logger.info(f"✅ Manifest saved: {self.manifest_path}")
        except Exception as e:
            logger.error(f"❌ Failed to save manifest: {e}")
    
    def generate_for_lesson(self, lesson: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Generate appropriate assets for a lesson
        
        Args:
            lesson: Lesson metadata with subject, topic, grade_level, etc.
            
        Returns:
            Dictionary of generated asset paths by category
        """
        subject = lesson.get('subject', '').lower()
        topic = lesson.get('topic', '').lower()
        grade_level = lesson.get('grade_level', '')
        
        generated_assets = {
            "math_diagrams": [],
            "3d_shapes": [],
            "molecules": [],
            "simulations": [],
            "biology_models": [],
            "plant_models": [],
            "molecular_models": [],
            "circuit_models": [],
            "geometric_shapes": [],
            "optics_models": []
        }
        
        logger.info(f"📚 Generating assets for {subject} - {topic} ({grade_level})")
        
        # Mathematics diagrams
        if subject in ['mathematics', 'math']:
            try:
                if 'trigonometry' in topic or 'trig' in topic:
                    path = self.generators['math_2d'].generate_trigonometric_functions()
                    generated_assets['math_diagrams'].append(path)
                
                elif 'quadratic' in topic or 'parabola' in topic:
                    path = self.generators['math_2d'].generate_quadratic_function()
                    generated_assets['math_diagrams'].append(path)
                
                elif 'circle' in topic or 'geometry' in topic:
                    path = self.generators['math_2d'].generate_circle_theorem()
                    generated_assets['math_diagrams'].append(path)
                
                elif 'statistics' in topic or 'data' in topic:
                    path = self.generators['math_2d'].generate_histogram()
                    generated_assets['math_diagrams'].append(path)
                    path = self.generators['math_2d'].generate_scatter_plot()
                    generated_assets['math_diagrams'].append(path)
                
                # Geometric shapes for mensuration and 3D geometry
                if 'geometry' in self.generators:
                    if 'cube' in topic:
                        meta = self.generators['geometry'].generate_cube()
                        generated_assets['geometric_shapes'] = [meta['filepath']]
                    elif 'cuboid' in topic or 'rectangular prism' in topic:
                        meta = self.generators['geometry'].generate_cuboid()
                        generated_assets['geometric_shapes'] = [meta['filepath']]
                    elif 'cylinder' in topic:
                        meta = self.generators['geometry'].generate_cylinder()
                        generated_assets['geometric_shapes'] = [meta['filepath']]
                    elif 'cone' in topic:
                        meta = self.generators['geometry'].generate_cone()
                        generated_assets['geometric_shapes'] = [meta['filepath']]
                    elif 'sphere' in topic:
                        meta = self.generators['geometry'].generate_sphere()
                        generated_assets['geometric_shapes'] = [meta['filepath']]
                    elif 'pyramid' in topic:
                        meta = self.generators['geometry'].generate_pyramid()
                        generated_assets['geometric_shapes'] = [meta['filepath']]
                    elif 'prism' in topic and 'cube' not in topic and 'cuboid' not in topic:
                        meta = self.generators['geometry'].generate_prisms()
                        generated_assets['geometric_shapes'] = [meta['filepath']]
                    elif 'composite' in topic or 'combined shapes' in topic:
                        meta = self.generators['geometry'].generate_composite_solids()
                        generated_assets['geometric_shapes'] = [meta['filepath']]
                    elif 'mensuration' in topic or '3d geometry' in topic or 'geometric shapes' in topic or 'solid shapes' in topic:
                        shapes = self.generators['geometry'].generate_all_shapes()
                        generated_assets['geometric_shapes'] = [s['filepath'] for s in shapes]
            except Exception as e:
                logger.warning(f"⚠️ Math generation failed: {e}")
        
        # 3D Shapes for geometry
        if 'geometry' in topic or 'solid' in topic or 'shape' in topic:
            try:
                shapes = self.generators['shapes_3d'].generate_all_basic_shapes()
                generated_assets['3d_shapes'] = [s['glb_file'] for s in shapes]
            except Exception as e:
                logger.warning(f"⚠️ 3D shape generation failed: {e}")
        
        # Biology models for anatomy/physiology
        if subject in ['biology', 'bio']:
            try:
                if 'biology' in self.generators:
                    if 'digestive' in topic or 'digestion' in topic:
                        meta = self.generators['biology'].generate_digestive_system()
                        generated_assets['biology_models'] = [meta['filepath']]
                    elif 'respiratory' in topic or 'breathing' in topic:
                        meta = self.generators['biology'].generate_respiratory_system()
                        generated_assets['biology_models'] = [meta['filepath']]
                    elif 'circulatory' in topic or 'heart' in topic or 'blood' in topic:
                        meta = self.generators['biology'].generate_circulatory_system()
                        generated_assets['biology_models'] = [meta['filepath']]
                    elif 'excretory' in topic or 'kidney' in topic:
                        meta = self.generators['biology'].generate_excretory_system()
                        generated_assets['biology_models'] = [meta['filepath']]
                    elif 'skeletal' in topic or 'bone' in topic:
                        meta = self.generators['biology'].generate_skeletal_system()
                        generated_assets['biology_models'] = [meta['filepath']]
                    elif 'nervous' in topic or 'brain' in topic:
                        meta = self.generators['biology'].generate_nervous_system()
                        generated_assets['biology_models'] = [meta['filepath']]
                    elif 'muscular' in topic or 'muscle' in topic:
                        meta = self.generators['biology'].generate_muscular_system()
                        generated_assets['biology_models'] = [meta['filepath']]
                    elif 'body' in topic or 'anatomy' in topic and 'plant' not in topic:
                        # Generate all body systems
                        systems = self.generators['biology'].generate_all_body_systems()
                        generated_assets['biology_models'] = [s['filepath'] for s in systems]
                    
                    # Plant models for botany
                    elif 'plant' in topic or 'photosynthesis' in topic or 'leaf' in topic or 'root' in topic:
                        if 'plants' in self.generators:
                            if 'cell' in topic:
                                meta = self.generators['plants'].generate_plant_cell()
                                generated_assets['plant_models'] = [meta['filepath']]
                            elif 'leaf' in topic:
                                meta = self.generators['plants'].generate_leaf_structure()
                                generated_assets['plant_models'] = [meta['filepath']]
                            elif 'root' in topic:
                                meta = self.generators['plants'].generate_root_system()
                                generated_assets['plant_models'] = [meta['filepath']]
                            elif 'flower' in topic:
                                meta = self.generators['plants'].generate_flower_structure()
                                generated_assets['plant_models'] = [meta['filepath']]
                            elif 'photosynthesis' in topic:
                                meta = self.generators['plants'].generate_photosynthesis_process()
                                generated_assets['plant_models'] = [meta['filepath']]
                            elif 'plant' in topic:
                                # Generate all plant models
                                plants = self.generators['plants'].generate_all_plant_models()
                                generated_assets['plant_models'] = [p['filepath'] for p in plants]
                    
                    # Cell biology models (Priority #7)
                    elif 'cell' in topic or 'mitochondria' in topic or 'nucleus' in topic or 'membrane' in topic or 'division' in topic or 'bio_001' in topic:
                        if 'cells' in self.generators:
                            if 'animal cell' in topic or 'animal_cell' in topic:
                                meta = self.generators['cells'].generate_animal_cell()
                                generated_assets['cell_models'] = [meta['filepath']]
                            elif 'plant cell' in topic or 'plant_vs_animal' in topic or 'comparison' in topic:
                                meta = self.generators['cells'].generate_plant_vs_animal_cell()
                                generated_assets['cell_models'] = [meta['filepath']]
                            elif 'mitochondria' in topic or 'powerhouse' in topic:
                                meta = self.generators['cells'].generate_mitochondria()
                                generated_assets['cell_models'] = [meta['filepath']]
                            elif 'membrane' in topic or 'phospholipid' in topic:
                                meta = self.generators['cells'].generate_cell_membrane()
                                generated_assets['cell_models'] = [meta['filepath']]
                            elif 'nucleus' in topic or 'chromatin' in topic or 'nucleolus' in topic:
                                meta = self.generators['cells'].generate_nucleus()
                                generated_assets['cell_models'] = [meta['filepath']]
                            elif 'division' in topic or 'mitosis' in topic or 'meiosis' in topic:
                                meta = self.generators['cells'].generate_cell_division()
                                generated_assets['cell_models'] = [meta['filepath']]
                            elif 'cell' in topic or 'bio_001' in topic:
                                # Generate all cell biology models
                                cells = self.generators['cells'].generate_all_models()
                                generated_assets['cell_models'] = [c['filepath'] for c in cells]
            except Exception as e:
                logger.warning(f"⚠️ Biology/Plant generation failed: {e}")
        
        # Chemistry molecules
        if subject in ['chemistry', 'chem']:
            try:
                # Check for molecular structure topics (Priority #3)
                if 'molecular' in self.generators:
                    if 'atom' in topic or 'atomic' in topic:
                        meta = self.generators['molecular'].generate_atom_models()
                        generated_assets['molecules'].append(meta['filepath'])
                    elif 'ionic' in topic or 'ion' in topic:
                        meta = self.generators['molecular'].generate_ionic_bonding()
                        generated_assets['molecules'].append(meta['filepath'])
                    elif 'covalent' in topic or 'molecule' in topic:
                        meta = self.generators['molecular'].generate_covalent_bonding()
                        generated_assets['molecules'].append(meta['filepath'])
                    elif 'metallic' in topic or 'metal' in topic:
                        meta = self.generators['molecular'].generate_metallic_bonding()
                        generated_assets['molecules'].append(meta['filepath'])
                    elif 'hydrocarbon' in topic or 'alkane' in topic:
                        meta = self.generators['molecular'].generate_hydrocarbon_series()
                        generated_assets['molecules'].append(meta['filepath'])
                    elif 'benzene' in topic or 'aromatic' in topic:
                        meta = self.generators['molecular'].generate_benzene_ring()
                        generated_assets['molecules'].append(meta['filepath'])
                    elif 'protein' in topic or 'amino' in topic:
                        meta = self.generators['molecular'].generate_protein_structure()
                        generated_assets['molecules'].append(meta['filepath'])
                    elif 'dna' in topic or 'helix' in topic or 'nucleic' in topic:
                        meta = self.generators['molecular'].generate_dna_helix()
                        generated_assets['molecules'].append(meta['filepath'])
                    elif 'bonding' in topic or 'structure' in topic:
                        # Generate all molecular models
                        molecules = self.generators['molecular'].generate_all_molecular_models()
                        generated_assets['molecules'] = [m['filepath'] for m in molecules]
                
                # Fallback to chemistry generator for simple molecules
                if 'organic' in topic or 'hydrocarbon' in topic:
                    molecules = self.generators['chemistry'].generate_hydrocarbons()
                    generated_assets['molecules'] = [m['mol_file'] for m in molecules]
                else:
                    molecules = self.generators['chemistry'].generate_common_molecules()
                    generated_assets['molecules'] = [m['mol_file'] for m in molecules]
            except Exception as e:
                logger.warning(f"⚠️ Chemistry generation failed: {e}")
        
        # Physics simulations
        if subject in ['physics', 'phys']:
            try:
                # Check for circuit topics (Priority #4)
                if 'circuits' in self.generators:
                    if 'series' in topic and 'circuit' in topic:
                        meta = self.generators['circuits'].generate_series_circuit()
                        generated_assets['simulations'].append(meta['filepath'])
                    elif 'parallel' in topic and 'circuit' in topic:
                        meta = self.generators['circuits'].generate_parallel_circuit()
                        generated_assets['simulations'].append(meta['filepath'])
                    elif 'component' in topic or 'resistor' in topic or 'capacitor' in topic:
                        meta = self.generators['circuits'].generate_circuit_components()
                        generated_assets['simulations'].append(meta['filepath'])
                    elif 'transformer' in topic:
                        meta = self.generators['circuits'].generate_transformer()
                        generated_assets['simulations'].append(meta['filepath'])
                    elif 'motor' in topic:
                        meta = self.generators['circuits'].generate_electric_motor()
                        generated_assets['simulations'].append(meta['filepath'])
                    elif 'generator' in topic:
                        meta = self.generators['circuits'].generate_generator()
                        generated_assets['simulations'].append(meta['filepath'])
                    elif 'circuit' in topic or 'electric' in topic or 'electrical' in topic:
                        # Generate all circuit models
                        circuits = self.generators['circuits'].generate_all_circuit_models()
                        generated_assets['simulations'] = [c['filepath'] for c in circuits]
                
                # Wave & Optics models (Priority #6)
                if 'optics' in self.generators:
                    if 'electromagnetic' in topic or 'spectrum' in topic:
                        meta = self.generators['optics'].generate_electromagnetic_spectrum()
                        generated_assets['optics_models'].append(meta['filepath'])
                    elif 'reflection' in topic or 'mirror' in topic:
                        meta = self.generators['optics'].generate_reflection_mirrors()
                        generated_assets['optics_models'].append(meta['filepath'])
                    elif 'refraction' in topic or 'lens' in topic:
                        meta = self.generators['optics'].generate_refraction_lenses()
                        generated_assets['optics_models'].append(meta['filepath'])
                    elif 'total internal reflection' in topic or 'fiber' in topic:
                        meta = self.generators['optics'].generate_total_internal_reflection()
                        generated_assets['optics_models'].append(meta['filepath'])
                    elif 'prism' in topic and ('dispersion' in topic or 'rainbow' in topic):
                        meta = self.generators['optics'].generate_prism_dispersion()
                        generated_assets['optics_models'].append(meta['filepath'])
                    elif 'wave' in topic and ('transverse' in topic or 'longitudinal' in topic or 'types' in topic):
                        meta = self.generators['optics'].generate_wave_types()
                        generated_assets['optics_models'].append(meta['filepath'])
                    elif 'optics' in topic or 'phy_010' in topic or 'phy_011' in topic:
                        models = self.generators['optics'].generate_all_models()
                        generated_assets['optics_models'] = [m['filepath'] for m in models]
                
                # Simple Machines models (Priority #8)
                if 'machines' in self.generators:
                    if 'lever' in topic or 'fulcrum' in topic:
                        meta = self.generators['machines'].generate_lever_types()
                        generated_assets['machine_models'].append(meta['filepath'])
                    elif 'pulley' in topic:
                        meta = self.generators['machines'].generate_pulley_systems()
                        generated_assets['machine_models'].append(meta['filepath'])
                    elif 'inclined plane' in topic or 'ramp' in topic:
                        meta = self.generators['machines'].generate_inclined_plane()
                        generated_assets['machine_models'].append(meta['filepath'])
                    elif 'wheel' in topic and 'axle' in topic:
                        meta = self.generators['machines'].generate_wheel_and_axle()
                        generated_assets['machine_models'].append(meta['filepath'])
                    elif 'wedge' in topic or 'screw' in topic:
                        meta = self.generators['machines'].generate_wedge_screw()
                        generated_assets['machine_models'].append(meta['filepath'])
                    elif 'gear' in topic:
                        meta = self.generators['machines'].generate_gear_systems()
                        generated_assets['machine_models'].append(meta['filepath'])
                    elif 'simple machine' in topic or 'phy_004' in topic or 'mechanical advantage' in topic:
                        models = self.generators['machines'].generate_all_models()
                        generated_assets['machine_models'] = [m['filepath'] for m in models]
                
                # Earth and Space models (Priority #9)
                if 'space' in self.generators:
                    if 'earth' in topic and 'layer' in topic:
                        meta = self.generators['space'].generate_earth_layers()
                        generated_assets['space_models'].append(meta['filepath'])
                    elif 'tectonic' in topic or 'plate' in topic:
                        meta = self.generators['space'].generate_tectonic_plates()
                        generated_assets['space_models'].append(meta['filepath'])
                    elif 'volcano' in topic or 'volcanic' in topic:
                        meta = self.generators['space'].generate_volcano()
                        generated_assets['space_models'].append(meta['filepath'])
                    elif 'water cycle' in topic or 'water' in topic:
                        meta = self.generators['space'].generate_water_cycle()
                        generated_assets['space_models'].append(meta['filepath'])
                    elif 'rock cycle' in topic or 'geology' in topic or 'mineral' in topic:
                        meta = self.generators['space'].generate_rock_cycle()
                        generated_assets['space_models'].append(meta['filepath'])
                    elif 'moon' in topic or 'lunar' in topic or 'phase' in topic:
                        meta = self.generators['space'].generate_moon_phases()
                        generated_assets['space_models'].append(meta['filepath'])
                    elif 'earth' in topic or 'geol' in topic or 'astro' in topic or 'geo' in topic or 'space' in topic:
                        models = self.generators['space'].generate_all_models()
                        generated_assets['space_models'] = [m['filepath'] for m in models]
                
                # Other physics simulations
                if 'motion' in topic or 'pendulum' in topic:
                    path = self.generators['physics'].generate_pendulum_simulation()
                    generated_assets['simulations'].append(path)
                elif 'projectile' in topic:
                    path = self.generators['physics'].generate_projectile_motion_simulation()
                    generated_assets['simulations'].append(path)
                elif 'wave' in topic:
                    path = self.generators['physics'].generate_wave_simulation()
                    generated_assets['simulations'].append(path)
            except Exception as e:
                logger.warning(f"⚠️ Physics generation failed: {e}")
        
        # Agriculture models (Priority #10)
        if subject in ['agriculture', 'agricultural science', 'agric']:
            try:
                if 'agriculture' in self.generators:
                    if 'soil' in topic or 'layer' in topic:
                        meta = self.generators['agriculture'].generate_soil_layers()
                        generated_assets['agriculture_models'].append(meta['filepath'])
                    elif 'crop' in topic or 'growth' in topic or 'maize' in topic or 'rice' in topic:
                        meta = self.generators['agriculture'].generate_crop_growth_stages()
                        generated_assets['agriculture_models'].append(meta['filepath'])
                    elif 'livestock' in topic or 'animal' in topic or 'cow' in topic or 'goat' in topic or 'chicken' in topic:
                        meta = self.generators['agriculture'].generate_livestock_anatomy()
                        generated_assets['agriculture_models'].append(meta['filepath'])
                    elif 'tool' in topic or 'hoe' in topic or 'cutlass' in topic or 'plough' in topic:
                        meta = self.generators['agriculture'].generate_farm_tools_3d()
                        generated_assets['agriculture_models'].append(meta['filepath'])
                    elif 'irrigation' in topic or 'water' in topic or 'drip' in topic or 'sprinkler' in topic:
                        meta = self.generators['agriculture'].generate_irrigation_systems()
                        generated_assets['agriculture_models'].append(meta['filepath'])
                    elif 'greenhouse' in topic:
                        meta = self.generators['agriculture'].generate_greenhouse()
                        generated_assets['agriculture_models'].append(meta['filepath'])
                    elif 'agr' in topic or 'farm' in topic:
                        models = self.generators['agriculture'].generate_all_models()
                        generated_assets['agriculture_models'] = [m['filepath'] for m in models]
            except Exception as e:
                logger.warning(f"⚠️ Agriculture generation failed: {e}")
        
        # Reproductive Systems models (Priority #11)
        if subject in ['biology', 'bio'] and 'reproduction' in topic or 'reproductive' in topic or 'bio_007' in topic:
            try:
                if 'reproductive_systems' in self.generators:
                    if 'male' in topic or 'male reproductive' in topic or 'testis' in topic or 'spermatogenesis' in topic:
                        models = self.generators['reproductive_systems'].generate_male_reproductive_system()
                        generated_assets['reproductive_models'] = [models]
                    elif 'female' in topic or 'female reproductive' in topic or 'ovary' in topic or 'oogenesis' in topic:
                        models = self.generators['reproductive_systems'].generate_female_reproductive_system()
                        generated_assets['reproductive_models'] = [models]
                    elif 'flower' in topic or 'plant reproduction' in topic or 'pollination' in topic or 'stamen' in topic or 'pistil' in topic:
                        models = self.generators['reproductive_systems'].generate_flower_reproduction()
                        generated_assets['reproductive_models'] = [models]
                    elif 'fetus' in topic or 'development' in topic or 'embryo' in topic or 'pregnancy' in topic or 'trimester' in topic:
                        models = self.generators['reproductive_systems'].generate_fetus_development()
                        generated_assets['reproductive_models'] = [models]
                    elif 'gamete' in topic or 'sperm' in topic or 'egg' in topic or 'meiosis' in topic or 'polar body' in topic:
                        models = self.generators['reproductive_systems'].generate_gamete_formation()
                        generated_assets['reproductive_models'] = [models]
                    elif 'menstrual' in topic or 'cycle' in topic or 'hormone' in topic or 'FSH' in topic or 'LH' in topic:
                        models = self.generators['reproductive_systems'].generate_menstrual_cycle()
                        generated_assets['reproductive_models'] = [models]
                    elif 'reproduction' in topic or 'reproductive' in topic or 'bio_007' in topic:
                        models = self.generators['reproductive_systems'].generate_all_models()
                        generated_assets['reproductive_models'] = list(models.values())
            except Exception as e:
                logger.warning(f"⚠️ Reproductive Systems generation failed: {e}")
        
        # Mathematical Functions models (Priority #12)
        if subject in ['mathematics', 'math'] and 'function' in topic or 'graph' in topic or 'calculus' in topic or 'integration' in topic or 'derivative' in topic or 'math_012' in topic or 'math_013' in topic:
            try:
                if 'mathematical_functions' in self.generators:
                    if '3d' in topic or 'graph' in topic or 'polynomial' in topic:
                        models = self.generators['mathematical_functions'].generate_3d_graphs()
                        generated_assets['math_function_models'] = [models]
                    elif 'polynomial' in topic or 'root' in topic or 'extrema' in topic:
                        models = self.generators['mathematical_functions'].generate_polynomial_functions()
                        generated_assets['math_function_models'] = [models]
                    elif 'trigonometric' in topic or 'sine' in topic or 'cosine' in topic or 'wave' in topic:
                        models = self.generators['mathematical_functions'].generate_trigonometric_surfaces()
                        generated_assets['math_function_models'] = [models]
                    elif 'revolution' in topic or 'rotate' in topic or 'solid' in topic:
                        models = self.generators['mathematical_functions'].generate_surface_of_revolution()
                        generated_assets['math_function_models'] = [models]
                    elif 'integration' in topic or 'area' in topic or 'volume' in topic or 'accumulation' in topic:
                        models = self.generators['mathematical_functions'].generate_volume_integration()
                        generated_assets['math_function_models'] = [models]
                    elif 'tangent' in topic or 'derivative' in topic or 'partial' in topic or 'gradient' in topic:
                        models = self.generators['mathematical_functions'].generate_tangent_planes()
                        generated_assets['math_function_models'] = [models]
                    elif 'function' in topic or 'math_012' in topic or 'math_013' in topic:
                        models = self.generators['mathematical_functions'].generate_all_models()
                        generated_assets['math_function_models'] = list(models.values())
            except Exception as e:
                logger.warning(f"⚠️ Mathematical Functions generation failed: {e}")
        
        # Nigerian Cultural Models (Priority #13)
        if subject in ['social studies', 'social', 'history', 'government', 'civic'] and any(kw in topic for kw in ['nigeria', 'nigerian', 'culture', 'traditional', 'heritage', 'monument', 'government', 'architecture', 'craft', 'artifact', 'historical', 'soc_001', 'soc_002', 'soc_003', 'hist_001', 'gov_002']):
            try:
                if 'nigerian_cultural' in self.generators:
                    if 'architecture' in topic or 'hut' in topic or 'compound' in topic or 'traditional building' in topic:
                        models = self.generators['nigerian_cultural'].generate_traditional_architecture()
                        generated_assets['cultural_models'] = [models]
                    elif 'monument' in topic or 'flag' in topic or 'eagle' in topic or 'national symbol' in topic:
                        models = self.generators['nigerian_cultural'].generate_national_monuments()
                        generated_assets['cultural_models'] = [models]
                    elif 'government' in topic or 'parliament' in topic or 'assembly' in topic or 'legislature' in topic or 'gov_002' in topic:
                        models = self.generators['nigerian_cultural'].generate_government_buildings()
                        generated_assets['cultural_models'] = [models]
                    elif 'artifact' in topic or 'bronze' in topic or 'drum' in topic or 'mask' in topic or 'calabash' in topic:
                        models = self.generators['nigerian_cultural'].generate_cultural_artifacts()
                        generated_assets['cultural_models'] = [models]
                    elif 'historical site' in topic or 'wall' in topic or 'ancient city' in topic or 'benin' in topic or 'kano' in topic:
                        models = self.generators['nigerian_cultural'].generate_historical_sites()
                        generated_assets['cultural_models'] = [models]
                    elif 'craft' in topic or 'weaving' in topic or 'pottery' in topic or 'blacksmith' in topic or 'leather' in topic or 'dyeing' in topic:
                        models = self.generators['nigerian_cultural'].generate_traditional_crafts()
                        generated_assets['cultural_models'] = [models]
                    elif 'nigerian' in topic or 'soc_001' in topic or 'soc_002' in topic or 'soc_003' in topic or 'hist_001' in topic:
                        models = self.generators['nigerian_cultural'].generate_all_models()
                        generated_assets['cultural_models'] = models
            except Exception as e:
                logger.warning(f"⚠️ Nigerian Cultural Models generation failed: {e}")
        
        return generated_assets
    
    def generate_all_priority_assets(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate all high-priority assets from curriculum"""
        results = {
            "math_diagrams": {},
            "geometric_shapes": [],
            "chemistry_molecules": {},
            "physics_simulations": {},
            "biology_models": [],
            "plant_models": [],
            "molecular_models": [],
            "circuit_models": []
        }
        
        logger.info("🎨 Generating all priority assets...\n")
        
        # Generate 2D mathematical diagrams
        print("\n📊 Generating mathematical diagrams...")
        try:
            math_diagrams = self.generators['math_2d'].generate_all_basic_diagrams()
            results['math_diagrams'] = math_diagrams
            print(f"✅ Generated {len(math_diagrams)} mathematical diagrams")
        except Exception as e:
            logger.warning(f"⚠️ Math generation failed: {e}")
        
        # Generate 3D geometric shapes
        print("\n🎲 Generating 3D geometric shapes...")
        try:
            shapes = self.generators['shapes_3d'].generate_all_basic_shapes()
            results['geometric_shapes'] = shapes
            print(f"✅ Generated {len(shapes)} 3D shapes")
        except Exception as e:
            logger.warning(f"⚠️ 3D shape generation failed: {e}")
        
        # Generate chemistry molecules
        print("\n⚗️ Generating chemistry molecules...")
        try:
            molecules = self.generators['chemistry'].generate_all_priority_molecules()
            results['chemistry_molecules'] = molecules
            total_mols = sum(len(v) for v in molecules.values())
            print(f"✅ Generated {total_mols} chemistry molecules")
        except Exception as e:
            logger.warning(f"⚠️ Chemistry generation failed: {e}")
        
        # Generate physics simulations
        print("\n🔬 Generating physics simulations...")
        try:
            simulations = self.generators['physics'].generate_all_simulations()
            results['physics_simulations'] = simulations
            print(f"✅ Generated {len(simulations)} physics simulations")
        except Exception as e:
            logger.warning(f"⚠️ Physics generation failed: {e}")
        
        # Generate biology body systems
        print("\n🧬 Generating biology body systems...")
        try:
            if 'biology' in self.generators:
                body_systems = self.generators['biology'].generate_all_body_systems()
                results['biology_models'] = body_systems
                print(f"✅ Generated {len(body_systems)} biology models")
        except Exception as e:
            logger.warning(f"⚠️ Biology generation failed: {e}")
        
        # Generate plant models
        print("\n🌱 Generating plant anatomy models...")
        try:
            if 'plants' in self.generators:
                plant_models = self.generators['plants'].generate_all_plant_models()
                results['plant_models'] = plant_models
                print(f"✅ Generated {len(plant_models)} plant models")
        except Exception as e:
            logger.warning(f"⚠️ Plant generation failed: {e}")
        
        # Generate molecular models
        print("\n🧪 Generating molecular structure models...")
        try:
            if 'molecular' in self.generators:
                molecular_models = self.generators['molecular'].generate_all_molecular_models()
                results['molecular_models'] = molecular_models
                print(f"✅ Generated {len(molecular_models)} molecular models")
        except Exception as e:
            logger.warning(f"⚠️ Molecular generation failed: {e}")
        
        # Generate circuit models
        print("\n⚡ Generating circuit and electrical models...")
        try:
            if 'circuits' in self.generators:
                circuit_models = self.generators['circuits'].generate_all_circuit_models()
                results['circuit_models'] = circuit_models
                print(f"✅ Generated {len(circuit_models)} circuit models")
        except Exception as e:
            logger.warning(f"⚠️ Circuit generation failed: {e}")
        
        # Generate geometric shapes for mathematics
        print("\n📐 Generating geometric shapes for mensuration...")
        try:
            if 'geometry' in self.generators:
                geometric_shapes = self.generators['geometry'].generate_all_shapes()
                results['geometric_shapes'] = geometric_shapes
                print(f"✅ Generated {len(geometric_shapes)} geometric shape models")
        except Exception as e:
            logger.warning(f"⚠️ Geometric shape generation failed: {e}")

        # Generate wave & optics models
        print("\n🌈 Generating wave & optics models...")
        try:
            if 'optics' in self.generators:
                optics_models = self.generators['optics'].generate_all_models()
                results['optics_models'] = optics_models
                print(f"✅ Generated {len(optics_models)} wave & optics models")
        except Exception as e:
            logger.warning(f"⚠️ Wave/Optics generation failed: {e}")
        
        # Generate cell biology models
        print("\n🧬 Generating cell biology models...")
        try:
            if 'cells' in self.generators:
                cell_models = self.generators['cells'].generate_all_models()
                results['cell_models'] = cell_models
                print(f"✅ Generated {len(cell_models)} cell biology models")
        except Exception as e:
            logger.warning(f"⚠️ Cell biology generation failed: {e}")
        
        # Generate simple machines models
        print("\n🔧 Generating simple machines models...")
        try:
            if 'machines' in self.generators:
                machine_models = self.generators['machines'].generate_all_models()
                results['machine_models'] = machine_models
                print(f"✅ Generated {len(machine_models)} simple machines models")
        except Exception as e:
            logger.warning(f"⚠️ Simple machines generation failed: {e}")
        
        # Generate earth and space models
        print("\n🌍 Generating earth and space models...")
        try:
            if 'space' in self.generators:
                space_models = self.generators['space'].generate_all_models()
                results['space_models'] = space_models
                print(f"✅ Generated {len(space_models)} earth and space models")
        except Exception as e:
            logger.warning(f"⚠️ Earth/space generation failed: {e}")
        
        # Generate agriculture models
        print("\n🌾 Generating agriculture models...")
        try:
            if 'agriculture' in self.generators:
                agriculture_models = self.generators['agriculture'].generate_all_models()
                results['agriculture_models'] = agriculture_models
                print(f"✅ Generated {len(agriculture_models)} agriculture models")
        except Exception as e:
            logger.warning(f"⚠️ Agriculture generation failed: {e}")
        
        # Generate reproductive systems models
        print("\n🔬 Generating reproductive systems models...")
        try:
            if 'reproductive_systems' in self.generators:
                reproductive_models = self.generators['reproductive_systems'].generate_all_models()
                results['reproductive_models'] = reproductive_models
                print(f"✅ Generated {len(reproductive_models)} reproductive systems models")
        except Exception as e:
            logger.warning(f"⚠️ Reproductive systems generation failed: {e}")
        
        # Generate mathematical functions models
        print("\n📐 Generating mathematical functions models...")
        try:
            if 'mathematical_functions' in self.generators:
                math_function_models = self.generators['mathematical_functions'].generate_all_models()
                results['math_function_models'] = math_function_models
                print(f"✅ Generated {len(math_function_models)} mathematical functions models")
        except Exception as e:
            logger.warning(f"⚠️ Mathematical functions generation failed: {e}")
        
        # Generate Nigerian cultural models
        print("\n🏛️ Generating Nigerian cultural models...")
        try:
            if 'nigerian_cultural' in self.generators:
                cultural_models = self.generators['nigerian_cultural'].generate_all_models()
                results['cultural_models'] = cultural_models
                print(f"✅ Generated {len(cultural_models)} Nigerian cultural models")
        except Exception as e:
            logger.warning(f"⚠️ Nigerian cultural generation failed: {e}")
        
        # Update manifest
        self.manifest['updated_at'] = datetime.now().isoformat()
        self.manifest['total_assets'] = (
            len(results['math_diagrams']) +
            len(results['geometric_shapes']) +
            sum(len(v) for v in results['chemistry_molecules'].values()) +
            len(results['physics_simulations']) +
            len(results['biology_models']) +
            len(results['plant_models']) +
            len(results['molecular_models']) +
            len(results['circuit_models']) +
            len(results.get('geometric_shapes', [])) +
            len(results.get('optics_models', [])) +
            len(results.get('cell_models', [])) +
            len(results.get('machine_models', [])) +
            len(results.get('space_models', [])) +
            len(results.get('agriculture_models', [])) +
            len(results.get('reproductive_models', [])) +
            len(results.get('math_function_models', [])) +
            len(results.get('cultural_models', []))
        )
        self._save_manifest()
        
        print("\n" + "="*60)
        print(f"✅ Total assets generated: {self.manifest['total_assets']}")
        print(f"📄 Manifest saved: {self.manifest_path}")
        print("="*60)
        
        return results
    
    def generate_subject_pack(self, subject: str, grade_level: str = None) -> Dict[str, Any]:
        """
        Generate complete asset pack for a subject
        
        Args:
            subject: Subject name (Mathematics, Chemistry, Physics, etc.)
            grade_level: Optional grade level
            
        Returns:
            Dictionary of generated assets
        """
        logger.info(f"📚 Generating asset pack for {subject} ({grade_level or 'all levels'})")
        
        pack = {
            "subject": subject,
            "grade_level": grade_level,
            "generated_at": datetime.now().isoformat(),
            "assets": {}
        }
        
        subject_lower = subject.lower()
        
        # Generate subject-specific assets
        if subject_lower in ['mathematics', 'math']:
            try:
                pack['assets']['diagrams'] = self.generators['math_2d'].generate_all_basic_diagrams()
                pack['assets']['shapes'] = self.generators['shapes_3d'].generate_all_basic_shapes()
            except Exception as e:
                logger.warning(f"⚠️ Failed to generate math pack: {e}")
        
        elif subject_lower in ['chemistry', 'chem']:
            try:
                pack['assets']['molecules'] = self.generators['chemistry'].generate_all_priority_molecules()
            except Exception as e:
                logger.warning(f"⚠️ Failed to generate chemistry pack: {e}")
        
        elif subject_lower in ['physics', 'phys']:
            try:
                pack['assets']['simulations'] = self.generators['physics'].generate_all_simulations()
            except Exception as e:
                logger.warning(f"⚠️ Failed to generate physics pack: {e}")
        
        return pack
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get generation statistics"""
        stats = {
            "total_generators": len(self.generators),
            "generators": list(self.generators.keys()),
            "manifest": self.manifest,
            "timestamp": datetime.now().isoformat()
        }
        return stats


def main():
    """Command-line interface for asset generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Akulearn Graphics and 3D Asset Generator")
    parser.add_argument('--action', choices=['generate_all', 'generate_pack', 'generate_lesson', 'stats'],
                       default='generate_all', help='Action to perform')
    parser.add_argument('--subject', help='Subject for asset pack generation')
    parser.add_argument('--grade', help='Grade level')
    parser.add_argument('--lesson', type=json.loads, help='Lesson metadata as JSON')
    
    args = parser.parse_args()
    
    manager = AssetGeneratorManager()
    
    if args.action == 'generate_all':
        print("\n🎨 Generating all priority assets...\n")
        results = manager.generate_all_priority_assets()
        print("\n✅ Generation complete!")
    
    elif args.action == 'generate_pack' and args.subject:
        print(f"\n📚 Generating {args.subject} asset pack...\n")
        pack = manager.generate_subject_pack(args.subject, args.grade)
        print(f"\n✅ {args.subject} pack generated!")
        print(f"Assets: {len(pack['assets'])} categories")
    
    elif args.action == 'generate_lesson' and args.lesson:
        print(f"\n📖 Generating lesson assets...\n")
        assets = manager.generate_for_lesson(args.lesson)
        print(f"\n✅ Lesson assets generated!")
        for category, files in assets.items():
            if files:
                print(f"{category}: {len(files)} files")
    
    elif args.action == 'stats':
        stats = manager.get_statistics()
        print("\n" + "="*60)
        print("📊 Asset Generation Statistics")
        print("="*60)
        print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
