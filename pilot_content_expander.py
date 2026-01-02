#!/usr/bin/env python3
"""
Pilot Content Expander - Generate Additional Lessons
Creates 3 more high-priority lessons to complete the pilot set
"""

import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime


class PilotContentExpander:
    """Generate 3 additional pilot lessons"""
    
    def __init__(self):
        self.output_dir = "generated_content"
        self.diagrams_dir = os.path.join(self.output_dir, "diagrams")
        os.makedirs(self.diagrams_dir, exist_ok=True)
    
    def generate_chemical_bonding_lesson(self) -> dict:
        """Generate Chemistry lesson on Chemical Bonding"""
        topic_id = "chemistry_chemical_bonding_enhanced"
        
        # Create bonding diagrams
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # Ionic Bonding: Na + Cl
        ax = axes[0, 0]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Ionic Bonding: Na + Cl → Na⁺Cl⁻', fontsize=14, fontweight='bold')
        
        # Sodium atom
        na_circle = plt.Circle((2.5, 5), 0.8, color='orange', ec='black', linewidth=2)
        ax.add_patch(na_circle)
        ax.text(2.5, 5, 'Na', fontsize=16, ha='center', va='center', fontweight='bold')
        ax.text(2.5, 6.2, '11e⁻', fontsize=10, ha='center')
        
        # Electron
        electron = plt.Circle((3.8, 5), 0.15, color='red', ec='black', linewidth=1)
        ax.add_patch(electron)
        ax.text(3.8, 5.5, 'e⁻', fontsize=9, ha='center')
        
        # Arrow
        ax.arrow(4.5, 5, 1.5, 0, head_width=0.3, head_length=0.3, fc='blue', ec='blue', linewidth=2)
        
        # Chlorine atom
        cl_circle = plt.Circle((7.5, 5), 0.9, color='green', ec='black', linewidth=2)
        ax.add_patch(cl_circle)
        ax.text(7.5, 5, 'Cl', fontsize=16, ha='center', va='center', fontweight='bold')
        ax.text(7.5, 6.3, '17e⁻', fontsize=10, ha='center')
        
        ax.text(5, 2, 'Electron Transfer: Na loses 1e⁻, Cl gains 1e⁻', fontsize=11, ha='center',
                bbox=dict(boxstyle='round', facecolor='yellow'))
        
        # Covalent Bonding: H₂O
        ax = axes[0, 1]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Covalent Bonding: Water (H₂O)', fontsize=14, fontweight='bold')
        
        # Oxygen
        o_circle = plt.Circle((5, 5), 1.2, color='lightblue', ec='black', linewidth=2)
        ax.add_patch(o_circle)
        ax.text(5, 5, 'O', fontsize=18, ha='center', va='center', fontweight='bold')
        
        # Hydrogen atoms
        h1_circle = plt.Circle((3, 6.5), 0.6, color='lightyellow', ec='black', linewidth=2)
        ax.add_patch(h1_circle)
        ax.text(3, 6.5, 'H', fontsize=14, ha='center', va='center', fontweight='bold')
        
        h2_circle = plt.Circle((3, 3.5), 0.6, color='lightyellow', ec='black', linewidth=2)
        ax.add_patch(h2_circle)
        ax.text(3, 3.5, 'H', fontsize=14, ha='center', va='center', fontweight='bold')
        
        # Covalent bonds (shared electrons)
        ax.plot([3.6, 4.2], [6.3, 5.8], 'r-', linewidth=3, label='Shared electrons')
        ax.plot([3.6, 4.2], [3.7, 4.2], 'r-', linewidth=3)
        
        # Electron dots
        for x, y in [(3.8, 6.1), (4.0, 5.9), (3.8, 3.9), (4.0, 4.1)]:
            ax.plot(x, y, 'ro', markersize=8)
        
        ax.text(5, 2, 'Electron Sharing: 2 pairs shared', fontsize=11, ha='center',
                bbox=dict(boxstyle='round', facecolor='lightgreen'))
        
        # Metallic Bonding
        ax = axes[1, 0]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Metallic Bonding: Sea of Electrons', fontsize=14, fontweight='bold')
        
        # Metal ions in lattice
        positions = [(2, 2), (2, 5), (2, 8), (5, 2), (5, 5), (5, 8), (8, 2), (8, 5), (8, 8)]
        for x, y in positions:
            ion = plt.Circle((x, y), 0.4, color='silver', ec='black', linewidth=2)
            ax.add_patch(ion)
            ax.text(x, y, 'M⁺', fontsize=10, ha='center', va='center', fontweight='bold')
        
        # Free electrons
        np.random.seed(42)
        for _ in range(20):
            x = np.random.uniform(1, 9)
            y = np.random.uniform(1, 9)
            ax.plot(x, y, 'ro', markersize=5, alpha=0.7)
        
        ax.text(5, 0.5, 'Delocalized electrons move freely', fontsize=11, ha='center',
                bbox=dict(boxstyle='round', facecolor='lightcyan'))
        
        # Bond types comparison
        ax = axes[1, 1]
        ax.axis('off')
        ax.set_title('Comparison of Bond Types', fontsize=14, fontweight='bold')
        
        data = [
            ['Property', 'Ionic', 'Covalent', 'Metallic'],
            ['Formation', 'e⁻ transfer', 'e⁻ sharing', 'e⁻ sea'],
            ['State at RT', 'Solid', 'Gas/Liquid/Solid', 'Solid'],
            ['Melting Point', 'High', 'Variable', 'High'],
            ['Conductivity', 'Molten/Aqueous', 'Poor', 'Excellent'],
            ['Example', 'NaCl', 'H₂O, CO₂', 'Cu, Fe']
        ]
        
        y_start = 9
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                color = 'lightblue' if i == 0 else 'white'
                weight = 'bold' if i == 0 else 'normal'
                ax.text(j*2.5 + 0.5, y_start - i*1.3, cell, fontsize=9, 
                       bbox=dict(boxstyle='round', facecolor=color),
                       fontweight=weight)
        
        plt.tight_layout()
        diagram_path = os.path.join(self.diagrams_dir, f"{topic_id}_bonding.png")
        plt.savefig(diagram_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "id": topic_id,
            "title": "Chemical Bonding: Ionic, Covalent, and Metallic",
            "subject": "Chemistry",
            "topic": "Chemical Bonding",
            "subtopic": "Types of Chemical Bonds",
            "content_type": "study_guide",
            "difficulty": "intermediate",
            "exam_board": "WAEC",
            "content": """# Chemical Bonding: Complete Guide

## 1. Why Atoms Bond

Atoms bond to achieve **stable electron configuration** (usually 8 valence electrons - octet rule).

**Exceptions**: H and He need only 2 electrons (duplet rule).

## 2. Ionic Bonding

### Definition
- Transfer of electrons from metal to non-metal
- Forms oppositely charged ions
- Electrostatic attraction holds ions together

### Example: Sodium Chloride (NaCl)
- Na (2,8,1) → Na⁺ (2,8) + e⁻
- Cl (2,8,7) + e⁻ → Cl⁻ (2,8,8)
- Na⁺Cl⁻ forms ionic compound

### Properties
✓ High melting/boiling points
✓ Conduct electricity when molten or in solution
✓ Hard but brittle crystals
✓ Soluble in water

### Nigerian Example
Common salt from Lagos salt industry - NaCl is ionic compound.

## 3. Covalent Bonding

### Definition
- Sharing of electron pairs between non-metals
- Both atoms contribute electrons
- Strong directional bonds

### Types
**Single Bond**: 1 pair shared (H-H)
**Double Bond**: 2 pairs shared (O=O)
**Triple Bond**: 3 pairs shared (N≡N)

### Example: Water (H₂O)
- O needs 2 electrons
- Each H shares 1 electron with O
- 2 O-H bonds form

### Properties
✓ Variable melting/boiling points
✓ Poor electrical conductors
✓ Can be gases, liquids, or solids
✓ Variable solubility

## 4. Metallic Bonding

### Definition
- Bonding in metals
- Positive metal ions in lattice
- Delocalized "sea of electrons" moving freely

### Properties
✓ High electrical/thermal conductivity
✓ Malleable and ductile
✓ Metallic luster
✓ High melting points (usually)

### Nigerian Context
Copper wiring in Lagos homes - metallic bonding enables conductivity.

## 5. WAEC Exam Tips

✅ Draw electron diagrams clearly
✅ Show electron transfer (ionic) vs sharing (covalent)
✅ State properties and relate to bond type
✅ Practice dot-and-cross diagrams
✅ Learn common examples for each bond type

## Practice Problems

1. Draw electron configuration for MgO formation
2. Explain why NaCl conducts when molten
3. Why is diamond hard but graphite soft? (both covalent)
4. Predict bond type: CaCl₂, H₂, Al
""",
            "diagrams": [diagram_path],
            "worked_examples": [
                {
                    "problem": "Explain the bonding in magnesium oxide (MgO).",
                    "solution": "Mg (2,8,2) loses 2e⁻ → Mg²⁺ (2,8)\nO (2,6) gains 2e⁻ → O²⁻ (2,8)\nIonic bonding by electron transfer.",
                    "answer": "Ionic bond, Mg²⁺O²⁻"
                }
            ],
            "practice_problems": [
                {
                    "question": "What type of bonding exists in CO₂?",
                    "difficulty": "basic",
                    "answer": "Covalent (double bonds)",
                    "hint": "Non-metal + Non-metal"
                }
            ],
            "nigerian_context": "Salt industry in Lagos, copper wiring in homes",
            "estimated_read_time": 20,
            "prerequisites": ["Atomic structure", "Electron configuration"],
            "learning_objectives": [
                "Distinguish between ionic, covalent, and metallic bonding",
                "Draw electron transfer and sharing diagrams",
                "Relate properties to bond type"
            ],
            "created_at": datetime.now().isoformat(),
            "status": "published"
        }
    
    def generate_cell_structure_lesson(self) -> dict:
        """Generate Biology lesson on Cell Structure"""
        topic_id = "biology_cell_structure_enhanced"
        
        # Create cell diagrams
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Animal Cell
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        ax1.set_aspect('equal')
        ax1.axis('off')
        ax1.set_title('Animal Cell', fontsize=16, fontweight='bold')
        
        # Cell membrane
        membrane = plt.Circle((5, 5), 4, fill=False, edgecolor='purple', linewidth=3)
        ax1.add_patch(membrane)
        
        # Nucleus
        nucleus = plt.Circle((5, 5), 1.5, color='lightblue', ec='darkblue', linewidth=2)
        ax1.add_patch(nucleus)
        ax1.text(5, 5, 'Nucleus', fontsize=10, ha='center', fontweight='bold')
        
        # Nucleolus
        nucleolus = plt.Circle((5, 5.5), 0.4, color='darkblue')
        ax1.add_patch(nucleolus)
        
        # Mitochondria
        for x, y in [(3, 7), (7, 7), (7, 3)]:
            mito = mpatches.Ellipse((x, y), 0.8, 0.4, color='red', ec='darkred', linewidth=1.5)
            ax1.add_patch(mito)
            ax1.plot([x-0.2, x, x+0.2], [y, y, y], 'darkred', linewidth=1)
        ax1.text(3, 7.7, 'Mitochondrion', fontsize=8)
        
        # Ribosomes (small dots)
        np.random.seed(42)
        for _ in range(15):
            x = np.random.uniform(1.5, 8.5)
            y = np.random.uniform(1.5, 8.5)
            if np.sqrt((x-5)**2 + (y-5)**2) > 1.8:  # Outside nucleus
                ax1.plot(x, y, 'ko', markersize=3)
        ax1.text(2, 2, 'Ribosomes', fontsize=8)
        
        # Lysosomes
        for x, y in [(3, 3), (6.5, 5.5)]:
            lyso = plt.Circle((x, y), 0.3, color='yellow', ec='orange', linewidth=1.5)
            ax1.add_patch(lyso)
        ax1.text(3, 2.3, 'Lysosome', fontsize=8)
        
        # Cytoplasm label
        ax1.text(5, 1, 'Cytoplasm', fontsize=9, ha='center', style='italic')
        ax1.text(5, 0.3, 'Cell Membrane', fontsize=9, ha='center', 
                bbox=dict(boxstyle='round', facecolor='purple', alpha=0.3))
        
        # Plant Cell
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 10)
        ax2.set_aspect('equal')
        ax2.axis('off')
        ax2.set_title('Plant Cell', fontsize=16, fontweight='bold')
        
        # Cell wall
        wall = mpatches.Rectangle((0.5, 0.5), 9, 9, fill=False, edgecolor='brown', linewidth=4)
        ax2.add_patch(wall)
        
        # Cell membrane (inside wall)
        membrane2 = mpatches.Rectangle((0.8, 0.8), 8.4, 8.4, fill=False, edgecolor='purple', linewidth=2)
        ax2.add_patch(membrane2)
        
        # Nucleus
        nucleus2 = plt.Circle((3, 6), 1.2, color='lightblue', ec='darkblue', linewidth=2)
        ax2.add_patch(nucleus2)
        ax2.text(3, 6, 'Nucleus', fontsize=9, ha='center', fontweight='bold')
        
        # Large central vacuole
        vacuole = mpatches.Rectangle((5.5, 2), 3.5, 6, color='lightcyan', ec='cyan', linewidth=2)
        ax2.add_patch(vacuole)
        ax2.text(7.25, 5, 'Vacuole\n(sap)', fontsize=9, ha='center')
        
        # Chloroplasts
        for x, y in [(2, 3), (3.5, 4), (2.5, 7.5), (4.5, 7)]:
            chloro = mpatches.Ellipse((x, y), 0.6, 0.4, color='green', ec='darkgreen', linewidth=1.5)
            ax2.add_patch(chloro)
            # Grana (stacks)
            for i in range(3):
                ax2.plot([x-0.15+i*0.15, x-0.15+i*0.15], [y-0.1, y+0.1], 'darkgreen', linewidth=1)
        ax2.text(2, 2.3, 'Chloroplast', fontsize=8)
        
        # Mitochondria
        mito2 = mpatches.Ellipse((4, 3), 0.6, 0.3, color='red', ec='darkred', linewidth=1.5)
        ax2.add_patch(mito2)
        
        # Labels
        ax2.text(5, 0.8, 'Cell Wall', fontsize=9, ha='center', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='brown', alpha=0.3))
        ax2.text(2, 0.8, 'Cell Membrane', fontsize=8, ha='center')
        
        plt.tight_layout()
        diagram_path = os.path.join(self.diagrams_dir, f"{topic_id}_cells.png")
        plt.savefig(diagram_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "id": topic_id,
            "title": "Cell Structure and Functions",
            "subject": "Biology",
            "topic": "Cell Biology",
            "subtopic": "Cell Structure and Organelles",
            "content_type": "study_guide",
            "difficulty": "basic",
            "exam_board": "WAEC",
            "content": """# Cell Structure: The Building Blocks of Life

## 1. Cell Theory

**Three Principles**:
1. All living things are made of cells
2. Cells are the basic unit of life
3. All cells come from pre-existing cells

## 2. Types of Cells

### Prokaryotic Cells
- No true nucleus
- No membrane-bound organelles
- Example: Bacteria

### Eukaryotic Cells
- True nucleus with nuclear membrane
- Membrane-bound organelles
- Examples: Plant and animal cells

## 3. Animal Cell Organelles

### Nucleus
- **Function**: Controls cell activities, contains DNA
- **Nigerian Context**: Like Aso Rock - the control center of Nigeria

### Mitochondrion (plural: Mitochondria)
- **Function**: Powerhouse of cell, produces energy (ATP)
- **Formula**: Glucose + O₂ → CO₂ + H₂O + Energy
- **Like**: NEPA generating electricity

### Ribosome
- **Function**: Protein synthesis
- **Location**: Free in cytoplasm or on ER

### Lysosome
- **Function**: Digestion, waste removal
- **Contains**: Digestive enzymes
- **Like**: Lagos waste management agency

### Cell Membrane
- **Function**: Controls what enters/exits cell
- **Structure**: Phospholipid bilayer
- **Property**: Selectively permeable

## 4. Plant Cell Organelles

### Cell Wall
- **Function**: Protection, shape, support
- **Composition**: Cellulose
- **Unique to**: Plants, fungi, bacteria

### Chloroplast
- **Function**: Photosynthesis
- **Contains**: Chlorophyll (green pigment)
- **Equation**: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂

### Large Central Vacuole
- **Function**: Storage of water, nutrients, waste
- **Contains**: Cell sap
- **Provides**: Turgidity (firmness)

## 5. Differences: Plant vs Animal Cells

| Feature | Plant Cell | Animal Cell |
|---------|-----------|-------------|
| Cell Wall | ✓ Present | ✗ Absent |
| Chloroplasts | ✓ Present | ✗ Absent |
| Vacuole | Large, central | Small, many |
| Shape | Fixed (rectangular) | Irregular |
| Nutrition | Autotrophic | Heterotrophic |

## 6. Cell Processes

### Diffusion
- Movement from high to low concentration
- No energy required
- Example: Oxygen into cells

### Osmosis
- Diffusion of water through membrane
- Important for plant turgidity

### Active Transport
- Movement against concentration gradient
- Requires energy (ATP)
- Example: Mineral absorption by roots

## 7. WAEC Exam Tips

✅ **Draw clear diagrams** - label at least 5 organelles
✅ **State functions** - don't just name organelles
✅ **Know differences** - plant vs animal cells
✅ **Understand processes** - diffusion, osmosis, active transport
✅ **Use Nigerian examples** - makes answers relatable

## 8. Nigerian Context Examples

**Plantain Cell**: Has cell wall (gives firm texture), chloroplasts (green when unripe), large vacuole (stores starch)

**Human Blood Cell**: No cell wall (flexible for moving through vessels), mitochondria (energy for oxygen transport)

## Practice Questions

1. List 3 differences between plant and animal cells
2. Explain the function of mitochondria
3. Why do plants cells have cell walls?
4. Draw and label an animal cell (5 parts minimum)
5. What happens to plant cells in salty water? (osmosis)

## Summary

- Cells are basic units of life
- Animal cells: nucleus, mitochondria, ribosomes, lysosomes
- Plant cells: also have cell wall, chloroplasts, large vacuole
- Each organelle has specific function
- Understand cell processes: diffusion, osmosis, active transport
""",
            "diagrams": [diagram_path],
            "worked_examples": [
                {
                    "problem": "Why do plant cells not burst when placed in water?",
                    "solution": "Cell wall provides support and prevents bursting. Water enters by osmosis, cell becomes turgid, but wall resists further expansion.",
                    "answer": "Cell wall prevents bursting"
                }
            ],
            "practice_problems": [
                {
                    "question": "Name the organelle that contains chlorophyll.",
                    "difficulty": "basic",
                    "answer": "Chloroplast",
                    "hint": "Used for photosynthesis"
                }
            ],
            "nigerian_context": "Plantain cells, blood cells, yam storage",
            "estimated_read_time": 22,
            "prerequisites": ["Basic biology"],
            "learning_objectives": [
                "Identify cell organelles and their functions",
                "Distinguish plant and animal cells",
                "Understand cell processes"
            ],
            "created_at": datetime.now().isoformat(),
            "status": "published"
        }
    
    def generate_reproduction_lesson(self) -> dict:
        """Generate Biology lesson on Reproduction"""
        topic_id = "biology_reproduction_enhanced"
        
        # Create reproduction diagrams
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # Asexual Reproduction Types
        ax = axes[0, 0]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        ax.set_title('Asexual Reproduction Types', fontsize=14, fontweight='bold')
        
        types = [
            'Binary Fission (Bacteria)',
            'Budding (Yeast)',
            'Vegetative Propagation (Plants)',
            'Spore Formation (Fungi)',
            'Fragmentation (Starfish)'
        ]
        
        y = 9
        for i, rtype in enumerate(types):
            color = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'lightcyan'][i]
            ax.text(5, y, rtype, fontsize=11, ha='center',
                   bbox=dict(boxstyle='round', facecolor=color, edgecolor='black', linewidth=2))
            y -= 1.5
        
        ax.text(5, 1, 'One parent → Identical offspring', fontsize=10, ha='center',
               bbox=dict(boxstyle='round', facecolor='yellow'), fontweight='bold')
        
        # Sexual Reproduction Process
        ax = axes[0, 1]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        ax.set_title('Sexual Reproduction in Flowering Plants', fontsize=13, fontweight='bold')
        
        # Flower diagram (simple)
        # Stigma
        ax.plot([5, 5], [8, 6.5], 'g-', linewidth=3)
        stigma = plt.Circle((5, 8.2), 0.3, color='pink', ec='darkred', linewidth=2)
        ax.add_patch(stigma)
        ax.text(6, 8.2, 'Stigma', fontsize=9)
        
        # Style
        ax.text(6, 7, 'Style', fontsize=9)
        
        # Ovary
        ovary = mpatches.Rectangle((4.3, 5.5), 1.4, 1, color='lightgreen', ec='green', linewidth=2)
        ax.add_patch(ovary)
        ax.text(6, 6, 'Ovary', fontsize=9)
        ax.plot(4.8, 6, 'ro', markersize=8)
        ax.text(4, 6, 'Ovule', fontsize=8)
        
        # Anther
        for x in [3, 7]:
            ax.plot([x, x], [7, 5], 'brown', linewidth=2)
            anther = mpatches.Rectangle((x-0.3, 7), 0.6, 0.5, color='yellow', ec='orange', linewidth=2)
            ax.add_patch(anther)
        ax.text(2, 7.3, 'Anther\n(pollen)', fontsize=8)
        ax.text(3, 4.5, 'Filament', fontsize=8)
        
        # Labels
        ax.text(5, 3.5, 'Female: Carpel (Stigma + Style + Ovary)', fontsize=9, ha='center',
               bbox=dict(boxstyle='round', facecolor='pink'))
        ax.text(5, 2.5, 'Male: Stamen (Anther + Filament)', fontsize=9, ha='center',
               bbox=dict(boxstyle='round', facecolor='lightyellow'))
        
        # Pollination process
        ax = axes[1, 0]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        ax.set_title('Pollination and Fertilization', fontsize=14, fontweight='bold')
        
        steps = [
            '1. Pollen lands on stigma (Pollination)',
            '2. Pollen tube grows through style',
            '3. Male nucleus travels down tube',
            '4. Fertilization in ovary',
            '5. Zygote → Embryo → Seed',
            '6. Ovary → Fruit',
            '',
            'Agents of Pollination:',
            '• Wind (grasses, maize)',
            '• Insects (flowers with nectar)',
            '• Birds (bright colored flowers)',
            '• Water (aquatic plants)'
        ]
        
        y = 9.5
        for step in steps:
            if step.startswith('Agents'):
                ax.text(5, y, step, fontsize=10, ha='center', fontweight='bold')
                y -= 0.8
            elif step.startswith('•'):
                ax.text(5, y, step, fontsize=9, ha='center',
                       bbox=dict(boxstyle='round', facecolor='lightblue'))
                y -= 0.8
            elif step:
                ax.text(5, y, step, fontsize=10, ha='center')
                y -= 0.8
            else:
                y -= 0.5
        
        # Comparison table
        ax = axes[1, 1]
        ax.axis('off')
        ax.set_title('Asexual vs Sexual Reproduction', fontsize=14, fontweight='bold')
        
        data = [
            ['Feature', 'Asexual', 'Sexual'],
            ['Parents', 'One', 'Two'],
            ['Gametes', 'No', 'Yes'],
            ['Offspring', 'Identical', 'Variable'],
            ['Speed', 'Fast', 'Slower'],
            ['Adaptation', 'Poor', 'Better'],
            ['Example', 'Yam tuber', 'Coconut seed']
        ]
        
        y_start = 9
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                color = 'lightyellow' if i == 0 else 'white'
                weight = 'bold' if i == 0 else 'normal'
                ax.text(j*3 + 0.5, y_start - i*1.2, cell, fontsize=10,
                       bbox=dict(boxstyle='round', facecolor=color),
                       fontweight=weight, ha='center')
        
        plt.tight_layout()
        diagram_path = os.path.join(self.diagrams_dir, f"{topic_id}_reproduction.png")
        plt.savefig(diagram_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "id": topic_id,
            "title": "Reproduction in Living Organisms",
            "subject": "Biology",
            "topic": "Reproduction",
            "subtopic": "Asexual and Sexual Reproduction",
            "content_type": "study_guide",
            "difficulty": "intermediate",
            "exam_board": "WAEC",
            "content": """# Reproduction: Continuity of Life

## 1. Types of Reproduction

### Asexual Reproduction
- **One parent** only
- **No gametes** (sex cells)
- Offspring **genetically identical** to parent (clones)
- **Faster** than sexual reproduction

### Sexual Reproduction
- **Two parents** (male and female)
- Involves **gametes** (sperm and egg)
- Offspring **genetically different** from parents
- Provides **variation** for adaptation

## 2. Asexual Reproduction Methods

### Binary Fission
- Single organism splits into two
- Example: Bacteria, Amoeba
- Very rapid multiplication

### Budding
- Small outgrowth (bud) forms on parent
- Bud detaches and grows independently
- Example: Yeast, Hydra

### Vegetative Propagation
- New plants from vegetative parts
- Examples:
  * Stem: Cassava, Sugarcane
  * Root: Sweet potato
  * Tuber: Yam, Potato
  * Bulb: Onion, Garlic
  * Rhizome: Ginger

### Spore Formation
- Produces many spores
- Spores dispersed by wind
- Example: Fungi, Ferns

## 3. Sexual Reproduction in Flowering Plants

### Parts of a Flower

**Male Parts (Stamen)**:
- Anther: Produces pollen grains
- Filament: Supports anther

**Female Parts (Carpel/Pistil)**:
- Stigma: Receives pollen
- Style: Tube connecting stigma to ovary
- Ovary: Contains ovules (eggs)

### Pollination
**Definition**: Transfer of pollen from anther to stigma

**Types**:
1. **Self-Pollination**: Same flower or same plant
2. **Cross-Pollination**: Different plants (same species)

**Agents of Pollination**:
- **Wind**: Light, dry pollen; abundant; feathery stigma (e.g., maize, grasses)
- **Insects**: Bright colors, nectar, scent, sticky pollen (e.g., hibiscus, sunflower)
- **Birds**: Bright red/orange, lots of nectar (e.g., bird of paradise)
- **Water**: Aquatic plants

### Fertilization
1. Pollen lands on stigma
2. Pollen tube grows down style
3. Male nucleus travels through tube
4. Reaches ovary, fuses with egg
5. Forms zygote → embryo → seed
6. Ovary becomes fruit

## 4. Sexual Reproduction in Humans

### Male Reproductive System
- Testes: Produce sperm and testosterone
- Sperm duct: Transports sperm
- Penis: Delivers sperm

### Female Reproductive System
- Ovaries: Produce eggs (ova) and hormones
- Fallopian tubes: Site of fertilization
- Uterus: Where baby develops
- Vagina: Birth canal

### Fertilization
- Sperm meets egg in fallopian tube
- Fusion forms zygote
- Zygote implants in uterus
- Develops into embryo → fetus → baby
- **Gestation period**: 9 months (280 days)

## 5. Nigerian Agricultural Context

### Asexual Reproduction in Farming
- **Cassava**: Stem cuttings planted
- **Yam**: Seed yam (tuber piece) planted
- **Plantain**: Suckers transplanted
- **Advantages**: Faster, maintains good traits

### Sexual Reproduction in Farming
- **Maize**: Pollinated by wind, grows from seed
- **Tomatoes**: Insect-pollinated, grows from seed
- **Advantages**: Produces variation, disease resistance

## 6. WAEC Exam Tips

✅ **Label flower diagrams** clearly (stigma, anther, ovary, etc.)
✅ **Distinguish** self vs cross-pollination
✅ **State agents** of pollination with examples
✅ **Compare** asexual vs sexual reproduction
✅ **Use Nigerian examples** (cassava, yam, maize)
✅ **Know fertilization process** step-by-step

## 7. Common WAEC Questions

1. Explain the term pollination
2. State 3 differences between asexual and sexual reproduction
3. Draw and label parts of a flower
4. Describe fertilization in flowering plants
5. Name 2 crops propagated vegetatively

## Practice Questions

1. What is the male gamete in plants?
2. Where does fertilization occur in humans?
3. Give 2 advantages of sexual reproduction
4. Name the process by which yam is propagated
5. State 3 agents of cross-pollination

## Summary

- Two main types: Asexual (one parent) and Sexual (two parents)
- Asexual: Binary fission, budding, vegetative propagation, spores
- Sexual (plants): Pollination → Fertilization → Seed formation
- Nigerian crops: Cassava (asexual), Maize (sexual)
- Sexual reproduction provides variation for adaptation
""",
            "diagrams": [diagram_path],
            "worked_examples": [
                {
                    "problem": "Explain how cassava is propagated in Nigerian farms.",
                    "solution": "Cassava is propagated vegetatively using stem cuttings. Mature stems are cut into pieces (15-20cm), planted in soil. Each cutting grows roots and shoots, forming new cassava plant identical to parent.",
                    "answer": "Vegetative propagation via stem cuttings"
                }
            ],
            "practice_problems": [
                {
                    "question": "What type of reproduction occurs in yam cultivation?",
                    "difficulty": "basic",
                    "answer": "Asexual (vegetative propagation using seed yam)",
                    "hint": "Farmers plant pieces of yam tuber"
                }
            ],
            "nigerian_context": "Cassava, yam, plantain propagation; maize pollination",
            "estimated_read_time": 28,
            "prerequisites": ["Cell structure", "Plant structure"],
            "learning_objectives": [
                "Distinguish asexual and sexual reproduction",
                "Describe pollination and fertilization in plants",
                "Relate reproduction to Nigerian agriculture"
            ],
            "created_at": datetime.now().isoformat(),
            "status": "published"
        }
    
    def generate_all_additional_content(self) -> list:
        """Generate 3 additional lessons"""
        print("=" * 70)
        print("PILOT CONTENT EXPANDER - Adding 3 More Lessons")
        print("=" * 70)
        print()
        
        additional_content = []
        
        print("📝 Generating additional enhanced lessons...")
        print()
        
        print("  1/3 Chemistry: Chemical Bonding...")
        content1 = self.generate_chemical_bonding_lesson()
        additional_content.append(content1)
        print("      ✓ Generated with bonding diagrams")
        
        print("  2/3 Biology: Cell Structure...")
        content2 = self.generate_cell_structure_lesson()
        additional_content.append(content2)
        print("      ✓ Generated with plant and animal cell diagrams")
        
        print("  3/3 Biology: Reproduction...")
        content3 = self.generate_reproduction_lesson()
        additional_content.append(content3)
        print("      ✓ Generated with reproduction process diagrams")
        
        print()
        print(f"✅ Generated {len(additional_content)} additional lessons")
        print(f"📊 Total new diagrams: {sum(len(c.get('diagrams', [])) for c in additional_content)}")
        
        # Merge with existing content
        self.merge_with_existing(additional_content)
        
        return additional_content
    
    def merge_with_existing(self, new_content: list):
        """Merge new content with existing pilot_content.json"""
        pilot_file = os.path.join(self.output_dir, "pilot_content.json")
        
        # Load existing
        with open(pilot_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        
        # Add new content
        existing_data["content"].extend(new_content)
        existing_data["metadata"]["total_items"] = len(existing_data["content"])
        existing_data["metadata"]["last_updated"] = datetime.now().isoformat()
        
        # Save merged
        with open(pilot_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        print()
        print(f"💾 Merged content saved to: {pilot_file}")
        print(f"📊 Total pilot lessons: {existing_data['metadata']['total_items']}")
        print()
        print("🎯 Pilot Content Summary:")
        for item in existing_data["content"]:
            print(f"  • {item['subject']}: {item['topic']}")
        
        print()
        print("Next steps:")
        print("1. Review all 5 lessons in generated_content/")
        print("2. Check all diagrams in generated_content/diagrams/")
        print("3. Import into Wave 3 platform using wave3_content_importer.py")
        print("4. Test with students via enhanced dashboards")


def main():
    """Main execution"""
    expander = PilotContentExpander()
    expander.generate_all_additional_content()
    
    print()
    print("🎉 Complete pilot content package ready!")
    print("📚 Total: 5 high-quality lessons with diagrams")


if __name__ == "__main__":
    main()
