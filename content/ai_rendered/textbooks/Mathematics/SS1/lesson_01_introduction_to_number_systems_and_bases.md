# Introduction to Number Systems and Bases

**Mathematics | SS1 | Unit 1: Number Systems**

---

## Lesson Information

- **Duration**: 90 minutes
- **Estimated Pages**: 8
- **NERDC Code**: MA.SS1.1.1
- **NERDC Description**: Number systems: binary, octal, denary, hexadecimal
- **WAEC Topic**: Number Systems and Bases (10%)
- **Learning Level**: Foundational

## Learning Objectives

By the end of this lesson, you will be able to:

1. Understand different number systems (binary, octal, denary, hexadecimal)
2. Convert numbers between different bases
3. Apply number system concepts to real-world digital technology
4. Perform arithmetic operations in different bases
5. Understand positional notation and place values

## Prerequisites

Before starting this lesson, ensure you understand:

- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Understanding of powers and exponents
- Familiarity with whole numbers and decimals

## Content


### 1.1: What is a Number System?

*Duration: 15 minutes*

A number system is a method of representing numbers using symbols or digits. The most commonly used number system in daily life is the Denary (or Decimal) system, which uses ten digits: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9.

In mathematics and computer science, we use different number systems depending on the context. The choice of base (or radix) determines how many unique digits we need and how we interpret their positions.

Key Concept: Positional Notation
In any number system, the position of a digit determines its value. In the denary system, the number 234 means:
- 2 × 10² + 3 × 10¹ + 4 × 10⁰ = 200 + 30 + 4 = 234

This positional principle applies to all number systems. In any base b, a digit in position p (counting from the right, starting at 0) has a value multiplied by b^p.


### 1.2: Common Number Systems

*Duration: 20 minutes*

1. **Denary (Base 10)**
   - Digits: 0-9
   - Used in everyday life and commerce in Nigeria and worldwide
   - Example: 456 in denary = 4 × 10² + 5 × 10¹ + 6 × 10⁰

2. **Binary (Base 2)**
   - Digits: 0, 1
   - Used in all digital computers and electronic systems
   - Foundation of modern technology
   - Example: 1011 in binary = 1 × 2³ + 0 × 2² + 1 × 2¹ + 1 × 2⁰ = 8 + 0 + 2 + 1 = 11 in denary

3. **Octal (Base 8)**
   - Digits: 0-7
   - Used in computer programming and system administration
   - Efficient representation of binary numbers
   - Example: 52 in octal = 5 × 8¹ + 2 × 8⁰ = 40 + 2 = 42 in denary

4. **Hexadecimal (Base 16)**
   - Digits: 0-9, A-F (where A=10, B=11, C=12, D=13, E=14, F=15)
   - Widely used in computer science (memory addresses, color codes in web design)
   - Nigerian software developers frequently use this in embedded systems
   - Example: 2A in hexadecimal = 2 × 16¹ + 10 × 16⁰ = 32 + 10 = 42 in denary

**Nigerian Context**: Mobile phone technology, banking systems, and ATM networks all use these number systems internally. Understanding them helps you appreciate how technology works in your country.


### 1.3: Conversion Between Bases

*Duration: 35 minutes*

**Method 1: Converting FROM any base TO Denary**

Step 1: Write the number with place values
Step 2: Multiply each digit by its place value (base^position)
Step 3: Add all the products

Example: Convert 1101₂ (binary) to denary
- 1101₂ = 1×2³ + 1×2² + 0×2¹ + 1×2⁰
- = 1×8 + 1×4 + 0×2 + 1×1
- = 8 + 4 + 0 + 1
- = 13₁₀

Example: Convert 3A₁₆ (hexadecimal) to denary
- 3A₁₆ = 3×16¹ + 10×16⁰
- = 3×16 + 10×1
- = 48 + 10
- = 58₁₀

**Method 2: Converting FROM Denary TO any base**

Step 1: Divide the denary number by the target base
Step 2: Write down the remainder
Step 3: Divide the quotient by the base again
Step 4: Repeat until quotient is 0
Step 5: Read remainders from bottom to top (for bases 2, 8, 10) or replace digits ≥ 10 with letters (for base 16)

Example: Convert 25₁₀ to binary
- 25 ÷ 2 = 12 remainder 1
- 12 ÷ 2 = 6 remainder 0
- 6 ÷ 2 = 3 remainder 0
- 3 ÷ 2 = 1 remainder 1
- 1 ÷ 2 = 0 remainder 1
- Read from bottom: 11001₂
- Check: 1×16 + 1×8 + 0×4 + 0×2 + 1×1 = 25 ✓

Example: Convert 255₁₀ to hexadecimal
- 255 ÷ 16 = 15 remainder 15 (F)
- 15 ÷ 16 = 0 remainder 15 (F)
- Read from bottom: FF₁₆
- Check: 15×16 + 15×1 = 240 + 15 = 255 ✓


### 1.4: Arithmetic in Different Bases

*Duration: 15 minutes*

Addition in different bases follows the same principle as denary addition, but you carry when the sum reaches the base value.

**Binary Addition Example**
```
  1101₂
+  101₂
-------
 10010₂
```
Check: 13₁₀ + 5₁₀ = 18₁₀ = 10010₂ ✓

**Octal Addition Example**
```
   34₈
+  25₈
-------
   61₈
```
Check: 28₁₀ + 21₁₀ = 49₁₀ = 61₈ ✓

**Hexadecimal Addition Example**
```
   2A₁₆
+  1F₁₆
-------
   49₁₆
```
Check: 42₁₀ + 31₁₀ = 73₁₀ = 49₁₆ ✓

Note: When adding in different bases, remember:
- In binary: carry when sum ≥ 2
- In octal: carry when sum ≥ 8
- In hexadecimal: carry when sum ≥ 16


## Worked Examples


### Example 1.1: Converting Denary to Binary (Nigerian Tech Example)

**Context**: A Nigerian software developer needs to understand how memory addresses work in a microcontroller. If a device has 64 memory locations, how is this represented in binary?

**Problem**: Convert 64₁₀ to binary

**Solution**:
```
Method: Repeated division by 2
- 64 ÷ 2 = 32 remainder 0
- 32 ÷ 2 = 16 remainder 0
- 16 ÷ 2 = 8 remainder 0
- 8 ÷ 2 = 4 remainder 0
- 4 ÷ 2 = 2 remainder 0
- 2 ÷ 2 = 1 remainder 0
- 1 ÷ 2 = 0 remainder 1

Reading from bottom: 1000000₂

Verification: 1×2⁶ = 64₁₀ ✓
```

**Skills Tested**: Division, Conversion algorithm, Verification


### Example 1.2: Color Codes in Web Design (Nigerian Web Developer Context)

**Context**: Nigerian web designers use hexadecimal color codes. What does #FF5733 mean?

**Problem**: Convert hexadecimal color code FF₁₆ (red component) to decimal

**Solution**:
```
FF₁₆ = F×16¹ + F×16⁰ = 15×16 + 15×1 = 240 + 15 = 255₁₀

This means the red component is at maximum intensity (255 out of 255).
```

**Skills Tested**: Hexadecimal conversion, Place value understanding


### Example 1.3: Octal Numbers in Unix File Permissions

**Context**: File permissions in Nigerian server farms often use octal notation. What does permission 755 mean?

**Problem**: Convert 755₈ to decimal to understand its value

**Solution**:
```
755₈ = 7×8² + 5×8¹ + 5×8⁰
     = 7×64 + 5×8 + 5×1
     = 448 + 40 + 5
     = 493₁₀
```

**Skills Tested**: Octal conversion, Place values with base 8


## Practice Problems


### Basic Level


**1.1.B**: Convert 12₁₀ to binary

> **Answer**: 1100₂

> **Explanation**: 12 ÷ 2 = 6 r0; 6 ÷ 2 = 3 r0; 3 ÷ 2 = 1 r1; 1 ÷ 2 = 0 r1. Read: 1100₂


**1.2.B**: Convert 11₂ to decimal

> **Answer**: 3₁₀

> **Explanation**: 11₂ = 1×2¹ + 1×2⁰ = 2 + 1 = 3₁₀


**1.3.B**: Convert 7₈ to decimal

> **Answer**: 7₁₀

> **Explanation**: 7₈ = 7×8⁰ = 7₁₀


**1.4.B**: What is 10₂ in decimal?

> **Answer**: 2₁₀

> **Explanation**: 10₂ = 1×2¹ + 0×2⁰ = 2 + 0 = 2₁₀


### Core Level


**1.5.C**: Convert 45₁₀ to binary

> **Answer**: 101101₂

> **Explanation**: 45 ÷ 2 = 22 r1; 22 ÷ 2 = 11 r0; 11 ÷ 2 = 5 r1; 5 ÷ 2 = 2 r1; 2 ÷ 2 = 1 r0; 1 ÷ 2 = 0 r1. Read: 101101₂


**1.6.C**: Convert 10110₂ to decimal

> **Answer**: 22₁₀

> **Explanation**: 10110₂ = 1×2⁴ + 0×2³ + 1×2² + 1×2¹ + 0×2⁰ = 16 + 0 + 4 + 2 + 0 = 22₁₀


**1.7.C**: Add: 1101₂ + 101₂

> **Answer**: 10010₂

> **Explanation**: In binary: 1 + 1 = 10 (write 0, carry 1); 0 + 0 + carry 1 = 1; 1 + 1 = 10 (write 0, carry 1); 1 + carry 1 = 10. Result: 10010₂


**1.8.C**: Convert 127₁₀ to hexadecimal

> **Answer**: 7F₁₆

> **Explanation**: 127 ÷ 16 = 7 r15 (F); 7 ÷ 16 = 0 r7. Read: 7F₁₆


### Challenge Level


**1.9.CH**: A web color is #FF7700. Convert FF₁₆ and 77₁₆ to decimal. What do these represent?

> **Answer**: FF₁₆ = 255₁₀; 77₁₆ = 119₁₀. In RGB, this is (255, 119, 0), a deep orange color.

> **Explanation**: FF₁₆ = 15×16 + 15 = 255; 77₁₆ = 7×16 + 7 = 112 + 7 = 119. These are RGB intensity values.


**1.10.CH**: Convert 1111111₂ to decimal and hexadecimal. Why is this number significant in computing?

> **Answer**: 1111111₂ = 127₁₀ = 7F₁₆. It is the maximum value for a signed 8-bit integer, and one less than 128, a power of 2.

> **Explanation**: 1111111₂ = 64 + 32 + 16 + 8 + 4 + 2 + 1 = 127. In computing, 128 = 2⁷ is a boundary value.


## Glossary


**Base (Radix)**: The number of unique digits used in a number system. Denary has base 10, binary has base 2, octal has base 8, hexadecimal has base 16.

- *Example*: In base 16 (hexadecimal), the digits are 0-9 and A-F.


**Binary**: A number system with base 2, using only digits 0 and 1. The foundation of all digital computing.

- *Example*: The binary number 1010 equals 10 in decimal.


**Denary (Decimal)**: The number system with base 10, using digits 0-9. The standard system used in everyday life.

- *Example*: The denary number 42 has a 4 in the tens place and a 2 in the ones place.


**Hexadecimal**: A number system with base 16, using digits 0-9 and letters A-F. Commonly used in computing for memory addresses and color codes.

- *Example*: The hexadecimal number FF equals 255 in decimal.


**Octal**: A number system with base 8, using digits 0-7. Historically used in computing.

- *Example*: The octal number 77 equals 63 in decimal.


**Positional Notation**: A system where the position of a digit determines its value, multiplied by a power of the base.

- *Example*: In denary, 234 = 2×10² + 3×10¹ + 4×10⁰.


**Place Value**: The value assigned to a digit based on its position in a number.

- *Example*: In binary 1010, the leftmost 1 has a place value of 2³ = 8.


## Assessment


### Quick Checks (Understanding Check)

1. What are the four number systems we studied?

2. How many unique digits does hexadecimal use?

3. Explain positional notation in your own words

4. Why is binary important for computers?


### End-of-Lesson Quiz


**1. Convert 101₂ to decimal**

- 3

- 4

- 5

- 6

> **Correct Answer**: 5


**2. What is 1F₁₆ in decimal?**

- 29

- 30

- 31

- 32

> **Correct Answer**: 31


**3. Which base uses only digits 0 and 1?**

- Octal

- Denary

- Binary

- Hexadecimal

> **Correct Answer**: Binary


### WAEC Exam-Style Questions


**1. WAEC-style: Convert 256₁₀ to binary and express your answer in the form 2^n**

> **Answer Guide**: 256₁₀ = 100000000₂ = 2⁸


**2. WAEC-style: A memory address in a computer system is represented as ABCD₁₆. Convert this to denary.**

> **Answer Guide**: ABCD₁₆ = 10×16³ + 11×16² + 12×16¹ + 13×16⁰ = 40960 + 2816 + 192 + 13 = 43981₁₀


## Summary


This lesson covered the fundamentals of Mathematics at SS1 level.

Key topics included:

- 1.1: What is a Number System?

- 1.2: Common Number Systems

- 1.3: Conversion Between Bases

- 1.4: Arithmetic in Different Bases


## Visual Aids & Resources


- **Place Value Chart for Different Bases** (table): Comparison of place values across base 2, 8, 10, and 16


- **Binary to Denary Conversion Flow Chart** (flowchart): Step-by-step visual for converting from binary to denary


---


**Prepared for**: Mathematics SS1

**WAEC Tags**: number_systems, base_conversion, binary, hexadecimal, octal...

**Learning Path**: Unit 1 → Number Systems
