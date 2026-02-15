"""
Reproductive Systems 3D Model Generator - Priority #11

Generates 6 interactive reproductive biology models for Nigerian secondary education (bio_007).
Culturally sensitive implementation for SS2/SS3 Biology curriculum.

Models:
1. male_reproductive_system.glb - Male anatomy with organs and ducts
2. female_reproductive_system.glb - Female anatomy with ovary cycle
3. flower_reproduction.glb - Plant pollination and fertilization
4. fetus_development.glb - Embryonic development stages (trimester progression)
5. gamete_formation.glb - Spermatogenesis and oogenesis processes
6. menstrual_cycle.glb - Hormonal and physical phases of menstrual cycle

Educational Focus: Comprehensive, medically accurate, culturally appropriate for Nigerian schools
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
import trimesh

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class ReproductiveSystemsModelGenerator:
    """Generates 6 reproductive system models for Nigerian secondary biology education."""

    def __init__(self):
        """Initialize the generator."""
        self.output_dir = Path('generated_assets/reproductive_systems')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("🔬 Reproductive Systems Generator initialized")

    def _create_sphere(self, center: Tuple[float, float, float], radius: float, color: Tuple[int, int, int], subdivisions: int = 2) -> trimesh.Trimesh:
        """Create a sphere primitive."""
        sphere = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
        sphere.apply_translation(center)
        sphere.visual.vertex_colors = color
        return sphere

    def _create_cylinder(self, start: Tuple[float, float, float], end: Tuple[float, float, float], radius: float, color: Tuple[int, int, int], sections: int = 16) -> trimesh.Trimesh:
        """Create a cylinder between two points."""
        height = np.linalg.norm(np.array(end) - np.array(start))
        cyl = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
        direction = np.array(end) - np.array(start)
        if height > 0:
            direction = direction / height
        up = np.array([0, 0, 1])
        if abs(np.dot(direction, up)) > 0.99:
            up = np.array([1, 0, 0])
        right = np.cross(direction, up)
        right = right / np.linalg.norm(right)
        actual_up = np.cross(right, direction)
        rotation_matrix = np.column_stack([right, actual_up, direction])
        transform = np.eye(4)
        transform[:3, :3] = rotation_matrix
        cyl.apply_transform(transform)
        mid_point = (np.array(start) + np.array(end)) / 2
        cyl.apply_translation(mid_point)
        cyl.visual.vertex_colors = color
        return cyl

    def _create_box(self, center: Tuple[float, float, float], extents: Tuple[float, float, float], color: Tuple[int, int, int]) -> trimesh.Trimesh:
        """Create a box primitive."""
        box = trimesh.creation.box(extents=extents)
        box.apply_translation(center)
        box.visual.vertex_colors = color
        return box

    def _create_cone(self, height: float, radius: float, color: Tuple[int, int, int], position: Tuple[float, float, float] = (0, 0, 0)) -> trimesh.Trimesh:
        """Create a cone primitive."""
        cone = trimesh.creation.cone(radius=radius, height=height, sections=16)
        cone.apply_translation(position)
        cone.visual.vertex_colors = color
        return cone

    def generate_male_reproductive_system(self) -> str:
        """Generate male reproductive system model."""
        logger.info("📍 Generating male reproductive system...")
        meshes = []

        # Pelvic structure (reference)
        pelvis_box = self._create_box((0, 0, -2), (3, 2, 0.5), (200, 150, 100))
        meshes.append(pelvis_box)

        # Testes (2)
        left_testis = self._create_sphere((-1.2, 0, 0.5), 0.4, (220, 180, 160))
        right_testis = self._create_sphere((1.2, 0, 0.5), 0.4, (220, 180, 160))
        meshes.extend([left_testis, right_testis])

        # Epididymis (coiled tube on each testis) - represented as torus-like
        left_epididymis_1 = self._create_cylinder((-1.2, 0, 0.9), (-1.2, 0.4, 0.9), 0.15, (180, 150, 140))
        left_epididymis_2 = self._create_cylinder((-1.2, 0.4, 0.9), (-1.2, 0, 1.2), 0.15, (180, 150, 140))
        right_epididymis_1 = self._create_cylinder((1.2, 0, 0.9), (1.2, 0.4, 0.9), 0.15, (180, 150, 140))
        right_epididymis_2 = self._create_cylinder((1.2, 0.4, 0.9), (1.2, 0, 1.2), 0.15, (180, 150, 140))
        meshes.extend([left_epididymis_1, left_epididymis_2, right_epididymis_1, right_epididymis_2])

        # Vas deferens (ducts from testes to urethra)
        left_vas = self._create_cylinder((-1.2, 0, 1.2), (-0.3, 0, 2.5), 0.12, (160, 140, 130))
        right_vas = self._create_cylinder((1.2, 0, 1.2), (0.3, 0, 2.5), 0.12, (160, 140, 130))
        meshes.extend([left_vas, right_vas])

        # Prostate gland (around urethra)
        prostate = self._create_sphere((0, 0, 2.2), 0.35, (200, 100, 80))
        meshes.append(prostate)

        # Seminal vesicles (2, behind bladder)
        left_seminal = self._create_box((-0.6, -0.3, 2.8), (0.3, 0.4, 0.5), (180, 120, 100))
        right_seminal = self._create_box((0.6, -0.3, 2.8), (0.3, 0.4, 0.5), (180, 120, 100))
        meshes.extend([left_seminal, right_seminal])

        # Cowper's glands (Bulbourethral glands)
        left_cowper = self._create_sphere((-0.4, 0.2, 1.5), 0.15, (200, 150, 130))
        right_cowper = self._create_sphere((0.4, 0.2, 1.5), 0.15, (200, 150, 130))
        meshes.extend([left_cowper, right_cowper])

        # Urethra (central channel)
        urethra = self._create_cylinder((0, 0, 2.2), (0, 0, -3), 0.1, (150, 120, 110))
        meshes.append(urethra)

        # Penis (external)
        penis_shaft = self._create_cylinder((0, 0.5, -2.5), (0, 1.5, -2.5), 0.25, (220, 180, 160))
        glans = self._create_cone(0.4, 0.3, (230, 190, 170), (0, 1.8, -2.5))
        meshes.extend([penis_shaft, glans])

        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        file_path = self.output_dir / 'male_reproductive_system.glb'
        combined.export(file_path)
        file_size = file_path.stat().st_size / 1024
        logger.info(f"✅ male_reproductive_system.glb created ({file_size:.2f} KB)")
        return str(file_path)

    def generate_female_reproductive_system(self) -> str:
        """Generate female reproductive system model."""
        logger.info("📍 Generating female reproductive system...")
        meshes = []

        # Pelvic structure (reference)
        pelvis_box = self._create_box((0, 0, -2), (3.5, 2.5, 0.5), (200, 150, 100))
        meshes.append(pelvis_box)

        # Ovaries (2)
        left_ovary = self._create_sphere((-1.3, -0.5, 0.8), 0.35, (220, 150, 180))
        right_ovary = self._create_sphere((1.3, -0.5, 0.8), 0.35, (220, 150, 180))
        # Add follicles on ovaries
        left_follicles = [self._create_sphere((-1.1, -0.3, 0.6), 0.08, (180, 100, 140)) for _ in range(3)]
        right_follicles = [self._create_sphere((1.1, -0.3, 0.6), 0.08, (180, 100, 140)) for _ in range(3)]
        meshes.extend([left_ovary, right_ovary] + left_follicles + right_follicles)

        # Fallopian tubes (oviducts)
        left_tube = self._create_cylinder((-1.3, -0.5, 0.8), (-0.2, 0.3, 1.3), 0.15, (180, 140, 160))
        right_tube = self._create_cylinder((1.3, -0.5, 0.8), (0.2, 0.3, 1.3), 0.15, (180, 140, 160))
        # Fimbriae (finger-like projections at tube opening)
        for i in range(4):
            angle = i * np.pi / 2
            fimbriae_pos = (-1.3 + 0.3*np.cos(angle), -0.5 + 0.3*np.sin(angle), 0.8)
            fimbriae = self._create_cone(0.2, 0.05, (160, 120, 140), fimbriae_pos)
            meshes.append(fimbriae)
        meshes.extend([left_tube, right_tube])

        # Uterus (pear-shaped)
        uterus_body = self._create_sphere((0, 0, 1.2), 0.4, (200, 100, 120))
        uterus_neck = self._create_cylinder((0, 0, 1.2), (0, 0, 0.4), 0.2, (180, 80, 100))
        meshes.extend([uterus_body, uterus_neck])

        # Endometrium (uterine lining) - inner layer
        endometrium = self._create_sphere((0, 0, 1.2), 0.35, (220, 140, 160))
        meshes.append(endometrium)

        # Vagina (canal)
        vagina = self._create_cylinder((0, -0.5, 0.4), (0, -1.5, 0.4), 0.3, (180, 100, 130))
        meshes.append(vagina)

        # Cervix (opening into vagina)
        cervix = self._create_sphere((0, 0, 0.4), 0.22, (170, 80, 110))
        meshes.append(cervix)

        # Clitoris
        clitoris = self._create_sphere((0, 0.1, -0.3), 0.08, (200, 100, 130))
        meshes.append(clitoris)

        # Labia (external genitalia)
        labia_major_left = self._create_box((-0.5, -0.8, -0.5), (0.3, 0.4, 0.2), (200, 130, 150))
        labia_major_right = self._create_box((0.5, -0.8, -0.5), (0.3, 0.4, 0.2), (200, 130, 150))
        meshes.extend([labia_major_left, labia_major_right])

        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        file_path = self.output_dir / 'female_reproductive_system.glb'
        combined.export(file_path)
        file_size = file_path.stat().st_size / 1024
        logger.info(f"✅ female_reproductive_system.glb created ({file_size:.2f} KB)")
        return str(file_path)

    def generate_flower_reproduction(self) -> str:
        """Generate flower pollination and reproduction model."""
        logger.info("📍 Generating flower reproduction model...")
        meshes = []

        # Flower base
        flower_base = self._create_cylinder((0, 0, 0), (0, 0, -1), 0.3, (100, 150, 80))
        meshes.append(flower_base)

        # Sepals (4, green)
        for i in range(4):
            angle = i * np.pi / 2
            sepal_x = 0.4 * np.cos(angle)
            sepal_y = 0.4 * np.sin(angle)
            sepal = self._create_box((sepal_x, sepal_y, -0.2), (0.2, 0.2, 0.1), (80, 150, 60))
            meshes.append(sepal)

        # Petals (4, colored)
        petal_colors = [(255, 100, 150), (255, 150, 100), (100, 150, 255), (255, 255, 100)]
        for i, color in enumerate(petal_colors):
            angle = (i + 0.5) * np.pi / 2
            petal_x = 0.6 * np.cos(angle)
            petal_y = 0.6 * np.sin(angle)
            petal = self._create_cone(0.5, 0.15, color, (petal_x, petal_y, 0.3))
            meshes.append(petal)

        # Stamens (male parts - anthers + filaments)
        for i in range(6):
            angle = i * np.pi / 3
            stamen_x = 0.25 * np.cos(angle)
            stamen_y = 0.25 * np.sin(angle)
            filament = self._create_cylinder((stamen_x, stamen_y, 0), (stamen_x, stamen_y, 0.3), 0.05, (200, 180, 140))
            anther = self._create_sphere((stamen_x, stamen_y, 0.35), 0.08, (255, 200, 50))  # Pollen grains
            meshes.extend([filament, anther])

        # Pistil (female part - stigma + style + ovary)
        stigma = self._create_sphere((0, 0, 0.4), 0.12, (200, 100, 150))
        style = self._create_cylinder((0, 0, 0.4), (0, 0, 0.05), 0.08, (180, 100, 140))
        ovary = self._create_sphere((0, 0, 0), 0.15, (150, 180, 200))
        meshes.extend([stigma, style, ovary])

        # Pollen grain (floating - representing pollination)
        pollen_grain = self._create_sphere((0.3, 0.3, 0.5), 0.05, (255, 220, 100))
        meshes.append(pollen_grain)

        # Pollen tube (growing down after pollination)
        pollen_tube = self._create_cylinder((0.3, 0.3, 0.5), (0, 0, 0.1), 0.03, (220, 200, 100))
        meshes.append(pollen_tube)

        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        file_path = self.output_dir / 'flower_reproduction.glb'
        combined.export(file_path)
        file_size = file_path.stat().st_size / 1024
        logger.info(f"✅ flower_reproduction.glb created ({file_size:.2f} KB)")
        return str(file_path)

    def generate_fetus_development(self) -> str:
        """Generate embryonic/fetal development stages (3 trimesters)."""
        logger.info("📍 Generating fetus development stages...")
        meshes = []

        # Add labels for stages visually
        # Stage 1: Early embryo (Week 4-8)
        embryo_stage1 = self._create_sphere((-2, 0, 0), 0.3, (200, 150, 200))
        amniotic_sac1 = self._create_sphere((-2, 0, 0), 0.4, (180, 200, 220))
        amniotic_sac1.visual.vertex_colors = [180, 200, 220, 100]  # Semi-transparent
        meshes.extend([amniotic_sac1, embryo_stage1])

        # Stage 2: Early fetus (Week 12) - Trimester 1
        fetus_stage2_body = self._create_sphere((0, 0, 0), 0.5, (200, 160, 180))
        fetus_stage2_head = self._create_sphere((0, 0, 0.6), 0.35, (220, 180, 200))
        # Early limb buds
        limb_1 = self._create_cylinder((-0.4, 0, 0.2), (-0.6, 0, 0.1), 0.1, (200, 160, 180))
        limb_2 = self._create_cylinder((0.4, 0, 0.2), (0.6, 0, 0.1), 0.1, (200, 160, 180))
        limb_3 = self._create_cylinder((-0.3, 0, -0.4), (-0.4, 0, -0.7), 0.1, (200, 160, 180))
        limb_4 = self._create_cylinder((0.3, 0, -0.4), (0.4, 0, -0.7), 0.1, (200, 160, 180))
        amniotic_sac2 = self._create_sphere((0, 0, 0), 0.7, (180, 200, 220))
        meshes.extend([amniotic_sac2, fetus_stage2_body, fetus_stage2_head, limb_1, limb_2, limb_3, limb_4])

        # Stage 3: Mid-trimester fetus (Week 20) - Trimester 2
        fetus_stage3_body = self._create_sphere((2, 0, 0), 0.65, (210, 170, 190))
        fetus_stage3_head = self._create_sphere((2, 0, 0.8), 0.4, (230, 190, 210))
        # More developed limbs
        stage3_limb_1 = self._create_cylinder((1.5, 0, 0.2), (1.1, 0, -0.1), 0.12, (210, 170, 190))
        stage3_limb_2 = self._create_cylinder((2.5, 0, 0.2), (2.9, 0, -0.1), 0.12, (210, 170, 190))
        stage3_limb_3 = self._create_cylinder((1.8, 0, -0.5), (1.6, 0, -1.0), 0.12, (210, 170, 190))
        stage3_limb_4 = self._create_cylinder((2.2, 0, -0.5), (2.4, 0, -1.0), 0.12, (210, 170, 190))
        # Umbilical cord
        umbilical = self._create_cylinder((2, 0, -0.7), (2, -0.8, -0.7), 0.08, (255, 150, 100))
        amniotic_sac3 = self._create_sphere((2, 0, 0), 0.85, (180, 200, 220))
        meshes.extend([amniotic_sac3, fetus_stage3_body, fetus_stage3_head, stage3_limb_1, stage3_limb_2, stage3_limb_3, stage3_limb_4, umbilical])

        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        file_path = self.output_dir / 'fetus_development.glb'
        combined.export(file_path)
        file_size = file_path.stat().st_size / 1024
        logger.info(f"✅ fetus_development.glb created ({file_size:.2f} KB)")
        return str(file_path)

    def generate_gamete_formation(self) -> str:
        """Generate spermatogenesis and oogenesis processes."""
        logger.info("📍 Generating gamete formation (spermatogenesis & oogenesis)...")
        meshes = []

        # SPERMATOGENESIS (left side)
        # Primary spermatocyte (diploid)
        primary_sperm = self._create_sphere((-2, 1, 0), 0.35, (200, 150, 200))
        # Nucleus
        nucleus_primary = self._create_sphere((-2, 1, 0), 0.2, (100, 50, 150))
        meshes.extend([primary_sperm, nucleus_primary])

        # Secondary spermatocytes (haploid, after meiosis 1)
        secondary_sperm1 = self._create_sphere((-3, 1.5, 0), 0.28, (180, 130, 180))
        secondary_sperm2 = self._create_sphere((-1, 1.5, 0), 0.28, (180, 130, 180))
        nucleus_sec1 = self._create_sphere((-3, 1.5, 0), 0.15, (80, 30, 130))
        nucleus_sec2 = self._create_sphere((-1, 1.5, 0), 0.15, (80, 30, 130))
        meshes.extend([secondary_sperm1, secondary_sperm2, nucleus_sec1, nucleus_sec2])

        # Spermatids (developing sperm)
        for i, x_pos in enumerate([-3.5, -2.5, -1.5, -0.5]):
            spermatid = self._create_sphere((x_pos, 2.2, 0), 0.2, (150, 100, 150))
            nucleus_sperm = self._create_sphere((x_pos, 2.2, 0), 0.1, (60, 20, 120))
            meshes.extend([spermatid, nucleus_sperm])

        # Mature spermatozoa (with flagella)
        for i, x_pos in enumerate([-3.5, -2.5, -1.5, -0.5]):
            head = self._create_sphere((x_pos, 3.3, 0), 0.15, (120, 80, 140))
            midpiece = self._create_cylinder((x_pos, 3.3, 0), (x_pos, 3.3, -0.3), 0.08, (100, 60, 130))
            flagella = self._create_cylinder((x_pos, 3.3, -0.3), (x_pos, 3.3, -0.9), 0.05, (80, 40, 120))
            meshes.extend([head, midpiece, flagella])

        # OOGENESIS (right side)
        # Primary oocyte (diploid, in prophase I)
        primary_oocyte = self._create_sphere((2, 1, 0), 0.35, (220, 160, 200))
        nucleus_primary_oocyte = self._create_sphere((2, 1, 0), 0.2, (120, 80, 160))
        # First polar body
        polar_body1_early = self._create_sphere((2, 1.5, 0.3), 0.1, (150, 100, 150))
        meshes.extend([primary_oocyte, nucleus_primary_oocyte, polar_body1_early])

        # Secondary oocyte (after meiosis 1, metaphase II)
        secondary_oocyte = self._create_sphere((3.2, 1.5, 0), 0.3, (200, 140, 180))
        nucleus_sec_oocyte = self._create_sphere((3.2, 1.5, 0), 0.15, (100, 60, 150))
        # First polar body (degenerates)
        polar_body1 = self._create_sphere((3.5, 1.8, 0.2), 0.08, (120, 80, 130))
        meshes.extend([secondary_oocyte, nucleus_sec_oocyte, polar_body1])

        # Ovum (mature, after meiosis 2)
        ovum = self._create_sphere((4.5, 2.2, 0), 0.32, (180, 140, 180))
        nucleus_ovum = self._create_sphere((4.5, 2.2, 0), 0.12, (100, 50, 150))
        # Polar bodies
        polar_body2 = self._create_sphere((4.8, 2.5, 0.2), 0.06, (100, 60, 130))
        polar_body3 = self._create_sphere((4.3, 2.5, 0.2), 0.06, (100, 60, 130))
        # Zona pellucida (clear layer around ovum)
        zona = self._create_sphere((4.5, 2.2, 0), 0.38, (200, 180, 200))
        meshes.extend([ovum, nucleus_ovum, polar_body2, polar_body3, zona])

        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        file_path = self.output_dir / 'gamete_formation.glb'
        combined.export(file_path)
        file_size = file_path.stat().st_size / 1024
        logger.info(f"✅ gamete_formation.glb created ({file_size:.2f} KB)")
        return str(file_path)

    def generate_menstrual_cycle(self) -> str:
        """Generate menstrual cycle with 4 main phases (simplified)."""
        logger.info("📍 Generating menstrual cycle...")
        meshes = []

        # PHASE 1: MENSTRUATION (Days 1-5) - Simplified
        uterus_phase1 = self._create_sphere((-2, 0, 0), 0.5, (200, 100, 120))
        endometrium_shedding = self._create_sphere((-2, 0, 0), 0.45, (220, 150, 180))
        meshes.extend([uterus_phase1, endometrium_shedding])

        # PHASE 2: FOLLICULAR PHASE (Days 5-13) - Simplified
        ovary_phase2 = self._create_sphere((0, 0, 0), 0.45, (220, 150, 180))
        follicle_1 = self._create_sphere((0.3, 0.2, 0), 0.12, (180, 120, 160))
        uterus_phase2 = self._create_sphere((0, 1.2, 0), 0.48, (200, 120, 140))
        meshes.extend([ovary_phase2, follicle_1, uterus_phase2])

        # PHASE 3: OVULATION (Around Day 14) - Simplified
        mature_follicle = self._create_sphere((2, 0, 0), 0.35, (200, 140, 180))
        ovum_released = self._create_sphere((2.5, 0.3, 0), 0.12, (180, 140, 180))
        uterus_phase3 = self._create_sphere((2, 1.2, 0), 0.5, (200, 120, 140))
        meshes.extend([mature_follicle, ovum_released, uterus_phase3])

        # PHASE 4: LUTEAL PHASE (Days 14-28) - Simplified
        corpus_luteum = self._create_sphere((4, 0, 0), 0.4, (255, 200, 100))
        uterus_phase4 = self._create_sphere((4, 1.2, 0), 0.5, (200, 100, 120))
        meshes.extend([corpus_luteum, uterus_phase4])

        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        file_path = self.output_dir / 'menstrual_cycle.glb'
        combined.export(file_path)
        file_size = file_path.stat().st_size / 1024
        logger.info(f"✅ menstrual_cycle.glb created ({file_size:.2f} KB)")
        return str(file_path)

    def generate_all_models(self) -> Dict[str, str]:
        """Generate all reproductive system models and return file paths."""
        logger.info("🔬 Generating all reproductive system models...")

        models = {
            'male_reproductive_system': self.generate_male_reproductive_system(),
            'female_reproductive_system': self.generate_female_reproductive_system(),
            'flower_reproduction': self.generate_flower_reproduction(),
            'fetus_development': self.generate_fetus_development(),
            'gamete_formation': self.generate_gamete_formation(),
            'menstrual_cycle': self.generate_menstrual_cycle(),
        }

        # Generate manifest
        self.generate_manifest()

        return models

    def generate_manifest(self) -> None:
        """Generate manifest with metadata for all reproductive models."""
        manifest = {
            "priority": 11,
            "category": "Reproductive Biology",
            "curriculum_topics": ["bio_007"],
            "grade_levels": ["SS2", "SS3"],
            "total_models": 6,
            "models": [
                {
                    "id": "male_reproductive_system",
                    "name": "Male Reproductive System",
                    "filename": "male_reproductive_system.glb",
                    "description": "Complete male reproductive anatomy with testes, epididymis, vas deferens, prostate, seminal vesicles, and external genitalia",
                    "anatomical_focus": ["Spermatogenesis", "Hormone regulation", "Sexual function"],
                    "curriculum_alignment": "bio_007 - Human Reproductive Systems",
                    "nigerian_context": "Standard medical biology curriculum (SS2/SS3)",
                    "educational_value": "Understand male reproductive anatomy and sperm production"
                },
                {
                    "id": "female_reproductive_system",
                    "name": "Female Reproductive System",
                    "filename": "female_reproductive_system.glb",
                    "description": "Complete female reproductive anatomy with ovaries, fallopian tubes, uterus, vagina, and external genitalia",
                    "anatomical_focus": ["Oogenesis", "Menstrual cycle", "Fertility"],
                    "curriculum_alignment": "bio_007 - Human Reproductive Systems",
                    "nigerian_context": "Standard medical biology curriculum (SS2/SS3)",
                    "educational_value": "Understand female reproductive anatomy and egg production"
                },
                {
                    "id": "flower_reproduction",
                    "name": "Flower Reproduction and Pollination",
                    "filename": "flower_reproduction.glb",
                    "description": "Plant reproductive system showing flower structure, stamens, pistil, pollen grains, and pollination process",
                    "anatomical_focus": ["Stamen (male)", "Pistil (female)", "Pollination", "Fertilization"],
                    "curriculum_alignment": "bio_007 - Reproduction in Plants",
                    "nigerian_context": "Agricultural relevance - Understanding crop reproduction",
                    "educational_value": "Understand plant reproductive strategies and pollination mechanisms"
                },
                {
                    "id": "fetus_development",
                    "name": "Fetal Development Stages",
                    "filename": "fetus_development.glb",
                    "description": "Embryonic and fetal development from conception through three trimesters",
                    "anatomical_focus": ["Embryogenesis", "Organ formation", "Fetal growth", "Placental development"],
                    "curriculum_alignment": "bio_007 - Human Development",
                    "nigerian_context": "Prenatal care understanding for health education",
                    "educational_value": "Understand human development and importance of maternal health"
                },
                {
                    "id": "gamete_formation",
                    "name": "Gamete Formation (Spermatogenesis & Oogenesis)",
                    "filename": "gamete_formation.glb",
                    "description": "Comparative study of sperm and egg production showing meiosis processes",
                    "anatomical_focus": ["Meiosis", "Chromosome reduction", "Polar bodies", "Gamete maturation"],
                    "curriculum_alignment": "bio_007 - Gametogenesis",
                    "nigerian_context": "Foundation for understanding inherited traits",
                    "educational_value": "Understand meiosis and the formation of gametes"
                },
                {
                    "id": "menstrual_cycle",
                    "name": "Menstrual Cycle Phases",
                    "filename": "menstrual_cycle.glb",
                    "description": "Complete 28-day menstrual cycle with menstrual, follicular, ovulation, and luteal phases",
                    "anatomical_focus": ["Hormone regulation", "Endometrial changes", "Ovulation", "Hormone cycles"],
                    "curriculum_alignment": "bio_007 - Female Reproductive Physiology",
                    "nigerian_context": "Health education - Understanding female reproductive health",
                    "educational_value": "Understand hormonal regulation of reproductive cycles"
                }
            ],
            "total_file_size_kb": None,  # Will be updated after all models generated
            "file_format": "glb",
            "target_platform": "WebAR, VR headsets, Mobile AR",
            "cultural_sensitivity_notes": "All models presented with scientific accuracy and cultural appropriateness for Nigerian secondary education. Emphasis on biological processes and health understanding rather than explicit content.",
            "lesson_routing_keywords": {
                "male_reproduction": ["male reproductive system", "testis", "testis", "epididymis", "vas deferens", "prostate", "semen", "sperm production", "spermatogenesis"],
                "female_reproduction": ["female reproductive system", "ovary", "fallopian tube", "uterus", "vagina", "egg", "oogenesis", "ovulation"],
                "plant_reproduction": ["flower reproduction", "pollination", "stamen", "pistil", "anther", "stigma", "ovule", "seed formation"],
                "development": ["fetus development", "embryo", "pregnancy", "trimester", "gestation", "placenta", "umbilical cord"],
                "meiosis": ["gamete formation", "spermatogenesis", "oogenesis", "meiosis", "polar body", "chromosome reduction", "haploid"],
                "hormones": ["menstrual cycle", "hormone", "FSH", "LH", "estrogen", "progesterone", "ovulation", "menstruation", "cycle"]
            }
        }

        manifest_path = self.output_dir / 'reproductive_systems_manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        logger.info(f"📋 Manifest created: {manifest_path}")


def main():
    """Generate all reproductive system models."""
    generator = ReproductiveSystemsModelGenerator()
    models = generator.generate_all_models()

    print("\n✅ Generated 6 Reproductive Systems models:")
    for model_name, model_path in models.items():
        file_size = Path(model_path).stat().st_size / 1024
        print(f"  - {model_name}.glb: {file_size:.2f} KB")

    # Calculate total
    total_size = sum(Path(path).stat().st_size for path in models.values()) / 1024
    print(f"\nTotal: {total_size:.2f} KB")


if __name__ == '__main__':
    main()
