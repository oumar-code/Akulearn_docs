#!/usr/bin/env python3
"""
SS2 NERDC Content Generator
Generates comprehensive educational content for Senior Secondary School 2 (SS2)
across all subjects with learning options and NERDC curriculum alignment.
"""

import json
import datetime
import uuid

def generate_ss2_comprehensive_nerdc_content():
    """
    Generate comprehensive NERDC-aligned content for SS2 across all subjects.
    Includes learning options, practice problems, and exam preparation.
    """

    content_items = []

    # Mathematics SS2 - Quadratic Equations
    math_content = {
        "id": f"nerdc-math-ss2-quadratic-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Quadratic Equations and Their Applications (SS2)",
        "subject": "Mathematics",
        "level": "SS2",
        "curriculum_framework": "NERDC Senior Secondary School Mathematics",
        "learning_objectives": [
            "Solve quadratic equations by factorization, completing the square, and quadratic formula",
            "Apply quadratic equations to real-life problems",
            "Graph quadratic functions and identify key features",
            "Understand the relationship between roots and coefficients"
        ],
        "content": """
## 📐 Quadratic Equations and Their Applications

### Core Concepts
A quadratic equation is an equation of the form ax² + bx + c = 0, where a ≠ 0.

**Key Methods of Solution:**
1. **Factorization**: Express as (px + q)(rx + s) = 0
2. **Completing the Square**: Transform to (x + h)² = k form
3. **Quadratic Formula**: x = [-b ± √(b² - 4ac)] / 2a

### Worked Examples

**Example 1: Factorization**
Solve x² + 5x + 6 = 0
Solution: (x + 2)(x + 3) = 0
x = -2 or x = -3

**Example 2: Quadratic Formula**
Solve 2x² - 7x + 3 = 0
Solution: x = [7 ± √(25)] / 4 = [7 ± 5]/4
x = 3 or x = 0.5

### Common Misconceptions
- Forgetting the ± sign in quadratic formula
- Not checking if solutions are valid in the context
- Confusing roots with coefficients

### Real-Life Applications
- Projectile motion in physics
- Profit maximization in business
- Area optimization problems
- Population growth modeling

### Practice Problems

**Basic Level:**
1. Solve x² + 8x + 15 = 0
2. Find roots of 3x² - 5x - 2 = 0

**Intermediate Level:**
3. A rectangular garden has area 50m². If length is 2m more than width, find dimensions.
4. Ball thrown upward reaches 20m height. Find time to reach maximum height (g=10m/s²).

**Advanced Level:**
5. Find quadratic equation with roots 3+√2 and 3-√2
6. Solve x² + (k-1)x + k = 0. Find k so one root is double the other.

### WAEC Exam Preparation
- Practice past questions on word problems
- Master all three solution methods
- Understand discriminant (b²-4ac) interpretation
- Focus on applications in physics and business

### Study Tips
- Create flashcards for formulas
- Practice graphing parabolas
- Work through 50+ problems weekly
- Join study groups for discussion

### Additional Resources
- Khan Academy: Quadratic Equations
- YouTube: MathTheBeautiful (applications)
- Textbook: New General Mathematics SS2
- Online calculator for verification
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Draw graphs of quadratic functions using graphing software",
                    "Create mind maps showing relationships between roots and coefficients",
                    "Use color-coded diagrams for factorization steps",
                    "Watch animated videos of projectile motion problems"
                ],
                "activities": [
                    "Graph quadratic functions and identify vertex, axis of symmetry",
                    "Create visual representations of word problems",
                    "Use GeoGebra for interactive quadratic explorations"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build physical models of parabolic trajectories",
                    "Use algebra tiles for factorization practice",
                    "Create quadratic function art with string and pins",
                    "Act out real-life scenarios involving quadratic relationships"
                ],
                "activities": [
                    "Conduct projectile motion experiments with balls",
                    "Build quadratic function sculptures using clay",
                    "Create movement sequences representing equation solving"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to podcasts explaining quadratic concepts",
                    "Record yourself explaining solutions step-by-step",
                    "Participate in math discussion groups",
                    "Use rhythm and rhyme for memorizing formulas"
                ],
                "activities": [
                    "Teach quadratic concepts to classmates",
                    "Create audio explanations of worked examples",
                    "Listen to math songs and mnemonics"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed explanations of each solution method",
                    "Create summary notes for different problem types",
                    "Maintain a problem-solving journal",
                    "Read quadratic applications in real-world contexts"
                ],
                "activities": [
                    "Write quadratic word problems and solutions",
                    "Create cheat sheets for exam preparation",
                    "Write explanations of common mistakes and how to avoid them"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Solve x² + 10x + 21 = 0",
                "Find roots of 2x² + x - 6 = 0",
                "Solve (x + 3)² = 16"
            ],
            "intermediate": [
                "Area of rectangle is 48cm², length exceeds width by 4cm",
                "Ball reaches 18m height, find initial velocity",
                "Find k so x² + kx + 9 = 0 has equal roots"
            ],
            "advanced": [
                "Solve x⁴ - 5x² + 4 = 0 by substitution",
                "Find quadratic with roots that are reciprocals",
                "Solve using quadratic formula: √(x+1) + √(x-1) = 2"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Word problems involving area, motion, profit",
                "Equations reducible to quadratic form",
                "Maximum/minimum value problems",
                "Simultaneous equations with quadratics"
            ],
            "common_questions": [
                "Solve quadratic equations by all methods",
                "Applications in physics and business",
                "Nature of roots and discriminant",
                "Sum and product of roots"
            ],
            "time_management": "Allocate 15-20 minutes per question, show all working clearly",
            "scoring_tips": "Full marks for correct answer with proper working, partial marks for method"
        },
        "career_connections": [
            "Engineering: Trajectory calculations for rockets, bridges",
            "Business: Profit maximization, cost analysis",
            "Architecture: Parabolic arch design",
            "Data Science: Modeling non-linear relationships"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic algebra, factorization, coordinate geometry"],
        "tags": ["quadratic equations", "algebra", "word problems", "applications", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(math_content)

    # Physics SS2 - Electricity
    physics_content = {
        "id": f"nerdc-physics-ss2-electricity-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Electricity and Electrical Circuits (SS2)",
        "subject": "Physics",
        "level": "SS2",
        "curriculum_framework": "NERDC Senior Secondary School Physics",
        "learning_objectives": [
            "Understand electric current, potential difference, and resistance",
            "Apply Ohm's law to electrical circuits",
            "Calculate equivalent resistance in series and parallel circuits",
            "Understand electrical power and energy consumption"
        ],
        "content": """
## ⚡ Electricity and Electrical Circuits

### Core Concepts
Electricity is the flow of electric charge through conductors.

**Fundamental Quantities:**
- **Current (I)**: Rate of flow of charge (Amperes)
- **Potential Difference (V)**: Electrical pressure (Volts)
- **Resistance (R)**: Opposition to current flow (Ohms)
- **Power (P)**: Rate of energy transfer (Watts)

**Ohm's Law:** V = IR (for ohmic conductors)

### Circuit Configurations

**Series Circuits:**
- Total resistance: R_total = R1 + R2 + R3
- Same current through all components
- Total voltage: V_total = V1 + V2 + V3

**Parallel Circuits:**
- Total resistance: 1/R_total = 1/R1 + 1/R2 + 1/R3
- Same voltage across all components
- Total current: I_total = I1 + I2 + I3

### Worked Examples

**Example 1: Series Circuit**
Three resistors: 2Ω, 3Ω, 5Ω connected in series to 12V battery.
- R_total = 2 + 3 + 5 = 10Ω
- I_total = V/R = 12/10 = 1.2A
- Power = VI = 12 × 1.2 = 14.4W

**Example 2: Parallel Circuit**
Two 4Ω resistors in parallel with 12V battery.
- 1/R_total = 1/4 + 1/4 = 0.5, so R_total = 2Ω
- I_total = 12/2 = 6A
- Current through each resistor = 3A

### Common Misconceptions
- Thinking current is used up in series circuits
- Confusing resistance addition in parallel vs series
- Not understanding power as energy per time

### Real-Life Applications
- Household wiring and electrical safety
- Power distribution systems
- Electronic devices and appliances
- Renewable energy systems (solar panels)

### Practice Problems

**Basic Level:**
1. Calculate current when 5V is applied across 10Ω resistor
2. Find total resistance of 3Ω and 6Ω in series
3. Calculate power dissipated in 4Ω resistor with 2A current

**Intermediate Level:**
4. Two 8Ω resistors in parallel, find equivalent resistance
5. 12V battery, 3Ω and 6Ω in series, find current and power
6. Household circuit: 240V, 100W bulb, calculate current

**Advanced Level:**
7. Complex circuit with series-parallel combinations
8. Calculate energy consumed by 2000W heater in 2 hours
9. Design circuit for specific power requirements

### WAEC Exam Preparation
- Circuit diagram interpretation
- Calculation problems with multiple steps
- Electrical safety and power consumption
- Real-world application problems

### Study Tips
- Build simple circuits with batteries and bulbs
- Use online circuit simulators
- Practice unit conversions (kW, kWh, etc.)
- Understand electrical safety rules

### Additional Resources
- PhET Interactive Simulations: Circuit Construction Kit
- YouTube: Physics Ninja (circuit analysis)
- Textbook: Senior Secondary Physics
- Multimeter for practical measurements
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Draw detailed circuit diagrams with color coding",
                    "Create flow charts for circuit analysis steps",
                    "Use circuit simulation software to visualize current flow",
                    "Watch animations of electron movement in circuits"
                ],
                "activities": [
                    "Design and draw complex circuit schematics",
                    "Create visual guides for series vs parallel circuits",
                    "Use diagramming tools to map electrical systems"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build physical circuits with wires, batteries, and components",
                    "Use hands-on circuit kits for experimentation",
                    "Create circuit models with clay or recycled materials",
                    "Conduct electrical safety demonstrations"
                ],
                "activities": [
                    "Assemble series and parallel circuit boards",
                    "Measure actual voltages and currents with multimeters",
                    "Build simple electrical devices (buzzers, switches)"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to explanations of circuit principles",
                    "Record and playback circuit analysis procedures",
                    "Participate in physics discussion groups",
                    "Use audio descriptions of electrical concepts"
                ],
                "activities": [
                    "Explain circuit concepts to peers verbally",
                    "Create audio recordings of problem solutions",
                    "Listen to physics podcasts and lectures"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed explanations of circuit laws",
                    "Create step-by-step problem-solving guides",
                    "Maintain a circuit analysis notebook",
                    "Read about electrical engineering applications"
                ],
                "activities": [
                    "Write circuit design specifications",
                    "Document experimental results and observations",
                    "Create study guides for electrical concepts"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Calculate I when V=12V, R=4Ω",
                "Find R_total for 2Ω + 3Ω in series",
                "Calculate P when V=6V, I=2A"
            ],
            "intermediate": [
                "Two 5Ω resistors in parallel, find R_eq",
                "12V battery, 4Ω and 8Ω in series, find I and P",
                "240V, 60W bulb, calculate resistance"
            ],
            "advanced": [
                "Complex circuit: series-parallel combinations",
                "Calculate cost of running 1500W heater for 3 hours",
                "Design lighting circuit for 5 rooms"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Ohm's law applications",
                "Series and parallel circuit calculations",
                "Power and energy problems",
                "Circuit diagram interpretation"
            ],
            "common_questions": [
                "Calculate equivalent resistance",
                "Find current, voltage, power in circuits",
                "Solve problems with multiple resistors",
                "Electrical energy and power calculations"
            ],
            "time_management": "Allocate 10-15 minutes per calculation problem",
            "scoring_tips": "Show all working steps, include correct units, round appropriately"
        },
        "career_connections": [
            "Electrical Engineering: Circuit design and analysis",
            "Power Systems: Grid distribution and transmission",
            "Electronics: Device development and testing",
            "Renewable Energy: Solar and wind power systems"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic electricity concepts, algebra, units"],
        "tags": ["electricity", "circuits", "ohms law", "power", "resistance", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(physics_content)

    # Chemistry SS2 - Organic Chemistry
    chemistry_content = {
        "id": f"nerdc-chemistry-ss2-organic-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Introduction to Organic Chemistry (SS2)",
        "subject": "Chemistry",
        "level": "SS2",
        "curriculum_framework": "NERDC Senior Secondary School Chemistry",
        "learning_objectives": [
            "Understand the unique properties of carbon compounds",
            "Classify organic compounds by functional groups",
            "Name and draw structural formulas of organic molecules",
            "Understand isomerism and its types"
        ],
        "content": """
## 🧪 Introduction to Organic Chemistry

### Core Concepts
Organic chemistry is the study of carbon-containing compounds.

**Unique Properties of Carbon:**
- Tetravalency (forms 4 bonds)
- Catenation (forms chains and rings)
- Isomerism (same formula, different structures)
- Multiple bond formation

**Functional Groups:** Specific atom groupings that determine compound properties

### Major Classes of Organic Compounds

**Alkanes (CₙH₂ₙ₊₂):**
- General formula: CₙH₂ₙ₊₂
- Saturated hydrocarbons
- Combustion: Complete and incomplete
- Substitution reactions

**Alkenes (CₙH₂ₙ):**
- General formula: CₙH₂ₙ
- Unsaturated hydrocarbons
- Addition reactions
- Geometric isomerism

**Alkynes (CₙH₂ₙ₋₂):**
- General formula: CₙH₂ₙ₋₂
- Triple bond between carbons
- Highly reactive

### Structural Isomerism
Compounds with same molecular formula but different structural arrangements.

**Example:** C₄H₁₀
- Butane: CH₃-CH₂-CH₂-CH₃
- 2-Methylpropane: CH₃-CH(CH₃)-CH₃

### Worked Examples

**Example 1: Naming Alkanes**
CH₃-CH₂-CH₂-CH₃ → Butane
CH₃-CH(CH₃)-CH₃ → 2-Methylpropane

**Example 2: Combustion**
C₃H₈ + 5O₂ → 3CO₂ + 4H₂O + heat

**Example 3: Addition Reaction**
CH₂=CH₂ + H₂ → CH₃-CH₃ (Nickel catalyst)

### Common Misconceptions
- All carbon compounds are organic
- Organic compounds are only from living things
- All hydrocarbons are alkanes
- Structural formulas show actual shape

### Real-Life Applications
- Petroleum products and fuels
- Plastics and polymers
- Pharmaceuticals and medicines
- Food additives and preservatives
- Clothing fibers and textiles

### Practice Problems

**Basic Level:**
1. Name CH₃-CH₂-CH₂-CH₃
2. Write structural formula of propane
3. Identify: alkane, alkene, or alkyne: C₂H₄

**Intermediate Level:**
4. Draw isomers of C₅H₁₂
5. Write combustion equation for C₄H₁₀
6. Explain why alkenes undergo addition reactions

**Advanced Level:**
7. Draw all isomers of C₆H₁₄
8. Calculate percentage composition of carbon in ethene
9. Explain catenation and its importance

### WAEC Exam Preparation
- Nomenclature of organic compounds
- Structural formulas and isomerism
- Chemical reactions and equations
- Properties and uses of organic compounds

### Study Tips
- Learn IUPAC naming rules systematically
- Practice drawing structural formulas
- Create flashcards for functional groups
- Understand reaction mechanisms

### Additional Resources
- Organic Chemistry Tutor YouTube channel
- MolView app for 3D molecular structures
- Textbook: Senior Secondary Chemistry
- Online molecular drawing tools
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Draw detailed structural formulas and diagrams",
                    "Create color-coded molecular models",
                    "Use molecular visualization software",
                    "Watch animations of organic reactions"
                ],
                "activities": [
                    "Build 3D models of organic molecules",
                    "Create visual guides for functional groups",
                    "Design molecular structure charts"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build molecular models with balls and sticks",
                    "Conduct simple organic chemistry experiments",
                    "Create physical representations of isomers",
                    "Use hands-on laboratory activities"
                ],
                "activities": [
                    "Assemble molecular model kits",
                    "Perform distillation or crystallization experiments",
                    "Create tactile models of carbon bonding"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to organic chemistry podcasts",
                    "Record explanations of naming rules",
                    "Participate in chemistry discussion groups",
                    "Use mnemonic devices for functional groups"
                ],
                "activities": [
                    "Teach organic concepts to classmates",
                    "Create audio guides for laboratory procedures",
                    "Listen to chemistry lectures and explanations"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed reaction mechanisms",
                    "Create study guides for organic families",
                    "Maintain a laboratory notebook",
                    "Read organic chemistry research articles"
                ],
                "activities": [
                    "Write systematic names for complex molecules",
                    "Document experimental procedures and results",
                    "Create comparison charts of organic compound classes"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Name CH₃-CH₂-CH₃",
                "Draw ethene structure",
                "Identify C₃H₆ as alkane/alkene/alkyne"
            ],
            "intermediate": [
                "Draw 3 isomers of C₄H₁₀",
                "Write complete combustion of C₂H₆",
                "Explain addition polymerization"
            ],
            "advanced": [
                "Draw all isomers of C₅H₁₂",
                "Calculate % carbon in benzene (C₆H₆)",
                "Explain resonance in organic compounds"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "IUPAC nomenclature",
                "Structural formulas and isomerism",
                "Organic reactions and mechanisms",
                "Properties and uses of organic compounds"
            ],
            "common_questions": [
                "Naming organic compounds",
                "Drawing structural formulas",
                "Writing chemical equations",
                "Explaining reaction types"
            ],
            "time_management": "Allocate 12-18 minutes per question, focus on accuracy",
            "scoring_tips": "Correct structural formulas essential, clear labeling required"
        },
        "career_connections": [
            "Pharmaceutical Chemistry: Drug development",
            "Petrochemical Engineering: Fuel production",
            "Polymer Science: Plastic manufacturing",
            "Forensic Chemistry: Compound identification"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic chemistry, bonding, chemical reactions"],
        "tags": ["organic chemistry", "hydrocarbons", "functional groups", "isomerism", "nomenclature", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(chemistry_content)

    # Biology SS2 - Reproduction
    biology_content = {
        "id": f"nerdc-biology-ss2-reproduction-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Reproduction in Living Organisms (SS2)",
        "subject": "Biology",
        "level": "SS2",
        "curriculum_framework": "NERDC Senior Secondary School Biology",
        "learning_objectives": [
            "Distinguish between sexual and asexual reproduction",
            "Understand human reproductive systems",
            "Explain gametogenesis and fertilization",
            "Understand reproductive health and contraception"
        ],
        "content": """
## 🧬 Reproduction in Living Organisms

### Core Concepts
Reproduction is the biological process by which new individuals are produced.

**Types of Reproduction:**
- **Asexual**: Single parent, offspring genetically identical
- **Sexual**: Two parents, offspring genetically diverse

### Asexual Reproduction Methods
- **Binary Fission**: Bacteria, amoeba
- **Budding**: Yeast, hydra
- **Vegetative Propagation**: Plants (cuttings, tubers)
- **Spore Formation**: Fungi, ferns
- **Regeneration**: Planaria, starfish

### Sexual Reproduction in Plants
- **Flowers**: Reproductive structures
- **Pollination**: Transfer of pollen grains
- **Fertilization**: Fusion of gametes
- **Seed Formation**: Zygote develops into embryo

### Human Reproductive System

**Male Reproductive System:**
- Testes: Produce sperm and testosterone
- Epididymis: Sperm maturation
- Vas deferens: Sperm transport
- Seminal vesicles and prostate: Semen production
- Penis: Copulatory organ

**Female Reproductive System:**
- Ovaries: Produce ova and hormones
- Fallopian tubes: Site of fertilization
- Uterus: Implantation and development
- Cervix: Uterus opening
- Vagina: Birth canal and copulation

### Gametogenesis
- **Spermatogenesis**: Sperm production in testes
- **Oogenesis**: Egg production in ovaries
- **Meiosis**: Reduction division producing gametes

### Menstrual Cycle
- **Follicular Phase**: Follicle development
- **Ovulation**: Egg release (Day 14)
- **Luteal Phase**: Corpus luteum formation
- **Menstruation**: Shedding of uterine lining

### Fertilization and Development
- **Fertilization**: Sperm + egg = zygote
- **Cleavage**: Rapid cell division
- **Implantation**: Embryo attaches to uterus
- **Placenta**: Nutrient exchange organ

### Reproductive Health
- **Contraception**: Birth control methods
- **STDs**: Sexually transmitted diseases
- **Infertility**: Causes and treatments
- **Prenatal Care**: Healthy pregnancy

### Worked Examples

**Example 1: Punnett Square**
Parents: Tt × Tt (tongue rolling)
Offspring: TT, Tt, Tt, tt (3:1 ratio)

**Example 2: Menstrual Cycle**
Day 1-5: Menstruation
Day 14: Ovulation
Day 15-28: Luteal phase

### Common Misconceptions
- Asexual reproduction produces identical offspring only
- Fertilization occurs in the uterus
- Menstruation means pregnancy loss
- All contraceptives prevent STDs

### Real-Life Applications
- Agriculture: Plant propagation techniques
- Medicine: Assisted reproduction technologies
- Conservation: Endangered species breeding programs
- Family planning and population control

### Practice Problems

**Basic Level:**
1. Distinguish between asexual and sexual reproduction
2. Label male reproductive organs
3. Explain pollination and fertilization

**Intermediate Level:**
4. Describe the menstrual cycle phases
5. Explain gametogenesis process
6. Compare vegetative propagation methods

**Advanced Level:**
7. Discuss advantages of sexual reproduction
8. Explain hormonal control of reproduction
9. Analyze population growth patterns

### WAEC Exam Preparation
- Reproductive system diagrams and labeling
- Processes of gametogenesis and fertilization
- Reproductive health and contraception
- Plant and animal reproduction comparison

### Study Tips
- Create labeled diagrams of reproductive systems
- Use mnemonic devices for remembering structures
- Practice Punnett square problems regularly
- Understand hormonal relationships

### Additional Resources
- Khan Academy: Human Reproduction
- Visible Body app for 3D anatomy
- Textbook: Senior Secondary Biology
- Educational videos on reproductive health
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Draw detailed diagrams of reproductive systems",
                    "Create flow charts of reproductive processes",
                    "Use color-coded anatomical models",
                    "Watch animations of fertilization and development"
                ],
                "activities": [
                    "Label and color reproductive system diagrams",
                    "Create visual timelines of menstrual cycle",
                    "Design infographics about reproductive health"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build 3D models of reproductive organs",
                    "Conduct plant propagation experiments",
                    "Create physical representations of cell division",
                    "Use role-playing for reproductive processes"
                ],
                "activities": [
                    "Assemble anatomical model kits",
                    "Grow plants from cuttings or tubers",
                    "Demonstrate mitosis/meiosis with objects"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to reproductive biology podcasts",
                    "Record explanations of complex processes",
                    "Participate in biology discussion groups",
                    "Use audio descriptions of anatomical structures"
                ],
                "activities": [
                    "Teach reproductive concepts to peers",
                    "Create audio guides for laboratory dissections",
                    "Listen to expert lectures on reproductive health"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed process descriptions",
                    "Create study guides for reproductive systems",
                    "Maintain a reproductive health journal",
                    "Read scientific articles on reproduction"
                ],
                "activities": [
                    "Write research papers on reproductive technologies",
                    "Document experimental observations",
                    "Create comparison charts of reproduction methods"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "List 3 methods of asexual reproduction",
                "Name male reproductive organs",
                "Explain pollination process"
            ],
            "intermediate": [
                "Describe menstrual cycle phases",
                "Explain spermatogenesis",
                "Compare sexual vs asexual reproduction"
            ],
            "advanced": [
                "Analyze genetic variation in offspring",
                "Explain hormonal control mechanisms",
                "Discuss reproductive health issues"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Reproductive system anatomy",
                "Gametogenesis and fertilization",
                "Plant reproduction processes",
                "Reproductive health and contraception"
            ],
            "common_questions": [
                "Labeling reproductive system diagrams",
                "Explaining reproductive processes",
                "Comparing reproduction methods",
                "Reproductive health problems"
            ],
            "time_management": "Allocate 15-20 minutes per essay question",
            "scoring_tips": "Accurate labeling essential, clear explanations required"
        },
        "career_connections": [
            "Medicine: Obstetrics and gynecology",
            "Agriculture: Plant breeding and propagation",
            "Veterinary Science: Animal reproduction",
            "Public Health: Family planning programs"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic biology, cell division, plant/animal systems"],
        "tags": ["reproduction", "gametogenesis", "fertilization", "reproductive health", "menstrual cycle", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(biology_content)

    # English SS2 - Literature
    english_content = {
        "id": f"nerdc-english-ss2-literature-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Introduction to Literature (SS2)",
        "subject": "English Language",
        "level": "SS2",
        "curriculum_framework": "NERDC Senior Secondary School English",
        "learning_objectives": [
            "Identify and analyze different literary genres",
            "Understand literary devices and their effects",
            "Appreciate African literature and writers",
            "Develop critical thinking through literary analysis"
        ],
        "content": """
## 📚 Introduction to Literature

### Core Concepts
Literature is the art of written works that express human experience and imagination.

**Major Genres:**
- **Prose**: Novels, short stories, essays
- **Poetry**: Verses expressing emotions and ideas
- **Drama**: Plays performed on stage

### Literary Devices and Techniques

**Figures of Speech:**
- **Simile**: Comparison using 'like' or 'as'
- **Metaphor**: Direct comparison without 'like' or 'as'
- **Personification**: Giving human qualities to non-human things
- **Hyperbole**: Deliberate exaggeration
- **Irony**: Contrast between expectation and reality

**Poetic Devices:**
- **Alliteration**: Repetition of initial consonant sounds
- **Assonance**: Repetition of vowel sounds
- **Onomatopoeia**: Words imitating sounds
- **Rhyme**: Similar sounding words
- **Rhythm**: Pattern of stressed/unstressed syllables

### Prose Analysis
- **Theme**: Central message or idea
- **Plot**: Sequence of events
- **Character**: People in the story
- **Setting**: Time and place of action
- **Point of View**: Perspective of narrator

### Poetry Appreciation
- **Structure**: Stanzas, lines, rhyme scheme
- **Imagery**: Vivid descriptions appealing to senses
- **Mood**: Emotional atmosphere
- **Tone**: Author's attitude toward subject

### African Literature
- **Chinua Achebe**: Things Fall Apart, Arrow of God
- **Wole Soyinka**: The Lion and the Jewel, Kongi's Harvest
- **Chimamanda Ngozi Adichie**: Americanah, Half of a Yellow Sun
- **Ngũgĩ wa Thiong'o**: The River Between, Weep Not Child

### Worked Examples

**Example 1: Simile and Metaphor**
Simile: "Life is like a box of chocolates"
Metaphor: "Time is a thief"

**Example 2: Poem Analysis**
"She walks in beauty, like the night" (Lord Byron)
- Imagery: Visual beauty
- Simile: Comparison with night
- Theme: Feminine beauty

**Example 3: Prose Analysis**
"Things Fall Apart" by Chinua Achebe
- Theme: Clash of cultures
- Setting: Nigerian village, colonial era
- Protagonist: Okonkwo

### Common Misconceptions
- Literature is only for entertainment
- Poetry must always rhyme
- African literature is inferior
- Literary devices are decorative only

### Real-Life Applications
- Critical thinking development
- Cultural understanding and empathy
- Communication skills enhancement
- Emotional intelligence growth
- Historical and social awareness

### Practice Problems

**Basic Level:**
1. Identify simile: "As brave as a lion"
2. Explain metaphor in "Time is money"
3. Name 3 African writers and their works

**Intermediate Level:**
4. Analyze theme in a short poem
5. Compare characters in a story
6. Explain irony in a given situation

**Advanced Level:**
7. Write critical analysis of a poem
8. Discuss cultural themes in African literature
9. Compare literary devices across genres

### WAEC Exam Preparation
- Literary terms and definitions
- Poetry analysis and appreciation
- Prose comprehension and analysis
- African literature questions
- Essay writing on literary themes

### Study Tips
- Read widely across genres
- Keep a vocabulary journal
- Practice writing literary analyses
- Join literature discussion groups
- Memorize key literary terms

### Additional Resources
- British Council: Literature resources
- African Writers Trust online library
- Poetry Foundation website
- Textbook: New Concept English Literature
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Create mind maps of literary works",
                    "Draw storyboards for plot analysis",
                    "Use color coding for literary devices",
                    "Watch film adaptations of literary works"
                ],
                "activities": [
                    "Design book covers for studied texts",
                    "Create visual timelines of literary periods",
                    "Make character relationship diagrams"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Act out scenes from plays",
                    "Create physical representations of poems",
                    "Use movement to express literary themes",
                    "Build models representing story structures"
                ],
                "activities": [
                    "Perform dramatic readings",
                    "Create dance interpretations of poems",
                    "Build dioramas of story settings"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to audiobook versions of texts",
                    "Record poetry recitations",
                    "Participate in literature discussion podcasts",
                    "Use rhythm and intonation in readings"
                ],
                "activities": [
                    "Create audio recordings of analyses",
                    "Listen to literary criticism podcasts",
                    "Perform oral interpretations of poems"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed book reviews",
                    "Create character analysis essays",
                    "Maintain a reading journal",
                    "Write poetry and short stories"
                ],
                "activities": [
                    "Compose literary analyses",
                    "Write creative responses to texts",
                    "Create study guides for literary works"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Identify 5 figures of speech",
                "Name 3 African literary works",
                "Explain difference between prose and poetry"
            ],
            "intermediate": [
                "Analyze theme in a short story",
                "Compare two poems by same author",
                "Explain character development"
            ],
            "advanced": [
                "Write critical essay on cultural themes",
                "Compare literary devices in two genres",
                "Analyze author's use of symbolism"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Literary terms and devices",
                "Poetry analysis and appreciation",
                "Prose comprehension",
                "African literature questions"
            ],
            "common_questions": [
                "Explain literary devices",
                "Analyze poems and passages",
                "Discuss themes and characters",
                "Compare literary works"
            ],
            "time_management": "Allocate 20-25 minutes per essay question",
            "scoring_tips": "Clear structure, textual evidence, personal response"
        },
        "career_connections": [
            "Writing and Journalism: Content creation",
            "Education: Literature teaching",
            "Publishing: Editorial and content development",
            "Media: Script writing and criticism"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic English grammar, reading comprehension"],
        "tags": ["literature", "poetry", "prose", "drama", "literary devices", "African literature", "WAEC"],
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
        # Load existing content
        with open('content_data.json', 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"content": []}

    # Add new content
    data["content"].extend(content_items)

    # Save updated content
    with open('content_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully saved {len(content_items)} comprehensive SS2 NERDC content items")
    return True

def main():
    """
    Main function to generate and save SS2 NERDC content.
    """
    print("🚀 Generating Comprehensive SS2 NERDC Curriculum Content with Learning Options...")

    # Generate content
    content_items = generate_ss2_comprehensive_nerdc_content()

    # Display generation statistics
    subjects = {}
    for item in content_items:
        subj = item.get('subject', 'Unknown')
        subjects[subj] = subjects.get(subj, 0) + 1

    print(f"\n✅ Generated {len(content_items)} comprehensive SS2 content items")
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

    print("\n📚 SS2 Topics Covered:")
    print("  • Mathematics: Quadratic Equations and Applications")
    print("  • Physics: Electricity and Electrical Circuits")
    print("  • Chemistry: Introduction to Organic Chemistry")
    print("  • Biology: Reproduction in Living Organisms")
    print("  • English: Introduction to Literature")

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