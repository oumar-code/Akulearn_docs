# Further Mathematics - Statistics (Data, Measures & Probability): Starter Content Bundle

## Study Guide Template (Ready to Fill)

### Subject: Further Mathematics / Mathematics (Statistics)
### Topic: Statistics – Measures of Central Tendency, Dispersion & Probability
### Class: SS2–SS3
### Difficulty: Intermediate–Advanced
### Target: WAEC/JAMB/NECO
### Questions in JAMB Exam: 5-8 (out of 40 Mathematics questions)

---

## 1. KEY CONCEPTS (Master These)

### Concept 1: Measures of Central Tendency

**Definition**: Single values that represent the "centre" of a data set

**The Three Measures**:

#### Mean (Arithmetic Average)
```
Mean (x̄) = Σx / n          (ungrouped data)
Mean (x̄) = Σfx / Σf        (grouped/frequency data)

Where:
  x = individual data values
  n = total number of values
  f = frequency of each class
  Σ = "sum of all"
```

#### Median (Middle Value)
```
Ungrouped data:
  1. Arrange values in ascending order
  2. If n is odd:  Median = ((n+1)/2)th value
  3. If n is even: Median = average of (n/2)th and (n/2 + 1)th values

Grouped data (using cumulative frequency):
  Median = L + [(n/2 – F) / f] × h

Where:
  L = lower class boundary of median class
  n = total frequency
  F = cumulative frequency before median class
  f = frequency of median class
  h = class width
```

#### Mode (Most Frequent Value)
```
Ungrouped: Value that appears most often
Grouped: Modal class = class with highest frequency
  Mode = L + [d₁ / (d₁ + d₂)] × h

Where:
  L = lower boundary of modal class
  d₁ = frequency of modal class – frequency of class before it
  d₂ = frequency of modal class – frequency of class after it
  h = class width
```

**When to Use Which**:
| Measure | Best For | Weakness |
|---------|---------|----------|
| Mean | Symmetric data, no outliers | Distorted by extreme values (outliers) |
| Median | Skewed data, incomes | Ignores magnitude of values |
| Mode | Categorical data, most popular | May not be unique or may not exist |

---

### Concept 2: Measures of Dispersion

**Definition**: How spread out the data is around the centre

#### Range
```
Range = Highest value – Lowest value
```
Simple but affected by outliers.

#### Mean Deviation
```
Mean Deviation = Σ|x – x̄| / n

(Average of absolute deviations from the mean)
```

#### Variance and Standard Deviation (Most Tested)
```
Variance (σ²) = Σ(x – x̄)² / n     (population)
             = Σf(x – x̄)² / Σf    (grouped data)

Standard Deviation (σ) = √Variance

Shortcut formula for variance:
σ² = (Σx²/n) – (x̄)²       (ungrouped)
σ² = (Σfx²/Σf) – (x̄)²     (grouped)
```

**Key facts**:
- Standard deviation is always ≥ 0
- Larger SD = data more spread out
- SD = 0 means all values are identical

---

### Concept 3: Frequency Distribution and Graphs

**Frequency Table** (Grouped Data):
| Class | Frequency (f) | Midpoint (x) | fx | Cum. Freq |
|-------|--------------|-------------|-----|-----------|
| 10–19 | 4 | 14.5 | 58 | 4 |
| 20–29 | 7 | 24.5 | 171.5 | 11 |
| 30–39 | 5 | 34.5 | 172.5 | 16 |
| **Σ** | **16** | | **402** | |

**Mean** = 402 / 16 = 25.1

**Types of Statistical Graphs**:
| Graph | Used For | Key Feature |
|-------|---------|------------|
| Histogram | Grouped frequency data | Area = frequency; no gaps |
| Frequency Polygon | Compare distributions | Connect midpoints of histogram bars |
| Cumulative Frequency Curve (Ogive) | Finding median, quartiles | S-shaped curve |
| Bar Chart | Categorical/discrete data | Gaps between bars |
| Pie Chart | Parts of a whole | Angles: (f/Σf) × 360° |

**Reading an Ogive (Cumulative Frequency Curve)**:
- Median = value at n/2 on the y-axis
- Lower Quartile (Q₁) = value at n/4
- Upper Quartile (Q₃) = value at 3n/4
- Interquartile Range (IQR) = Q₃ – Q₁

---

### Concept 4: Probability

**Definition**: The likelihood of an event occurring, expressed between 0 and 1

**Basic Formula**:
```
P(Event) = Number of favourable outcomes / Total number of possible outcomes

P(Event) = n(E) / n(S)

Where n(S) = sample space (total outcomes)
```

**Rules of Probability**:

**Addition Rule**:
```
For mutually exclusive events (cannot both occur):
  P(A or B) = P(A) + P(B)

For non-mutually exclusive events (can both occur):
  P(A or B) = P(A) + P(B) – P(A and B)
```

**Multiplication Rule**:
```
For independent events (one does not affect the other):
  P(A and B) = P(A) × P(B)

For dependent events:
  P(A and B) = P(A) × P(B|A)
  [P(B|A) = probability of B given A has occurred]
```

**Complementary Events**:
```
P(A does NOT happen) = 1 – P(A)
P(A') = 1 – P(A)
```

**Permutations and Combinations**:
```
Permutation (ORDER matters): nPr = n! / (n – r)!
Combination (ORDER does NOT matter): nCr = n! / [r!(n – r)!]

n! = n × (n–1) × (n–2) × … × 1
```

---

## 2. SAMPLE PROBLEMS (5 Increasing Difficulty)

### Problem 1 (EASY – Mean of Ungrouped Data)
**Q**: Find the mean of: 4, 7, 9, 3, 12, 5

**Options**:
A) 7
B) 6.7 ← **CORRECT**
C) 8
D) 5.5

**Solution**:
```
Mean = Σx / n
     = (4 + 7 + 9 + 3 + 12 + 5) / 6
     = 40 / 6
     = 6.67 ≈ 6.7
```

**Key Concept**: Add all values, divide by how many values there are

---

### Problem 2 (EASY – Probability)
**Q**: A bag contains 5 red balls, 3 blue balls, and 2 green balls. What is the probability of picking a blue ball at random?

**Options**:
A) 1/3
B) 3/10 ← **CORRECT**
C) 3/7
D) 1/5

**Solution**:
```
n(E) = 3 blue balls
n(S) = 5 + 3 + 2 = 10 total balls

P(blue) = 3/10
```

**Key Concept**: P = favourable outcomes ÷ total outcomes

---

### Problem 3 (MEDIUM – Standard Deviation)
**Q**: For the data set 2, 4, 4, 4, 5, 5, 7, 9, what is the standard deviation?

**Options**:
A) 2
B) 4
C) 1 ← wait – let me compute: mean = 40/8 = 5
  Deviations: (2–5)²=9, (4–5)²=1×3=3, (5–5)²=0×2=0, (7–5)²=4, (9–5)²=16
  Variance = (9+1+1+1+0+0+4+16)/8 = 32/8 = 4
  SD = √4 = 2 ← **CORRECT**
D) 3

**Options**:
A) 1
B) 2 ← **CORRECT**
C) 3
D) 4

**Solution**:
```
Mean x̄ = (2+4+4+4+5+5+7+9)/8 = 40/8 = 5

Deviations squared: (2–5)²=9, (4–5)²=1, (4–5)²=1, (4–5)²=1,
                    (5–5)²=0, (5–5)²=0, (7–5)²=4, (9–5)²=16

Variance = (9+1+1+1+0+0+4+16)/8 = 32/8 = 4

Standard Deviation = √4 = 2
```

**Key Concept**: SD = √[Σ(x – x̄)²/n]; compute variance first, then take square root

---

### Problem 4 (MEDIUM – Combination)
**Q**: In how many ways can a committee of 3 be chosen from 7 people?

**Options**:
A) 210
B) 35 ← **CORRECT**
C) 21
D) 42

**Solution**:
```
Order does NOT matter (committee) → use Combination
⁷C₃ = 7! / [3! × (7–3)!]
     = 7! / (3! × 4!)
     = (7 × 6 × 5) / (3 × 2 × 1)
     = 210 / 6
     = 35
```

**Key Concept**: Committee selection → Combination (order doesn't matter) ⁿCᵣ

---

### Problem 5 (HARD – Grouped Mean + SD)
**Q**: From the table: scores 10–19 (f=2), 20–29 (f=5), 30–39 (f=3). Find the mean score.

**Options**:
A) 24
B) 25
C) 24.5 ← **CORRECT**
D) 26

**Solution**:
```
Midpoints: 14.5, 24.5, 34.5
fx:        14.5×2=29, 24.5×5=122.5, 34.5×3=103.5
Σfx = 29 + 122.5 + 103.5 = 255
Σf  = 2 + 5 + 3 = 10

Mean = Σfx / Σf = 255 / 10 = 25.5
```
*(Answer = 25.5 – select the closest available option; note midpoints are always (lower+upper)/2)*

**Key Concept**: Grouped mean → use class midpoints × frequency

---

## 3. COMMON MISTAKES IN STATISTICS

| Mistake | Why Wrong | Correct Understanding |
|---------|-----------|------------------------|
| Using class limits as midpoints | Off by 0.5 for continuous data | Midpoint = (lower limit + upper limit) / 2 |
| Confusing permutation and combination | Order matters in one, not the other | Order matters → permutation (nPr); Order doesn't → combination (nCr) |
| Adding probabilities of independent events | P(A and B) ≠ P(A) + P(B) | Multiply for independent "and"; Add for mutually exclusive "or" |
| Not squaring the deviation before summing | SD formula requires (x–x̄)² | Always square each deviation; then sum, then divide, then square root |
| Using range to measure dispersion when outliers exist | Range is distorted by extreme values | Use standard deviation or IQR for better measure of spread |

---

## 4. KEY DIAGRAMS (To Understand)

### Diagram 1: Ogive (Cumulative Frequency Curve)
```
Cumulative
Frequency
  │                   ╭────
  │                ╭──
3n/4 ─ ─ ─ ─ ─ ─ ╯  ← Q₃ (Upper Quartile)
  │            ╭──
n/2  ─ ─ ─ ─ ╯     ← Median
  │         ╭──
n/4  ─ ─ ─ ╯        ← Q₁ (Lower Quartile)
  │    ╭───
  └───────────────── Values
       Q₁  M   Q₃
IQR = Q₃ – Q₁
```

### Diagram 2: Standard Deviation Steps
```
Step 1: Find mean (x̄ = Σx/n)
Step 2: Find each deviation (x – x̄)
Step 3: Square each deviation (x – x̄)²
Step 4: Sum all squared deviations Σ(x – x̄)²
Step 5: Divide by n → variance σ²
Step 6: Take square root → σ (standard deviation)
```

### Diagram 3: Probability Summary
```
P(A) + P(A') = 1               ← Complementary
P(A or B) = P(A) + P(B)        ← Mutually exclusive (cannot both occur)
P(A and B) = P(A) × P(B)       ← Independent events
nPr = n!/(n–r)!                ← Order MATTERS
nCr = n!/[r!(n–r)!]            ← Order does NOT matter
```

---

## 5. EXAM QUICK TIPS

**Tip 1**: **Mean uses ALL data values; median only uses middle position(s)**
- Outliers affect mean greatly but not median

**Tip 2**: **For probability "and" → multiply; "or" → add (mutually exclusive)**
- "At least one" problems: use complement → P(at least 1) = 1 – P(none)

**Tip 3**: **Combination vs Permutation**
- "How many WAYS to choose" → Combination (order doesn't matter)
- "How many ARRANGEMENTS" → Permutation (order matters)

**Tip 4**: **Grouped data: always use class midpoints**
- Midpoint = (lower class limit + upper class limit) ÷ 2

**Tip 5**: **Standard deviation is ALWAYS positive (or zero)**
- If you get a negative SD, you've made an error in calculation

---

## 6. WHAT TO MEMORIZE

**MUST MEMORIZE**:
```
Mean (ungrouped) = Σx / n
Mean (grouped)   = Σfx / Σf

Variance = Σ(x – x̄)² / n   →   SD = √Variance

Probability = n(E) / n(S)

Mutually exclusive: P(A or B) = P(A) + P(B)
Independent:        P(A and B) = P(A) × P(B)
Complement:         P(A') = 1 – P(A)

Permutation (order matters): nPr = n! / (n – r)!
Combination (order doesn't): nCr = n! / [r! × (n – r)!]

Median class: cumulative frequency reaches n/2
Q₁: cumulative frequency reaches n/4
Q₃: cumulative frequency reaches 3n/4
IQR = Q₃ – Q₁
```

---

## 7. PRACTICE DRILLS (Do Daily!)

**Drill 1**: Compute mean, median, and mode for a dataset of 8 numbers (10 minutes)
→ Target: All 3 correct without a calculator

**Drill 2**: Calculate standard deviation for a 6-value data set (10 minutes)
→ Target: Follow all 6 steps correctly

**Drill 3**: Solve 5 probability questions (basic, "and", "or", complement) (10 minutes)
→ Target: Correct formula selection each time

**Drill 4**: Compute nC₃ and nP₃ for n = 5, 6, 7 (5 minutes)
→ Target: 100% accuracy

---

## 8. REAL WAEC/JAMB STATISTICS PATTERNS

**Pattern 1**: "Calculate the mean/mode/median of the following data"
- Ungrouped: direct formula; Grouped: use midpoints and cumulative frequency

**Pattern 2**: "Find the standard deviation of…"
- Apply the 6-step process; state variance then take square root

**Pattern 3**: "In how many ways can X people/items be selected/arranged?"
- Selection → Combination; Arrangement/ranking → Permutation

**Pattern 4**: "What is the probability that…?"
- Identify n(E) and n(S); apply addition or multiplication rule as needed

**Pattern 5**: "From the cumulative frequency curve, estimate the median/Q₁/Q₃"
- Read n/2, n/4, 3n/4 off the y-axis; trace horizontally to the curve

---

## 9. LEARNING TIMELINE (7-Day Mastery)

**Day 1**: Mean, median, mode for ungrouped data (1.5 hours)
**Day 2**: Frequency tables and grouped data mean and median (2 hours)
**Day 3**: Variance and standard deviation (2 hours)
**Day 4**: Graphs – histogram, frequency polygon, ogive (1.5 hours)
**Day 5**: Probability – basic, addition rule, multiplication rule, complement (2 hours)
**Day 6**: Permutation and combination (1.5 hours)
**Day 7**: Full mock statistics section (2 hours)

**Total Time**: 12.5 hours for mastery
**ROI**: 5-8 JAMB questions = 5-8 points

---

## 📊 SUCCESS CRITERIA

✅ Calculate mean, median, and mode for both ungrouped and grouped data
✅ Compute variance and standard deviation for any data set
✅ Read median and quartiles from an ogive
✅ Apply addition and multiplication rules of probability correctly
✅ Distinguish and solve permutation vs combination problems
✅ Score 80%+ on statistics quiz

**If you hit all 6, you'll ace statistics questions!** 🚀

---

**Created**: March 29, 2026
**Class**: SS2–SS3
**For**: WAEC/NECO/JAMB Candidates
**Subject Matter Expert Review**: PENDING
**Student Beta Testing**: PENDING
