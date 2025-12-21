#!/usr/bin/env python3
"""
Additional Subjects NERDC Content Generator
Generates comprehensive educational content for additional subjects
across all levels (SS1-SS3) with learning options and NERDC curriculum alignment.
"""

import json
import datetime
import uuid

def generate_additional_subjects_content():
    """
    Generate comprehensive NERDC-aligned content for additional subjects.
    Includes learning options, practice problems, and exam preparation.
    """

    content_items = []

    # Further Mathematics SS1 - Sets and Logic
    further_math_ss1 = {
        "id": f"nerdc-further-math-ss1-sets-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Sets, Logic and Proof (Further Mathematics SS1)",
        "subject": "Further Mathematics",
        "level": "SS1",
        "curriculum_framework": "NERDC Senior Secondary School Further Mathematics",
        "learning_objectives": [
            "Understand set theory and operations",
            "Apply logical reasoning and proof techniques",
            "Solve problems using Venn diagrams",
            "Understand basic mathematical logic"
        ],
        "content": """
## 🔢 Sets, Logic and Proof

### Core Concepts
Further Mathematics builds advanced mathematical thinking and problem-solving skills.

**Set Theory:**
- **Set**: Collection of distinct objects
- **Elements**: Members of a set
- **Universal Set**: Set containing all possible elements
- **Empty Set**: Set with no elements (∅)

**Set Operations:**
- **Union**: A ∪ B = {x | x ∈ A or x ∈ B}
- **Intersection**: A ∩ B = {x | x ∈ A and x ∈ B}
- **Complement**: A' = {x ∈ U | x ∉ A}
- **Difference**: A - B = {x ∈ A | x ∉ B}

**Logic:**
- **Proposition**: Statement that is true or false
- **Truth Tables**: Systematic way to determine validity
- **Logical Connectives**: ∧ (and), ∨ (or), ¬ (not), → (implies)
- **Tautology**: Always true statement

### Worked Examples

**Example 1: Set Operations**
If A = {1, 2, 3, 4} and B = {3, 4, 5, 6}
A ∪ B = {1, 2, 3, 4, 5, 6}
A ∩ B = {3, 4}
A' = {5, 6} (if U = {1, 2, 3, 4, 5, 6})

**Example 2: Truth Table**
Construct truth table for (P ∧ Q) → R

**Example 3: Proof by Contradiction**
Prove √2 is irrational by contradiction.

### Common Misconceptions
- Sets can contain duplicate elements
- Empty set is the same as zero
- All mathematical statements are provable
- Logic is only for computers

### Real-Life Applications
- Computer science and programming
- Database design and queries
- Decision making in business
- Cryptography and security
- Artificial intelligence reasoning

### Practice Problems

**Basic Level:**
1. List elements of set A = {x | x is even, 1 ≤ x ≤ 10}
2. Find A ∪ B and A ∩ B for given sets
3. Draw Venn diagram for three sets

**Intermediate Level:**
4. Prove set identity: A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)
5. Construct truth table for ¬(P ∨ Q) ↔ (¬P ∧ ¬Q)
6. Solve problem using inclusion-exclusion principle

**Advanced Level:**
7. Prove mathematical induction for sum formula
8. Analyze logical argument validity
9. Apply set theory to real-world problem

### WAEC Exam Preparation
- Set theory operations and Venn diagrams
- Basic logical reasoning
- Simple proof techniques
- Problem-solving applications

### Study Tips
- Practice with real objects to understand sets
- Create truth tables systematically
- Learn proof techniques step-by-step
- Apply concepts to programming logic

### Additional Resources
- Discrete Mathematics textbooks
- Khan Academy: Sets and Logic
- YouTube: Professor Leonard (Logic)
- Online set theory visualizers
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Draw detailed Venn diagrams for set operations",
                    "Create visual truth tables and logic circuits",
                    "Use color coding for different set operations",
                    "Watch animations of logical proofs"
                ],
                "activities": [
                    "Design visual representations of set relationships",
                    "Create flow charts for logical reasoning",
                    "Make diagrams showing proof structures"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Use physical objects to demonstrate set operations",
                    "Build logic gates with physical components",
                    "Create tangible models of mathematical proofs",
                    "Use manipulatives for set theory concepts"
                ],
                "activities": [
                    "Use cards or tokens to represent set elements",
                    "Build physical Venn diagrams with hoops",
                    "Construct logic circuit models"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to logic and set theory podcasts",
                    "Record yourself explaining proofs",
                    "Participate in mathematics discussion groups",
                    "Use rhythmic patterns for logical operations"
                ],
                "activities": [
                    "Create audio explanations of set operations",
                    "Listen to mathematical reasoning lectures",
                    "Record step-by-step problem solutions"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed proof explanations",
                    "Create study guides for logical operators",
                    "Maintain a mathematical reasoning journal",
                    "Read mathematical logic papers"
                ],
                "activities": [
                    "Write formal mathematical proofs",
                    "Document solution strategies",
                    "Create comparison charts of logical connectives"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "A = {1,3,5}, B = {2,3,4}, find A ∪ B, A ∩ B",
                "Draw Venn diagram for A ∩ B = ∅",
                "List subsets of {1, 2}"
            ],
            "intermediate": [
                "Prove De Morgan's law: (A ∪ B)' = A' ∩ B'",
                "Construct truth table for P → (Q ∧ R)",
                "Solve inclusion-exclusion problem"
            ],
            "advanced": [
                "Prove by mathematical induction: 1+2+...+n = n(n+1)/2",
                "Analyze validity of logical argument",
                "Apply set theory to combinatorics problem"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Set operations and Venn diagrams",
                "Basic logical reasoning",
                "Simple proof techniques",
                "Problem-solving applications"
            ],
            "common_questions": [
                "Perform set operations",
                "Construct and interpret Venn diagrams",
                "Apply basic logic principles",
                "Solve problems using set theory"
            ],
            "time_management": "Allocate 15-20 minutes per problem",
            "scoring_tips": "Show all working clearly, use correct notation"
        },
        "career_connections": [
            "Computer Science: Algorithm design and analysis",
            "Engineering: Systems analysis and optimization",
            "Finance: Risk assessment and decision making",
            "Research: Statistical analysis and modeling"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic mathematics, logical thinking"],
        "tags": ["further mathematics", "sets", "logic", "proof", "discrete math", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(further_math_ss1)

    # Geography SS1 - Introduction to Geography
    geography_ss1 = {
        "id": f"nerdc-geography-ss1-intro-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Introduction to Geography and Map Reading (SS1)",
        "subject": "Geography",
        "level": "SS1",
        "curriculum_framework": "NERDC Senior Secondary School Geography",
        "learning_objectives": [
            "Understand the scope and importance of geography",
            "Read and interpret different types of maps",
            "Understand map projections and scales",
            "Identify major geographical features"
        ],
        "content": """
## 🌍 Introduction to Geography and Map Reading

### Core Concepts
Geography is the study of Earth's physical features, climate, and human activities.

**Branches of Geography:**
- **Physical Geography**: Landforms, climate, vegetation, soils
- **Human Geography**: Population, settlement, economic activities
- **Environmental Geography**: Human-environment interactions
- **Cartography**: Map making and interpretation

**Map Essentials:**
- **Scale**: Ratio between map distance and actual distance
- **Projection**: Method of representing Earth's curved surface on flat map
- **Legend**: Explains symbols used on map
- **Grid Reference**: System for locating positions

**Types of Maps:**
- **Topographic Maps**: Show physical features and elevation
- **Political Maps**: Show boundaries and cities
- **Thematic Maps**: Show specific data (population, climate)
- **Aerial Photographs**: Bird's eye view images

### Worked Examples

**Example 1: Scale Calculation**
Map scale: 1:50,000
Distance on map: 5cm
Actual distance = 5cm × 50,000 = 250,000cm = 2.5km

**Example 2: Grid Reference**
On a map with 100m grid squares:
Point at intersection of grid lines 35 and 42 = 3542
More precise: 354275 (35 easting, 42 northing, 75m east, 75m north)

**Example 3: Map Reading**
Identify: Rivers, mountains, roads, settlements, vegetation

### Common Misconceptions
- Geography is only about memorizing capitals
- All maps are accurate representations
- Physical geography doesn't affect human life
- Maps are outdated in digital age

### Real-Life Applications
- Urban planning and development
- Environmental conservation
- Disaster management and emergency response
- Transportation and logistics
- Climate change adaptation
- International relations and geopolitics

### Practice Problems

**Basic Level:**
1. Convert map scale 1:25,000 to statement form
2. Identify major physical features on a map
3. Locate Nigeria on world map

**Intermediate Level:**
4. Calculate actual distance from map measurement
5. Give 6-figure grid reference for a point
6. Compare different map projections

**Advanced Level:**
7. Interpret topographic map for land use planning
8. Analyze thematic map data patterns
9. Evaluate map accuracy and reliability

### WAEC Exam Preparation
- Map reading and interpretation
- Geographical concepts and definitions
- Basic map calculations
- Identification of geographical features

### Study Tips
- Practice with real maps and atlases
- Learn map symbols and conventions
- Study current geographical events
- Use online mapping tools

### Additional Resources
- National Geographic maps
- Google Earth for 3D visualization
- Geography textbooks and atlases
- Online GIS and mapping tools
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Study detailed maps and globes",
                    "Create visual diagrams of geographical concepts",
                    "Use color coding for different map features",
                    "Watch geographical documentaries"
                ],
                "activities": [
                    "Draw and label geographical features",
                    "Create visual timelines of geographical events",
                    "Design thematic maps for data presentation"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build physical models of landforms",
                    "Use globes and maps for hands-on exploration",
                    "Create geographical games and puzzles",
                    "Conduct field observations and measurements"
                ],
                "activities": [
                    "Build 3D models of mountains and valleys",
                    "Use physical maps for navigation exercises",
                    "Create geographical scavenger hunts"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to geography podcasts and lectures",
                    "Record explanations of geographical processes",
                    "Participate in geography discussion groups",
                    "Use audio descriptions of maps"
                ],
                "activities": [
                    "Create audio guides for map reading",
                    "Listen to geographical case studies",
                    "Record oral presentations on geographical topics"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed geographical descriptions",
                    "Create study guides for map reading",
                    "Maintain a geography observation journal",
                    "Read geographical research and reports"
                ],
                "activities": [
                    "Write geographical reports and analyses",
                    "Document field observations",
                    "Create comparison charts of geographical features"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Convert 1:100,000 scale to statement",
                "Identify 5 physical features on Nigeria map",
                "List 4 types of maps"
            ],
            "intermediate": [
                "Calculate distance: 3cm on 1:50,000 map",
                "Give 4-figure grid reference",
                "Compare Mercator vs Peters projection"
            ],
            "advanced": [
                "Interpret contour lines on topographic map",
                "Analyze population density patterns",
                "Evaluate environmental impact assessment"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Map reading and interpretation",
                "Geographical concepts and definitions",
                "Basic map calculations and scales",
                "Identification of geographical features"
            ],
            "common_questions": [
                "Interpret maps and diagrams",
                "Calculate distances and areas",
                "Identify and describe geographical features",
                "Explain geographical processes"
            ],
            "time_management": "Allocate 15-20 minutes per map question",
            "scoring_tips": "Label diagrams clearly, use geographical terminology"
        },
        "career_connections": [
            "Urban Planning: City development and infrastructure",
            "Environmental Science: Conservation and management",
            "GIS Specialist: Geographic information systems",
            "International Development: Aid and development work"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic map skills, general knowledge"],
        "tags": ["geography", "maps", "cartography", "physical features", "map reading", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(geography_ss1)

    # Economics SS1 - Basic Economic Concepts
    economics_ss1 = {
        "id": f"nerdc-economics-ss1-basic-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Basic Economic Concepts and Principles (SS1)",
        "subject": "Economics",
        "level": "SS1",
        "curriculum_framework": "NERDC Senior Secondary School Economics",
        "learning_objectives": [
            "Understand basic economic concepts and terminology",
            "Explain the concept of scarcity and choice",
            "Distinguish between needs and wants",
            "Understand production and consumption"
        ],
        "content": """
## 💰 Basic Economic Concepts and Principles

### Core Concepts
Economics is the study of how individuals and societies allocate scarce resources.

**Fundamental Concepts:**
- **Scarcity**: Limited resources, unlimited wants
- **Choice**: Decision-making due to scarcity
- **Opportunity Cost**: Value of next best alternative forgone
- **Scale of Preference**: Ranking of wants by importance

**Needs vs Wants:**
- **Needs**: Essential for survival (food, shelter, clothing)
- **Wants**: Desirable but not essential items
- **Goods**: Physical items (cars, phones, books)
- **Services**: Non-physical benefits (haircut, teaching)

**Production and Consumption:**
- **Production**: Creation of goods and services
- **Consumption**: Using goods and services to satisfy wants
- **Factors of Production**: Land, Labor, Capital, Entrepreneurship
- **Division of Labor**: Specialization in production

### Worked Examples

**Example 1: Opportunity Cost**
A student has ₦500 and must choose between:
- Movie ticket: ₦300
- Textbook: ₦250
If chooses movie, opportunity cost is textbook (₦250)
If chooses textbook, opportunity cost is movie (₦300)

**Example 2: Scale of Preference**
Student's wants ranked by priority:
1. Food and water (most important)
2. Clothing and shelter
3. Education and healthcare
4. Entertainment and luxury items

**Example 3: Production Possibility Curve**
With limited resources, a farmer can produce:
- 10 bags rice OR 20 bags maize
- 5 bags rice AND 10 bags maize
- Shows trade-offs and efficiency

### Common Misconceptions
- Economics is only about money
- Rich people don't face scarcity
- Government can solve all economic problems
- Economic growth benefits everyone equally

### Real-Life Applications
- Personal financial planning and budgeting
- Business decision-making and resource allocation
- Government policy and economic planning
- International trade and globalization
- Environmental resource management
- Career planning and salary negotiations

### Practice Problems

**Basic Level:**
1. Distinguish between needs and wants with examples
2. Explain why scarcity forces choice
3. List 4 factors of production

**Intermediate Level:**
4. Calculate opportunity cost in a budget decision
5. Construct a simple scale of preference
6. Explain division of labor in a factory

**Advanced Level:**
7. Analyze production possibility curve shifts
8. Evaluate economic impact of government policies
9. Apply economic principles to real-world problems

### WAEC Exam Preparation
- Basic economic concepts and definitions
- Scarcity, choice, and opportunity cost
- Needs vs wants, goods vs services
- Factors of production

### Study Tips
- Relate concepts to daily life experiences
- Create personal budget examples
- Study current economic news
- Practice with real-world scenarios

### Additional Resources
- Economics textbooks for secondary schools
- BBC Economics resources
- Khan Academy: Microeconomics
- Financial planning websites
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Create diagrams of economic concepts",
                    "Draw production possibility curves",
                    "Use charts for economic data visualization",
                    "Watch economic documentaries"
                ],
                "activities": [
                    "Design visual aids for economic principles",
                    "Create economic concept maps",
                    "Make infographics about economic systems"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Use physical objects for economic simulations",
                    "Create role-playing scenarios for economic decisions",
                    "Build models of economic systems",
                    "Conduct economic experiments with play money"
                ],
                "activities": [
                    "Simulate market transactions with tokens",
                    "Create physical production possibility models",
                    "Build economic decision-making games"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to economics podcasts and lectures",
                    "Record explanations of economic concepts",
                    "Participate in economics discussion groups",
                    "Use audio for vocabulary building"
                ],
                "activities": [
                    "Create audio explanations of economic theories",
                    "Listen to economic news analysis",
                    "Record oral presentations on economic topics"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed economic analyses",
                    "Create study guides for economic terms",
                    "Maintain an economic observation journal",
                    "Read economic news and reports"
                ],
                "activities": [
                    "Write economic opinion pieces",
                    "Document personal financial decisions",
                    "Create comparison charts of economic systems"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Give 3 examples each of needs and wants",
                "Explain scarcity with personal example",
                "List factors of production with examples"
            ],
            "intermediate": [
                "Calculate opportunity cost: ₦1000 for phone vs laptop",
                "Rank wants in order of preference",
                "Explain specialization benefits"
            ],
            "advanced": [
                "Analyze economic impact of price increase",
                "Evaluate government intervention in markets",
                "Apply economic principles to environmental issues"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Basic economic concepts and definitions",
                "Scarcity, choice, and opportunity cost",
                "Needs vs wants, goods vs services",
                "Factors of production and division of labor"
            ],
            "common_questions": [
                "Define and explain economic concepts",
                "Distinguish between economic terms",
                "Give examples of economic principles",
                "Explain economic relationships"
            ],
            "time_management": "Allocate 10-15 minutes per definition question",
            "scoring_tips": "Use economic terminology correctly, give relevant examples"
        },
        "career_connections": [
            "Business Administration: Management and finance",
            "Banking and Finance: Investment and loans",
            "Government: Policy making and economic planning",
            "Entrepreneurship: Business planning and management"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic mathematics, general knowledge"],
        "tags": ["economics", "scarcity", "choice", "opportunity cost", "production", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(economics_ss1)

    # Computer Science SS1 - Introduction to Computing
    computer_science_ss1 = {
        "id": f"nerdc-computer-ss1-intro-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Introduction to Computing and Basic Programming (SS1)",
        "subject": "Computer Science",
        "level": "SS1",
        "curriculum_framework": "NERDC Senior Secondary School Computer Science",
        "learning_objectives": [
            "Understand computer systems and components",
            "Learn basic programming concepts",
            "Understand data representation in computers",
            "Develop algorithmic thinking"
        ],
        "content": """
## 💻 Introduction to Computing and Basic Programming

### Core Concepts
Computer Science is the study of computers, computational systems, and computation itself.

**Computer Systems:**
- **Hardware**: Physical components (CPU, memory, storage, input/output)
- **Software**: Programs and operating systems
- **Data**: Information processed by computers
- **Users**: People who interact with computer systems

**Programming Fundamentals:**
- **Algorithm**: Step-by-step procedure to solve a problem
- **Program**: Set of instructions written in programming language
- **Variables**: Named storage locations for data
- **Data Types**: Different kinds of data (numbers, text, boolean)

**Basic Programming Concepts:**
- **Input**: Getting data into the program
- **Processing**: Manipulating data according to instructions
- **Output**: Displaying results
- **Control Structures**: Sequence, selection, iteration

### Worked Examples

**Example 1: Algorithm Development**
Problem: Calculate average of three numbers
Algorithm:
1. Get three numbers from user
2. Add the numbers together
3. Divide sum by 3
4. Display the result

**Example 2: Pseudocode**
BEGIN
    INPUT num1, num2, num3
    sum = num1 + num2 + num3
    average = sum / 3
    OUTPUT average
END

**Example 3: Flowchart Symbols**
- Rectangle: Process/operation
- Diamond: Decision point
- Arrow: Flow direction
- Oval: Start/End

### Common Misconceptions
- Programming is only for math experts
- Computers think like humans
- All software is the same
- Coding is just typing fast

### Real-Life Applications
- Mobile app development
- Website creation and management
- Data analysis and visualization
- Automation and robotics
- Artificial intelligence and machine learning
- Cybersecurity and network management

### Practice Problems

**Basic Level:**
1. Identify computer hardware components
2. Explain difference between RAM and ROM
3. Draw flowchart for simple daily activity

**Intermediate Level:**
4. Write algorithm to find largest of three numbers
5. Create pseudocode for temperature conversion
6. Explain binary number system

**Advanced Level:**
7. Design program to calculate compound interest
8. Create flowchart for grading system
9. Debug simple programming errors

### WAEC Exam Preparation
- Computer system components and functions
- Basic programming concepts
- Algorithm development and flowcharts
- Data representation (binary, decimal)

### Study Tips
- Practice coding regularly on simple problems
- Learn one programming language well
- Understand concepts before syntax
- Work on real projects

### Additional Resources
- Scratch programming for beginners
- Codecademy interactive tutorials
- Khan Academy: Computer Science
- FreeCodeCamp online courses
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Create flowcharts and diagrams for algorithms",
                    "Use color coding for different programming elements",
                    "Watch coding tutorial videos",
                    "Design user interface mockups"
                ],
                "activities": [
                    "Draw detailed flowcharts for processes",
                    "Create visual programming concept maps",
                    "Design algorithm visualization diagrams"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build simple circuits and electronic projects",
                    "Use physical programming kits (Arduino, Raspberry Pi)",
                    "Create tangible algorithms with cards or objects",
                    "Build computer hardware models"
                ],
                "activities": [
                    "Assemble computer hardware components",
                    "Create physical flowcharts with sticky notes",
                    "Build simple robots or automated systems"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to programming podcasts and lectures",
                    "Record yourself explaining code",
                    "Participate in coding discussion groups",
                    "Use audio for learning programming syntax"
                ],
                "activities": [
                    "Create audio explanations of programming concepts",
                    "Listen to coding interviews and discussions",
                    "Record debugging sessions"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed code documentation",
                    "Create study guides for programming concepts",
                    "Maintain a coding journal",
                    "Read programming blogs and tutorials"
                ],
                "activities": [
                    "Write pseudocode for complex problems",
                    "Document project development processes",
                    "Create comparison charts of programming languages"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Label 5 computer hardware components",
                "Convert decimal 25 to binary",
                "Draw flowchart for making tea"
            ],
            "intermediate": [
                "Write algorithm to check if number is even",
                "Create pseudocode for area calculation",
                "Explain difference between RAM and hard disk"
            ],
            "advanced": [
                "Design program for student grading system",
                "Create flowchart for ATM transaction",
                "Debug logical errors in sample code"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Computer system components and functions",
                "Basic programming concepts and algorithms",
                "Data representation and number systems",
                "Flowchart design and interpretation"
            ],
            "common_questions": [
                "Identify and explain computer components",
                "Design algorithms and flowcharts",
                "Convert between number systems",
                "Explain programming concepts"
            ],
            "time_management": "Allocate 12-18 minutes per programming question",
            "scoring_tips": "Use correct technical terminology, show clear logic"
        },
        "career_connections": [
            "Software Development: Programming and app creation",
            "Data Science: Analysis and machine learning",
            "Cybersecurity: System protection and ethical hacking",
            "IT Support: Technical troubleshooting and maintenance"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic computer usage, logical thinking"],
        "tags": ["computer science", "programming", "algorithms", "hardware", "software", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(computer_science_ss1)

    return content_items

def save_to_content_service(content_items):
    """
    Save the generated content to the content service database.
    """
    try:
        # Use absolute path to root content_data.json
        content_file_path = 'content_data.json'
        with open(content_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"content": []}

    # Add new content
    data["content"].extend(content_items)

    # Save updated content
    with open(content_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully saved {len(content_items)} additional subjects content items")
    return True

def main():
    """
    Main function to generate and save additional subjects content.
    """
    print("🚀 Generating Additional Subjects NERDC Curriculum Content...")

    # Generate content
    content_items = generate_additional_subjects_content()

    # Display generation statistics
    subjects = {}
    for item in content_items:
        subj = item.get('subject', 'Unknown')
        subjects[subj] = subjects.get(subj, 0) + 1

    print(f"\n✅ Generated {len(content_items)} additional subjects content items")
    print("\n📚 Content Breakdown:")
    for subj, count in subjects.items():
        print(f"  {subj}: {count} items")

    # Save to database
    save_to_content_service(content_items)

    print("\n📊 Content Features:")
    print("  ✓ NERDC Senior Secondary School Curriculum Alignment")
    print("  ✓ Comprehensive Subject Coverage (Further Mathematics, Geography, Economics, Computer Science)")
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

    print("\n📚 Additional Subjects Covered:")
    print("  • Further Mathematics: Sets, Logic and Proof")
    print("  • Geography: Introduction to Geography and Map Reading")
    print("  • Economics: Basic Economic Concepts and Principles")
    print("  • Computer Science: Introduction to Computing and Programming")

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