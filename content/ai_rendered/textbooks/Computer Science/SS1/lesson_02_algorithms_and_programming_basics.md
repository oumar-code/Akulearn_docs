# Algorithms and Programming Basics

**Computer Science | SS1 | Unit 1: Algorithms and Programming Basics**

---

## Lesson Information

- **Duration**: 90 minutes
- **Estimated Pages**: 13
- **NERDC Code**: CS.SS1.2.1-2.3
- **NERDC Description**: Algorithms, flowcharts, pseudocode, introductory programming
- **WAEC Topic**: Algorithms and Problem Solving (10%)
- **Learning Level**: Foundational

## Learning Objectives

By the end of this lesson, you will be able to:

1. Define algorithm and outline its properties (finite, effective, ordered)
2. Represent simple tasks using step-by-step instructions, flowcharts, and pseudocode
3. Identify basic data types and variables
4. Use sequence, selection, and iteration constructs in pseudocode
5. Trace simple algorithms for correctness and output

## Prerequisites

Before starting this lesson, ensure you understand:

- Basic computer literacy
- Comfort with arithmetic and logical thinking
- Understanding of input/output from prior lesson

## Content


### 2.1: What Is an Algorithm?

*Duration: 20 minutes*

**Algorithm**: finite, ordered steps to solve a problem. Properties: correctness, efficiency, clarity. Examples: cooking recipe, ATM transaction sequence (insert card → enter PIN → select amount → dispense cash).


### 2.2: Representing Algorithms: Text and Diagrams

*Duration: 22 minutes*

**Natural language**: plain steps. **Pseudocode**: structured, language-agnostic; uses INPUT, OUTPUT, IF, WHILE. **Flowcharts**: start/end, process, decision, input/output symbols; arrows show flow. 

**Nigerian context**: Schools use flowcharts on paper when computers are limited; use pseudocode to prepare before coding.


### 2.3: Data Types, Variables, and Expressions

*Duration: 24 minutes*

Common types: integer, real/float, string, Boolean. Variables store values with names; assignment uses ← or = depending on notation. Expressions combine operators: arithmetic (+, -, *, /, mod), relational (<, >, =, !=), logical (AND, OR, NOT).


### 2.4: Control Structures: Sequence, Selection, Iteration

*Duration: 24 minutes*

**Sequence**: steps in order. **Selection**: IF/ELSE or CASE for decisions (e.g., PIN correct?). **Iteration**: loops (FOR, WHILE, REPEAT-UNTIL) for repetition (e.g., count students). 
Include simple input/output statements and counters.


## Worked Examples


### Example 2.1: Pseudocode for Even/Odd

**Context**: Determine if a number is even or odd.

**Problem**: Write pseudocode using selection.

**Solution**:
```
INPUT N; IF N mod 2 = 0 THEN OUTPUT "Even" ELSE OUTPUT "Odd"; ENDIF
```

**Skills Tested**: Selection, Modulo operator, Input/output


### Example 2.2: Flowchart for Average of 3 Scores

**Context**: Compute average of three test scores.

**Problem**: Represent with a flowchart.

**Solution**:
```
Start → Input S1,S2,S3 → Sum = S1+S2+S3 → Avg = Sum/3 → Output Avg → End.
```

**Skills Tested**: Sequence, Arithmetic, Flowchart mapping


### Example 2.3: Counting Students with For Loop

**Context**: Count 1 to 5 students.

**Problem**: Use iteration to print numbers 1..5.

**Solution**:
```
FOR i ← 1 TO 5 DO OUTPUT i; ENDFOR
```

**Skills Tested**: Iteration, Loop bounds


## Practice Problems


### Basic Level


**2.1.B**: Define algorithm in one sentence.

> **Answer**: A finite, ordered set of steps to solve a problem.

> **Explanation**: Core definition.


**2.2.B**: List three flowchart symbols.

> **Answer**: Start/End (terminator), Process, Decision, Input/Output.

> **Explanation**: Common symbols.


**2.3.B**: Name two primitive data types.

> **Answer**: Integer, Boolean (others: real, string).

> **Explanation**: Simple recall.


### Core Level


**2.4.C**: Write pseudocode to input two numbers and output their sum.

> **Answer**: INPUT A,B; SUM ← A+B; OUTPUT SUM

> **Explanation**: Sequence and arithmetic.


**2.5.C**: Convert this to a decision: If temperature > 30, print "Hot", else print "Mild".

> **Answer**: IF temp > 30 THEN OUTPUT "Hot" ELSE OUTPUT "Mild" ENDIF

> **Explanation**: Selection pattern.


**2.6.C**: Describe difference between WHILE and FOR loops in plain terms.

> **Answer**: FOR: known iteration count/range; WHILE: repeat while condition true, count may be unknown.

> **Explanation**: Loop intent.


### Challenge Level


**2.7.CH**: Trace: N=7; IF N mod 2 = 0 THEN print Even ELSE print Odd.

> **Answer**: Outputs Odd.

> **Explanation**: Modulo trace.


**2.8.CH**: Write a REPEAT-UNTIL loop to keep asking for PIN until correct (1234).

> **Answer**: REPEAT INPUT pin UNTIL pin = 1234

> **Explanation**: Post-condition loop.


**2.9.CH**: State two reasons pseudocode is useful before coding on limited lab time.

> **Answer**: Language-agnostic planning; easy to review on paper; reduces coding errors/time when PCs are few.

> **Explanation**: Planning benefits.


**2.10.CH**: Given: FOR i=1 TO 3 PRINT i*i. List outputs.

> **Answer**: 1, 4, 9.

> **Explanation**: Loop/output trace.


## Glossary


**Algorithm**: Finite, ordered steps to solve a problem.

- *Example*: Counting students algorithm.


**Pseudocode**: Structured, language-neutral way to write algorithms.

- *Example*: IF score >= 50 THEN PASS


**Flowchart**: Diagram showing algorithm flow with standard symbols.

- *Example*: Decision diamond for PIN correct?


**Variable**: Named storage for a value that can change.

- *Example*: count ← 0


**Iteration**: Repeating steps using loops.

- *Example*: FOR i=1 TO 10


## Assessment


### Quick Checks (Understanding Check)

1. State two properties of an algorithm.

2. What symbol denotes decision in a flowchart?

3. Give an example of a Boolean expression.

4. Name the three basic control structures.

5. Why use pseudocode?


### End-of-Lesson Quiz


**1. An algorithm must be:**

- Infinite

- Random

- Finite

- Hardware

> **Correct Answer**: Finite


**2. Flowchart decision symbol shape is:**

- Rectangle

- Oval

- Diamond

- Parallelogram

> **Correct Answer**: Diamond


**3. Selection is implemented with:**

- FOR

- IF/ELSE

- PRINT

- INPUT

> **Correct Answer**: IF/ELSE


**4. Data type for TRUE/FALSE:**

- String

- Boolean

- Integer

- Float

> **Correct Answer**: Boolean


**5. Loop that repeats while condition true:**

- FOR

- WHILE

- PRINT

- CASE

> **Correct Answer**: WHILE


### WAEC Exam-Style Questions


**1. Describe with an example how you would obtain the average score of 40 students using iteration.**

> **Answer Guide**: Use loop to sum scores then divide by 40; show FOR or WHILE; include input/output.


**2. Explain two advantages of using flowcharts and two of using pseudocode when planning programs in a resource-limited Nigerian school lab.**

> **Answer Guide**: Flowcharts visualize flow; pseudocode quick to write/read; both save PC time and reduce errors.


## Summary


This lesson covered the fundamentals of Computer Science at SS1 level.

Key topics included:

- 2.1: What Is an Algorithm?

- 2.2: Representing Algorithms: Text and Diagrams

- 2.3: Data Types, Variables, and Expressions

- 2.4: Control Structures: Sequence, Selection, Iteration


## Visual Aids & Resources


- **Flowchart Symbols Reference** (chart): Common shapes with meanings.


- **Sample Pseudocode Layout** (text): Indentation, IF, loops examples.


- **Algorithm vs Program Venn** (diagram): Relationship between algorithm, pseudocode, code.


---


**Prepared for**: Computer Science SS1

**WAEC Tags**: algorithms, flowcharts, pseudocode, data types, variables...

**Learning Path**: Unit 1 → Algorithms and Programming Basics
