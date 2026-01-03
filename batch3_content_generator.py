#!/usr/bin/env python3
"""
Generate Batch 3 - 5 High-Priority Advanced Lessons
1. Sequence and Series (Math)
2. Temperature and Heat (Physics)
3. Matrices and Determinants (Math)
4. Variation (Math)
5. Angles and Triangles (Math)
"""

import json
from datetime import datetime
from pathlib import Path

def generate_sequence_series():
    """Generate Mathematics: Sequence and Series lesson"""
    return {
        "id": "math_sequence_series_advanced",
        "title": "Sequence and Series: From Bank Interest to Lagos Property Prices",
        "subject": "Mathematics",
        "topic": "Sequence and Series",
        "difficulty": "advanced",
        "exam_weight": "high",
        "read_time_minutes": 28,
        "created_at": datetime.now().isoformat(),
        "learning_objectives": [
            "Identify arithmetic and geometric progressions",
            "Calculate nth term and sum formulas",
            "Apply sequences to Nigerian financial planning",
            "Solve complex sequence problems",
            "Understand real-world pattern applications"
        ],
        "prerequisites": ["Patterns", "Algebra", "Basic number sequences"],
        "content": """
# Sequence and Series: From Bank Interest to Lagos Property Prices

## Introduction
In Nigeria, patterns drive finance and growth. Bank savings grow in geometric progression (compound interest). Property prices in Lagos increase in arithmetic progression. Civil servant salaries follow predictable sequences. Understanding sequences and series unlocks the mathematics of growth, investment, and planning.

## Part 1: Arithmetic Progression (AP)

### Definition
An Arithmetic Progression is a sequence where the difference between consecutive terms is constant.

**Form**: a, a+d, a+2d, a+3d, ...

**Examples**:
- 2, 5, 8, 11, ... (first term a=2, common difference d=3)
- 100, 95, 90, 85, ... (a=100, d=-5)

### Nigerian Example 1: Civil Servant Salary Progression
A teacher starts at ₦120,000/month with ₦5,000 annual increment.

**Sequence**:
- Year 1: ₦120,000
- Year 2: ₦125,000
- Year 3: ₦130,000
- Year 4: ₦135,000

This is AP with a = 120,000 and d = 5,000.

### nth Term of AP
**Formula**: Tₙ = a + (n-1)d

**Problem**: What is the teacher's salary in year 10?
- Tₙ = 120,000 + (10-1) × 5,000
- T₁₀ = 120,000 + 45,000 = ₦165,000

**WAEC Tip**: Always write the formula before substituting values!

### Sum of n Terms of AP
**Formula**: Sₙ = n/2 [2a + (n-1)d] OR Sₙ = n/2 (first + last)

**Worked Example 1: Total Salary Over 10 Years**
How much total salary does the teacher earn in 10 years?

**Solution**:
- First term: a = 120,000
- Last term (year 10): T₁₀ = 165,000
- Number of terms: n = 10

**Using formula**:
- S₁₀ = 10/2 (120,000 + 165,000)
- S₁₀ = 5 × 285,000
- **S₁₀ = ₦1,425,000**

**Meaning**: Total earnings over 10 years = ₦1.425 million

## Part 2: Geometric Progression (GP)

### Definition
A Geometric Progression is a sequence where the ratio between consecutive terms is constant.

**Form**: a, ar, ar², ar³, ...

**Examples**:
- 2, 6, 18, 54, ... (a=2, r=3)
- 100, 50, 25, 12.5, ... (a=100, r=0.5)

### Nigerian Example 2: Bank Compound Interest
₦100,000 deposited in GTBank at 10% annual interest.

**Balance after each year**:
- Year 0: ₦100,000
- Year 1: ₦100,000 × 1.1 = ₦110,000
- Year 2: ₦110,000 × 1.1 = ₦121,000
- Year 3: ₦133,100
- Year 4: ₦146,410

**This is GP** with a = 100,000 and r = 1.1

### nth Term of GP
**Formula**: Tₙ = ar^(n-1)

**Problem**: How much money after 5 years?
- T₅ = 100,000 × (1.1)⁴
- T₅ = 100,000 × 1.4641
- T₅ = **₦146,410**

### Sum of n Terms of GP
**Formula**: Sₙ = a(r^n - 1)/(r - 1) [when r ≠ 1]

**Worked Example 2: Total Interest Earned**
What is the total amount in bank account after 5 years?

**Solution**:
- a = 100,000
- r = 1.1
- n = 5

**Using formula**:
- S₅ = 100,000(1.1⁵ - 1)/(1.1 - 1)
- S₅ = 100,000(1.6105 - 1)/0.1
- S₅ = 100,000(0.6105)/0.1
- S₅ = 100,000 × 6.105
- **S₅ = ₦610,500** (total amount after 5 years)

**Interest earned** = 610,500 - 100,000 × 5 = ₦110,500

## Part 3: Sum to Infinity (GP Only)

### When -1 < r < 1
The series approaches a finite limit.

**Formula**: S∞ = a/(1-r)

**Worked Example 3: Recurring Decimal**
The decimal 0.333... = 1/3 can be written as a GP.

**0.333...** = 0.3 + 0.03 + 0.003 + ...
- a = 0.3
- r = 0.1
- S∞ = 0.3/(1-0.1) = 0.3/0.9 = **1/3** ✓

## Part 4: Real Nigerian Applications

### Property Prices in Lagos
Lekki property values appreciate 5% annually (GP with r = 1.05).

Starting price: ₦10,000,000 in 2020.

**Price by year**:
- 2020: ₦10,000,000
- 2022: ₦10,000,000 × (1.05)² = ₦11,025,000
- 2025: ₦10,000,000 × (1.05)⁵ = ₦12,762,815

**Question**: After 10 years, value = ?
- T₁₁ = 10,000,000 × (1.05)¹⁰ = ₦16,288,946

### MTN Subscriber Growth
MTN Nigeria adds 2 million subscribers annually (AP).

**Year 1**: 60 million subscribers
**Year 2**: 62 million
**Year 3**: 64 million

**Total subscribers by year 5**:
- a = 60 million
- d = 2 million
- n = 5
- S₅ = 5/2[2(60) + (5-1)×2] = 2.5[120 + 8] = **320 million subscriber-years**

### Dangote Cement Distribution
Production increases 15% annually (GP with r = 1.15).

**Starting production**: 5 million tonnes in 2020.

**Projected for 2026**:
- T₇ = 5 × (1.15)⁶ = 5 × 2.313 = **11.57 million tonnes**

## WAEC Exam Tips

1. **Identify the sequence**: Look for constant difference (AP) or constant ratio (GP)
2. **Write known values**: a (first term), d or r, n (number of terms)
3. **Choose correct formula**: AP or GP sum formula
4. **Show substitution**: Write values into formula before calculating
5. **State units**: Always include ₦, tonnes, years, etc.
6. **Check reasonableness**: Does answer make sense in context?
7. **Practice with negative terms**: Some sequences decrease

## Practice Problems

**Problem 1**: A trader's monthly profit increases from ₦50,000 by ₦10,000 each month. Find total profit in 12 months.

**Problem 2**: UBA offers 8% compound interest on savings. If ₦500,000 is invested, find amount after 3 years.

**Problem 3**: An AP has first term 5 and common difference 3. Find the sum of first 20 terms.

**Problem 4**: A GP has first term 2 and common ratio 3. Find the 6th term.

## Key Formulas

- **AP nth term**: Tₙ = a + (n-1)d
- **AP sum**: Sₙ = n/2[2a + (n-1)d]
- **GP nth term**: Tₙ = ar^(n-1)
- **GP sum**: Sₙ = a(r^n - 1)/(r - 1)
- **GP infinite sum**: S∞ = a/(1-r) [when |r| < 1]

## Nigerian Context Importance

Understanding sequences helps with:
- **Banking**: Calculate investment returns and loan repayment
- **Business**: Project growth and sales forecasts
- **Property**: Predict appreciation and investment value
- **Demographics**: Plan for population changes
- **Salary**: Understand career earning potential
- **Telecommunications**: Analyze subscriber growth

This knowledge directly applies to Nigerian financial planning and business decisions!
""",
        "tags": ["sequence", "series", "AP", "GP", "compound interest", "WAEC", "high priority", "banking", "property", "Lagos", "investment"],
        "nigerian_context": "GTBank compound interest (10% APY), teacher salary progression (₦5,000/year increment), Lagos property appreciation (5% annually), MTN subscriber growth (2M annually), Dangote cement production growth (15% annually), civil servant earnings",
        "summary": "Advanced mathematics lesson covering arithmetic progressions (AP), geometric progressions (GP), and their applications. Nigerian contexts: Teacher salary progression (₦120k → ₦165k over 10 years), bank savings with compound interest (₦100k at 10% = ₦146,410 in 4 years), Lagos property appreciation (₦10M → ₦12.76M in 5 years), MTN subscriber growth, Dangote cement expansion. Includes formulas, 6 worked examples with Nigerian scenarios.",
        "views": 0,
        "likes": 0,
        "status": "published"
    }

def generate_temperature_heat():
    """Generate Physics: Temperature and Heat lesson"""
    return {
        "id": "physics_temperature_heat_advanced",
        "title": "Temperature and Heat: From Lagos Climate to Nigerian Kitchens",
        "subject": "Physics",
        "topic": "Temperature and Heat",
        "difficulty": "intermediate",
        "exam_weight": "high",
        "read_time_minutes": 27,
        "created_at": datetime.now().isoformat(),
        "learning_objectives": [
            "Convert between temperature scales (Celsius, Fahrenheit, Kelvin)",
            "Understand heat capacity and specific heat capacity",
            "Calculate latent heat in phase changes",
            "Apply concepts to Nigerian cooking and climate",
            "Solve calorimetry and thermal problems"
        ],
        "prerequisites": ["Energy concepts", "Measurement", "Unit conversions"],
        "content": """
# Temperature and Heat: From Lagos Climate to Nigerian Kitchens

## Introduction
Every Nigerian experiences temperature daily: Lagos heat at 27°C, Jos coolness at 20°C, Sokoto's blazing 42°C. Food cooks at precise temperatures, vaccines need cold storage, and electricity consumption depends on climate. Understanding temperature and heat is essential for daily life in Nigeria.

## Part 1: Temperature Scales

### Celsius Scale
Most common in Nigeria. Based on water freezing (0°C) and boiling (100°C) at sea level.

**Nigerian Temperature Examples**:
- Lagos average: 27°C (warm year-round)
- Jos Plateau: 20°C (cooler highland)
- Sokoto dry season: 42°C (very hot)
- Cool room: 16°C
- Normal body: 37°C
- Fever: 39-40°C

### Fahrenheit Scale
Used in some medical contexts and old British instruments.

**Conversion**:
- F = 9/5 × C + 32
- C = 5/9 × (F - 32)

**Worked Example 1: Lagos Temperature Conversion**
Lagos average is 27°C. Convert to Fahrenheit.
- F = 9/5 × 27 + 32
- F = 48.6 + 32
- **F = 80.6°F** (warm and comfortable)

### Kelvin Scale
Absolute temperature scale. K = C + 273 (or C + 273.15 precisely)

**Nigerian temperatures in Kelvin**:
- Lagos 27°C = 300 K
- Jos 20°C = 293 K
- Sokoto 42°C = 315 K

**WAEC Tip**: Always convert to Kelvin for gas law calculations!

## Part 2: Heat Capacity and Specific Heat Capacity

### Heat Capacity (C)
Energy needed to raise 1 object by 1°C.

**Formula**: Q = C × ΔT

where:
- Q = heat energy (joules)
- C = heat capacity (J/°C)
- ΔT = temperature change (°C)

### Specific Heat Capacity (c)
Energy needed to raise 1 kg of substance by 1°C.

**Formula**: Q = m × c × ΔT

**Worked Example 2: Heating Nigerian Soup**
A pot of vegetable soup (5 kg) needs heating from 25°C to 95°C.

**Given**:
- Mass m = 5 kg
- Temperature change: ΔT = 95 - 25 = 70°C
- Specific heat of water (main component): c = 4,200 J/kg°C

**Solution**:
- Q = m × c × ΔT
- Q = 5 × 4,200 × 70
- Q = 1,470,000 J = **1.47 MJ**

**Meaning**: Need 1.47 million joules of energy to heat the soup.

**Nigerian context**: A gas stove releases ~30 MJ per hour, so this takes ~3 minutes.

### Specific Heat Values (Common Nigerian Materials)
| Material | Specific Heat (J/kg°C) |
|----------|----------------------|
| Water | 4,200 |
| Cooking oil | 2,000 |
| Sand (Sahara) | 800 |
| Iron (cookware) | 450 |
| Aluminum | 900 |

## Part 3: Latent Heat

### Latent Heat of Fusion (Melting)
Energy needed to melt solid without temperature change.

**Formula**: Q = m × Lf

- Ice: Lf = 334,000 J/kg
- Energy to melt 1 kg ice = 334 kJ

### Latent Heat of Vaporization (Boiling)
Energy needed to convert liquid to gas without temperature change.

**Formula**: Q = m × Lv

- Water: Lv = 2,260,000 J/kg (2.26 MJ)
- Energy to boil 1 kg water = 2,260 kJ

**Worked Example 3: Boiling Water for Pap**
Heating 2 kg water from 25°C to boiling (100°C), then completely boiling it.

**Step 1 - Heating**:
- Q₁ = m × c × ΔT
- Q₁ = 2 × 4,200 × 75
- Q₁ = 630,000 J

**Step 2 - Boiling (vaporization)**:
- Q₂ = m × Lv
- Q₂ = 2 × 2,260,000
- Q₂ = 4,520,000 J

**Total energy**:
- Q_total = 630,000 + 4,520,000 = **5,150,000 J = 5.15 MJ**

**Meaning**: Mostly goes to vaporization, not heating!

## Part 4: Heat Transfer Methods

### Conduction
Direct transfer through material (no movement).

**Nigerian Example**: Metal pot conducting heat to food inside.
- Aluminum pot conducts heat quickly (high conductivity)
- Traditional clay pots conduct slowly

**Application**: Choose materials wisely for cooking efficiency!

### Convection
Transfer through movement of liquid/gas.

**Nigerian Example**: Hot water in soup rising, cold sinking.
- Creates circular motion
- Distributes heat throughout

**Application**: Stir soup for even heating (stronger convection).

### Radiation
Transfer through electromagnetic waves (no contact needed).

**Nigerian Example**: Nigerian sun warming Lagos without touching.
- Infrared radiation heats skin, buildings
- Solar panels use this to generate electricity (Kaduna installations)

## Part 5: Real Nigerian Heat Applications

### Air Conditioning Load (Lagos)
To keep room at 22°C when outside is 32°C:

**Heat entering** ≈ Building surface area × Temperature difference × U-value

Modern Lagos office building (500 m²) requires:
- Cooling capacity: ~60 kW
- Cost: ₦50,000/month electricity (NEPA rate)

### Cooking Efficiency
Gas stove (~10 kW) vs electric kettle (2 kW):
- **Gas**: Heats water in 5 minutes (efficient, cheaper)
- **Electric**: Heats water in 10 minutes (less efficient, more expensive)

**Cost comparison**:
- Gas: 1 liter water = ₦50 cost
- Electricity: 1 liter water = ₦120 cost (2.4× more expensive)

### Vaccine Cold Chain
Pfizer vaccine storage: 2-8°C required.

**Cooling needed**: Remove heat to maintain low temperature.
- Nigerian cold store in Lagos: ₦5M system
- Running cost: ₦100,000/month electricity

## WAEC Exam Tips

1. **Check temperature units**: Problem might be in K, not °C
2. **Include latent heat**: Don't forget vaporization/fusion energy
3. **Show all steps**: Heating then boiling (two separate processes)
4. **State formula first**: Write Q = mc∆T before substituting
5. **Use correct c value**: Different materials have different specific heat
6. **Units matter**: Answer in joules, always

## Practice Problems

**Problem 1**: Convert 40°C to Fahrenheit and Kelvin.

**Problem 2**: How much energy to heat 10 kg iron from 20°C to 100°C? (c = 450 J/kg°C)

**Problem 3**: How much energy to melt 5 kg ice at 0°C? (Lf = 334,000 J/kg)

**Problem 4**: A Lagos building loses 100 kJ heat per minute. How long for 5 MJ loss?

## Key Equations

- **Conversion**: F = 9/5C + 32, K = C + 273
- **Heat capacity**: Q = mc∆T
- **Latent heat**: Q = mL
- **Total thermal energy**: Q_total = mc∆T + mL

## Nigerian Context Importance

Temperature and heat knowledge helps with:
- **Cooking**: Efficient food preparation (gas vs electric)
- **Climate**: Adapt to Lagos heat or Jos coolness
- **Health**: Fever understanding, vaccine storage
- **Business**: AC costs, refrigeration, solar thermal
- **Energy**: Electricity consumption, efficiency improvements
- **Construction**: Thermal insulation design

This knowledge makes Nigerian daily life more efficient and economical!
""",
        "tags": ["temperature", "heat", "specific heat capacity", "latent heat", "WAEC", "high priority", "Nigeria climate", "Lagos", "cooking", "thermometer"],
        "nigerian_context": "Lagos temperature 27°C average, Jos 20°C, Sokoto 42°C, Nigerian soup heating (5kg from 25→95°C), gas stove vs electric kettle efficiency, Pfizer vaccine cold chain storage (2-8°C), Lagos AC cooling (60 kW systems), NEPA electricity costs (₦50k-120k/month), solar panel installations Kaduna",
        "summary": "Temperature and heat physics lesson covering Celsius/Fahrenheit/Kelvin scales, specific heat capacity, latent heat of fusion/vaporization, and heat transfer (conduction, convection, radiation). Nigerian contexts: Lagos 27°C, Jos 20°C, Sokoto 42°C, soup heating calculations (5kg × 4,200 J/kg°C × 70°C = 1.47 MJ), gas vs electric cooking costs, vaccine cold storage (2-8°C), AC systems (60 kW for Lagos offices). Includes 3 detailed worked examples.",
        "views": 0,
        "likes": 0,
        "status": "published"
    }

def generate_matrices_determinants():
    """Generate Mathematics: Matrices and Determinants lesson"""
    return {
        "id": "math_matrices_determinants_advanced",
        "title": "Matrices and Determinants: From MTN Data to Simultaneous Equations",
        "subject": "Mathematics",
        "topic": "Matrices and Determinants",
        "difficulty": "advanced",
        "exam_weight": "high",
        "read_time_minutes": 30,
        "created_at": datetime.now().isoformat(),
        "learning_objectives": [
            "Perform matrix operations (addition, subtraction, multiplication)",
            "Calculate determinants of 2×2 and 3×3 matrices",
            "Find inverse of matrices",
            "Solve simultaneous equations using matrices",
            "Apply matrix concepts to Nigerian business scenarios"
        ],
        "prerequisites": ["Algebra", "Simultaneous equations", "Number operations"],
        "content": """
# Matrices and Determinants: From MTN Data to Simultaneous Equations

## Introduction
Matrices organize data efficiently. MTN tracks subscribers by region and plan in matrix form. Dangote analyzes production across factories using matrices. Universities use matrices to process thousands of admission applications. Matrices solve complex problems that would be tedious with traditional algebra.

## Part 1: Matrix Basics

### Definition
A matrix is rectangular array of numbers arranged in rows and columns.

**Form**: 
```
A = [a₁₁  a₁₂  a₁₃]
    [a₂₁  a₂₂  a₂₃]
    [a₃₁  a₃₂  a₃₃]
```

**Notation**: 3×3 matrix (3 rows, 3 columns)

### Nigerian Example 1: MTN Subscription Data
MTN tracks 3 plans across 3 months.

```
           January  February  March
Premium:    500,000  520,000  540,000
Standard:  1,000,000 1,050,000 1,100,000
Basic:     2,000,000 1,900,000 1,800,000

Matrix A = [500,000   520,000   540,000]
           [1,000,000 1,050,000 1,100,000]
           [2,000,000 1,900,000 1,800,000]
```

## Part 2: Matrix Operations

### Addition and Subtraction
Add/subtract corresponding elements.

**Example**:
```
A = [1  2]    B = [2  1]
    [3  4]        [1  2]

A + B = [3  3]
        [4  6]
```

### Scalar Multiplication
Multiply every element by a constant.

```
2A = [2  4]
     [6  8]
```

### Matrix Multiplication
For A(m×n) × B(n×p) = C(m×p)

**Worked Example 1: Dangote Sales Calculation**

Production matrix (3 factories × 2 products):
```
P = [100  50]   (Factory 1: 100 bags cement, 50 bags flour)
    [120  60]   (Factory 2)
    [80   40]   (Factory 3)
```

Price per unit:
```
Price = [₦5,000]   (Cement price per bag)
        [₦2,000]   (Flour price per bag)
```

**Revenue from each factory**:
```
Revenue = P × Price

Factory 1: 100(5,000) + 50(2,000) = 500,000 + 100,000 = ₦600,000
Factory 2: 120(5,000) + 60(2,000) = 600,000 + 120,000 = ₦720,000
Factory 3: 80(5,000) + 40(2,000) = 400,000 + 80,000 = ₦480,000

Total revenue = ₦1,800,000
```

## Part 3: Determinants

### 2×2 Determinant
For matrix A = [a  b]
               [c  d]

**Formula**: |A| = ad - bc

**Example**:
```
A = [3  2]
    [1  4]

|A| = 3(4) - 2(1) = 12 - 2 = 10
```

### 3×3 Determinant (Method of Cofactors)
For matrix A = [a  b  c]
               [d  e  f]
               [g  h  i]

**Formula**: |A| = a(ei - fh) - b(di - fg) + c(dh - eg)

**Worked Example 2: Calculate 3×3 Determinant**

```
A = [2  3  1]
    [1  0  2]
    [3  1  1]

|A| = 2(0×1 - 2×1) - 3(1×1 - 2×3) + 1(1×1 - 0×3)
    = 2(-2) - 3(1-6) + 1(1)
    = -4 - 3(-5) + 1
    = -4 + 15 + 1
    = 12
```

## Part 4: Matrix Inverse

### Definition
For matrix A, inverse A⁻¹ satisfies: A × A⁻¹ = I (identity matrix)

### 2×2 Inverse
For A = [a  b]
        [c  d]

**Formula**: A⁻¹ = 1/|A| × [d   -b]
                            [-c   a]

**Important**: Matrix must be invertible (|A| ≠ 0)

**Worked Example 3: Inverse of 2×2 Matrix**

```
A = [4  3]
    [2  1]

Step 1: Find determinant
|A| = 4(1) - 3(2) = 4 - 6 = -2

Step 2: Apply inverse formula
A⁻¹ = 1/(-2) × [1   -3]  = [-1/2   3/2]
              [-2    4]    [1     -2]

Verification: A × A⁻¹ = I ✓
```

## Part 5: Solving Simultaneous Equations Using Matrices

### System of Equations
```
2x + 3y = 8
x + 2y = 5
```

### Matrix Form
```
[2  3] [x]   [8]
[1  2] [y] = [5]

A × X = B  where:
A = coefficient matrix
X = [x, y]ᵀ (unknowns)
B = [8, 5]ᵀ (constants)
```

### Solution
X = A⁻¹ × B

**Worked Example 4: Nigerian Market Pricing**

A Lagos market sells yam and cassava. One customer pays ₦12,000 for 2 yams + 3 cassavas. Another pays ₦7,500 for 1 yam + 2 cassavas.

**Equations**:
- 2x + 3y = 12,000 (x = yam price, y = cassava price)
- 1x + 2y = 7,500

**Matrix solution**:
```
[2  3] [x]   [12,000]
[1  2] [y] = [7,500]

Step 1: Find |A|
|A| = 2(2) - 3(1) = 4 - 3 = 1

Step 2: Find A⁻¹
A⁻¹ = 1/1 × [2   -3]  = [2   -3]
           [-1    2]    [-1   2]

Step 3: Calculate X = A⁻¹ × B
[x]   [2   -3] [12,000]   [24,000 - 22,500]   [1,500]
[y] = [-1   2] [7,500]  = [-12,000 + 15,000] = [3,000]
```

**Answer**: Yam = ₦1,500 each, Cassava = ₦3,000 each

**Verification**:
- 2(1,500) + 3(3,000) = 3,000 + 9,000 = ₦12,000 ✓
- 1(1,500) + 2(3,000) = 1,500 + 6,000 = ₦7,500 ✓

## Part 6: Real Nigerian Applications

### University Admission Processing
JAMB processes 2 million applications. Scores in Matrix form:
```
             Math  English  Science
Student 1:   78     82       75
Student 2:   85     79       88
...
Student 2M:  ...    ...      ...
```

Can calculate aggregate scores using matrix multiplication instantly.

### MTN Network Analysis
Connection matrix between 36 states:
```
[Connection between Lagos-Abuja]
[Connection between Lagos-Kano]
[... 666 connections total]
```

Determinant ≠ 0 means network is connected (robust system).

### Dangote Production Analysis
Multi-factory production data solved using matrix equations:
- 5 factories producing 8 products
- Constraints: Raw material availability, worker capacity, shipping
- Solution: Optimal production allocation (₦billions in efficiency)

## WAEC Exam Tips

1. **Check invertibility**: Always calculate determinant first
2. **Show row operations**: For 3×3 matrices, show expansion steps
3. **Verify multiplication**: 2×3 matrix × 3×2 matrix = 2×2 result
4. **Identity matrix**: Remember I has 1s on diagonal, 0s elsewhere
5. **Check solutions**: Always verify by substituting back
6. **Scalar vs matrix**: Be clear when multiplying numbers vs matrices

## Practice Problems

**Problem 1**: Find determinant of [5  3; 2  4]

**Problem 2**: Calculate inverse of [2  1; 3  2]

**Problem 3**: Solve using matrices: 3x + 2y = 13, x + y = 5

**Problem 4**: If A × B = C, and |A| = 3, |B| = 2, find |C|

## Key Formulas

- **2×2 Determinant**: |A| = ad - bc
- **3×3 Determinant**: |A| = a(ei - fh) - b(di - fg) + c(dh - eg)
- **2×2 Inverse**: A⁻¹ = 1/|A| × [d -b; -c a]
- **Matrix solution**: X = A⁻¹ × B

## Nigerian Context Importance

Matrices solve Nigerian problems:
- **Business**: Process multi-location data (MTN, Dangote)
- **Education**: Handle admissions efficiently (JAMB)
- **Government**: Census data organization and analysis
- **Telecommunications**: Network routing and optimization
- **Finance**: Multi-investment portfolio management
- **Technology**: Graphics, AI, data processing

This mathematical tool powers modern Nigerian business and technology!
""",
        "tags": ["matrices", "determinants", "inverse", "simultaneous equations", "WAEC", "high priority", "MTN", "Dangote", "JAMB", "business data"],
        "nigerian_context": "MTN subscription data by plan/region, Dangote multi-factory production analysis, JAMB processing 2M applications, market pricing (yam ₦1,500 vs cassava ₦3,000), network connectivity analysis (36 states), multi-product revenue calculations, university admission processing",
        "summary": "Advanced mathematics lesson on matrices and determinants covering operations (addition, subtraction, multiplication), 2×2 and 3×3 determinants, matrix inverses, and solving simultaneous equations using matrices. Nigerian applications: MTN subscriber analysis, Dangote production optimization (Factory 1: 100 bags cement + 50 bags flour = ₦600k revenue), market pricing (yam/cassava), JAMB admissions processing. Includes 4 detailed worked examples with Nigerian business scenarios.",
        "views": 0,
        "likes": 0,
        "status": "published"
    }

def generate_variation():
    """Generate Mathematics: Variation lesson"""
    return {
        "id": "math_variation_advanced",
        "title": "Variation: From Taxi Fares to Electricity Bills",
        "subject": "Mathematics",
        "topic": "Variation",
        "difficulty": "intermediate",
        "exam_weight": "high",
        "read_time_minutes": 25,
        "created_at": datetime.now().isoformat(),
        "learning_objectives": [
            "Identify direct, inverse, and joint variation",
            "Write variation equations and solve for constants",
            "Apply variation to Nigerian transportation and commerce",
            "Solve complex variation problems",
            "Understand real-world proportional relationships"
        ],
        "prerequisites": ["Ratios", "Proportions", "Basic algebra"],
        "content": """
# Variation: From Taxi Fares to Electricity Bills

## Introduction
Everything in Nigeria varies in relation to something else. Taxi fare varies with distance. NEPA bills vary with electricity consumed. Worker productivity varies with rest time. Fertilizer yield varies with rainfall and nutrients. Understanding variation unlocks prediction and planning in Nigerian life.

## Part 1: Direct Variation

### Definition
y varies directly with x means: y = kx

where k is the constant of variation.

**Property**: When x increases, y increases proportionally.

### Nigerian Example 1: Taxi Fares in Lagos
Typical rate: ₦100 per kilometer

**Relationship**: Fare = 100 × Distance

**Worked Example**:
- 5 km trip costs: Fare = 100 × 5 = ₦500
- 15 km trip costs: Fare = 100 × 15 = ₦1,500
- 25 km trip costs: Fare = 100 × 25 = ₦2,500

**Pattern**: Fare varies directly with distance (k = 100)

### Finding the Constant
**If y varies directly with x**, and y = 20 when x = 4:

- y = kx
- 20 = k(4)
- k = 5

**So equation is y = 5x**

## Part 2: Inverse Variation

### Definition
y varies inversely with x means: y = k/x

where k is the constant.

**Property**: When x increases, y decreases.

### Nigerian Example 2: Workers and Project Time
Building a 100 m² house requires 1,000 man-hours of work.

**If 10 workers work on the project**:
- Time = 1,000/10 = 100 hours each
- Total time: 100 hours

**If 20 workers work on project**:
- Time = 1,000/20 = 50 hours each
- Total time: 50 hours

**Pattern**: More workers → less time (inverse variation, k = 1,000)

### Worked Example: Supplies Management
A delivery driver uses fuel inversely proportional to remaining supplies. With 500 liters fuel, can cover 2,000 km (k = 500 × 2,000 = 1,000,000).

**How far with 250 liters**?
- Distance = 1,000,000/250
- Distance = **4,000 km** ✓

## Part 3: Joint Variation

### Definition
z varies jointly with x and y means: z = kxy

**Property**: z changes with changes in both x and y.

### Nigerian Example 3: Farm Harvest
Crop yield depends on fertilizer AND rainfall.

**Formula**: Yield = k × Fertilizer × Rainfall

If k = 50 (kg yield per unit fertilizer per unit rainfall):
- With 100 units fertilizer and 500 mm rainfall:
  Yield = 50 × 100 × 500 = 2,500,000 kg

- With 100 units fertilizer and 300 mm rainfall (less rain):
  Yield = 50 × 100 × 300 = 1,500,000 kg

**Both factors matter for maximum yield**

## Part 4: Partial Variation

### Definition
y partially varies with x when: y = a + kx

**Property**: y has a fixed component (a) plus variable component (kx)

### Nigerian Example 4: NEPA Electricity Billing
Bill = Base fee + Usage charge
Bill = 1,000 + 68 × kWh

**If use 500 kWh**:
- Bill = 1,000 + 68 × 500
- Bill = 1,000 + 34,000
- **Bill = ₦35,000**

**If use 200 kWh**:
- Bill = 1,000 + 68 × 200
- Bill = 1,000 + 13,600
- **Bill = ₦14,600**

**Pattern**: Even with 0 kWh, you pay ₦1,000 base fee

## Part 5: Complex Variation Problems

### Worked Example 1: Transport Cost Analysis
A hauling company charges: Cost = Base + (Distance × Rate) + (Weight × Factor)

**Cost = 5,000 + 100D + 50W**

where D = distance (km), W = weight (tonnes)

**For 100 km trip with 5 tonnes**:
- Cost = 5,000 + 100(100) + 50(5)
- Cost = 5,000 + 10,000 + 250
- **Cost = ₦15,250**

### Worked Example 2: Dangote Cement Production
Production depends on workers (W) and machines (M):

**Production = 10 × W × M**

(10 bags per worker-machine unit per day)

**With 50 workers and 10 machines**:
- Production = 10 × 50 × 10 = 5,000 bags/day

**To increase to 10,000 bags/day**, double either:
- Option A: 100 workers + 10 machines
- Option B: 50 workers + 20 machines

## Part 6: Real Nigerian Applications

### Market Trading
Price inversely varies with abundance:
- When tomatoes abundant, price low (₦50/kg)
- When tomatoes scarce, price high (₦300/kg)
- **Equation**: Price × Quantity = constant

### Manufacturing
Output directly varies with:
- Number of machines (more machines = more output)
- Worker skill (trained workers = more output)
- **Formula**: Output = k × Machines × Skill level

### Transportation Network
Delivery time partially varies:
- **Time = Fixed + Distance/Speed**
- Fixed time: Vehicle prep, paperwork (1 hour)
- Variable time: Distance/Speed

**Lagos to Ibadan (120 km, average 60 km/h)**:
- Time = 1 + 120/60 = 1 + 2 = 3 hours

## WAEC Exam Tips

1. **Identify variation type**: Read problem carefully (direct, inverse, or joint)
2. **Find constant first**: Use given values to calculate k
3. **Write equation clearly**: State y = kx before solving
4. **Substitute completely**: Replace all variables with numbers
5. **Check units**: Include units in final answer
6. **Reasonableness test**: Does answer make sense?

## Practice Problems

**Problem 1**: y varies directly with x. If y = 30 when x = 6, find y when x = 10.

**Problem 2**: m varies inversely with n. If m = 20 when n = 5, find m when n = 2.

**Problem 3**: z varies jointly with x and y. If z = 60 when x = 3 and y = 4, find z when x = 2 and y = 5.

**Problem 4**: Monthly rent = ₦50,000 + ₦500/m² × area. Find rent for 100 m² apartment.

## Key Formulas

- **Direct**: y = kx
- **Inverse**: y = k/x
- **Joint**: z = kxy
- **Partial**: y = a + kx

## Nigerian Context Importance

Variation helps predict and plan:
- **Transportation**: Calculate fares, delivery times
- **Commerce**: Price-supply relationships, profit margins
- **Manufacturing**: Production planning with resources
- **Agriculture**: Yield predictions with inputs
- **Utilities**: Calculate bills (NEPA, water, internet)
- **Business**: Cost analysis, pricing strategies

This mathematical tool directly applies to Nigerian daily commerce and planning!
""",
        "tags": ["variation", "direct", "inverse", "joint", "partial", "WAEC", "high priority", "commerce", "transport", "NEPA billing"],
        "nigerian_context": "Lagos taxi fares (₦100/km), NEPA billing (₦1,000 base + ₦68/kWh), farm harvest (fertilizer × rainfall variation), market tomato prices (₦50-₦300/kg by season), building construction (workers vs time), Dangote cement production (workers × machines), transportation costs (fixed + distance).",
        "summary": "Mathematics lesson on variation covering direct variation (y=kx), inverse variation (y=k/x), joint variation (z=kxy), and partial variation (y=a+kx). Nigerian applications: Lagos taxi fares ₦100/km, NEPA electricity (₦1,000 base + ₦68/kWh = ₦35,000 for 500 kWh), farm yield with fertilizer and rainfall, building time with workers, cement production analysis. Includes worked examples for each variation type with real Nigerian scenarios.",
        "views": 0,
        "likes": 0,
        "status": "published"
    }

def generate_angles_triangles():
    """Generate Mathematics: Angles and Triangles lesson"""
    return {
        "id": "math_angles_triangles_advanced",
        "title": "Angles and Triangles: From Roof Design to Land Surveying",
        "subject": "Mathematics",
        "topic": "Angles and Triangles",
        "difficulty": "basic",
        "exam_weight": "high",
        "read_time_minutes": 23,
        "created_at": datetime.now().isoformat(),
        "learning_objectives": [
            "Calculate angles in polygons",
            "Identify similar and congruent triangles",
            "Apply Pythagoras theorem to Nigerian construction",
            "Solve geometric problems involving triangles",
            "Use triangle properties in land measurements"
        ],
        "prerequisites": ["Basic geometry", "Angle properties", "Measurement"],
        "content": """
# Angles and Triangles: From Roof Design to Land Surveying

## Introduction
Nigerian buildings feature precise angles: Abuja pyramidal roofs, Lagos warehouse triangular supports, Niger Bridge trusses. Land surveyors use triangulation to measure property boundaries. Traditional Yoruba geometric patterns display mathematical precision. Understanding angles and triangles is essential for Nigerian architecture, engineering, and surveying.

## Part 1: Angles in Polygons

### Interior Angle Sum
For a polygon with n sides:

**Sum of interior angles = (n - 2) × 180°**

### Nigerian Example 1: Abuja Building Designs
A hexagonal (6-sided) office building common in Abuja.

**Interior angle sum**:
- Sum = (6 - 2) × 180°
- Sum = 4 × 180°
- Sum = **720°**

**Each angle (regular hexagon)**:
- Each angle = 720°/6 = **120°**

### Exterior Angles
**Sum of exterior angles = 360°** (always)

For regular polygon:
- Each exterior angle = 360°/n

**Regular hexagon exterior angle**:
- 360°/6 = **60°**

**WAEC Tip**: Exterior angles always sum to 360° regardless of polygon shape!

## Part 2: Triangle Properties

### Triangle Angle Sum
All triangles: **∠A + ∠B + ∠C = 180°**

### Triangle Types
- **Acute**: All angles < 90°
- **Right**: One angle = 90°
- **Obtuse**: One angle > 90°
- **Equilateral**: All angles = 60°
- **Isosceles**: Two equal angles
- **Scalene**: All different angles

### Worked Example 1: Roof Truss Design
A Nigerian roof truss forms triangle with:
- ∠A = 35°
- ∠B = 65°
- ∠C = ?

**Solution**:
- ∠A + ∠B + ∠C = 180°
- 35° + 65° + ∠C = 180°
- ∠C = **80°**

## Part 3: Similar Triangles

### Definition
Triangles are similar if:
- All corresponding angles equal
- All corresponding sides proportional

### Nigerian Example 2: Shadow Measurement
Aso Rock in Abuja casts shadow. Using small triangle, we measure:

**Small triangle**:
- Height of stick: 2 m
- Shadow: 1.5 m

**Large triangle**:
- Aso Rock shadow: 300 m
- Height: ?

**Since triangles are similar**:
- 2/1.5 = Height/300
- Height = 2 × 300/1.5
- Height = 600/1.5
- **Height = 400 m**

(Note: Actual Aso Rock height is 256 m, accounting for angle differences)

## Part 4: Pythagoras Theorem

### Formula
For right triangle: **a² + b² = c²**

where c is hypotenuse (longest side).

### Nigerian Example 3: Land Plot Measurement
A triangular Lagos property plot:
- Two sides: 80 m and 60 m
- These are perpendicular (right angle between them)
- Third side (diagonal): ?

**Solution**:
- a² + b² = c²
- 80² + 60² = c²
- 6,400 + 3,600 = c²
- 10,000 = c²
- c = **100 m**

**Common Pythagorean triples in Nigeria**:
- 3-4-5 (scaling: 30-40-50, 60-80-100)
- 5-12-13
- 8-15-17

### Worked Example: Niger Bridge Measurement
A bridge support triangle:
- Height: 50 m
- Base: 120 m
- Slant length: ?

**Solution**:
- 50² + 120² = c²
- 2,500 + 14,400 = c²
- 16,900 = c²
- c = **130 m**

## Part 5: Congruent Triangles

### Conditions for Congruence
1. **SSS** (Side-Side-Side): All three sides equal
2. **SAS** (Side-Angle-Side): Two sides and included angle equal
3. **ASA** (Angle-Side-Angle): Two angles and included side equal
4. **RHS** (Right-Hypotenuse-Side): Right angle, hypotenuse, and one side equal

### Nigerian Example 4: Identical Roof Trusses
Two roof trusses must be congruent:
- First truss: sides 5 m, 6 m, 7 m
- Second truss: sides 5 m, 6 m, 7 m

**By SSS**: Trusses are congruent ✓ (identical shapes, sizes)

## Part 6: Real Nigerian Applications

### Land Surveying
Property boundaries often use triangulation:
- Surveyor measures baseline (100 m)
- Measures angles to boundary corners (45° and 75°)
- Calculates property perimeter and area

### Construction
Roof trusses use 30-60-90 and 45-45-90 triangles:
- **45-45-90**: Isosceles, sides ratio 1:1:√2
- **30-60-90**: Sides ratio 1:√3:2

### Architecture
Nigerian traditional patterns use:
- Equilateral triangles (Igbo crafts)
- Isosceles triangles (Hausa designs)
- Right triangles (building foundations)

## WAEC Exam Tips

1. **Draw diagrams**: Always sketch the triangle first
2. **Label clearly**: Mark all angles and sides
3. **State theorem**: Write "By Pythagoras theorem..." before using
4. **Check angle sum**: Verify angles add to 180°
5. **Similar triangles**: Establish correspondence clearly
6. **Units matter**: Include m, cm, degrees in answer

## Practice Problems

**Problem 1**: Pentagon (5 sides) interior angle sum = ?

**Problem 2**: Right triangle has sides 3 cm and 4 cm. Hypotenuse = ?

**Problem 3**: Two similar triangles have corresponding sides 4 cm and 6 cm. If first triangle's perimeter is 12 cm, find second triangle's perimeter.

**Problem 4**: Triangle angles are x, 2x, and 3x. Find x.

## Key Formulas

- **Polygon angle sum**: (n-2) × 180°
- **Exterior angle sum**: 360°
- **Triangle angle sum**: 180°
- **Pythagoras**: a² + b² = c²

## Nigerian Context Importance

Triangle geometry applies to:
- **Construction**: Building design, roof truss angles
- **Surveying**: Property boundary measurement
- **Engineering**: Bridge support structures
- **Land measurement**: Triangulation for area calculation
- **Architecture**: Traditional pattern design
- **Arts**: Textile and craft geometric designs

This foundational geometry enables accurate Nigerian construction and measurement!
""",
        "tags": ["angles", "triangles", "Pythagoras", "similar", "congruent", "WAEC", "high priority", "construction", "surveying", "Abuja"],
        "nigerian_context": "Abuja hexagonal building design (120° interior angles), Aso Rock height measurement by shadows (400m calculation), triangular Lagos land plots (80m × 60m = 100m diagonal), Niger Bridge support calculations (50m × 120m = 130m), roof truss designs (30-60-90 triangles), Yoruba geometric patterns, property surveying by triangulation",
        "summary": "Geometry lesson covering polygon interior angles ((n-2)×180°), triangle properties (angle sum 180°), similar and congruent triangles, and Pythagoras theorem (a²+b²=c²). Nigerian applications: Abuja hexagonal buildings (120° angles), Aso Rock shadow measurement, Lagos land plot diagonal (80×60=100m), Niger Bridge supports (50×120=130m), roof trusses with 30-60-90 triangles. Includes 4 worked examples with Nigerian construction and surveying scenarios.",
        "views": 0,
        "likes": 0,
        "status": "published"
    }

def generate_batch3():
    """Generate and save all 5 Batch 3 lessons"""
    print("=" * 70)
    print("GENERATING BATCH 3 - 5 HIGH-PRIORITY LESSONS")
    print("=" * 70)
    
    lessons = []
    
    print("\n[1/5] Generating Mathematics: Sequence and Series...")
    lessons.append(generate_sequence_series())
    print("   ✅ Complete (28 min read)")
    
    print("\n[2/5] Generating Physics: Temperature and Heat...")
    lessons.append(generate_temperature_heat())
    print("   ✅ Complete (27 min read)")
    
    print("\n[3/5] Generating Mathematics: Matrices and Determinants...")
    lessons.append(generate_matrices_determinants())
    print("   ✅ Complete (30 min read)")
    
    print("\n[4/5] Generating Mathematics: Variation...")
    lessons.append(generate_variation())
    print("   ✅ Complete (25 min read)")
    
    print("\n[5/5] Generating Mathematics: Angles and Triangles...")
    lessons.append(generate_angles_triangles())
    print("   ✅ Complete (23 min read)")
    
    # Save to batch3_extension.json
    output_path = Path("generated_content/batch3_content.json")
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump({
            "metadata": {
                "version": "3.0",
                "total_items": 5,
                "generator": "Batch3ContentGenerator",
                "generated_date": datetime.now().isoformat(),
                "total_read_time_minutes": sum(l["read_time_minutes"] for l in lessons),
                "exam_board": "WAEC"
            },
            "content": lessons
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved to: {output_path}")
    print("\n" + "=" * 70)
    print("BATCH 3 GENERATION COMPLETE - 5 LESSONS")
    print("=" * 70)
    print(f"\n📚 Generated lessons:")
    for lesson in lessons:
        print(f"   - {lesson['subject']}: {lesson['title']}")
    print(f"\n📊 Total read time: {sum(l['read_time_minutes'] for l in lessons)} minutes")
    print(f"✅ Coverage: Sequence/Series, Temperature, Matrices, Variation, Angles/Triangles")
    print("\nNext: Merge with existing batch3 items and deploy to Wave 3")

if __name__ == "__main__":
    generate_batch3()
