#!/usr/bin/env python3
"""
SS2 Additional Subjects NERDC Content Generator
Generates comprehensive educational content for Senior Secondary School 2 (SS2)
for additional subjects: Further Mathematics, Geography, Economics, Computer Science
"""

import json
import datetime

def generate_ss2_additional_subjects_content():
    """
    Generate comprehensive NERDC-aligned content for SS2 additional subjects.
    """

    content_items = []

    # Further Mathematics SS2 - Matrices and Determinants
    further_math_ss2 = {
        "id": f"nerdc-further-math-ss2-matrices-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Matrices and Determinants (Further Mathematics SS2)",
        "subject": "Further Mathematics",
        "level": "SS2",
        "curriculum_framework": "NERDC Senior Secondary School Further Mathematics",
        "learning_objectives": [
            "Understand matrix operations and properties",
            "Calculate determinants of 2x2 and 3x3 matrices",
            "Apply matrices to solve systems of linear equations",
            "Understand matrix transformations and applications"
        ],
        "content": """
## 🔢 Matrices and Determinants

### Core Concepts
A matrix is a rectangular array of numbers arranged in rows and columns.

**Matrix Operations:**
- **Addition/Subtraction**: Element-wise operations
- **Scalar Multiplication**: Multiply each element by a constant
- **Matrix Multiplication**: Row by column multiplication
- **Transpose**: Interchange rows and columns

**Determinants:**
- **2x2 Matrix**: det = ad - bc
- **3x3 Matrix**: Expansion by minors or Sarrus rule
- **Properties**: det(AB) = det(A)det(B), det(A^T) = det(A)

### Worked Examples

**Example 1: Matrix Addition**
If A = [1 2; 3 4] and B = [5 6; 7 8]
A + B = [6 8; 10 12]

**Example 2: Determinant of 2x2 Matrix**
For matrix [3 4; 1 2], det = (3×2) - (4×1) = 6 - 4 = 2

**Example 3: Cramer's Rule**
Solve: 2x + 3y = 7, x - y = 1
D = 2(-1) - 3(1) = -5
Dx = 7(-1) - 3(1) = -10
Dy = 2(1) - 7(1) = -5
x = Dx/D = 2, y = Dy/D = 1

### Common Misconceptions
- Matrix multiplication is commutative
- Determinant of product equals product of determinants (only for square matrices)
- Any matrix can be inverted
- Matrix operations follow the same rules as real numbers

### Real-Life Applications
- Computer graphics and transformations
- Cryptography and encryption
- Economic modeling and input-output analysis
- Network analysis and traffic flow
- Quantum mechanics and physics simulations

### Practice Problems

**Basic Level:**
1. Add matrices A = [2 3; 1 4] and B = [1 2; 3 1]
2. Find determinant of [5 2; 3 7]
3. Multiply matrix [1 2] by scalar 3

**Intermediate Level:**
4. Solve system: x + 2y = 5, 3x - y = 2 using matrices
5. Find inverse of [2 1; 1 1] using adjoint method
6. Calculate determinant of 3x3 matrix using expansion

**Advanced Level:**
7. Apply matrix transformation to rotate a point 90°
8. Solve system using Gaussian elimination
9. Prove matrix properties using determinants

### WAEC Exam Preparation
- Matrix operations and properties
- Determinant calculations
- Systems of linear equations
- Matrix applications in real life

### Study Tips
- Practice matrix operations manually before using calculators
- Understand the geometric interpretation of transformations
- Learn determinant properties and their proofs
- Apply concepts to real-world problems

### Additional Resources
- Linear Algebra textbooks
- Khan Academy: Matrices
- MIT OpenCourseWare: Linear Algebra
- Geogebra for matrix visualizations
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Draw matrix grids and visualize transformations",
                    "Use color coding for matrix elements",
                    "Create geometric representations of matrix operations",
                    "Watch animations of matrix transformations"
                ],
                "activities": [
                    "Design visual matrix multiplication diagrams",
                    "Create transformation animations",
                    "Build 3D matrix visualization models"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Use physical grids or tiles for matrix representation",
                    "Build 3D models of coordinate transformations",
                    "Create tangible matrix operation manipulatives",
                    "Use gestures to demonstrate matrix rotations"
                ],
                "activities": [
                    "Construct physical matrix boards",
                    "Build transformation puzzles",
                    "Create matrix operation games"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to matrix operation explanations",
                    "Record yourself explaining determinant calculations",
                    "Participate in mathematics discussion groups",
                    "Use rhythmic patterns for matrix rules"
                ],
                "activities": [
                    "Create audio explanations of matrix concepts",
                    "Record step-by-step solution processes",
                    "Listen to linear algebra lectures"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed matrix operation procedures",
                    "Create study guides for determinant methods",
                    "Maintain a matrix problem-solving journal",
                    "Read linear algebra research papers"
                ],
                "activities": [
                    "Write formal matrix proofs",
                    "Document solution strategies",
                    "Create comparison charts of matrix methods"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "A = [3 1; 2 4], B = [1 2; 3 1], find A + B",
                "Calculate det[2 3; 1 4]",
                "Find 2A where A = [1 2; 3 4]"
            ],
            "intermediate": [
                "Solve: 2x + y = 7, x + 3y = 11 using matrices",
                "Find inverse of [4 2; 3 1]",
                "Calculate det of 3x3 matrix"
            ],
            "advanced": [
                "Apply rotation matrix to point (3,4)",
                "Solve 3x3 system using Cramer's rule",
                "Prove det(AB) = det(A)det(B)"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Matrix addition, subtraction, and scalar multiplication",
                "Matrix multiplication and properties",
                "Determinants of 2x2 and 3x3 matrices",
                "Solving systems of linear equations",
                "Matrix applications"
            ],
            "common_questions": [
                "Perform basic matrix operations",
                "Calculate determinants",
                "Solve systems using matrices",
                "Apply matrices to real-world problems"
            ],
            "time_management": "Allocate 20-25 minutes per matrix problem",
            "scoring_tips": "Show matrix operations step-by-step, use correct notation"
        },
        "career_connections": [
            "Data Science: Machine learning algorithms",
            "Engineering: Structural analysis and simulations",
            "Computer Graphics: 3D transformations",
            "Finance: Portfolio optimization models"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic algebra, coordinate geometry"],
        "tags": ["further mathematics", "matrices", "determinants", "linear algebra", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(further_math_ss2)

    # Geography SS2 - Climate and Weather
    geography_ss2 = {
        "id": f"nerdc-geography-ss2-climate-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Climate and Weather Systems (SS2)",
        "subject": "Geography",
        "level": "SS2",
        "curriculum_framework": "NERDC Senior Secondary School Geography",
        "learning_objectives": [
            "Understand the difference between weather and climate",
            "Identify major climate types and their characteristics",
            "Explain weather formation processes",
            "Analyze climate change impacts and adaptations"
        ],
        "content": """
## 🌤️ Climate and Weather Systems

### Core Concepts
Weather is the atmospheric conditions at a specific time and place, while climate is the long-term average weather pattern.

**Weather Elements:**
- **Temperature**: Heat content of the atmosphere
- **Precipitation**: Water falling from the atmosphere
- **Humidity**: Amount of water vapor in the air
- **Wind**: Movement of air masses
- **Pressure**: Weight of the atmosphere

**Climate Classification:**
- **Tropical**: High temperatures, high rainfall
- **Temperate**: Moderate temperatures, seasonal rainfall
- **Polar**: Low temperatures, low precipitation
- **Arid**: Low rainfall, high temperature variations

### Worked Examples

**Example 1: Temperature Conversion**
Celsius to Fahrenheit: °F = (°C × 9/5) + 32
Fahrenheit to Celsius: °C = (°F - 32) × 5/9
25°C = (25 × 9/5) + 32 = 77°F

**Example 2: Humidity Calculation**
Relative Humidity = (Actual vapor density / Saturation vapor density) × 100%
If actual vapor = 10g/m³, saturation = 20g/m³
RH = (10/20) × 100% = 50%

**Example 3: Wind Speed Analysis**
Beaufort Scale: Force 5 = 17-21 knots = Moderate breeze
Affects wave height, shipping, and land activities

### Common Misconceptions
- Weather and climate mean the same thing
- Climate change only affects polar regions
- All deserts are hot (cold deserts exist)
- Weather can be accurately predicted forever

### Real-Life Applications
- Agriculture and crop planning
- Disaster management and emergency response
- Urban planning and infrastructure design
- Aviation and transportation safety
- Tourism and recreation planning
- Climate change adaptation strategies

### Practice Problems

**Basic Level:**
1. Convert 30°C to Fahrenheit
2. Identify characteristics of tropical climate
3. List 4 weather elements

**Intermediate Level:**
4. Calculate relative humidity given vapor densities
5. Compare Mediterranean and Tropical climates
6. Explain formation of rainfall

**Advanced Level:**
7. Analyze climate change impacts on agriculture
8. Evaluate weather modification techniques
9. Assess climate adaptation strategies

### WAEC Exam Preparation
- Weather elements and measurements
- Climate types and characteristics
- Weather forecasting and instruments
- Climate change and environmental issues

### Study Tips
- Keep a personal weather diary
- Study current weather maps and forecasts
- Learn climate zones through world maps
- Understand local climate patterns

### Additional Resources
- Meteorological department websites
- Climate data from NASA and NOAA
- National Geographic climate articles
- Weather apps and forecasting tools
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Study detailed climate maps and weather charts",
                    "Create visual diagrams of weather systems",
                    "Use color coding for climate zones",
                    "Watch weather documentaries and animations"
                ],
                "activities": [
                    "Draw climate zone maps",
                    "Create weather system diagrams",
                    "Design climate change infographics"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build weather instrument models",
                    "Create physical climate zone representations",
                    "Conduct weather observation experiments",
                    "Use movement to demonstrate weather processes"
                ],
                "activities": [
                    "Build simple weather stations",
                    "Create climate zone dioramas",
                    "Conduct rainfall measurement activities"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to weather reports and forecasts",
                    "Record explanations of climate processes",
                    "Participate in geography discussion groups",
                    "Use audio descriptions of weather patterns"
                ],
                "activities": [
                    "Create audio weather reports",
                    "Listen to climate change discussions",
                    "Record geographical case studies"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed climate descriptions",
                    "Create study guides for weather elements",
                    "Maintain a weather observation journal",
                    "Read climate research reports"
                ],
                "activities": [
                    "Write climate impact assessments",
                    "Document weather patterns",
                    "Create comparison charts of climate types"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Convert 20°C to Fahrenheit",
                "Name 3 characteristics of desert climate",
                "List weather measuring instruments"
            ],
            "intermediate": [
                "Calculate RH: actual vapor 15g/m³, saturation 30g/m³",
                "Compare tropical and temperate climates",
                "Explain monsoon formation"
            ],
            "advanced": [
                "Analyze climate change effects on Nigeria",
                "Evaluate desertification causes and solutions",
                "Assess urban heat island effects"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Weather elements and measurements",
                "Climate types and characteristics",
                "Weather instruments and forecasting",
                "Climate change and human activities"
            ],
            "common_questions": [
                "Describe weather elements",
                "Explain climate classification",
                "Analyze weather maps",
                "Discuss climate change impacts"
            ],
            "time_management": "Allocate 15-20 minutes per climate question",
            "scoring_tips": "Use geographical terminology, support with examples"
        },
        "career_connections": [
            "Meteorology: Weather forecasting",
            "Environmental Science: Climate research",
            "Urban Planning: Climate-resilient design",
            "Agriculture: Climate-smart farming"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic geography, map reading"],
        "tags": ["geography", "climate", "weather", "meteorology", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(geography_ss2)

    # Economics SS2 - Theory of Demand and Supply
    economics_ss2 = {
        "id": f"nerdc-economics-ss2-demand-supply-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Theory of Demand and Supply (SS2)",
        "subject": "Economics",
        "level": "SS2",
        "curriculum_framework": "NERDC Senior Secondary School Economics",
        "learning_objectives": [
            "Understand the law of demand and factors affecting demand",
            "Explain the law of supply and factors affecting supply",
            "Analyze market equilibrium and price determination",
            "Apply demand and supply analysis to real-world situations"
        ],
        "content": """
## 📈 Theory of Demand and Supply

### Core Concepts
Demand is the quantity of a good consumers are willing and able to buy at different prices. Supply is the quantity producers are willing and able to sell at different prices.

**Law of Demand:** As price increases, quantity demanded decreases (inverse relationship)

**Law of Supply:** As price increases, quantity supplied increases (direct relationship)

**Market Equilibrium:** Point where quantity demanded equals quantity supplied

### Worked Examples

**Example 1: Demand Schedule**
Price (₦) | Quantity Demanded
100       | 20
80        | 30
60        | 50
40        | 80

**Example 2: Supply Schedule**
Price (₦) | Quantity Supplied
100       | 80
80        | 60
60        | 40
40        | 20

**Example 3: Equilibrium Price**
At equilibrium: Qd = Qs = 50 units, Price = ₦60

### Common Misconceptions
- Demand and quantity demanded mean the same thing
- Supply and quantity supplied are identical
- Price always equals equilibrium price
- Demand curves always slope downward

### Real-Life Applications
- Pricing strategies in business
- Government taxation and subsidy policies
- Agricultural product pricing
- Stock market analysis
- Housing market dynamics
- International trade negotiations

### Practice Problems

**Basic Level:**
1. Define demand and list 4 factors affecting it
2. Explain the law of supply with an example
3. Draw a simple demand curve

**Intermediate Level:**
4. Calculate equilibrium price from demand and supply schedules
5. Explain how price changes affect market equilibrium
6. Analyze impact of government intervention

**Advanced Level:**
7. Apply demand-supply analysis to real market situations
8. Evaluate price control effects on markets
9. Analyze international trade using demand-supply model

### WAEC Exam Preparation
- Laws of demand and supply
- Factors affecting demand and supply
- Market equilibrium and price determination
- Applications to real-world situations

### Study Tips
- Create demand-supply diagrams for different scenarios
- Study current market news and price changes
- Practice calculating equilibrium points
- Understand government market interventions

### Additional Resources
- Economics textbooks for secondary schools
- BBC Economics: Markets
- Khan Academy: Supply and Demand
- Financial news websites
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Draw detailed demand and supply diagrams",
                    "Create visual representations of market equilibrium",
                    "Use color coding for different market scenarios",
                    "Watch economics animations and videos"
                ],
                "activities": [
                    "Design market equilibrium diagrams",
                    "Create visual aids for economic concepts",
                    "Make infographics about market forces"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Use physical objects to simulate markets",
                    "Create role-playing scenarios for buyers and sellers",
                    "Build models of supply and demand interactions",
                    "Use manipulatives for price-quantity relationships"
                ],
                "activities": [
                    "Simulate market transactions with tokens",
                    "Build physical demand-supply models",
                    "Create market simulation games"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to economics podcasts and lectures",
                    "Record explanations of market concepts",
                    "Participate in economics discussion groups",
                    "Use audio for vocabulary building"
                ],
                "activities": [
                    "Create audio explanations of economic theories",
                    "Listen to market analysis discussions",
                    "Record oral presentations on economic topics"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed economic analyses",
                    "Create study guides for market concepts",
                    "Maintain an economics observation journal",
                    "Read economic news and reports"
                ],
                "activities": [
                    "Write market analysis reports",
                    "Document price change observations",
                    "Create comparison charts of market structures"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "List 5 factors affecting demand",
                "Explain law of supply with diagram",
                "Define market equilibrium"
            ],
            "intermediate": [
                "Find equilibrium: Demand P=100-2Q, Supply P=20+3Q",
                "Analyze price floor effects",
                "Explain shortage vs surplus"
            ],
            "advanced": [
                "Apply demand-supply to petrol pricing in Nigeria",
                "Evaluate subsidy removal effects",
                "Analyze black market formation"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Laws of demand and supply",
                "Factors affecting demand and supply",
                "Market equilibrium",
                "Price determination"
            ],
            "common_questions": [
                "Explain demand and supply laws",
                "Analyze market equilibrium",
                "Discuss factors affecting markets",
                "Apply concepts to real situations"
            ],
            "time_management": "Allocate 15-20 minutes per market analysis question",
            "scoring_tips": "Use diagrams, explain with examples, show understanding"
        },
        "career_connections": [
            "Business: Pricing and marketing strategies",
            "Finance: Market analysis and investment",
            "Government: Economic policy and planning",
            "Research: Economic modeling and forecasting"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic economics concepts"],
        "tags": ["economics", "demand", "supply", "markets", "equilibrium", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(economics_ss2)

    # Computer Science SS2 - Programming Fundamentals
    computer_science_ss2 = {
        "id": f"nerdc-computer-science-ss2-programming-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Programming Fundamentals and Control Structures (SS2)",
        "subject": "Computer Science",
        "level": "SS2",
        "curriculum_framework": "NERDC Senior Secondary School Computer Science",
        "learning_objectives": [
            "Understand programming concepts and algorithms",
            "Write programs using control structures",
            "Debug and test computer programs",
            "Apply programming to solve problems"
        ],
        "content": """
## 💻 Programming Fundamentals and Control Structures

### Core Concepts
Programming is the process of creating instructions for computers to follow. An algorithm is a step-by-step procedure to solve a problem.

**Control Structures:**
- **Sequence**: Statements executed in order
- **Selection**: if-else statements for decision making
- **Iteration**: Loops for repetition (for, while)

**Programming Concepts:**
- **Variables**: Storage locations for data
- **Data Types**: Integer, float, string, boolean
- **Operators**: Arithmetic, relational, logical
- **Functions**: Reusable code blocks

### Worked Examples

**Example 1: Simple Program**
```
# Calculate area of rectangle
length = 5
width = 3
area = length * width
print("Area =", area)
```

**Example 2: Selection Structure**
```
# Check if number is positive
num = int(input("Enter number: "))
if num > 0:
    print("Positive")
else:
    print("Not positive")
```

**Example 3: Loop Structure**
```
# Print numbers 1 to 5
for i in range(1, 6):
    print(i)
```

### Common Misconceptions
- Programming is only for math experts
- Computers understand human language
- All programs work perfectly first time
- Programming is about memorizing syntax

### Real-Life Applications
- Business applications and automation
- Scientific research and data analysis
- Game development and entertainment
- Web development and e-commerce
- Mobile app development
- Artificial intelligence and machine learning

### Practice Problems

**Basic Level:**
1. Write program to calculate simple interest
2. Create program to check if number is even or odd
3. Write program to find maximum of two numbers

**Intermediate Level:**
4. Create program to calculate factorial
5. Write program to check prime numbers
6. Create simple calculator program

**Advanced Level:**
7. Implement binary search algorithm
8. Create program to sort array of numbers
9. Develop simple game logic

### WAEC Exam Preparation
- Programming concepts and terminology
- Algorithm development and flowcharts
- Basic programming constructs
- Problem-solving with programs

### Study Tips
- Practice coding regularly on different problems
- Learn one programming language thoroughly
- Understand logic before writing code
- Debug programs systematically

### Additional Resources
- Python documentation and tutorials
- Codecademy programming courses
- freeCodeCamp curriculum
- Programming practice websites
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Draw flowcharts for program logic",
                    "Create visual representations of algorithms",
                    "Use color coding for different code elements",
                    "Watch programming tutorial videos"
                ],
                "activities": [
                    "Design algorithm flowcharts",
                    "Create visual code structure diagrams",
                    "Make programming concept infographics"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Type code and run programs hands-on",
                    "Build physical models of algorithms",
                    "Use tangible programming aids",
                    "Create coding gesture demonstrations"
                ],
                "activities": [
                    "Write and test code interactively",
                    "Build algorithm puzzles",
                    "Create physical coding challenges"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to programming podcasts and lectures",
                    "Record code explanation walkthroughs",
                    "Participate in coding discussion groups",
                    "Use audio for learning syntax"
                ],
                "activities": [
                    "Create audio code explanations",
                    "Listen to algorithm analysis",
                    "Record debugging sessions"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed code documentation",
                    "Create programming study guides",
                    "Maintain a coding journal",
                    "Read programming books and articles"
                ],
                "activities": [
                    "Write algorithm pseudocode",
                    "Document code solutions",
                    "Create programming language comparisons"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Write program: area = length × width",
                "Create if-else for positive/negative check",
                "Write loop to print 1 to 10"
            ],
            "intermediate": [
                "Calculate compound interest with loop",
                "Check if string is palindrome",
                "Find sum of array elements"
            ],
            "advanced": [
                "Implement bubble sort algorithm",
                "Create number guessing game",
                "Build simple calculator with functions"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Programming concepts and terminology",
                "Algorithm development",
                "Control structures",
                "Basic programming problems"
            ],
            "common_questions": [
                "Write simple programs",
                "Draw flowcharts",
                "Explain programming concepts",
                "Solve problems with algorithms"
            ],
            "time_management": "Allocate 20-25 minutes per programming question",
            "scoring_tips": "Write clear, well-formatted code with comments"
        },
        "career_connections": [
            "Software Development: Application programming",
            "Data Science: Analytical programming",
            "Web Development: Full-stack programming",
            "Game Development: Interactive programming"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Intermediate",
        "prerequisites": ["Basic computer skills, logic"],
        "tags": ["computer science", "programming", "algorithms", "control structures", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(computer_science_ss2)

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

    print(f"✅ Successfully saved {len(content_items)} SS2 additional subjects content items")
    return True

def main():
    """
    Main function to generate and save SS2 additional subjects content.
    """
    print("🚀 Generating SS2 Additional Subjects NERDC Curriculum Content...")

    # Generate content
    content_items = generate_ss2_additional_subjects_content()

    # Display generation statistics
    subjects = {}
    for item in content_items:
        subj = item.get('subject', 'Unknown')
        subjects[subj] = subjects.get(subj, 0) + 1

    print(f"\n✅ Generated {len(content_items)} SS2 additional subjects content items")
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

if __name__ == '__main__':
    main()