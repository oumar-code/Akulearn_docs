#!/usr/bin/env python3
"""
Comprehensive NERDC Curriculum Content Generator
Generates educational content for all subjects based on Nigerian NERDC curriculum
Includes learning options and comprehensive study materials
"""

import json
import os
from datetime import datetime

def generate_comprehensive_nerdc_content():
    """Generate NERDC-aligned content for multiple subjects and levels"""

    content_items = [
        # PHYSICS SS1 - Mechanics
        {
            "id": f"nerdc_physics_mechanics_ss1_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": "Newton's Laws of Motion (SS1)",
            "subject": "Physics",
            "topic": "Mechanics",
            "level": "SS1",
            "content_type": "study_guide",
            "difficulty": "basic",
            "exam_board": "WAEC",
            "curriculum_framework": "NERDC Senior Secondary School",
            "content": """# Newton's Laws of Motion (SS1)

**Curriculum Framework:** NERDC Senior Secondary School
**Subject:** Physics
**Level:** SS1
**Topic:** Mechanics

## Learning Objectives
By completing this lesson, you will be able to:
- State and explain Newton's three laws of motion
- Apply Newton's laws to solve problems
- Distinguish between different types of forces
- Calculate force, mass, and acceleration

## Introduction
Mechanics is the branch of physics that deals with the motion of objects and the forces that cause motion. Newton's laws form the foundation of classical mechanics and are essential for understanding how objects move and interact.

## Core Concepts and Definitions
- **Force:** A push or pull that can change an object's motion
- **Mass:** The amount of matter in an object (measured in kg)
- **Acceleration:** The rate of change of velocity (measured in m/s²)
- **Inertia:** The tendency of an object to resist changes in its motion

## Newton's Three Laws of Motion

### First Law (Law of Inertia)
**An object at rest stays at rest, and an object in motion stays in motion with the same speed and direction unless acted upon by an unbalanced force.**

**Examples:**
- A book on a table remains at rest until pushed
- A moving car will keep moving at constant speed unless brakes are applied
- Passengers lurch forward when a bus stops suddenly

### Second Law (F = ma)
**The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.**

**Formula:** F = ma
- F = force (Newtons, N)
- m = mass (kilograms, kg)
- a = acceleration (m/s²)

### Third Law (Action-Reaction)
**For every action, there is an equal and opposite reaction.**

**Examples:**
- Rocket propulsion: exhaust gases push down, rocket goes up
- Walking: feet push backward on ground, ground pushes forward on feet
- Book on table: gravity pulls book down, table pushes book up

## Worked Examples

### Example 1: Newton's Second Law
**Problem:** A 5 kg object accelerates at 2 m/s². Calculate the force acting on it.

**Solution:**
F = ma
F = 5 kg × 2 m/s²
F = 10 N

### Example 2: Force Calculations
**Problem:** What force is needed to accelerate a 10 kg mass at 3 m/s²?

**Solution:**
F = ma
F = 10 × 3
F = 30 N

### Example 3: Mass Calculation
**Problem:** A force of 50 N accelerates an object at 5 m/s². Find the mass.

**Solution:**
F = ma
50 = m × 5
m = 50 ÷ 5
m = 10 kg

## Common Misconceptions to Avoid

1. **Misconception:** Force and motion are the same thing
   **Reality:** Force causes motion; motion is the result of force

2. **Misconception:** Heavier objects fall faster than lighter ones
   **Reality:** In the absence of air resistance, all objects fall at the same rate

3. **Misconception:** Action and reaction forces cancel each other out
   **Reality:** They act on different objects and don't cancel each other

## Practice Problems

### Basic Level
1. State Newton's first law of motion
2. What is the SI unit of force?
3. Define inertia with an example
4. What is the relationship between force, mass, and acceleration?
5. Give two examples of action-reaction pairs

### Intermediate Level
6. Calculate the force needed to accelerate a 3 kg mass at 4 m/s²
7. A force of 20 N acts on a 4 kg mass. Find the acceleration
8. What mass would accelerate at 2 m/s² under a force of 15 N?
9. Explain why passengers in a car lurch forward when it stops
10. Describe the forces acting on a book resting on a table

### Advanced Level
11. A 2 kg object experiences two forces: 10 N east and 6 N west. Find the net force and acceleration
12. Calculate the acceleration of a 5 kg object with forces of 25 N north and 10 N south acting on it
13. A car of mass 1000 kg accelerates from rest to 20 m/s in 10 seconds. What force is acting on it?
14. Explain the motion of a rocket using Newton's laws
15. A person pushes a 50 kg box with a force of 200 N but it doesn't move. Why?

## Important Formulas and Rules
- **Force:** F = ma
- **Weight:** W = mg (g = 9.8 m/s²)
- **Net Force:** F_net = ΣF (vector sum of all forces)
- **Acceleration:** a = (v - u)/t (for constant acceleration)

## Connections to Real-Life Situations

### Transportation
- Car acceleration and braking
- Rocket launches and space travel
- Aircraft takeoff and landing
- Bicycle and motorcycle dynamics

### Sports
- Ball trajectories in football, basketball
- Forces in running, jumping, throwing
- Equipment design (lighter materials for speed)

### Engineering
- Bridge and building design
- Vehicle safety features (seat belts, airbags)
- Elevator and escalator mechanics
- Robotic movement and automation

### Daily Life
- Walking and running mechanics
- Lifting and carrying objects
- Friction in daily activities
- Collision safety in vehicles

## Exam Preparation Guide

### WAEC Exam Focus
- Newton's laws (40-50% of mechanics questions)
- Force calculations (30-40% of questions)
- Real-life applications (20-30% of questions)
- Conceptual understanding (required for all questions)

### Study Strategy
1. Memorize the three laws and their applications
2. Practice force calculations regularly
3. Understand vector nature of forces
4. Learn common examples and applications
5. Review past WAEC questions

### Time Management Tips
- Spend 2-3 minutes per calculation question
- Read theory questions carefully
- Show all working steps clearly
- Check units in calculations
- Review answers for reasonableness

### Answering Exam Questions
- State laws clearly and completely
- Show all calculation steps
- Include units in final answers
- Explain concepts with examples
- Use diagrams where helpful

## 🎓 Learning Tips - Choose Your Preferred Learning Style

### Visual Learning
**Best for:** Learners who prefer diagrams and visual representations
- Draw force diagrams for different situations
- Create mind maps connecting the three laws
- Use color-coding for different types of forces
- Watch animations of Newton's laws in action
- Create flowcharts for problem-solving steps

### Kinesthetic Learning
**Best for:** Learners who learn by doing hands-on activities
- Perform experiments with toy cars and ramps
- Build simple models demonstrating inertia
- Use spring scales to measure forces
- Conduct collision experiments with marbles
- Practice pushing objects of different masses

### Auditory Learning
**Best for:** Learners who understand better through listening and discussion
- Listen to detailed explanations of each law
- Join physics discussion groups
- Record yourself explaining the laws
- Participate in class demonstrations
- Discuss real-life applications with peers

### Reading/Writing Learning
**Best for:** Learners who prefer text-based information
- Create detailed notes on each law
- Write summaries of force calculations
- Create flashcards for formulas and laws
- Write step-by-step solutions to problems
- Maintain a physics journal with observations

## Summary of Key Points
- Newton's first law explains inertia and balanced forces
- Newton's second law relates force, mass, and acceleration (F = ma)
- Newton's third law states action-reaction pairs are equal and opposite
- Forces are vectors with magnitude and direction
- Mass and weight are different concepts
- Practice calculations regularly to build confidence

## Additional Resources
- Textbook: Senior Secondary Physics
- Online: PhET Interactive Simulations
- Videos: Crash Course Physics - Newton's Laws
- Apps: Physics calculator apps
- Experiments: Simple pendulum, Atwood's machine

## Frequently Asked Questions

**Q: Why do we need three laws?**
A: Each law explains different aspects of motion and forces - inertia, acceleration, and interactions.

**Q: What's the difference between mass and weight?**
A: Mass is the amount of matter (constant), weight is the force due to gravity (varies with location).

**Q: Do Newton's laws apply in space?**
A: Yes, but in the absence of gravity and air resistance, motion continues unchanged (first law).

**Q: How do seat belts work?**
A: They provide the unbalanced force needed to slow you down gradually during a collision.

**Q: What's the best way to learn Newton's laws?**
A: Combine understanding the concepts with practicing calculations and observing real-life examples.""",
            "estimated_read_time": 50,
            "prerequisites": ["basic_physics_concepts"],
            "learning_options": ["visual", "kinesthetic", "auditory", "reading_writing"],
            "related_questions": ["waec_physics_ss1_mechanics_2020_q1", "waec_physics_ss1_mechanics_2021_q2"],
            "tags": ["physics", "mechanics", "newton", "laws", "motion", "ss1", "nerdc", "learning_tips"],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "author": "Physics Curriculum Expert",
            "version": 1
        },

        # CHEMISTRY SS1 - Atomic Structure
        {
            "id": f"nerdc_chemistry_atoms_ss1_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": "Atomic Structure and Bonding (SS1)",
            "subject": "Chemistry",
            "topic": "Atomic Structure",
            "level": "SS1",
            "content_type": "study_guide",
            "difficulty": "basic",
            "exam_board": "WAEC",
            "curriculum_framework": "NERDC Senior Secondary School",
            "content": """# Atomic Structure and Bonding (SS1)

**Curriculum Framework:** NERDC Senior Secondary School
**Subject:** Chemistry
**Level:** SS1
**Topic:** Atomic Structure

## Learning Objectives
By completing this lesson, you will be able to:
- Describe the structure of atoms
- Understand electron configuration
- Explain different types of chemical bonding
- Predict bonding types from periodic table position

## Introduction
Atoms are the basic building blocks of matter. Understanding atomic structure and how atoms bond together is fundamental to understanding chemistry. This knowledge explains why substances behave the way they do and how chemical reactions occur.

## Core Concepts and Definitions
- **Atom:** The smallest particle of an element that retains its chemical properties
- **Proton:** Positively charged particle in the nucleus (+1 charge)
- **Neutron:** Neutral particle in the nucleus (0 charge)
- **Electron:** Negatively charged particle orbiting the nucleus (-1 charge)
- **Atomic Number:** Number of protons in an atom
- **Mass Number:** Total number of protons and neutrons

## Atomic Structure Models

### Dalton's Model (1803)
- Atoms are solid, indivisible spheres
- All atoms of same element are identical
- Compounds form when atoms combine in fixed ratios

### Thomson's Model (1897)
- Atoms contain negatively charged electrons
- "Plum pudding" model - electrons embedded in positive sphere
- Discovered electrons through cathode ray experiments

### Rutherford's Model (1911)
- Nuclear model - dense positive nucleus
- Electrons orbit nucleus like planets around sun
- Most of atom is empty space
- Discovered nucleus through gold foil experiment

### Bohr's Model (1913)
- Electrons orbit nucleus in fixed energy levels
- Energy levels are quantized
- Electrons can jump between levels by absorbing/emitting energy

### Modern Quantum Model
- Electron cloud model
- Electrons exist in orbitals, not fixed orbits
- Heisenberg uncertainty principle
- Schrödinger wave equation

## Electron Configuration

### Energy Levels and Sublevels
- **K shell (n=1):** 2 electrons maximum
- **L shell (n=2):** 8 electrons maximum
- **M shell (n=3):** 18 electrons maximum
- **N shell (n=4):** 32 electrons maximum

### Orbital Shapes
- **s orbitals:** Spherical shape, 2 electrons
- **p orbitals:** Dumbbell shape, 6 electrons
- **d orbitals:** Complex shapes, 10 electrons
- **f orbitals:** Very complex shapes, 14 electrons

## Chemical Bonding

### Ionic Bonding
**Definition:** Transfer of electrons from metal to non-metal
**Characteristics:**
- Electrostatic attraction between oppositely charged ions
- High melting/boiling points
- Conduct electricity when molten or dissolved
- Brittle crystalline solids

**Examples:**
- NaCl (sodium chloride): Na⁺ + Cl⁻
- MgO (magnesium oxide): Mg²⁺ + O²⁻
- CaF₂ (calcium fluoride): Ca²⁺ + 2F⁻

### Covalent Bonding
**Definition:** Sharing of electrons between non-metal atoms
**Characteristics:**
- Strong bonds between atoms
- Low melting/boiling points (generally)
- Don't conduct electricity
- Can be solids, liquids, or gases

**Examples:**
- H₂ (hydrogen): H—H
- O₂ (oxygen): O=O
- CH₄ (methane): Carbon shares with 4 hydrogens

### Metallic Bonding
**Definition:** Attraction between positive metal ions and delocalized electrons
**Characteristics:**
- High melting/boiling points
- Good conductors of heat and electricity
- Malleable and ductile
- Shiny appearance

**Examples:**
- Copper, iron, aluminum
- Alloys (mixtures of metals)

## Worked Examples

### Example 1: Atomic Structure
**Problem:** Describe the structure of a carbon atom (atomic number 6, mass number 12)

**Solution:**
- Protons: 6 (same as atomic number)
- Electrons: 6 (same as protons in neutral atom)
- Neutrons: 12 - 6 = 6
- Electron configuration: 2,4 (K shell: 2, L shell: 4)

### Example 2: Electron Configuration
**Problem:** Write the electron configuration for sodium (atomic number 11)

**Solution:**
- K shell: 2 electrons
- L shell: 8 electrons
- M shell: 1 electron
- Configuration: 2,8,1

### Example 3: Bonding Type Prediction
**Problem:** Predict the type of bond formed between magnesium and chlorine

**Solution:**
- Magnesium is a metal (Group 2)
- Chlorine is a non-metal (Group 7)
- Metal + non-metal = ionic bonding
- Mg loses 2 electrons → Mg²⁺
- Cl gains 1 electron → Cl⁻
- Formula: MgCl₂

## Common Misconceptions to Avoid

1. **Misconception:** Atoms are indivisible
   **Reality:** Atoms consist of subatomic particles (protons, neutrons, electrons)

2. **Misconception:** Electrons orbit nucleus like planets
   **Reality:** Modern model describes electron clouds and probability regions

3. **Misconception:** All atoms of same element are identical
   **Reality:** Isotopes have different numbers of neutrons

4. **Misconception:** Ionic compounds conduct electricity in solid state
   **Reality:** Only when molten or dissolved (ions must be free to move)

## Practice Problems

### Basic Level
1. What are the three main subatomic particles?
2. Define atomic number and mass number
3. What is the charge of a proton, neutron, and electron?
4. Name the scientist who discovered the nucleus
5. What is the maximum number of electrons in the first energy level?

### Intermediate Level
6. Describe the structure of an atom of oxygen-16
7. Write electron configurations for Li, Be, B, C, N
8. Explain why atoms form bonds
9. Compare ionic and covalent bonding
10. Predict bonding between potassium and oxygen

### Advanced Level
11. Explain Rutherford's gold foil experiment and its conclusions
12. Describe the difference between Bohr's model and quantum model
13. Calculate the number of neutrons in calcium-40
14. Explain why metals are good conductors using bonding theory
15. Predict the formula of aluminum sulfide

## Important Formulas and Rules
- **Atomic Number (Z) = Number of protons**
- **Mass Number (A) = Protons + Neutrons**
- **Number of Neutrons = A - Z**
- **Number of Electrons = Z (for neutral atoms)**
- **Electron Configuration:** Follows 2n² rule for each energy level

## Connections to Real-Life Situations

### Technology and Materials
- Semiconductor materials (silicon chips)
- Alloys for construction and transportation
- Batteries and electrochemical cells
- Catalysts in industrial processes

### Medicine and Health
- Medical imaging (X-rays, MRI)
- Radiation therapy for cancer treatment
- Drug design and pharmaceutical bonding
- Understanding nutrient absorption

### Environment
- Water purification and treatment
- Air pollution control
- Recycling and material recovery
- Climate change and greenhouse gases

### Industry
- Petroleum refining and petrochemicals
- Fertilizer production
- Plastic manufacturing
- Metal extraction and processing

## Exam Preparation Guide

### WAEC Exam Focus
- Atomic structure (30-40% of questions)
- Electron configuration (20-30% of questions)
- Chemical bonding (30-40% of questions)
- Periodic table relationships (10-20% of questions)

### Study Strategy
1. Learn the structure of atoms thoroughly
2. Practice electron configurations regularly
3. Understand the three types of bonding
4. Learn to predict bonding from periodic table
5. Review past questions and common exam patterns

### Time Management Tips
- Spend 2-3 minutes per theory question
- Practice electron configuration quickly
- Read bonding questions carefully
- Show working for calculations
- Review answers for completeness

### Answering Exam Questions
- Draw diagrams where helpful (atomic structure, bonding)
- Use correct chemical notation and symbols
- Explain concepts clearly with examples
- Show electron transfer/dot-cross diagrams for bonding
- State assumptions in calculations

## 🎓 Learning Tips - Choose Your Preferred Learning Style

### Visual Learning
**Best for:** Learners who prefer diagrams and visual representations
- Draw atomic structure diagrams with colored particles
- Create bonding diagrams showing electron transfer/sharing
- Use periodic table charts for electron configuration
- Watch animations of atomic models and bonding
- Create mind maps connecting atomic concepts

### Kinesthetic Learning
**Best for:** Learners who learn by doing hands-on activities
- Build atomic models with balls and sticks
- Use molecular model kits for bonding demonstrations
- Conduct simple experiments (electrolysis, reactions)
- Create physical representations of electron shells
- Perform bonding simulations with objects

### Auditory Learning
**Best for:** Learners who understand better through listening and discussion
- Listen to detailed explanations of atomic theory
- Join chemistry discussion groups
- Record yourself explaining bonding types
- Participate in class demonstrations and experiments
- Discuss periodic table trends with peers

### Reading/Writing Learning
**Best for:** Learners who prefer text-based information
- Create detailed notes on atomic structure
- Write summaries of different bonding types
- Create flashcards for electron configurations
- Write step-by-step bonding explanations
- Maintain a chemistry journal with observations

## Summary of Key Points
- Atoms consist of protons, neutrons, and electrons
- Atomic number determines element identity
- Electrons occupy energy levels with specific capacities
- Ionic bonding involves electron transfer
- Covalent bonding involves electron sharing
- Metallic bonding involves delocalized electrons
- Bonding type can be predicted from periodic table position

## Additional Resources
- Textbook: Senior Secondary Chemistry
- Online: Periodic Table interactive websites
- Videos: Crash Course Chemistry - Atomic Structure
- Apps: Chemistry calculator and periodic table apps
- Experiments: Flame tests, conductivity tests

## Frequently Asked Questions

**Q: Why do atoms form bonds?**
A: To achieve stable electron configurations (usually 8 electrons in outer shell).

**Q: What's the difference between ionic and covalent bonds?**
A: Ionic bonds involve electron transfer between metal and non-metal; covalent bonds involve electron sharing between non-metals.

**Q: Why are metals good conductors?**
A: Delocalized electrons in metallic bonding can move freely, carrying electric charge.

**Q: How do I remember electron configurations?**
A: Use the pattern 2,8,8,18... or practice regularly with the first 20 elements.

**Q: What's the best way to learn atomic structure?**
A: Combine visual models with practice writing electron configurations and understanding bonding patterns.""",
            "estimated_read_time": 55,
            "prerequisites": ["basic_chemistry"],
            "learning_options": ["visual", "kinesthetic", "auditory", "reading_writing"],
            "related_questions": ["waec_chemistry_ss1_atoms_2020_q1", "waec_chemistry_ss1_bonding_2021_q3"],
            "tags": ["chemistry", "atomic_structure", "bonding", "ss1", "nerdc", "learning_tips"],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "author": "Chemistry Curriculum Expert",
            "version": 1
        },

        # BIOLOGY SS1 - Cell Biology
        {
            "id": f"nerdc_biology_cells_ss1_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": "Cell Structure and Function (SS1)",
            "subject": "Biology",
            "topic": "Cell Biology",
            "level": "SS1",
            "content_type": "study_guide",
            "difficulty": "basic",
            "exam_board": "WAEC",
            "curriculum_framework": "NERDC Senior Secondary School",
            "content": """# Cell Structure and Function (SS1)

**Curriculum Framework:** NERDC Senior Secondary School
**Subject:** Biology
**Level:** SS1
**Topic:** Cell Biology

## Learning Objectives
By completing this lesson, you will be able to:
- Describe the structure of plant and animal cells
- Explain the functions of cell organelles
- Compare prokaryotic and eukaryotic cells
- Understand cell specialization and differentiation

## Introduction
Cells are the basic structural and functional units of all living organisms. The cell theory states that all living things are made of cells, cells are the basic unit of life, and all cells come from pre-existing cells. Understanding cell structure and function is fundamental to biology.

## Core Concepts and Definitions
- **Cell:** The basic structural and functional unit of life
- **Organelle:** Specialized structures within cells that perform specific functions
- **Prokaryotic Cell:** Cells without a nucleus (bacteria)
- **Eukaryotic Cell:** Cells with a nucleus and membrane-bound organelles
- **Cell Membrane:** Selectively permeable barrier controlling substance movement
- **Cytoplasm:** Jelly-like substance where organelles are suspended

## Cell Theory
**Three main principles:**
1. **All living organisms are composed of cells**
2. **Cells are the basic unit of structure and function in living organisms**
3. **All cells come from pre-existing cells**

**Scientists involved:**
- **Robert Hooke (1665):** Discovered cells in cork tissue
- **Antonie van Leeuwenhoek (1670s):** First to observe living cells
- **Matthias Schleiden (1838):** All plants are made of cells
- **Theodor Schwann (1839):** All animals are made of cells
- **Rudolf Virchow (1855):** All cells come from pre-existing cells

## Prokaryotic vs Eukaryotic Cells

### Prokaryotic Cells
**Characteristics:**
- No nucleus
- No membrane-bound organelles
- Smaller size (1-10 μm)
- Genetic material in nucleoid region
- Examples: Bacteria, archaea

**Structures:**
- Cell wall (peptidoglycan)
- Cell membrane
- Cytoplasm
- Ribosomes
- Plasmids (optional)
- Flagella/pili (some)

### Eukaryotic Cells
**Characteristics:**
- True nucleus with nuclear membrane
- Membrane-bound organelles
- Larger size (10-100 μm)
- Complex internal structure
- Examples: Plants, animals, fungi, protists

## Plant Cell Structures

### Cell Wall
- **Function:** Provides structural support and protection
- **Composition:** Cellulose, hemicellulose, pectin
- **Location:** Outside cell membrane
- **Permeability:** Freely permeable to water and solutes

### Cell Membrane
- **Function:** Controls movement of substances in/out of cell
- **Structure:** Phospholipid bilayer with embedded proteins
- **Selective Permeability:** Allows some substances, blocks others

### Nucleus
- **Function:** Controls cell activities, contains genetic material
- **Structures:** Nuclear membrane, nucleolus, chromatin
- **Contains:** DNA (genetic information)

### Mitochondria
- **Function:** Site of cellular respiration, produces ATP (energy)
- **Structure:** Double membrane, cristae, matrix
- **Importance:** "Powerhouse of the cell"

### Endoplasmic Reticulum (ER)
- **Rough ER:** Studded with ribosomes, protein synthesis
- **Smooth ER:** No ribosomes, lipid synthesis, detoxification

### Golgi Apparatus
- **Function:** Modifies, sorts, packages proteins and lipids
- **Structure:** Stack of membrane-bound sacs
- **Produces:** Lysosomes, secretory vesicles

### Lysosomes
- **Function:** Contain digestive enzymes, break down waste
- **Structure:** Membrane-bound organelles
- **Importance:** Cellular cleanup and recycling

### Vacuoles
- **Function:** Storage, waste management, maintains turgor pressure
- **Structure:** Large membrane-bound storage sacs
- **Plant cells:** Large central vacuole (up to 90% of cell volume)

### Chloroplasts
- **Function:** Site of photosynthesis, converts light energy to chemical energy
- **Structure:** Double membrane, thylakoids, stroma
- **Contains:** Chlorophyll (green pigment)

### Ribosomes
- **Function:** Site of protein synthesis
- **Structure:** Composed of rRNA and proteins
- **Location:** Free in cytoplasm or bound to rough ER

## Animal Cell Structures
Similar to plant cells but lack:
- Cell wall
- Large central vacuole
- Chloroplasts

**Additional structures in animal cells:**
- Centrioles (involved in cell division)
- Cilia/flagella (movement)
- More lysosomes

## Cell Specialization
Cells differentiate to perform specific functions:

### Muscle Cells
- **Function:** Contraction and movement
- **Specializations:** Contractile proteins (actin, myosin), elongated shape

### Nerve Cells (Neurons)
- **Function:** Transmit electrical impulses
- **Specializations:** Long axons, dendrites, myelin sheath

### Red Blood Cells
- **Function:** Transport oxygen
- **Specializations:** Biconcave shape, no nucleus, hemoglobin

### Root Hair Cells
- **Function:** Absorption of water and minerals
- **Specializations:** Large surface area, thin walls

### Sperm Cells
- **Function:** Fertilization
- **Specializations:** Flagellum for movement, acrosome for penetration

## Worked Examples

### Example 1: Cell Comparison
**Problem:** Compare plant and animal cells

**Solution:**
| Feature | Plant Cell | Animal Cell |
|---------|------------|-------------|
| Cell Wall | Present (cellulose) | Absent |
| Chloroplasts | Present | Absent |
| Large Vacuole | Present | Absent/small |
| Centrioles | Absent | Present |
| Shape | Fixed/rectangular | Irregular |

### Example 2: Organelle Function
**Problem:** Explain the function of mitochondria in cellular respiration

**Solution:**
Mitochondria are the powerhouse of the cell. They convert chemical energy from food into ATP (adenosine triphosphate) through cellular respiration. The process involves:
1. Glycolysis (cytoplasm)
2. Krebs cycle (mitochondrial matrix)
3. Electron transport chain (inner mitochondrial membrane)
4. ATP production for cellular energy

### Example 3: Cell Specialization
**Problem:** Explain how root hair cells are adapted for their function

**Solution:**
Root hair cells are adapted for absorption:
- **Large surface area:** Increases absorption rate
- **Thin cell walls:** Reduces diffusion distance
- **Large vacuole:** Maintains turgor pressure
- **No chloroplasts:** Maximizes energy for absorption

## Common Misconceptions to Avoid

1. **Misconception:** All cells are the same
   **Reality:** Cells specialize for different functions

2. **Misconception:** Plant cells don't have mitochondria
   **Reality:** Plant cells have mitochondria for cellular respiration

3. **Misconception:** The cell membrane is solid
   **Reality:** It's a fluid mosaic of phospholipids and proteins

4. **Misconception:** Prokaryotic cells are primitive
   **Reality:** They're highly evolved and successful organisms

## Practice Problems

### Basic Level
1. What is the cell theory?
2. Name three differences between plant and animal cells
3. What is the function of the nucleus?
4. Define organelle
5. What is cytoplasm?

### Intermediate Level
6. Describe the structure and function of mitochondria
7. Explain how chloroplasts differ from mitochondria
8. Compare prokaryotic and eukaryotic cells
9. Describe cell specialization with examples
10. Explain the role of the cell membrane

### Advanced Level
11. Explain how the structure of a red blood cell relates to its function
12. Describe the process of protein synthesis involving organelles
13. Explain how the golgi apparatus and ER work together
14. Discuss the importance of lysosomes in cellular digestion
15. Explain how cell specialization contributes to organism function

## Important Concepts and Rules
- **Cell Theory:** All living things are made of cells
- **Surface Area to Volume Ratio:** Affects cell size and efficiency
- **Selective Permeability:** Cell membrane controls substance movement
- **Compartmentalization:** Organelles separate cellular processes
- **Cell Differentiation:** Cells become specialized for specific functions

## Connections to Real-Life Situations

### Health and Medicine
- Cancer: Uncontrolled cell division
- Stem cells: Undifferentiated cells for medical treatments
- Organ transplants: Tissue compatibility
- Genetic diseases: Cell function abnormalities

### Agriculture and Food
- Plant breeding: Improving crop cell structure
- Food preservation: Controlling microbial cell growth
- Fertilizers: Supporting plant cell function
- Genetic modification: Altering plant cell characteristics

### Biotechnology
- Cell culture: Growing cells in laboratory
- Vaccine production: Using cell cultures
- Bioremediation: Using microorganisms for cleanup
- Forensic science: DNA analysis from cells

### Environmental Science
- Pollution effects on cell function
- Climate change impact on plant cells
- Conservation of endangered species
- Ecosystem balance through cellular processes

## Exam Preparation Guide

### WAEC Exam Focus
- Cell structure and organelles (40-50% of questions)
- Cell theory and scientists (20-30% of questions)
- Prokaryotic vs eukaryotic cells (15-20% of questions)
- Cell specialization (10-15% of questions)

### Study Strategy
1. Learn organelles and their functions thoroughly
2. Practice drawing and labeling cell diagrams
3. Understand cell specialization examples
4. Review cell theory and historical development
5. Compare different cell types regularly

### Time Management Tips
- Spend 2-3 minutes per labeling question
- Read comparison questions carefully
- Practice drawing cells quickly and accurately
- Review answers for completeness
- Manage time for both theory and practical questions

### Answering Exam Questions
- Draw neat, labeled diagrams
- Use correct biological terminology
- Explain functions clearly with examples
- Compare structures systematically
- Show understanding of cell processes

## 🎓 Learning Tips - Choose Your Preferred Learning Style

### Visual Learning
**Best for:** Learners who prefer diagrams and visual representations
- Draw detailed cell diagrams with labels
- Create color-coded organelle charts
- Use mind maps for cell functions
- Watch animations of cell processes
- Create comparison tables for cell types

### Kinesthetic Learning
**Best for:** Learners who learn by doing hands-on activities
- Build 3D cell models with craft materials
- Use microscopes to observe real cells
- Conduct osmosis experiments with cells
- Create physical representations of organelles
- Perform cell staining and observation

### Auditory Learning
**Best for:** Learners who understand better through listening and discussion
- Listen to detailed explanations of cell structure
- Join biology study discussion groups
- Record yourself explaining organelle functions
- Participate in class demonstrations
- Discuss cell specialization with peers

### Reading/Writing Learning
**Best for:** Learners who prefer text-based information
- Create detailed notes on cell organelles
- Write summaries of cell processes
- Create flashcards for organelle functions
- Write step-by-step explanations of cell activities
- Maintain a biology journal with observations

## Summary of Key Points
- Cells are the basic units of life
- Plant and animal cells have different structures
- Organelles perform specific cellular functions
- Cells specialize for different organism functions
- Cell theory explains the fundamental nature of life
- Understanding cells is essential for all biological processes

## Additional Resources
- Textbook: Senior Secondary Biology
- Online: Cell structure interactive websites
- Videos: Amoeba Sisters cell biology
- Apps: Biology quiz and diagram apps
- Experiments: Onion cell observation, cheek cell staining

## Frequently Asked Questions

**Q: Why are cells so small?**
A: Surface area to volume ratio - cells need efficient exchange of materials with environment.

**Q: Do all cells have a nucleus?**
A: No, prokaryotic cells (bacteria) don't have a nucleus; eukaryotic cells do.

**Q: What's the difference between organelles and inclusions?**
A: Organelles are membrane-bound structures with specific functions; inclusions are stored materials.

**Q: How do cells know what to become?**
A: Through gene expression and environmental signals during differentiation.

**Q: What's the best way to learn cell biology?**
A: Combine visual learning (diagrams) with practical observation and regular review.""",
            "estimated_read_time": 60,
            "prerequisites": ["basic_biology"],
            "learning_options": ["visual", "kinesthetic", "auditory", "reading_writing"],
            "related_questions": ["waec_biology_ss1_cells_2020_q1", "waec_biology_ss1_organelles_2021_q2"],
            "tags": ["biology", "cell_biology", "organelles", "ss1", "nerdc", "learning_tips"],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "author": "Biology Curriculum Expert",
            "version": 1
        },

        # ENGLISH SS1 - Grammar
        {
            "id": f"nerdc_english_grammar_ss1_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": "Parts of Speech and Sentence Structure (SS1)",
            "subject": "English Language",
            "topic": "Grammar",
            "level": "SS1",
            "content_type": "study_guide",
            "difficulty": "basic",
            "exam_board": "WAEC",
            "curriculum_framework": "NERDC Senior Secondary School",
            "content": """# Parts of Speech and Sentence Structure (SS1)

**Curriculum Framework:** NERDC Senior Secondary School
**Subject:** English Language
**Level:** SS1
**Topic:** Grammar

## Learning Objectives
By completing this lesson, you will be able to:
- Identify and use the eight parts of speech correctly
- Construct grammatically correct sentences
- Understand subject-verb agreement
- Apply proper punctuation in writing

## Introduction
Grammar is the system of rules that governs how words are used in a language. Understanding parts of speech and sentence structure is fundamental to effective communication in English. This knowledge helps you write clearly, speak correctly, and understand complex texts.

## Core Concepts and Definitions
- **Parts of Speech:** Categories of words based on their grammatical function
- **Noun:** A naming word (person, place, thing, idea)
- **Pronoun:** A word that replaces a noun
- **Verb:** An action or state word
- **Adjective:** A word that describes a noun
- **Adverb:** A word that describes a verb, adjective, or adverb
- **Preposition:** A word that shows relationship
- **Conjunction:** A word that joins words or clauses
- **Interjection:** A word that expresses emotion

## The Eight Parts of Speech

### 1. Noun
**Definition:** A naming word for person, place, thing, or idea

**Types:**
- **Common nouns:** book, city, teacher, happiness
- **Proper nouns:** Lagos, Nigeria, Shakespeare, Monday
- **Abstract nouns:** love, freedom, beauty, courage
- **Collective nouns:** team, family, crowd, flock
- **Countable nouns:** book, pen, house (can be counted)
- **Uncountable nouns:** water, rice, music (cannot be counted)

**Examples:**
- The **boy** ran to the **school**.
- **Love** is a powerful **emotion**.

### 2. Pronoun
**Definition:** A word that replaces a noun to avoid repetition

**Types:**
- **Personal pronouns:** I, you, he, she, it, we, they
- **Possessive pronouns:** my, your, his, her, its, our, their
- **Reflexive pronouns:** myself, yourself, himself, herself, itself
- **Demonstrative pronouns:** this, that, these, those
- **Interrogative pronouns:** who, whom, whose, which, what
- **Relative pronouns:** who, whom, whose, which, that

**Examples:**
- **She** gave **her** book to **me**.
- The man **who** lives next door is a doctor.

### 3. Verb
**Definition:** A word that expresses action or state of being

**Types:**
- **Action verbs:** run, eat, sleep, write
- **Linking verbs:** be, seem, appear, become
- **Helping verbs:** is, are, was, were, has, have, will
- **Transitive verbs:** take an object (I ate an apple)
- **Intransitive verbs:** don't take an object (I sleep)

**Examples:**
- The dog **barks** loudly.
- **Be** kind to others.
- She **has finished** her homework.

### 4. Adjective
**Definition:** A word that describes or modifies a noun

**Types:**
- **Descriptive adjectives:** big, small, beautiful, intelligent
- **Quantitative adjectives:** some, many, few, several
- **Demonstrative adjectives:** this, that, these, those
- **Possessive adjectives:** my, your, his, her, its, our, their
- **Interrogative adjectives:** which, what, whose

**Examples:**
- The **big** dog ran quickly.
- **Whose** book is this?
- She has **many** friends.

### 5. Adverb
**Definition:** A word that describes or modifies a verb, adjective, or adverb

**Types:**
- **Adverbs of manner:** quickly, slowly, carefully, beautifully
- **Adverbs of time:** now, then, yesterday, tomorrow
- **Adverbs of place:** here, there, everywhere, nowhere
- **Adverbs of degree:** very, quite, almost, extremely
- **Adverbs of frequency:** always, often, sometimes, never

**Examples:**
- She sings **beautifully**.
- He arrived **yesterday**.
- The movie was **extremely** interesting.

### 6. Preposition
**Definition:** A word that shows relationship between nouns/pronouns and other words

**Common prepositions:**
- **Time:** at, on, in, during, before, after, since, for
- **Place:** in, on, at, under, over, beside, between, among
- **Direction:** to, from, towards, through, across, along
- **Other:** with, by, for, about, of, from, as

**Examples:**
- The book is **on** the table.
- She arrived **at** 5 o'clock.
- He lives **in** Lagos.

### 7. Conjunction
**Definition:** A word that joins words, phrases, or clauses

**Types:**
- **Coordinating conjunctions:** and, but, or, so, yet, for, nor
- **Subordinating conjunctions:** because, although, if, when, since, while, after
- **Correlative conjunctions:** either...or, neither...nor, both...and, not only...but also

**Examples:**
- I like tea **and** coffee.
- She stayed home **because** she was sick.
- **Either** you come **or** I will go.

### 8. Interjection
**Definition:** A word that expresses strong emotion or surprise

**Examples:**
- **Wow!** That's amazing!
- **Oh!** I forgot my keys.
- **Hey!** Look at that!
- **Alas!** The exam was difficult.

## Sentence Structure

### Basic Sentence Components
- **Subject:** Who/what the sentence is about
- **Predicate:** What the subject does or is
- **Object:** Who/what receives the action
- **Complement:** Completes the meaning of the subject/predicate

### Sentence Types

#### 1. Declarative Sentences
**Purpose:** Make statements
**Examples:**
- The sun is shining.
- I love reading books.

#### 2. Interrogative Sentences
**Purpose:** Ask questions
**Examples:**
- Are you coming?
- What is your name?

#### 3. Imperative Sentences
**Purpose:** Give commands or requests
**Examples:**
- Close the door.
- Please be quiet.

#### 4. Exclamatory Sentences
**Purpose:** Express strong emotion
**Examples:**
- What a beautiful day!
- I won the prize!

### Subject-Verb Agreement
**Rules:**
1. Singular subjects take singular verbs
2. Plural subjects take plural verbs
3. Compound subjects joined by "and" take plural verbs
4. Subjects joined by "or/nor" agree with the nearer subject

**Examples:**
- The boy **runs** fast. (singular)
- The boys **run** fast. (plural)
- Tom and Jerry **are** friends. (compound plural)
- Either the teacher or the students **are** coming. (plural nearer)

## Punctuation

### Basic Punctuation Marks
- **Period (.):** Ends declarative sentences
- **Question mark (?):** Ends interrogative sentences
- **Exclamation mark (!):** Ends exclamatory sentences
- **Comma (,):** Separates items in lists, clauses
- **Apostrophe ('):** Shows possession or contraction
- **Quotation marks (" "):** Enclose direct speech
- **Colon (:):** Introduces lists or explanations
- **Semicolon (;):** Joins related independent clauses

### Common Punctuation Rules
- Use commas in lists: I like apples, oranges, and bananas.
- Use apostrophe for possession: John's book
- Use quotation marks for direct speech: "Hello," he said.
- Use colon before lists: Bring these items: pen, paper, book.

## Worked Examples

### Example 1: Parts of Speech Identification
**Sentence:** The beautiful girl quickly ran to her big house.

**Analysis:**
- **The** (article)
- **beautiful** (adjective - describes girl)
- **girl** (noun - subject)
- **quickly** (adverb - describes ran)
- **ran** (verb - action)
- **to** (preposition - shows direction)
- **her** (possessive adjective - shows ownership)
- **big** (adjective - describes house)
- **house** (noun - object)

### Example 2: Subject-Verb Agreement
**Problem:** Correct the subject-verb agreement errors.

**Incorrect:** The students was studying.
**Correct:** The students **were** studying.

**Incorrect:** My brother and sister is coming.
**Correct:** My brother and sister **are** coming.

### Example 3: Sentence Construction
**Problem:** Construct different types of sentences using the word "run".

**Solutions:**
- Declarative: I run every morning.
- Interrogative: Do you run every morning?
- Imperative: Run to the store now!
- Exclamatory: How fast you run!

## Common Misconceptions to Avoid

1. **Misconception:** Adjectives and adverbs are the same
   **Reality:** Adjectives describe nouns; adverbs describe verbs/adjectives/adverbs

2. **Misconception:** All verbs need objects
   **Reality:** Intransitive verbs don't take objects

3. **Misconception:** Prepositions only show location
   **Reality:** They show various relationships (time, direction, possession)

4. **Misconception:** Conjunctions can join anything
   **Reality:** Different conjunctions join different grammatical units

## Practice Problems

### Basic Level
1. Identify the parts of speech in: "The quick brown fox jumps over the lazy dog."
2. Name the eight parts of speech.
3. What is a noun? Give 5 examples.
4. What is the difference between a common noun and a proper noun?
5. Define a pronoun and give examples.

### Intermediate Level
6. Correct subject-verb agreement in: "The committee have decided."
7. Identify adverbs in: "She sings very beautifully in the morning."
8. Use appropriate prepositions: "The book is ___ the table ___ the room."
9. Join sentences using conjunctions: "I studied. I passed the exam."
10. Punctuate: "what time does the train leave"

### Advanced Level
11. Analyze sentence structure: "Although it was raining, we went to the park."
12. Correct: "The boy which won the prize are happy."
13. Transform: Change "I am tired" to interrogative and imperative forms.
14. Explain the difference between transitive and intransitive verbs with examples.
15. Construct a complex sentence using at least 5 different parts of speech.

## Important Rules and Patterns
- **Noun → Pronoun:** Replace nouns with appropriate pronouns
- **Adjective Order:** Opinion, size, age, shape, color, origin, material, purpose
- **Verb Tenses:** Must be consistent within sentences
- **Parallel Structure:** Similar ideas should have similar grammatical structure
- **Active/Passive Voice:** Choose appropriate voice for clarity

## Connections to Real-Life Situations

### Academic Writing
- Research papers require precise grammar
- Essay writing demands proper sentence structure
- Examination answers need correct grammar for high scores
- Academic presentations require clear language

### Professional Communication
- Business emails must be grammatically correct
- Job applications require error-free writing
- Professional reports need proper structure
- Presentations demand clear sentence construction

### Digital Communication
- Social media posts should be grammatically sound
- Blog writing requires proper parts of speech usage
- Online content creation needs correct punctuation
- Professional networking demands proper language

### Creative Writing
- Stories require varied sentence structures
- Poetry uses parts of speech creatively
- Novels demand consistent grammar
- Scripts need proper dialogue punctuation

## Exam Preparation Guide

### WAEC Exam Focus
- Parts of speech identification (30-40% of questions)
- Sentence construction and correction (25-35% of questions)
- Subject-verb agreement (15-20% of questions)
- Punctuation (10-15% of questions)
- Grammar rules application (10-15% of questions)

### Study Strategy
1. Learn parts of speech with examples
2. Practice identifying parts in sentences
3. Master subject-verb agreement rules
4. Study punctuation rules and exceptions
5. Review common grammatical errors

### Time Management Tips
- Spend 1-2 minutes per identification question
- Read correction questions carefully
- Practice punctuation quickly
- Review answers for grammatical accuracy
- Manage time for both objective and essay questions

### Answering Exam Questions
- Read instructions and examples carefully
- Underline key words in questions
- Show working for correction questions
- Use correct grammatical terminology
- Explain answers where required

## 🎓 Learning Tips - Choose Your Preferred Learning Style

### Visual Learning
**Best for:** Learners who prefer diagrams and visual representations
- Create color-coded parts of speech charts
- Draw sentence structure diagrams
- Use mind maps for grammar rules
- Create visual timelines for verb tenses
- Design flowcharts for punctuation rules

### Kinesthetic Learning
**Best for:** Learners who learn by doing hands-on activities
- Act out parts of speech with body movements
- Build sentence structures with word cards
- Create physical models of sentence types
- Practice punctuation with writing exercises
- Role-play subject-verb agreement scenarios

### Auditory Learning
**Best for:** Learners who understand better through listening and discussion
- Listen to grammar rule explanations
- Join English discussion groups
- Record yourself reading and analyzing sentences
- Participate in pronunciation and intonation practice
- Discuss literature and grammar with peers

### Reading/Writing Learning
**Best for:** Learners who prefer text-based information
- Create detailed grammar notes and rules
- Write summaries of parts of speech
- Create flashcards for grammar terms
- Write practice sentences and paragraphs
- Maintain an English journal with corrections

## Summary of Key Points
- Eight parts of speech: noun, pronoun, verb, adjective, adverb, preposition, conjunction, interjection
- Sentences have subjects and predicates
- Subject-verb agreement is crucial for correctness
- Punctuation marks help clarify meaning
- Practice regularly to master grammar rules
- Apply grammar rules in all forms of communication

## Additional Resources
- Textbook: Senior Secondary English Grammar
- Online: Grammar practice websites
- Videos: English grammar tutorial channels
- Apps: Grammar check and practice apps
- Exercises: Daily grammar worksheets

## Frequently Asked Questions

**Q: Why is grammar important?**
A: Grammar ensures clear communication and is essential for academic and professional success.

**Q: How many parts of speech are there?**
A: There are eight traditional parts of speech in English.

**Q: What's the most common grammatical error?**
A: Subject-verb agreement errors are very common.

**Q: How can I improve my grammar?**
A: Practice regularly, read extensively, and seek feedback on your writing.

**Q: What's the best way to learn grammar?**
A: Combine theory with practice, use real-life examples, and apply rules consistently.""",
            "estimated_read_time": 50,
            "prerequisites": ["basic_english"],
            "learning_options": ["visual", "kinesthetic", "auditory", "reading_writing"],
            "related_questions": ["waec_english_ss1_grammar_2020_q1", "waec_english_ss1_parts_speech_2021_q2"],
            "tags": ["english", "grammar", "parts_speech", "sentence_structure", "ss1", "nerdc", "learning_tips"],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "author": "English Curriculum Expert",
            "version": 1
        }
    ]

    return content_items

def save_to_content_service(content_items):
    """Save content items to the content service"""
    # Load existing content
    content_file = "connected_stack/backend/content_data.json"

    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"content": [], "progress": {}}

    # Add new content
    for item in content_items:
        # Check if content with this ID already exists
        existing_ids = [c['id'] for c in data['content']]
        if item['id'] not in existing_ids:
            data['content'].append(item)
            print(f"✓ Added: {item['title']}")
        else:
            print(f"⚠ Skipped (already exists): {item['title']}")

    # Save back to file
    with open(content_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Successfully saved {len(content_items)} comprehensive NERDC content items")

def main():
    print("🚀 Generating Comprehensive NERDC Curriculum Content with Learning Options...\n")

    # Generate content
    content_items = generate_comprehensive_nerdc_content()

    # Save content
    save_to_content_service(content_items)

    # Print statistics
    print(f"\n📊 Content Generation Statistics:")
    print(f"  Total items: {len(content_items)}")
    subjects = {}
    levels = {}
    for item in content_items:
        subj = item['subject']
        level = item['level']
        subjects[subj] = subjects.get(subj, 0) + 1
        levels[level] = levels.get(level, 0) + 1

    print("  By Subject:")
    for subj, count in sorted(subjects.items()):
        print(f"    {subj}: {count} items")

    print("  By Level:")
    for level, count in sorted(levels.items()):
        print(f"    {level}: {count} items")

    print("\n🎓 Content Features:")
    print("  ✓ NERDC Senior Secondary School Curriculum Alignment")
    print("  ✓ Comprehensive Subject Coverage (Physics, Chemistry, Biology, English)")
    print("  ✓ Detailed Learning Objectives")
    print("  ✓ Core Concepts and Definitions")
    print("  ✓ Worked Examples with Solutions")
    print("  ✓ Common Misconceptions Addressed")
    print("  ✓ Practice Problems (Basic, Intermediate, Advanced)")
    print("  ✓ Real-Life Applications and Career Connections")
    print("  ✓ WAEC Exam Preparation Guidance")
    print("  ✓ 4 Learning Pathways (Visual, Kinesthetic, Auditory, Reading/Writing)")
    print("  ✓ Study Strategy Tips")
    print("  ✓ Time Management Advice")
    print("  ✓ Additional Resources and References")

    print("\n🎯 Learning Options Available:")
    print("  • Visual Learning: Diagrams, charts, mind maps, animations")
    print("  • Kinesthetic Learning: Hands-on activities, experiments, models")
    print("  • Auditory Learning: Listening, discussion, recordings")
    print("  • Reading/Writing Learning: Notes, summaries, flashcards, journals")

    print("\n📚 Subjects Covered:")
    print("  • Physics: Newton's Laws of Motion")
    print("  • Chemistry: Atomic Structure and Bonding")
    print("  • Biology: Cell Structure and Function")
    print("  • English: Parts of Speech and Sentence Structure")

    print("\n✨ Each content item includes:")
    print("  • 45-60 minute comprehensive study guides")
    print("  • WAEC-aligned learning objectives")
    print("  • Step-by-step worked examples")
    print("  • Practice exercises at 3 difficulty levels")
    print("  • Real-world applications")
    print("  • Exam preparation strategies")
    print("  • Personalized learning tips")

if __name__ == "__main__":
    main()