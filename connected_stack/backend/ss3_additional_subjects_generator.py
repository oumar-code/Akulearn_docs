#!/usr/bin/env python3
"""
SS3 Additional Subjects NERDC Content Generator
Generates comprehensive educational content for Senior Secondary School 3 (SS3)
for additional subjects: Further Mathematics, Geography, Economics, Computer Science
"""

import json
import datetime

def generate_ss3_additional_subjects_content():
    """
    Generate comprehensive NERDC-aligned content for SS3 additional subjects.
    """

    content_items = []

    # Further Mathematics SS3 - Calculus and Vectors
    further_math_ss3 = {
        "id": f"nerdc-further-math-ss3-calculus-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Introduction to Calculus and Vectors (Further Mathematics SS3)",
        "subject": "Further Mathematics",
        "level": "SS3",
        "curriculum_framework": "NERDC Senior Secondary School Further Mathematics",
        "learning_objectives": [
            "Understand basic concepts of differentiation and integration",
            "Apply calculus to solve real-world problems",
            "Work with vectors in 2D and 3D space",
            "Understand vector operations and applications"
        ],
        "content": """
## 🧮 Introduction to Calculus and Vectors

### Core Concepts
Calculus is the mathematical study of change and motion. It has two main branches: differential calculus (rates of change) and integral calculus (accumulation).

**Differentiation:**
- **Derivative**: Rate of change of a function
- **Power Rule**: d/dx(x^n) = nx^(n-1)
- **Product Rule**: d/dx(uv) = u'v + uv'
- **Chain Rule**: d/dx(f(g(x))) = f'(g(x)) × g'(x)

**Vectors:**
- **Scalar**: Quantity with magnitude only
- **Vector**: Quantity with magnitude and direction
- **Vector Operations**: Addition, subtraction, scalar multiplication
- **Dot Product**: u·v = |u||v|cosθ

### Worked Examples

**Example 1: Basic Differentiation**
d/dx(x³) = 3x²
d/dx(2x + 1) = 2

**Example 2: Product Rule**
d/dx(x² × sin(x)) = 2x × sin(x) + x² × cos(x)

**Example 3: Vector Addition**
If u = (2, 3) and v = (1, 4)
u + v = (3, 7)

**Example 4: Dot Product**
u = (3, 4), v = (1, 2)
u·v = 3×1 + 4×2 = 11

### Common Misconceptions
- Calculus is only for advanced mathematics
- Vectors are just arrows on paper
- Differentiation and integration are opposites
- All functions have derivatives

### Real-Life Applications
- Physics: Motion, forces, and energy
- Engineering: Design optimization and modeling
- Economics: Marginal analysis and optimization
- Computer graphics: 3D modeling and animation
- Navigation: GPS and directional calculations

### Practice Problems

**Basic Level:**
1. Find derivative of x⁴
2. Differentiate 3x² + 2x + 1
3. Add vectors u = (1,2) and v = (3,4)

**Intermediate Level:**
4. Apply product rule to x³ × e^x
5. Find dot product of (2,5) and (3,1)
6. Differentiate using chain rule

**Advanced Level:**
7. Solve optimization problems using derivatives
8. Apply vectors to resolve forces
9. Use calculus in real-world applications

### WAEC Exam Preparation
- Basic differentiation rules
- Vector operations in 2D
- Applications of calculus
- Problem-solving with vectors

### Study Tips
- Practice differentiation daily
- Visualize vectors geometrically
- Understand calculus applications
- Work through real-world examples

### Additional Resources
- Calculus textbooks
- Khan Academy: Calculus
- MIT OpenCourseWare
- Vector geometry software
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Draw detailed derivative graphs",
                    "Create vector diagrams with magnitudes and directions",
                    "Use color coding for different vector components",
                    "Watch calculus and vector animations"
                ],
                "activities": [
                    "Design vector addition diagrams",
                    "Create calculus function graphs",
                    "Build 3D vector visualization models"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Use physical vectors (arrows) for operations",
                    "Build 3D models of vector spaces",
                    "Create tangible calculus manipulatives",
                    "Use movement to demonstrate vector concepts"
                ],
                "activities": [
                    "Construct physical vector diagrams",
                    "Build calculus curve models",
                    "Create vector operation puzzles"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to calculus explanation podcasts",
                    "Record vector operation walkthroughs",
                    "Participate in mathematics discussion groups",
                    "Use audio for formula memorization"
                ],
                "activities": [
                    "Create audio calculus tutorials",
                    "Record vector problem solutions",
                    "Listen to mathematical lectures"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed calculus derivations",
                    "Create study guides for vector operations",
                    "Maintain a mathematics problem journal",
                    "Read advanced mathematics papers"
                ],
                "activities": [
                    "Write formal mathematical proofs",
                    "Document solution strategies",
                    "Create comparison charts of calculus methods"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "d/dx(x⁵) = ?",
                "d/dx(4x³ + 2x² + x + 1) = ?",
                "Add vectors (2,3) + (4,1)"
            ],
            "intermediate": [
                "d/dx(x² × cos(x)) = ?",
                "Dot product (3,4) · (1,2) = ?",
                "d/dx(sin(x) × e^x) = ?"
            ],
            "advanced": [
                "Find maximum of f(x) = -x² + 4x + 1",
                "Resolve force vectors of 5N at 30° and 3N at 60°",
                "Apply calculus to velocity problems"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Differentiation of polynomial functions",
                "Basic vector operations",
                "Applications of derivatives",
                "Vector geometry problems"
            ],
            "common_questions": [
                "Differentiate given functions",
                "Perform vector operations",
                "Solve calculus application problems",
                "Apply vectors to geometry"
            ],
            "time_management": "Allocate 20-25 minutes per calculus/vector problem",
            "scoring_tips": "Show all working steps, use correct mathematical notation"
        },
        "career_connections": [
            "Engineering: Structural analysis and design",
            "Physics: Motion and force calculations",
            "Computer Science: Graphics and game development",
            "Finance: Risk modeling and optimization"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Advanced",
        "prerequisites": ["Advanced algebra, trigonometry"],
        "tags": ["further mathematics", "calculus", "vectors", "differentiation", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(further_math_ss3)

    # Geography SS3 - Economic Geography and Development
    geography_ss3 = {
        "id": f"nerdc-geography-ss3-economic-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Economic Geography and Regional Development (SS3)",
        "subject": "Geography",
        "level": "SS3",
        "curriculum_framework": "NERDC Senior Secondary School Geography",
        "learning_objectives": [
            "Understand economic activities and their spatial distribution",
            "Analyze factors influencing economic development",
            "Examine regional development patterns",
            "Evaluate economic planning and policies"
        ],
        "content": """
## 🌍 Economic Geography and Regional Development

### Core Concepts
Economic geography studies the spatial distribution of economic activities and the factors that influence their location and development.

**Economic Activities:**
- **Primary**: Extraction of raw materials (agriculture, mining)
- **Secondary**: Manufacturing and processing
- **Tertiary**: Services (trade, transport, tourism)
- **Quaternary**: Information and research services

**Development Indicators:**
- **GDP per capita**: Economic output per person
- **Human Development Index**: Health, education, income
- **Infrastructure**: Transportation, communication, utilities

### Worked Examples

**Example 1: Economic Activity Classification**
- Oil extraction: Primary
- Car manufacturing: Secondary
- Banking services: Tertiary
- Software development: Quaternary

**Example 2: Development Measurement**
Country A: GDP/capita = $2,000, Literacy = 85%
Country B: GDP/capita = $500, Literacy = 60%
Country A shows higher development

**Example 3: Regional Disparities**
North Region: Agriculture-based, low infrastructure
South Region: Industrial, high infrastructure
Development gap requires balanced regional planning

### Common Misconceptions
- Economic development means only GDP growth
- All countries follow the same development path
- Natural resources guarantee economic success
- Urban areas are always more developed

### Real-Life Applications
- Regional planning and development policies
- Investment location decisions
- Infrastructure development planning
- International aid and development programs
- Environmental impact assessments
- Urban-rural development balance

### Practice Problems

**Basic Level:**
1. Classify economic activities in your community
2. List 4 factors affecting industrial location
3. Define economic development

**Intermediate Level:**
4. Compare development indicators of two countries
5. Analyze factors for regional disparities
6. Evaluate transportation impact on development

**Advanced Level:**
7. Assess economic planning strategies
8. Analyze globalization effects on development
9. Evaluate sustainable development approaches

### WAEC Exam Preparation
- Economic activities and classification
- Factors influencing economic development
- Regional development patterns
- Economic planning and policies

### Study Tips
- Study current economic development news
- Analyze development data and statistics
- Understand local economic geography
- Learn about development theories

### Additional Resources
- World Bank development reports
- UNDP Human Development Reports
- Economic geography textbooks
- National development planning documents
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Study economic activity maps",
                    "Create development indicator charts",
                    "Use color coding for economic regions",
                    "Watch economic development documentaries"
                ],
                "activities": [
                    "Design economic activity distribution maps",
                    "Create development comparison charts",
                    "Make regional development diagrams"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build models of economic systems",
                    "Create physical representations of development",
                    "Use manipulatives for economic concepts",
                    "Conduct economic simulation activities"
                ],
                "activities": [
                    "Construct economic development models",
                    "Build regional planning dioramas",
                    "Create economic activity sorting games"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to economic development podcasts",
                    "Record explanations of economic concepts",
                    "Participate in geography discussion groups",
                    "Use audio for economic terminology"
                ],
                "activities": [
                    "Create audio economic analyses",
                    "Listen to development case studies",
                    "Record regional development discussions"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed economic geography reports",
                    "Create study guides for development concepts",
                    "Maintain an economic observation journal",
                    "Read development economics papers"
                ],
                "activities": [
                    "Write regional development plans",
                    "Document economic activity surveys",
                    "Create comparison charts of development models"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Classify: farming, teaching, mining, banking",
                "List 5 factors for industrial location",
                "Define tertiary economic activities"
            ],
            "intermediate": [
                "Compare GDP of Nigeria vs Ghana",
                "Analyze causes of regional imbalance",
                "Evaluate tourism impact on development"
            ],
            "advanced": [
                "Assess Niger Delta development challenges",
                "Analyze ECOWAS economic integration",
                "Evaluate sustainable development in Nigeria"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Classification of economic activities",
                "Factors affecting economic development",
                "Regional development patterns",
                "Economic planning and policies"
            ],
            "common_questions": [
                "Classify economic activities",
                "Explain development factors",
                "Analyze regional disparities",
                "Discuss development strategies"
            ],
            "time_management": "Allocate 15-20 minutes per economic geography question",
            "scoring_tips": "Use geographical examples, show understanding of concepts"
        },
        "career_connections": [
            "Urban Planning: Regional development",
            "Economic Development: Policy planning",
            "International Development: Aid coordination",
            "Environmental Planning: Sustainable development"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Advanced",
        "prerequisites": ["Basic geography, economics"],
        "tags": ["geography", "economic", "development", "regional planning", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(geography_ss3)

    # Economics SS3 - National Income and Economic Growth
    economics_ss3 = {
        "id": f"nerdc-economics-ss3-national-income-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "National Income Accounting and Economic Growth (SS3)",
        "subject": "Economics",
        "level": "SS3",
        "curriculum_framework": "NERDC Senior Secondary School Economics",
        "learning_objectives": [
            "Understand concepts of national income measurement",
            "Explain methods of calculating national income",
            "Analyze economic growth and development",
            "Evaluate government economic policies"
        ],
        "content": """
## 📊 National Income Accounting and Economic Growth

### Core Concepts
National income accounting measures the total economic activity of a country. It includes all income earned by factors of production.

**Key Concepts:**
- **GDP**: Gross Domestic Product - total value of goods and services produced within a country
- **GNP**: Gross National Product - GDP plus net income from abroad
- **NNP**: Net National Product - GNP minus depreciation
- **NI**: National Income - NNP minus indirect taxes plus subsidies

**Economic Growth:** Sustained increase in real GDP over time

**Methods of Measurement:**
- **Product Method**: Sum of value added at each stage
- **Income Method**: Sum of all factor incomes
- **Expenditure Method**: Total spending on final goods and services

### Worked Examples

**Example 1: Expenditure Method**
GDP = C + I + G + (X - M)
Where: C = Consumption, I = Investment, G = Government spending, X = Exports, M = Imports

**Example 2: Income Method**
NI = Wages + Rent + Interest + Profit + Mixed Income

**Example 3: Real vs Nominal GDP**
Nominal GDP 2023: ₦100 trillion
Inflation: 10%
Real GDP = ₦100 trillion / 1.10 = ₦90.91 trillion

### Common Misconceptions
- GDP measures economic welfare completely
- Economic growth always means development
- All economic activities are included in GDP
- Higher GDP always means better living standards

### Real-Life Applications
- Government budget planning and taxation
- Economic policy formulation and evaluation
- Business investment decisions
- International economic comparisons
- Development planning and aid allocation
- Inflation and growth monitoring

### Practice Problems

**Basic Level:**
1. Define GDP and explain its importance
2. List components of expenditure method
3. Distinguish between real and nominal GDP

**Intermediate Level:**
4. Calculate GDP using expenditure method
5. Explain factors affecting economic growth
6. Analyze inflation effects on GDP

**Advanced Level:**
7. Evaluate government economic policies
8. Compare economic performance of countries
9. Assess sustainable economic development

### WAEC Exam Preparation
- Concepts of national income
- Methods of measuring national income
- Economic growth and development
- Government economic policies

### Study Tips
- Study current economic data and statistics
- Understand different GDP calculations
- Learn about economic indicators
- Analyze government economic reports

### Additional Resources
- National Bureau of Statistics reports
- World Bank economic data
- Economics textbooks
- Financial news and analysis
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Create GDP component diagrams",
                    "Draw economic growth charts",
                    "Use color coding for economic indicators",
                    "Watch economic data visualizations"
                ],
                "activities": [
                    "Design national income flow diagrams",
                    "Create economic growth trend charts",
                    "Make infographics about economic policies"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build physical models of economic flows",
                    "Create role-playing for economic transactions",
                    "Use manipulatives for economic concepts",
                    "Conduct economic simulation activities"
                ],
                "activities": [
                    "Construct economic cycle models",
                    "Build national income calculation games",
                    "Create economic policy simulation activities"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to economic policy discussions",
                    "Record explanations of economic concepts",
                    "Participate in economics seminars",
                    "Use audio for economic terminology"
                ],
                "activities": [
                    "Create audio economic analyses",
                    "Listen to GDP calculation methods",
                    "Record economic policy discussions"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed economic analyses",
                    "Create study guides for national income concepts",
                    "Maintain an economic policy journal",
                    "Read economic research reports"
                ],
                "activities": [
                    "Write economic policy recommendations",
                    "Document economic indicator analysis",
                    "Create comparison charts of economic systems"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Define GDP, GNP, NNP",
                "List expenditure method components",
                "Explain economic growth vs development"
            ],
            "intermediate": [
                "Calculate: C=500, I=100, G=200, X=50, M=30",
                "Explain inflation effects on real GDP",
                "Analyze unemployment impact on economy"
            ],
            "advanced": [
                "Evaluate Nigerian economic growth policies",
                "Compare GDP calculations for different countries",
                "Assess sustainable development indicators"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "National income concepts and measurement",
                "Methods of calculating national income",
                "Economic growth and development",
                "Government economic policies"
            ],
            "common_questions": [
                "Explain national income concepts",
                "Calculate GDP using different methods",
                "Analyze economic growth factors",
                "Discuss economic development policies"
            ],
            "time_management": "Allocate 15-20 minutes per national income question",
            "scoring_tips": "Use economic terminology, show calculations clearly"
        },
        "career_connections": [
            "Economic Planning: Government policy",
            "Financial Analysis: Economic forecasting",
            "International Development: Aid evaluation",
            "Business Strategy: Economic analysis"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Advanced",
        "prerequisites": ["Basic economics, mathematics"],
        "tags": ["economics", "national income", "GDP", "economic growth", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(economics_ss3)

    # Computer Science SS3 - Data Structures and Algorithms
    computer_science_ss3 = {
        "id": f"nerdc-computer-science-ss3-data-structures-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "title": "Data Structures and Algorithms (SS3)",
        "subject": "Computer Science",
        "level": "SS3",
        "curriculum_framework": "NERDC Senior Secondary School Computer Science",
        "learning_objectives": [
            "Understand basic data structures and their operations",
            "Implement fundamental algorithms",
            "Analyze algorithm efficiency",
            "Apply data structures to solve problems"
        ],
        "content": """
## 🗂️ Data Structures and Algorithms

### Core Concepts
Data structures are ways of organizing and storing data for efficient access and modification. Algorithms are step-by-step procedures for solving problems.

**Basic Data Structures:**
- **Arrays**: Fixed-size, indexed collection
- **Lists**: Dynamic collections with operations
- **Stacks**: Last-In-First-Out (LIFO) structure
- **Queues**: First-In-First-Out (FIFO) structure

**Fundamental Algorithms:**
- **Searching**: Linear search, binary search
- **Sorting**: Bubble sort, selection sort, insertion sort
- **Complexity**: Time and space analysis

### Worked Examples

**Example 1: Array Operations**
```
arr = [10, 20, 30, 40, 50]
# Access element at index 2: arr[2] = 30
# Insert 25 at index 2: [10, 20, 25, 30, 40, 50]
```

**Example 2: Stack Operations**
```
stack = []
stack.push(10)  # [10]
stack.push(20)  # [10, 20]
stack.pop()     # [10], returns 20
```

**Example 3: Linear Search**
```
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

### Common Misconceptions
- All data structures are arrays
- Efficient algorithms are always complex
- Data structures don't affect program performance
- Algorithms work the same in all programming languages

### Real-Life Applications
- Database management systems
- Search engines and information retrieval
- Social network algorithms
- E-commerce recommendation systems
- GPS navigation and routing
- Computer game development

### Practice Problems

**Basic Level:**
1. Implement array insertion and deletion
2. Create stack with push/pop operations
3. Write linear search algorithm

**Intermediate Level:**
4. Implement queue data structure
5. Write binary search algorithm
6. Create simple sorting algorithm

**Advanced Level:**
7. Analyze algorithm time complexity
8. Implement linked list operations
9. Solve complex algorithmic problems

### WAEC Exam Preparation
- Basic data structures (arrays, stacks, queues)
- Fundamental algorithms (searching, sorting)
- Algorithm analysis and efficiency
- Problem-solving with data structures

### Study Tips
- Implement data structures from scratch
- Practice algorithmic problem-solving
- Analyze algorithm efficiency
- Study real-world applications

### Additional Resources
- Data Structures textbooks
- LeetCode and HackerRank practice
- GeeksforGeeks tutorials
- Algorithm visualization tools
        """,
        "learning_options": {
            "visual": {
                "tips": [
                    "Draw data structure diagrams",
                    "Create algorithm flowcharts",
                    "Use color coding for algorithm steps",
                    "Watch data structure animations"
                ],
                "activities": [
                    "Design data structure visualization diagrams",
                    "Create algorithm execution flowcharts",
                    "Make complexity analysis charts"
                ]
            },
            "kinesthetic": {
                "tips": [
                    "Build physical models of data structures",
                    "Use tangible objects for algorithm simulation",
                    "Create hands-on coding activities",
                    "Construct algorithm puzzle games"
                ],
                "activities": [
                    "Build stack/queue models with cards",
                    "Create algorithm implementation challenges",
                    "Construct data structure sorting games"
                ]
            },
            "auditory": {
                "tips": [
                    "Listen to algorithm explanation podcasts",
                    "Record data structure walkthroughs",
                    "Participate in programming discussions",
                    "Use audio for algorithm memorization"
                ],
                "activities": [
                    "Create audio algorithm tutorials",
                    "Record code debugging sessions",
                    "Listen to technical programming lectures"
                ]
            },
            "reading_writing": {
                "tips": [
                    "Write detailed algorithm documentation",
                    "Create data structure study guides",
                    "Maintain a programming problem journal",
                    "Read algorithm research papers"
                ],
                "activities": [
                    "Write pseudocode for algorithms",
                    "Document data structure implementations",
                    "Create algorithm comparison charts"
                ]
            }
        },
        "practice_problems": {
            "basic": [
                "Implement stack with array",
                "Write linear search function",
                "Create array reversal algorithm"
            ],
            "intermediate": [
                "Implement queue with linked list",
                "Write binary search algorithm",
                "Create bubble sort implementation"
            ],
            "advanced": [
                "Analyze O(n log n) complexity",
                "Implement tree traversal",
                "Solve dynamic programming problems"
            ]
        },
        "exam_preparation": {
            "waec_focus": [
                "Array and list operations",
                "Stack and queue implementations",
                "Basic searching and sorting algorithms",
                "Algorithm efficiency analysis"
            ],
            "common_questions": [
                "Implement basic data structures",
                "Write simple algorithms",
                "Analyze algorithm complexity",
                "Solve programming problems"
            ],
            "time_management": "Allocate 20-25 minutes per algorithm question",
            "scoring_tips": "Write clear, efficient code with proper documentation"
        },
        "career_connections": [
            "Software Engineering: System design",
            "Data Science: Algorithm optimization",
            "Game Development: Data management",
            "Web Development: Performance optimization"
        ],
        "estimated_duration": "60 minutes",
        "difficulty_level": "Advanced",
        "prerequisites": ["Programming fundamentals"],
        "tags": ["computer science", "data structures", "algorithms", "programming", "WAEC"],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    content_items.append(computer_science_ss3)

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

    print(f"✅ Successfully saved {len(content_items)} SS3 additional subjects content items")
    return True

def main():
    """
    Main function to generate and save SS3 additional subjects content.
    """
    print("🚀 Generating SS3 Additional Subjects NERDC Curriculum Content...")

    # Generate content
    content_items = generate_ss3_additional_subjects_content()

    # Display generation statistics
    subjects = {}
    for item in content_items:
        subj = item.get('subject', 'Unknown')
        subjects[subj] = subjects.get(subj, 0) + 1

    print(f"\n✅ Generated {len(content_items)} SS3 additional subjects content items")
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