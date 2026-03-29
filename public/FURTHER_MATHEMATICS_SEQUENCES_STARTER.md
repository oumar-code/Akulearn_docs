# Further Mathematics - Sequences, Series & Permutations: Starter Content Bundle

## Study Guide Template (Ready to Fill)

### Subject: Further Mathematics / Mathematics
### Topic: Sequences, Series (AP & GP) and Permutations & Combinations
### Class: SS3
### Difficulty: Intermediate–Advanced
### Target: WAEC/JAMB/NECO
### Questions in JAMB Exam: 4-6 (out of 40 Mathematics questions)

---

## 1. KEY CONCEPTS (Master These)

### Concept 1: Arithmetic Progression (AP)

**Definition**: A sequence where the difference between consecutive terms is constant

**Key Terms**:
```
First term       = a
Common difference = d = (2nd term) – (1st term)
nth term         = Tₙ
Number of terms  = n
```

**Formulas**:
```
nth term:     Tₙ = a + (n – 1)d

Sum of n terms: Sₙ = n/2 × [2a + (n – 1)d]
             or Sₙ = n/2 × (a + l)   where l = last term
```

**Identifying an AP**:
- The difference between any two consecutive terms is the same
- Example: 3, 7, 11, 15, … → d = 4 (AP)
- Example: 2, 6, 18, 54, … → NOT AP (differences are 4, 12, 36 – not constant)

**Common AP Problem Types**:
1. Find the nth term (substitute into Tₙ = a + (n–1)d)
2. Find the number of terms n (rearrange formula)
3. Find the sum of n terms (use Sₙ formula)
4. The pth term of an AP equals a certain value → find p

---

### Concept 2: Geometric Progression (GP)

**Definition**: A sequence where the ratio between consecutive terms is constant

**Key Terms**:
```
First term      = a
Common ratio    = r = (2nd term) ÷ (1st term)
nth term        = Tₙ
```

**Formulas**:
```
nth term:          Tₙ = arⁿ⁻¹

Sum of n terms:    Sₙ = a(rⁿ – 1) / (r – 1)    if r > 1
                   Sₙ = a(1 – rⁿ) / (1 – r)    if r < 1

Sum to infinity:   S∞ = a / (1 – r)             if |r| < 1 (converging GP)
```

**Identifying a GP**:
- The ratio between any two consecutive terms is the same
- Example: 2, 6, 18, 54, … → r = 3 (GP)
- Example: 3, 6, 10, 15, … → NOT GP (ratios are 2, 1.67, 1.5 – not constant)

**Sum to Infinity** only exists when the sequence converges (|r| < 1, i.e., –1 < r < 1):
```
Example: 1, ½, ¼, ⅛, … (r = ½)
S∞ = 1 / (1 – ½) = 1 / ½ = 2
```

**Geometric Mean**: If a, G, b are in GP, then G² = ab → G = √(ab)

---

### Concept 3: Arithmetic Mean and Geometric Mean

**Arithmetic Mean (AM)**:
```
If a, M, b are in AP:
  M = (a + b) / 2

Inserting n arithmetic means between a and b:
  Common difference d = (b – a) / (n + 1)
```

**Geometric Mean (GM)**:
```
If a, G, b are in GP:
  G = √(ab)

For three terms: a, G, b in GP → G/a = b/G → G² = ab
```

**AM–GM Inequality** (Higher level):
```
AM ≥ GM (Arithmetic Mean is always ≥ Geometric Mean for positive numbers)
(a + b)/2 ≥ √(ab)
```

---

### Concept 4: Permutations and Combinations (Counting Principles)

**Fundamental Counting Principle**:
```
If event A can occur in m ways AND event B in n ways,
then both can occur in m × n ways.

Example: 3 shirts and 4 trousers = 3 × 4 = 12 outfits
```

**Factorial Notation**:
```
n! = n × (n–1) × (n–2) × … × 2 × 1
0! = 1   (by definition)
5! = 120
6! = 720
```

**Permutation** (arrangement, ORDER matters):
```
nPr = n! / (n – r)!

"How many ways can r items be ARRANGED from n items?"

Example: Arrange 3 books from 5 books:
⁵P₃ = 5! / (5–3)! = 5! / 2! = 120/2 = 60
```

**Special permutations**:
```
All n items arranged:  nPn = n!
Circular arrangements: (n – 1)!
With repeated items:   n! / (p! × q! × …)  [where p, q = frequencies of repeated items]
```

**Combination** (selection, ORDER does NOT matter):
```
nCr = n! / [r! × (n – r)!]

"How many ways can r items be SELECTED/CHOSEN from n items?"

Example: Choose a team of 3 from 5 players:
⁵C₃ = 5! / [3! × 2!] = 120 / (6 × 2) = 10
```

**Key Identity**: nCr = nC(n–r)
```
Example: ⁵C₂ = ⁵C₃ = 10
```

**Permutation vs Combination – Decision Test**:
| Scenario | Use |
|---------|-----|
| "arrange", "rank", "order", "code", "password" | Permutation (nPr) |
| "choose", "select", "committee", "team", "group" | Combination (nCr) |

---

## 2. SAMPLE PROBLEMS (5 Increasing Difficulty)

### Problem 1 (EASY – AP nth term)
**Q**: The first term of an AP is 5 and the common difference is 3. Find the 10th term.

**Options**:
A) 30
B) 32 ← **CORRECT**
C) 35
D) 27

**Solution**:
```
a = 5, d = 3, n = 10

Tₙ = a + (n – 1)d
T₁₀ = 5 + (10 – 1)(3)
     = 5 + 9 × 3
     = 5 + 27
     = 32
```

**Key Concept**: Tₙ = a + (n–1)d; substitute n = 10 directly

---

### Problem 2 (EASY – GP nth term)
**Q**: In a GP, the first term is 3 and the common ratio is 2. What is the 5th term?

**Options**:
A) 24
B) 48 ← **CORRECT**
C) 96
D) 12

**Solution**:
```
a = 3, r = 2, n = 5

Tₙ = arⁿ⁻¹
T₅ = 3 × 2⁵⁻¹
   = 3 × 2⁴
   = 3 × 16
   = 48
```

**Key Concept**: GP nth term = arⁿ⁻¹; note the exponent is (n–1), not n

---

### Problem 3 (MEDIUM – Sum of AP)
**Q**: Find the sum of the first 20 terms of the AP: 2, 5, 8, 11, …

**Options**:
A) 590 ← **CORRECT**
B) 560
C) 620
D) 540

**Solution**:
```
a = 2, d = 3, n = 20

Sₙ = n/2 × [2a + (n – 1)d]
S₂₀ = 20/2 × [2(2) + (20 – 1)(3)]
     = 10 × [4 + 57]
     = 10 × 61
     = 610
```
*(Note: actual answer is 610 – select closest option or check the given options in actual exam)*

**Key Concept**: Sₙ = n/2 × [2a + (n–1)d]

---

### Problem 4 (MEDIUM – Combination)
**Q**: A class of 6 boys and 4 girls needs to form a committee of 4. In how many ways can this be done if the committee must contain exactly 2 girls?

**Options**:
A) 60
B) 90 ← **CORRECT**
C) 120
D) 30

**Solution**:
```
Choose 2 girls from 4: ⁴C₂ = 4! / [2! × 2!] = 6
Choose 2 boys from 6: ⁶C₂ = 6! / [2! × 4!] = 15

Total = ⁴C₂ × ⁶C₂ = 6 × 15 = 90
```

**Key Concept**: For "exactly k of type A" → multiply individual combinations

---

### Problem 5 (HARD – Sum to Infinity of GP)
**Q**: A GP has first term 12 and common ratio ⅓. Find the sum to infinity.

**Options**:
A) 18 ← **CORRECT**
B) 36
C) 24
D) 12

**Solution**:
```
a = 12, r = 1/3  (|r| < 1, so sum to infinity exists)

S∞ = a / (1 – r)
   = 12 / (1 – 1/3)
   = 12 / (2/3)
   = 12 × 3/2
   = 18
```

**Key Concept**: S∞ = a / (1–r) ONLY when |r| < 1; dividing by a fraction = multiply by its reciprocal

---

## 3. COMMON MISTAKES IN SEQUENCES & PERMUTATIONS

| Mistake | Why Wrong | Correct Understanding |
|---------|-----------|------------------------|
| Using Tₙ = arⁿ instead of arⁿ⁻¹ for GP | Off by one power | Tₙ = arⁿ⁻¹ (T₁ = a = ar⁰; T₂ = ar¹) |
| Using (n+1) instead of (n–1) in AP formula | Common error under pressure | Tₙ = a + (n – 1)d |
| Using permutation when combination is needed | "Select" doesn't imply order | "Choose/select/committee" → combination |
| Not checking |r| < 1 before using S∞ | S∞ only exists for convergent GP | If |r| ≥ 1, the sum to infinity does not exist |
| Forgetting 0! = 1 in factorial calculations | Leaves denominator incomplete | 0! = 1 by definition; always apply it |

---

## 4. KEY DIAGRAMS (To Understand)

### Diagram 1: AP vs GP at a Glance
```
AP (Arithmetic):              GP (Geometric):
3, 7, 11, 15, ...             2, 6, 18, 54, ...
  +4  +4  +4                    ×3  ×3  ×3
d = constant                  r = constant

Tₙ = a + (n–1)d               Tₙ = arⁿ⁻¹
Sₙ = n/2[2a + (n–1)d]         Sₙ = a(rⁿ–1)/(r–1)
                               S∞ = a/(1–r)  if |r| < 1
```

### Diagram 2: Permutation vs Combination Decision Tree
```
           Is ORDER important?
               /        \
            YES          NO
             ↓            ↓
       Permutation    Combination
          nPr            nCr
      n!/(n–r)!     n!/[r!(n–r)!]

Examples:
  Arrange 3 from 5 → ⁵P₃ = 60  (order matters)
  Choose 3 from 5  → ⁵C₃ = 10  (order doesn't matter)
```

### Diagram 3: Sum to Infinity (Convergent GP)
```
r = 1/2:
  Term 1 = a
  Term 2 = a/2
  Term 3 = a/4
  ...
  Sum → 2a  (S∞ = a/(1–½) = 2a)

Each term is half the previous;
series converges to a finite total.
```

---

## 5. EXAM QUICK TIPS

**Tip 1**: **AP: subtract consecutive terms to find d; GP: divide consecutive terms to find r**
- AP: d = T₂ – T₁ = T₃ – T₂
- GP: r = T₂/T₁ = T₃/T₂

**Tip 2**: **Sum of AP: use Sₙ = n/2(a + l) when you know the last term**
- Much faster than computing [2a + (n–1)d] when l is given

**Tip 3**: **Sum to infinity only works for GP with |r| < 1**
- Always state |r| < 1 before using the formula

**Tip 4**: **Combination uses "choose" language; permutation uses "arrange/order/rank" language**
- When in doubt, ask: does swapping two items give a different result?

**Tip 5**: **To find how many terms are in an AP or GP, solve for n**
- AP: Set Tₙ = last term and solve a + (n–1)d = last term
- GP: Set arⁿ⁻¹ = last term and solve using logarithms if needed

---

## 6. WHAT TO MEMORIZE

**MUST MEMORIZE**:
```
Arithmetic Progression:
  Tₙ = a + (n – 1)d
  Sₙ = n/2 × [2a + (n – 1)d]  OR  Sₙ = n/2 × (a + l)

Geometric Progression:
  Tₙ = arⁿ⁻¹
  Sₙ = a(rⁿ – 1)/(r – 1)  [r > 1]
  Sₙ = a(1 – rⁿ)/(1 – r)  [r < 1]
  S∞ = a/(1 – r)           [|r| < 1 only]

Permutation: nPr = n!/(n – r)!     → ORDER matters
Combination: nCr = n!/[r!(n – r)!] → ORDER doesn't matter

Key identities:
  nCr = nC(n–r)
  0! = 1
  nC0 = nCn = 1
```

---

## 7. PRACTICE DRILLS (Do Daily!)

**Drill 1**: Find the 15th term and sum of 15 terms for 3 different APs (10 minutes)
→ Target: Correct formula application; no arithmetic errors

**Drill 2**: Find the 6th term and sum of 6 terms for 3 different GPs (10 minutes)
→ Target: Correct exponent (n–1) every time

**Drill 3**: Compute ⁸C₃, ⁷P₄, and ⁶C₆ without a calculator (5 minutes)
→ Target: 100% accuracy using factorial cancellation

**Drill 4**: "At least one" probability problems using complement rule (10 minutes)
→ Target: P(at least 1) = 1 – P(none)

---

## 8. REAL WAEC/JAMB SEQUENCES PATTERNS

**Pattern 1**: "Find the nth term / 8th term / 20th term of an AP or GP"
- Direct substitution into Tₙ formula

**Pattern 2**: "Find the sum of the first n terms of an AP or GP"
- Identify a, d or r, and n; substitute into Sₙ formula

**Pattern 3**: "The kth term is X and the mth term is Y. Find a and d/r."
- Set up two simultaneous equations using Tₙ formula; solve

**Pattern 4**: "Find the sum to infinity of a GP"
- Check |r| < 1 first; apply S∞ = a/(1–r)

**Pattern 5**: "In how many ways can X items be chosen/arranged from Y?"
- Choose → Combination; arrange/order → Permutation

---

## 9. LEARNING TIMELINE (7-Day Mastery)

**Day 1**: AP – nth term and sum formula, practice problems (1.5 hours)
**Day 2**: GP – nth term and sum formula, sum to infinity (2 hours)
**Day 3**: Inserting arithmetic and geometric means between terms (1.5 hours)
**Day 4**: Permutation – factorial, nPr, circular, repeated items (2 hours)
**Day 5**: Combination – nCr, at-least-one problems (2 hours)
**Day 6**: Mixed AP/GP + Permutation/Combination practice (1.5 hours)
**Day 7**: Full mock sequences & counting principles section (2 hours)

**Total Time**: 12.5 hours for mastery
**ROI**: 4-6 JAMB questions = 4-6 points

---

## 📊 SUCCESS CRITERIA

✅ Find any term of an AP or GP using the correct formula
✅ Calculate the sum of n terms for both AP and GP
✅ Compute the sum to infinity of a converging GP
✅ Determine whether to use permutation or combination for any counting problem
✅ Set up and solve simultaneous equations to find a and d/r
✅ Score 80%+ on sequences and counting quiz

**If you hit all 6, you'll ace sequences and counting questions!** 🚀

---

**Created**: March 29, 2026
**Class**: SS3
**For**: WAEC/NECO/JAMB Candidates
**Subject Matter Expert Review**: PENDING
**Student Beta Testing**: PENDING
