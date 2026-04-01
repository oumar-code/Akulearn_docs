# Mathematics - Calculus (Differentiation): Starter Content Bundle

## Study Guide Template (Ready to Fill)

### Subject: Mathematics
### Topic: Differentiation (Introduction to Calculus)
### Class: SS3
### Difficulty: Intermediate–Advanced
### Target: JAMB/WAEC/NECO
### Questions in JAMB Exam: 4-6 (out of 40 Mathematics questions)

---

## 1. KEY CONCEPTS (Master These)

### Concept 1: What is Differentiation?

**Definition**: The process of finding the rate of change of a function, or the gradient of a curve at any point

**Notation**:
```
If y = f(x), the derivative is written as:
  dy/dx   or   f'(x)   or   y'

"dy/dx" means "rate of change of y with respect to x"
```

**What the derivative tells you**:
- The **gradient (slope)** of a curve at any point
- The **rate of change** of one quantity with respect to another
- Where a function is **increasing** (dy/dx > 0) or **decreasing** (dy/dx < 0)
- Where **maximum or minimum** points occur (dy/dx = 0)

**Why Important**: 4-6 JAMB/WAEC questions; tested every year

---

### Concept 2: Rules of Differentiation

**Rule 1: Power Rule** (Most common in exams)
```
If y = xⁿ, then dy/dx = nxⁿ⁻¹

Examples:
y = x³     →  dy/dx = 3x²
y = x⁵     →  dy/dx = 5x⁴
y = x      →  dy/dx = 1  (n=1, so 1×x⁰ = 1)
y = 1      →  dy/dx = 0  (constant disappears)
```

**Rule 2: Constant Multiple Rule**
```
If y = kxⁿ, then dy/dx = knxⁿ⁻¹

Examples:
y = 3x²    →  dy/dx = 6x
y = 5x⁴    →  dy/dx = 20x³
y = 7x     →  dy/dx = 7
```

**Rule 3: Sum/Difference Rule**
```
If y = f(x) + g(x), then dy/dx = f'(x) + g'(x)
(Differentiate each term separately)

Example:
y = 3x² + 5x + 2
dy/dx = 6x + 5 + 0 = 6x + 5
```

**Rule 4: Product Rule**
```
If y = u × v, then dy/dx = u(dv/dx) + v(du/dx)

Example: y = x²(2x + 3)
u = x²,  du/dx = 2x
v = (2x+3), dv/dx = 2
dy/dx = x²(2) + (2x+3)(2x) = 2x² + 4x² + 6x = 6x² + 6x
```

**Rule 5: Chain Rule**
```
If y = [f(x)]ⁿ, then dy/dx = n[f(x)]ⁿ⁻¹ × f'(x)

Example: y = (3x + 2)⁴
dy/dx = 4(3x + 2)³ × 3 = 12(3x + 2)³
```

---

### Concept 3: Maximum and Minimum Points

**Finding Stationary Points** (Where gradient = 0):
```
Step 1: Find dy/dx
Step 2: Set dy/dx = 0 and solve for x
Step 3: Find y by substituting x back into original equation
Step 4: Find d²y/dx² (second derivative) to classify:
        - d²y/dx² < 0  → Maximum point
        - d²y/dx² > 0  → Minimum point
        - d²y/dx² = 0  → Point of inflection
```

---

### Concept 4: Applications of Differentiation

**Gradient of a Curve at a Point**:
```
Find dy/dx, then substitute the x-value of the point

Example: y = x² + 3x, find gradient at x = 2
dy/dx = 2x + 3
At x = 2: gradient = 2(2) + 3 = 7
```

**Velocity and Acceleration** (rates of change):
```
If s = displacement, t = time:
Velocity = ds/dt      (rate of change of displacement)
Acceleration = dv/dt = d²s/dt²  (rate of change of velocity)
```

---

## 2. SAMPLE PROBLEMS (5 Increasing Difficulty)

### Problem 1 (EASY – Power Rule)
**Q**: Differentiate y = x⁴ with respect to x.

**Options**:
A) x³
B) 4x³ ← **CORRECT**
C) 4x⁵
D) x⁵

**Solution**:
```
y = x⁴
Power Rule: dy/dx = n × xⁿ⁻¹
dy/dx = 4 × x⁴⁻¹ = 4x³
```

**Key Concept**: Power rule → bring down the power, reduce power by 1

---

### Problem 2 (EASY – Sum Rule)
**Q**: Find dy/dx if y = 3x² + 2x – 5

**Options**:
A) 3x + 2
B) 6x + 2 ← **CORRECT**
C) 6x² + 2
D) 3x² + 2

**Solution**:
```
y = 3x² + 2x – 5
dy/dx = d/dx(3x²) + d/dx(2x) + d/dx(–5)
dy/dx = 6x + 2 + 0
dy/dx = 6x + 2
```

**Key Concept**: Differentiate each term separately; constants disappear

---

### Problem 3 (MEDIUM – Gradient at a Point)
**Q**: Find the gradient of the curve y = x³ – 4x + 1 at the point where x = 2.

**Options**:
A) 4
B) 8 ← **CORRECT**
C) 12
D) –4

**Solution**:
```
y = x³ – 4x + 1
dy/dx = 3x² – 4

At x = 2:
gradient = 3(2)² – 4
         = 3(4) – 4
         = 12 – 4
         = 8
```

**Key Concept**: Find dy/dx first, then substitute the given x-value

---

### Problem 4 (MEDIUM – Stationary Points)
**Q**: Find the x-coordinate of the stationary point of y = x² – 6x + 8.

**Options**:
A) 2
B) 3 ← **CORRECT**
C) 6
D) –3

**Solution**:
```
y = x² – 6x + 8
dy/dx = 2x – 6

Set dy/dx = 0 (stationary point):
2x – 6 = 0
2x = 6
x = 3

Check: d²y/dx² = 2 > 0  → Minimum point at x = 3
y = (3)² – 6(3) + 8 = 9 – 18 + 8 = –1
Minimum point is (3, –1)
```

**Key Concept**: Stationary point: set dy/dx = 0 and solve for x

---

### Problem 5 (HARD – Chain Rule Application)
**Q**: Differentiate y = (2x³ + 5)⁴

**Options**:
A) 4(2x³ + 5)³
B) 6x²(2x³ + 5)³
C) 24x²(2x³ + 5)³ ← **CORRECT**
D) 4x(2x³ + 5)⁴

**Solution**:
```
y = (2x³ + 5)⁴
Let u = 2x³ + 5, so y = u⁴

Chain Rule: dy/dx = (dy/du) × (du/dx)
dy/du = 4u³ = 4(2x³ + 5)³
du/dx = 6x²

dy/dx = 4(2x³ + 5)³ × 6x²
dy/dx = 24x²(2x³ + 5)³
```

**Key Concept**: Chain rule = differentiate outer function × differentiate inner function

---

## 3. COMMON MISTAKES IN DIFFERENTIATION

| Mistake | Example | Correct Approach |
|---------|---------|-----------------|
| Not reducing the power | y=x³ → dy/dx = 3x³ | Power reduces by 1: dy/dx = 3x² |
| Forgetting constants become 0 | d/dx(7) = 7x | Constants differentiate to 0: d/dx(7) = 0 |
| Adding instead of multiplying in power rule | y=4x² → dy/dx = 4+2=6 | Multiply: 4×2 = 8, so dy/dx = 8x |
| Not substituting x-value for gradient | Finding dy/dx only | Must substitute x-value to get specific gradient |
| Wrong chain rule application | Only differentiating outer function | Must multiply by derivative of inner function |

---

## 4. KEY DIAGRAMS (To Understand)

### Diagram 1: Power Rule Visual
```
y = axⁿ
       ↓
dy/dx = n × a × xⁿ⁻¹
          ↑               ↑
   bring down power    reduce power by 1

Examples:
y = x⁵   →  5x⁴
y = 3x²   →  6x
y = 7x    →  7
y = 9     →  0
```

### Diagram 2: Maximum vs Minimum
```
         Maximum point
              ∩
             / \
            /   \
       →  /     \   →
                  \
dy/dx: + | 0 | –     (positive → zero → negative at maximum)

              ∪
       \   /
        \ /
         V          dy/dx: – | 0 | +  (at minimum)

d²y/dx² < 0 = Maximum
d²y/dx² > 0 = Minimum
```

### Diagram 3: Chain Rule Breakdown
```
y = [inner function]ⁿ

dy/dx = n × [inner function]ⁿ⁻¹ × d/dx(inner function)
          ↑                              ↑
  outer derivative                  inner derivative
```

---

## 5. EXAM QUICK TIPS

**Tip 1**: **Power rule is 90% of differentiation in JAMB**
- y = xⁿ → dy/dx = nxⁿ⁻¹
- Practice this until automatic

**Tip 2**: **Constants always differentiate to zero**
- d/dx(5) = 0
- d/dx(100) = 0

**Tip 3**: **Gradient at a point = find dy/dx, then substitute x-value**
- dy/dx gives the gradient FORMULA
- Substituting x gives the gradient VALUE at that point

**Tip 4**: **Stationary points: set dy/dx = 0**
- Solve for x → gives the x-coordinate(s)
- Use second derivative to classify (max or min)

**Tip 5**: **Chain rule: multiply by inner derivative**
- y = (3x + 1)⁵ → dy/dx = 5(3x+1)⁴ × 3 = 15(3x+1)⁴
- Never forget the "× 3" (inner derivative)

---

## 6. WHAT TO MEMORIZE

**MUST MEMORIZE**:
```
Power Rule: y = axⁿ → dy/dx = naxⁿ⁻¹

Sum Rule: d/dx(f + g) = f'(x) + g'(x)

Chain Rule: y = [f(x)]ⁿ → dy/dx = n[f(x)]ⁿ⁻¹ × f'(x)

Product Rule: y = uv → dy/dx = u(dv/dx) + v(du/dx)

Stationary Points:
- Set dy/dx = 0 → solve for x
- d²y/dx² < 0 → Maximum
- d²y/dx² > 0 → Minimum

Constants → 0 when differentiated
```

---

## 7. PRACTICE DRILLS (Do Daily!)

**Drill 1**: Differentiate 5 polynomial functions using power rule (5 minutes)
→ Target: 100% accuracy

**Drill 2**: Find gradient of 3 curves at specific points (5 minutes)
→ Target: Correct substitution, correct answers

**Drill 3**: Find stationary points and classify as max/min for 2 functions (10 minutes)
→ Target: Correct dy/dx, correct classification

**Drill 4**: Mixed differentiation questions (10 in 15 minutes)
→ Target: 8+ correct (80%+)

---

## 8. REAL JAMB/WAEC DIFFERENTIATION PATTERNS

**Pattern 1**: "Differentiate y = axⁿ + bxᵐ + c"
- Apply power rule to each term

**Pattern 2**: "Find the gradient at x = k"
- Differentiate, then substitute x = k

**Pattern 3**: "Find stationary/turning point of y = f(x)"
- Set dy/dx = 0, solve for x

**Pattern 4**: "Classify turning point as maximum or minimum"
- Find d²y/dx², check sign

**Pattern 5**: "Differentiate y = (ax + b)ⁿ"
- Apply chain rule

---

## 9. LEARNING TIMELINE (7-Day Mastery)

**Day 1**: Power rule + sum rule, simple polynomials (1.5 hours)
**Day 2**: Constants, constant multiples, more practice (1.5 hours)
**Day 3**: Gradient of a curve at a point (1.5 hours)
**Day 4**: Stationary points (max and min) (2 hours)
**Day 5**: Chain rule and product rule (2 hours)
**Day 6**: Review all + drill (2 hours)
**Day 7**: Full mock calculus section (1.5 hours)

**Total Time**: 12 hours for mastery
**ROI**: 4-6 JAMB questions = 4-6 points

---

## 📊 SUCCESS CRITERIA

✅ Differentiate any polynomial using power rule in under 30 seconds per term
✅ Find the gradient of a curve at any given point
✅ Find stationary points and classify as maximum or minimum
✅ Apply chain rule to composite functions
✅ Use differentiation in rates of change (velocity/acceleration)
✅ Score 80%+ on mixed differentiation quiz

**If you hit all 6, you'll ace calculus questions!** 🚀

---

**Created**: March 29, 2026
**Class**: SS3
**For**: JAMB/WAEC/NECO 2026 Candidates
**Subject Matter Expert Review**: PENDING
**Student Beta Testing**: PENDING
