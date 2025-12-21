#!/usr/bin/env python3
"""
SS3 NERDC Content Generator
Generates comprehensive educational content for Senior Secondary School 3 (SS3)
across all subjects with learning options and NERDC curriculum alignment.
"""

import json
import datetime
import uuid

def generate_ss3_comprehensive_nerdc_content():
    """
    Generate comprehensive NERDC-aligned content for SS3 across all subjects.
    Includes learning options, practice problems, and exam preparation.
    """

    content_items = []

    # Mathematics SS3 - Calculus
    math_content = {
        "id": f"nerdc-math-ss3-calculus-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Introduction to Calculus (SS3)",
        "subject": "Mathematics",
        "level": "SS3",
        "curriculum_framework": "NERDC Senior Secondary School Mathematics",
        "learning_objectives": [
            "Understand limits and continuity",
            "Differentiate algebraic functions",
            "Apply derivatives to rates of change and optimization",
            "Understand basic integration concepts"
        ],
        "content": """
## 📐 Introduction to Calculus

### Core Concepts
Calculus is the mathematical study of change and motion.

**Limits and Continuity:**
- **Limit**: Value a function approaches as input approaches a value
- **Continuity**: Function is continuous if limit equals function value
- **Asymptotes**: Lines that a curve approaches but never touches

**Differentiation:**
- **Derivative**: Rate of change of a function
- **Power Rule**: d/dx[xⁿ] = nxⁿ⁻¹
- **Product Rule**: d/dx[uv] = u'v + uv'
- **Quotient Rule**: d/dx[u/v] = (u'v - uv')/v²

**Applications:**
- **Rate of Change**: Velocity, acceleration
- **Optimization**: Maximum/minimum problems
- **Tangent Lines**: Slope of curve at a point

### Worked Examples

**Example 1: Basic Differentiation**
Find derivative of f(x) = 3x² + 2x - 1
Solution: f'(x) = 6x + 2

**Example 2: Product Rule**
Differentiate f(x) = (x² + 1)(x - 3)
Solution: f'(x) = (2x)(x - 3) + (x² + 1)(1) = 2x² - 6x + x² + 1 = 3x² - 6x + 1

**Example 3: Optimization**
Find maximum area of rectangle with perimeter 20m
Solution: A = xy, 2x + 2y = 20 → y = 10 - x
A = x(10 - x) = 10x - x²
dA/dx = 10 - 2x = 0 → x = 5, y = 5, A = 25m²

### Common Misconceptions
- Derivative is the same as slope
- Limits always exist
- All functions are differentiable
- Integration is just anti-differentiation

### Real-Life Applications
- Physics: Velocity and acceleration calculations
- Economics: Marginal cost and revenue analysis
- Engineering: Optimization of designs
- Medicine: Drug concentration modeling
- Computer Science: Algorithm optimization

### Practice Problems

**Basic Level:**
1. Find derivative of f(x) = x³ + 2x² - x + 1
2. Evaluate limit: lim(x→2) (x² - 4)/(x - 2)
3. Determine if f(x) = |x| is differentiable at x = 0

**Intermediate Level:**
4. Differentiate f(x) = (x² + 3)/(x - 1) using quotient rule
5. Find equation of tangent line to y = x² at x = 2
6. Solve optimization: Maximize profit P = 100x - x² - 50

**Advanced Level:**
7. Find second derivative of f(x) = eˣ sin x
8. Apply Rolle's theorem to f(x) = x³ - 3x on [-2, 2]
9. Evaluate definite integral ∫(1 to 3) (2x + 1) dx

### WAEC Exam Preparation
- Basic differentiation (power, product, quotient rules)
- Limits and continuity concepts
- Applications to maximum/minimum problems
- Simple integration problems

### Study Tips
- Master basic differentiation rules before applications
- Practice 50+ differentiation problems weekly
- Understand geometric interpretation of derivatives
- Use graphing calculators for visualization

### Additional Resources
- Khan Academy: Differential Calculus
- YouTube: Professor Leonard (Calculus)
- Textbook: Calculus by James Stewart
- Wolfram Alpha for derivative calculations
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Graph functions and their derivatives simultaneously",
                    "Create visual representations of limits approaching values",
                    "Use color-coded diagrams for differentiation rules",
                    "Watch animations of tangent lines and slopes"
                ],
                "activities": [
                    "Plot derivative graphs alongside original functions",
                    "Create visual guides for optimization problems",
                    "Design geometric interpretations of calculus concepts"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Use physical models to demonstrate rates of change",
                    "Build 3D representations of optimization problems",
                    "Create motion demonstrations for velocity concepts",
                    "Use manipulatives for understanding limits"
                ],
                "activities": [
                    "Construct physical models of maximum/minimum scenarios",
                    "Demonstrate calculus concepts with moving objects",
                    "Build geometric shapes to understand areas and volumes"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to calculus explanation podcasts",
                    "Record yourself explaining differentiation steps",
                    "Participate in math discussion groups",
                    "Use rhythm for memorizing rules"
                ],
                "activities": [
                    "Teach calculus concepts to classmates",
                    "Create audio explanations of complex problems",
                    "Listen to calculus lectures and problem solutions"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed explanations of calculus theorems",
                    "Create step-by-step solution guides",
                    "Maintain a calculus problem journal",
                    "Read calculus applications in real-world contexts"
                ],
                "activities": [
                    "Write proofs of basic calculus theorems",
                    "Document solution strategies for different problem types",
                    "Create comparison charts of differentiation rules"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "f(x) = 4x³ - 2x² + x - 1, find f'(x)",
                "lim(x→3) (x² - 9)/(x - 3)",
                "Is f(x) = √x continuous at x = 0?"
            ],
            "intermediate": [
                "Differentiate (x² + 5x + 6)/(x + 2)",
                "Tangent to y = x²/4 at x = 2",
                "Maximize A = xy subject to x + y = 10"
            ],
            "advanced": [
                "Second derivative of ln(x² + 1)",
                "Apply mean value theorem to f(x) = x³ - x",
                "∫(0 to 4) √(x + 1) dx"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Differentiation of polynomial functions",
                "Limits and continuity",
                "Applications to rates of change",
                "Basic integration problems"
            ],
            "common_questions": [
                "Find derivatives using various rules",
                "Solve limits problems",
                "Apply calculus to optimization",
                "Evaluate simple integrals"
            ],
            "time_management": "Allocate 15-20 minutes per calculus problem",
            "scoring_tips": "Show all differentiation steps clearly, include correct units"
        },
        "career_connections": [
            "Engineering: Design optimization and modeling",
            "Physics: Motion analysis and field theory",
            "Economics: Marginal analysis and optimization",
            "Computer Science: Algorithm analysis and machine learning"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Advanced",
        "prerequisites": ["Advanced algebra, functions, trigonometry"],
        "tags": ["calculus", "differentiation", "limits", "optimization", "integration", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(math_content)

    # Physics SS3 - Modern Physics
    physics_content = {
        "id": f"nerdc-physics-ss3-modern-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Modern Physics: Quantum Theory and Nuclear Physics (SS3)",
        "subject": "Physics",
        "level": "SS3",
        "curriculum_framework": "NERDC Senior Secondary School Physics",
        "learning_objectives": [
            "Understand photoelectric effect and quantum theory",
            "Explain wave-particle duality",
            "Understand nuclear structure and radioactivity",
            "Apply nuclear physics to energy production"
        ],
        "content": """
## ⚛️ Modern Physics: Quantum Theory and Nuclear Physics

### Core Concepts
Modern physics explains phenomena that classical physics cannot.

**Quantum Theory:**
- **Photoelectric Effect**: Light behaves as particles (photons)
- **Energy of Photon**: E = hf = hc/λ
- **Work Function**: Minimum energy to eject electron
- **Threshold Frequency**: f₀ = φ/h

**Wave-Particle Duality:**
- **de Broglie Wavelength**: λ = h/p
- **Uncertainty Principle**: Δx Δp ≥ h/4π
- **Quantum Numbers**: Describe electron states

**Nuclear Physics:**
- **Nuclear Structure**: Protons + neutrons
- **Radioactivity**: Alpha, beta, gamma decay
- **Half-Life**: Time for half of atoms to decay
- **Nuclear Reactions**: Fission and fusion

### Worked Examples

**Example 1: Photoelectric Effect**
Light of wavelength 400nm ejects electrons with 1.5eV kinetic energy.
Work function φ = hc/λ - KE = (1240/400) - 1.5 = 3.1 - 1.5 = 1.6eV

**Example 2: Nuclear Decay**
²³⁸U → ²³⁴Th + ⁴He (Alpha decay)
Mass defect = 238.0508 - (234.0436 + 4.0026) = 0.0046u
Energy released = 0.0046 × 931.5 = 4.29MeV

**Example 3: Half-Life Calculation**
Radioactive substance has half-life 8 hours. Initial mass 64g.
After 24 hours: 64g → 32g → 16g → 8g

### Common Misconceptions
- Light is only waves or only particles
- Nuclear reactions are chemical reactions
- All radiation is harmful
- Quantum effects only occur at atomic level

### Real-Life Applications
- Solar panels and photovoltaic cells
- Medical imaging (X-rays, PET scans)
- Nuclear power generation
- Radiation therapy for cancer treatment
- Semiconductor technology and computers
- Nuclear weapons and peace treaties

### Practice Problems

**Basic Level:**
1. Calculate energy of photon with λ = 600nm
2. Find threshold frequency for metal with φ = 2.3eV
3. What is de Broglie wavelength of electron moving at 2×10⁶ m/s?

**Intermediate Level:**
4. In photoelectric effect, stopping potential is 3V for λ = 400nm
5. Calculate half-life if 75% of sample decays in 20 days
6. Determine type of decay: ²⁴₁Am → ²³⁷Np + ?

**Advanced Level:**
7. Apply uncertainty principle to electron in 1nm box
8. Calculate binding energy of deuteron
9. Explain nuclear fusion in stars

### WAEC Exam Preparation
- Photoelectric effect calculations
- Nuclear decay equations
- Half-life problems
- Wave-particle duality concepts
- Nuclear energy calculations

### Study Tips
- Memorize key constants (h, c, e, etc.)
- Practice unit conversions (eV to J, u to kg)
- Understand energy-mass equivalence
- Draw nuclear decay diagrams

### Additional Resources
- PhET: Quantum Physics simulations
- YouTube: Physics Girl (Modern Physics)
- Textbook: Modern Physics by Serway
- CERN website for particle physics
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Draw energy level diagrams for atoms",
                    "Create visual representations of nuclear decay chains",
                    "Use color coding for different types of radiation",
                    "Watch animations of quantum phenomena"
                ],
                "activities": [
                    "Design diagrams showing photoelectric effect",
                    "Create visual guides for nuclear reactions",
                    "Make models of atomic energy levels"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build models of atomic structure",
                    "Use physical demonstrations of wave-particle duality",
                    "Create radioactive decay simulations with objects",
                    "Construct models of nuclear reactors"
                ],
                "activities": [
                    "Assemble atomic structure models",
                    "Demonstrate half-life with coin flipping",
                    "Build simple cloud chambers for radiation detection"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to quantum physics podcasts",
                    "Record explanations of nuclear processes",
                    "Participate in physics discussion groups",
                    "Use audio descriptions of quantum concepts"
                ],
                "activities": [
                    "Create audio explanations of modern physics",
                    "Listen to lectures on quantum mechanics",
                    "Record problem-solving strategies"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed explanations of quantum theory",
                    "Create study guides for nuclear physics",
                    "Maintain a physics concept journal",
                    "Read about quantum applications in technology"
                ],
                "activities": [
                    "Write research summaries on nuclear energy",
                    "Document experimental procedures",
                    "Create comparison charts of radiation types"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Photon energy for λ = 500nm",
                "Work function φ = 3.2eV, find threshold wavelength",
                "de Broglie wavelength for 5eV electron"
            ],
            "intermediate": [
                "Photoelectric effect: λ = 350nm, stopping V = 2.5V",
                "Half-life calculation: 80g → 10g in t hours",
                "Nuclear decay: ²²⁶Ra → ²²²Rn + ?"
            ],
            "advanced": [
                "Uncertainty principle application",
                "Nuclear binding energy calculation",
                "Quantum tunneling explanation"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Photoelectric effect and quantum theory",
                "Nuclear structure and radioactivity",
                "Half-life calculations",
                "Wave-particle duality"
            ],
            "common_questions": [
                "Calculate photon energies and work functions",
                "Solve nuclear decay problems",
                "Explain quantum concepts",
                "Calculate half-lives and decay rates"
            ],
            "time_management": "Allocate 12-18 minutes per modern physics problem",
            "scoring_tips": "Show all calculations with correct units, explain concepts clearly"
        },
        "career_connections": [
            "Nuclear Engineering: Power plant design",
            "Medical Physics: Radiation therapy equipment",
            "Quantum Computing: Research and development",
            "Renewable Energy: Solar technology development"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Advanced",
        "prerequisites": ["Basic physics, atomic structure, waves"],
        "tags": ["modern physics", "quantum theory", "nuclear physics", "photoelectric effect", "radioactivity", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(physics_content)

    # Chemistry SS3 - Electrochemistry
    chemistry_content = {
        "id": f"nerdc-chemistry-ss3-electrochemistry-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Electrochemistry and Chemical Kinetics (SS3)",
        "subject": "Chemistry",
        "level": "SS3",
        "curriculum_framework": "NERDC Senior Secondary School Chemistry",
        "learning_objectives": [
            "Understand electrochemical cells and their applications",
            "Calculate cell potentials and predict spontaneity",
            "Understand reaction rates and factors affecting them",
            "Apply collision theory to reaction mechanisms"
        ],
        "content": """
## ⚡ Electrochemistry and Chemical Kinetics

### Core Concepts
Electrochemistry studies chemical reactions involving electron transfer.

**Electrochemical Cells:**
- **Galvanic Cells**: Convert chemical to electrical energy
- **Electrolytic Cells**: Use electrical energy for chemical change
- **Standard Hydrogen Electrode**: Reference electrode (E⁰ = 0V)
- **Cell Potential**: E_cell = E_cathode - E_anode

**Reaction Kinetics:**
- **Rate of Reaction**: Change in concentration per unit time
- **Rate Law**: Rate = k[A]ᵐ[B]ⁿ
- **Order of Reaction**: m + n (from rate law)
- **Activation Energy**: Minimum energy for reaction

**Factors Affecting Rate:**
- **Concentration**: Higher concentration → faster rate
- **Temperature**: Higher temperature → faster rate
- **Surface Area**: Larger surface area → faster rate
- **Catalysts**: Lower activation energy

### Worked Examples

**Example 1: Cell Potential**
Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)
E_cell = E°_Cu - E°_Zn = 0.34 - (-0.76) = 1.10V

**Example 2: Rate Law Determination**
Reaction: A + B → C
Experiment data shows rate doubles when [A] doubles, unchanged when [B] doubles
Rate = k[A]¹[B]⁰ = k[A], first order in A, zero order in B

**Example 3: Activation Energy**
Reaction rate doubles every 10°C rise. Calculate activation energy.
k₂/k₁ = 2 = e^(-Ea/RT₂) / e^(-Ea/RT₁)
Ea ≈ 50 kJ/mol

### Common Misconceptions
- All metals dissolve in acids
- Catalysts are consumed in reactions
- Cell potential depends only on voltage
- Reaction rate is constant throughout

### Real-Life Applications
- Batteries and fuel cells for energy storage
- Electroplating for metal coating
- Corrosion prevention and control
- Industrial electrolysis for metal production
- Catalytic converters in automobiles
- Food preservation and spoilage control

### Practice Problems

**Basic Level:**
1. Calculate E_cell for Zn + 2H⁺ → Zn²⁺ + H₂
2. Determine order of reaction from rate data
3. Explain effect of temperature on reaction rate

**Intermediate Level:**
4. Design a galvanic cell with E_cell > 1.0V
5. Calculate activation energy from rate constants
6. Predict effect of catalyst on reaction mechanism

**Advanced Level:**
7. Calculate equilibrium constant from cell potential
8. Determine rate law from experimental data
9. Explain enzyme catalysis mechanism

### WAEC Exam Preparation
- Electrochemical cell calculations
- Standard electrode potentials
- Reaction kinetics and rate laws
- Factors affecting reaction rates
- Electrolysis calculations

### Study Tips
- Memorize standard electrode potentials
- Practice cell diagram notation
- Understand collision theory
- Create rate law expressions from data

### Additional Resources
- Khan Academy: Electrochemistry
- YouTube: Crash Course Chemistry
- Textbook: Physical Chemistry by Atkins
- Online electrochemistry simulators
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Draw detailed electrochemical cell diagrams",
                    "Create energy profile diagrams for reactions",
                    "Use color coding for oxidation/reduction processes",
                    "Watch animations of electron transfer"
                ],
                "activities": [
                    "Design visual guides for electrochemical series",
                    "Create reaction coordinate diagrams",
                    "Make models of electrolytic cells"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build physical models of electrochemical cells",
                    "Conduct electrolysis experiments",
                    "Use manipulatives for reaction kinetics",
                    "Create physical demonstrations of catalysts"
                ],
                "activities": [
                    "Assemble simple voltaic cells",
                    "Perform rate of reaction experiments",
                    "Build models showing activation energy"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to electrochemistry podcasts",
                    "Record explanations of reaction mechanisms",
                    "Participate in chemistry discussion groups",
                    "Use audio for memorizing electrode potentials"
                ],
                "activities": [
                    "Create audio guides for electrochemical concepts",
                    "Listen to lectures on chemical kinetics",
                    "Record problem-solving approaches"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed reaction mechanisms",
                    "Create study guides for electrochemical cells",
                    "Maintain a kinetics experiment journal",
                    "Read about industrial electrochemical processes"
                ],
                "activities": [
                    "Write research reports on fuel cells",
                    "Document experimental procedures and results",
                    "Create comparison charts of reaction rates"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "E_cell for Mg + Cu²⁺ → Mg²⁺ + Cu",
                "Rate law: rate = k[A]²[B]",
                "Effect of surface area on reaction rate"
            ],
            "intermediate": [
                "Design Daniell cell and calculate E_cell",
                "Calculate Ea from k₁ = 0.01, k₂ = 0.02 (T difference 10K)",
                "Predict rate change when concentration doubles"
            ],
            "advanced": [
                "Calculate K from E°_cell",
                "Determine reaction order from concentration-time data",
                "Explain heterogeneous catalysis"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Electrochemical cells and potentials",
                "Reaction kinetics and rate laws",
                "Factors affecting reaction rates",
                "Electrolysis and electrode potentials"
            ],
            "common_questions": [
                "Calculate cell potentials and predict spontaneity",
                "Determine reaction orders and rate constants",
                "Explain effects of temperature and catalysts",
                "Solve electrolysis problems"
            ],
            "time_management": "Allocate 15-20 minutes per electrochemistry problem",
            "scoring_tips": "Show all calculations clearly, explain concepts with examples"
        },
        "career_connections": [
            "Chemical Engineering: Industrial electrolysis",
            "Battery Technology: Energy storage systems",
            "Environmental Science: Corrosion control",
            "Pharmaceuticals: Drug reaction kinetics"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Advanced",
        "prerequisites": ["Basic chemistry, redox reactions, rates of reaction"],
        "tags": ["electrochemistry", "chemical kinetics", "electrochemical cells", "reaction rates", "activation energy", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(chemistry_content)

    # Biology SS3 - Evolution and Ecology
    biology_content = {
        "id": f"nerdc-biology-ss3-evolution-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Evolution and Ecology (SS3)",
        "subject": "Biology",
        "level": "SS3",
        "curriculum_framework": "NERDC Senior Secondary School Biology",
        "learning_objectives": [
            "Understand mechanisms of evolution",
            "Explain natural selection and adaptation",
            "Analyze population dynamics and ecosystem interactions",
            "Understand conservation and biodiversity"
        ],
        "content": """
## 🌿 Evolution and Ecology

### Core Concepts
Evolution explains the diversity of life and ecological systems sustain it.

**Evolution:**
- **Natural Selection**: Differential survival and reproduction
- **Genetic Variation**: Raw material for evolution
- **Adaptation**: Traits that improve survival
- **Speciation**: Formation of new species

**Ecology:**
- **Ecosystem**: Community + physical environment
- **Food Chains/Webs**: Energy flow in ecosystems
- **Nutrient Cycling**: Carbon, nitrogen, water cycles
- **Population Dynamics**: Growth, carrying capacity, limiting factors

**Biodiversity:**
- **Genetic Diversity**: Variety within species
- **Species Diversity**: Number and abundance of species
- **Ecosystem Diversity**: Variety of habitats

### Worked Examples

**Example 1: Natural Selection**
Peppered moths in industrial England:
- Light moths camouflaged on clean trees
- Dark moths camouflaged on polluted trees
- Pollution favored dark moth survival

**Example 2: Population Growth**
Bacterial population: 1000 cells, doubles every 20 minutes
After 2 hours (6 generations): 1000 × 2⁶ = 64,000 cells

**Example 3: Energy Flow**
Grass (1000 kJ) → Grasshopper (100 kJ) → Frog (10 kJ) → Snake (1 kJ)
Energy loss: 90% at each trophic level

### Common Misconceptions
- Evolution is goal-directed
- Humans evolved from chimpanzees
- Ecology is only about pollution
- All species in ecosystem are equal

### Real-Life Applications
- Medicine: Antibiotic resistance evolution
- Agriculture: Pest resistance management
- Conservation: Endangered species protection
- Climate Change: Ecosystem adaptation
- Public Health: Disease ecology

### Practice Problems

**Basic Level:**
1. Explain natural selection with example
2. Draw simple food chain
3. Define biodiversity

**Intermediate Level:**
4. Compare Lamarckism vs Darwinism
5. Analyze population growth curve
6. Explain nitrogen cycle

**Advanced Level:**
7. Discuss evidence for evolution
8. Analyze ecosystem stability factors
9. Design conservation strategy

### WAEC Exam Preparation
- Theories of evolution
- Natural selection mechanisms
- Ecosystem components and interactions
- Population ecology
- Conservation biology

### Study Tips
- Create evolutionary timelines
- Draw ecosystem diagrams
- Understand mathematical models
- Connect concepts to current issues

### Additional Resources
- HHMI: Evolution resources
- National Geographic: Ecology
- Textbook: Biology by Campbell
- Online biodiversity databases
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Create evolutionary tree diagrams",
                    "Draw detailed ecosystem food webs",
                    "Use color coding for different species interactions",
                    "Watch animations of evolutionary processes"
                ],
                "activities": [
                    "Design visual guides for natural selection",
                    "Create ecosystem component diagrams",
                    "Make biodiversity comparison charts"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build physical models of evolutionary trees",
                    "Create ecosystem simulations with objects",
                    "Use role-playing for predator-prey relationships",
                    "Construct food web models"
                ],
                "activities": [
                    "Assemble evolutionary timeline models",
                    "Demonstrate population growth with objects",
                    "Build habitat dioramas"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to evolution podcasts",
                    "Record explanations of ecological concepts",
                    "Participate in biology discussion groups",
                    "Use audio for species identification"
                ],
                "activities": [
                    "Create audio guides for evolutionary concepts",
                    "Listen to ecology lectures",
                    "Record field observation notes"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed evolutionary explanations",
                    "Create study guides for ecological systems",
                    "Maintain a field observation journal",
                    "Read conservation biology articles"
                ],
                "activities": [
                    "Write research reports on endangered species",
                    "Document experimental procedures",
                    "Create comparison charts of ecosystems"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Explain Darwin's theory of evolution",
                "Draw grassland food chain",
                "Define carrying capacity"
            ],
            "intermediate": [
                "Compare convergent vs divergent evolution",
                "Analyze predator-prey population cycles",
                "Explain carbon cycle processes"
            ],
            "advanced": [
                "Discuss human evolution evidence",
                "Analyze deforestation ecosystem impact",
                "Design biodiversity conservation plan"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Mechanisms of evolution",
                "Natural selection and adaptation",
                "Ecosystem structure and function",
                "Population ecology",
                "Conservation and biodiversity"
            ],
            "common_questions": [
                "Explain evolutionary theories",
                "Analyze ecosystem interactions",
                "Discuss conservation strategies",
                "Solve population ecology problems"
            ],
            "time_management": "Allocate 20-25 minutes per essay question",
            "scoring_tips": "Use specific examples, clear structure, scientific terminology"
        },
        "career_connections": [
            "Conservation Biology: Wildlife management",
            "Environmental Science: Ecosystem monitoring",
            "Public Health: Disease ecology",
            "Agriculture: Sustainable farming systems"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Advanced",
        "prerequisites": ["Basic biology, genetics, ecosystems"],
        "tags": ["evolution", "ecology", "natural selection", "biodiversity", "conservation", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(biology_content)

    # English SS3 - Essay Writing
    english_content = {
        "id": f"nerdc-english-ss3-essay-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Essay Writing and Advanced Literature (SS3)",
        "subject": "English Language",
        "level": "SS3",
        "curriculum_framework": "NERDC Senior Secondary School English",
        "learning_objectives": [
            "Write effective essays with clear structure and argumentation",
            "Analyze literary texts using advanced techniques",
            "Understand different essay types and their conventions",
            "Develop critical thinking through literary analysis"
        ],
        "content": """
## ✍️ Essay Writing and Advanced Literature

### Core Concepts
Essay writing combines creativity with critical analysis and structured argumentation.

**Essay Types:**
- **Expository**: Explains or informs
- **Argumentative**: Persuades with evidence
- **Analytical**: Examines components and relationships
- **Narrative**: Tells a story with purpose

**Essay Structure:**
- **Introduction**: Hook, background, thesis
- **Body Paragraphs**: Topic sentences, evidence, analysis
- **Conclusion**: Restate thesis, summarize, final thought

**Literary Analysis:**
- **Themes**: Central messages and ideas
- **Characterization**: How characters are developed
- **Plot Structure**: Exposition, rising action, climax, falling action, resolution
- **Literary Devices**: Symbolism, irony, foreshadowing, imagery

### Worked Examples

**Example 1: Thesis Statement**
Weak: "Shakespeare's Macbeth is about ambition."
Strong: "In Macbeth, Shakespeare demonstrates how unchecked ambition leads to moral corruption and downfall."

**Example 2: Topic Sentence**
"The use of symbolism in Lord of the Flies reinforces the theme of civilization's fragility."

**Example 3: Textual Evidence**
In Things Fall Apart, Achebe uses proverbs to illustrate Igbo cultural values: "A man who pays respect to the great paves the way for his own greatness."

### Common Misconceptions
- Essays are only for exams
- Literary analysis is subjective opinion
- All essays need 5 paragraphs
- Introduction should be long and detailed

### Real-Life Applications
- Academic writing for university
- Professional reports and proposals
- Critical thinking in all careers
- Effective communication skills
- Cultural understanding through literature

### Practice Problems

**Basic Level:**
1. Write a thesis statement for given topic
2. Identify main idea in paragraph
3. Explain a literary device

**Intermediate Level:**
4. Write introductory paragraph
5. Analyze character development
6. Compare two literary works

**Advanced Level:**
7. Write complete argumentative essay
8. Analyze theme development
9. Critique author's writing style

### WAEC Exam Preparation
- Essay planning and structure
- Literary text analysis
- Comprehension questions
- Grammar and vocabulary in context
- Creative writing tasks

### Study Tips
- Read widely across genres
- Practice timed essay writing
- Learn essay structures by type
- Analyze model essays
- Build vocabulary systematically

### Additional Resources
- Purdue OWL: Essay writing
- YouTube: Literature essay analysis
- Textbook: Advanced English Literature
- Online essay writing courses
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Create mind maps for essay planning",
                    "Draw plot diagrams for literary works",
                    "Use color coding for essay structure",
                    "Watch essay writing tutorial videos"
                ],
                "activities": [
                    "Design visual essay outlines",
                    "Create character relationship diagrams",
                    "Make theme development charts"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Act out scenes from literary works",
                    "Use physical objects for essay planning",
                    "Create storyboards for narratives",
                    "Build models representing essay structure"
                ],
                "activities": [
                    "Perform dramatic readings of essays",
                    "Use index cards for essay organization",
                    "Create physical representations of literary devices"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to essay writing podcasts",
                    "Record yourself reading essays aloud",
                    "Participate in literature discussion groups",
                    "Use audio for vocabulary building"
                ],
                "activities": [
                    "Create audio recordings of essay analyses",
                    "Listen to literary criticism podcasts",
                    "Record oral presentations of essay topics"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed essay outlines",
                    "Create study guides for literary terms",
                    "Maintain a writing journal",
                    "Read and analyze published essays"
                ],
                "activities": [
                    "Write practice essays on various topics",
                    "Create essay planning templates",
                    "Document writing process and revisions"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Write thesis for 'Importance of Education'",
                "Identify symbolism in a short poem",
                "Explain essay introduction structure"
            ],
            "intermediate": [
                "Write body paragraph with evidence",
                "Analyze conflict in a story",
                "Compare essay types"
            ],
            "advanced": [
                "Write complete expository essay",
                "Analyze author's purpose and technique",
                "Critique literary work's themes"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Essay writing structure and content",
                "Literary text comprehension",
                "Summary and analysis skills",
                "Grammar and vocabulary usage"
            ],
            "common_questions": [
                "Write essays on given topics",
                "Analyze passages and poems",
                "Answer comprehension questions",
                "Demonstrate writing skills"
            ],
            "time_management": "Allocate 45-60 minutes per essay question",
            "scoring_tips": "Clear structure, relevant content, good language use, originality"
        },
        "career_connections": [
            "Writing and Journalism: Article and feature writing",
            "Education: Teaching and curriculum development",
            "Law: Legal writing and argumentation",
            "Business: Report writing and communication"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Advanced",
        "prerequisites": ["Basic essay writing, literature analysis, grammar"],
        "tags": ["essay writing", "literature", "literary analysis", "creative writing", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(english_content)

    return content_items

def save_to_content_service(content_items):
    """
    Save the generated content to the content service database.
    """
    try:
        with open('content_data.json', 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"content": []}

    # Add new content
    data["content"].extend(content_items)

    # Save updated content
    with open('content_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully saved {len(content_items)} comprehensive SS3 NERDC content items")
    return True

def main():
    """
    Main function to generate and save SS3 NERDC content.
    """
    print("🚀 Generating Comprehensive SS3 NERDC Curriculum Content with Learning Options...")

    # Generate content
    content_items = generate_ss3_comprehensive_nerdc_content()

    # Display generation statistics
    subjects = {}
    for item in content_items:
        subj = item.get('subject', 'Unknown')
        subjects[subj] = subjects.get(subj, 0) + 1

    print(f"\n✅ Generated {len(content_items)} comprehensive SS3 content items")
    print("\n📚 Content Breakdown:")
    for subj, count in subjects.items():
        print(f"  {subj}: {count} items")

    # Save to database
    save_to_content_service(content_items)

    print("\n📊 Content Features:")
    print("  ✓ NERDC Senior Secondary School Curriculum Alignment")
    print("  ✓ Comprehensive Subject Coverage (Mathematics, Physics, Chemistry, Biology, English)")
    print("  ✓ Detailed Learning Objectives")
    print("  ✓ Core Concepts and Worked Examples")
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

    print("\n📚 SS3 Topics Covered:")
    print("  • Mathematics: Introduction to Calculus")
    print("  • Physics: Modern Physics (Quantum Theory and Nuclear Physics)")
    print("  • Chemistry: Electrochemistry and Chemical Kinetics")
    print("  • Biology: Evolution and Ecology")
    print("  • English: Essay Writing and Advanced Literature")

    print("\n✨ Each content item includes:")
    print("  • 45-60 minute comprehensive study guides")
    print("  • WAEC-aligned learning objectives")
    print("  • Step-by-step worked examples")
    print("  • Practice exercises at 3 difficulty levels")
    print("  • Real-world applications")
    print("  • Exam preparation strategies")
    print("  • Personalized learning tips")

if __name__ == '__main__':
    main()