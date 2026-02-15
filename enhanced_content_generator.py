#!/usr/bin/env python3
"""
Enhanced Content Generator with MCP Integration
Generates WAEC-aligned lessons using research and AI capabilities
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LessonContent:
    """Structured lesson content"""
    id: str
    title: str
    subject: str
    topic: str
    difficulty: str
    duration_minutes: int
    learning_objectives: List[str]
    key_concepts: List[str]
    sections: List[Dict[str, Any]]
    assessment: Dict[str, Any]
    waec_coverage: Dict[str, Any]
    tags: List[str]


class EnhancedContentGenerator:
    """Generate enhanced educational content with MCP integration"""
    
    # WAEC Topic Database
    WAEC_TOPICS = {
        "Mathematics": [
            "Sequences and Series", "Matrices and Determinants", "Variation",
            "Angles and Triangles", "Quadratic Equations and Functions",
            "Coordinate Geometry", "Calculus - Differentiation", "Calculus - Integration",
            "Complex Numbers", "Trigonometric Functions", "Permutation and Combination",
            "Probability and Statistics"
        ],
        "Physics": [
            "Mechanics - Forces and Motion", "Work, Energy and Power",
            "Temperature and Heat", "Properties of Matter", "Waves and Oscillations",
            "Electricity and Magnetism", "Electromagnetic Induction", "Light and Optics",
            "Modern Physics - Atomic Structure", "Nuclear Physics",
            "Thermodynamics", "Fluids and Pressure"
        ],
        "Chemistry": [
            "Atomic Structure and Bonding", "Periodic Table", "States of Matter",
            "Chemical Reactions and Equations", "Stoichiometry", "Acids, Bases and Salts",
            "Organic Chemistry - Hydrocarbons", "Organic Chemistry - Functional Groups",
            "Extraction of Metals", "Electrochemistry"
        ],
        "Biology": [
            "Cell Structure and Function", "Photosynthesis and Respiration",
            "Nutrition and Transport", "Coordination and Response", "Reproduction",
            "Heredity and Variation", "Evolution and Natural Selection",
            "Ecology and Ecosystems", "Diseases and Immunity", "Homeostasis"
        ],
        "English": [
            "Literary Analysis", "Grammar and Syntax", "Essay Writing",
            "Poetry and Verse", "Shakespearean Drama"
        ],
        "Economics": [
            "Microeconomics Principles", "Macroeconomics Overview"
        ],
        "Geography": [
            "Geomorphology and Ecosystems"
        ]
    }
    
    # Nigerian Context Examples
    NIGERIAN_CONTEXT = {
        "Mathematics": [
            "Population growth in Lagos (3.5% annually)",
            "Electricity tariff variation by region",
            "Bridge design across Niger River",
            "Rainfall patterns in Kainji Dam",
            "Naira exchange rate fluctuations"
        ],
        "Physics": [
            "Solar power potential in Northern Nigeria",
            "Mobile signal propagation in rural areas",
            "Vehicle speeds on Lagos-Ibadan Expressway",
            "Harmattan wind temperature variations"
        ],
        "Chemistry": [
            "Cement production at Dangote Cement",
            "Tin extraction in Jos Plateau",
            "Crude oil processing at Kaduna Refinery"
        ],
        "Biology": [
            "Mangrove swamps in Niger Delta",
            "Wildlife in Yankari Game Reserve",
            "Malaria prevention in tropical climate"
        ]
    }
    
    def __init__(self, curriculum_file: str = "curriculum_map.json", use_mcp: bool = False):
        self.curriculum_file = curriculum_file
        self.curriculum_data = self.load_curriculum()
        self.output_dir = "generated_content"
        self.images_dir = "generated_images"
        self.use_mcp = use_mcp
        self.generated_count = 0
        self.total_duration = 0
        
        # Initialize MCP servers if enabled
        if self.use_mcp:
            try:
                from mcp_server import MCPServerWrapper
                self.mcp_wrapper = MCPServerWrapper()
                logger.info("✅ MCP servers initialized (Brave Search + Wikipedia)")
            except ImportError:
                logger.warning("⚠️  MCP not available, will generate without research")
                self.mcp_wrapper = None
        else:
            self.mcp_wrapper = None
        
        # Create output directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        logger.info(f"✅ Output directory: {self.output_dir}")
    
    def load_curriculum(self) -> Dict[str, Any]:
        """Load curriculum map"""
        try:
            with open(self.curriculum_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Curriculum file not found: {self.curriculum_file}")
            return {"subjects": {}}
    
    def get_high_priority_topics(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get topics with highest exam weight"""
        high_priority = []
        
        for subject_name, subject_data in self.curriculum_data.get("subjects", {}).items():
            for topic in subject_data.get("topics", []):
                if topic.get("exam_weight") in ["very_high", "high"]:
                    high_priority.append({
                        "subject": subject_name,
                        "topic_id": topic["id"],
                        "topic_name": topic["name"],
                        "exam_weight": topic["exam_weight"],
                        "difficulty": topic["difficulty"],
                        "subtopics": topic.get("subtopics", [])
                    })
        
        # Sort by exam weight (very_high first)
        high_priority.sort(key=lambda x: 0 if x["exam_weight"] == "very_high" else 1)
        
        return high_priority[:limit]
    
    def generate_quadratic_equations_lesson(self) -> Dict[str, Any]:
        """Generate enhanced lesson on Quadratic Equations"""
        topic_id = "math_quadratic_equations_enhanced"
        
        # Generate diagram: Parabola with roots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Left: Parabola with positive discriminant
        x = np.linspace(-5, 5, 300)
        y1 = x**2 - 4*x + 3
        ax1.plot(x, y1, 'b-', linewidth=2.5, label='y = x² - 4x + 3')
        ax1.axhline(y=0, color='k', linewidth=0.8)
        ax1.axvline(x=0, color='k', linewidth=0.8)
        ax1.plot([1, 3], [0, 0], 'ro', markersize=10, label='Roots: x=1, x=3')
        ax1.plot([2], [-1], 'go', markersize=10, label='Vertex: (2, -1)')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlabel('x', fontsize=12)
        ax1.set_ylabel('y', fontsize=12)
        ax1.set_title('Quadratic with Two Real Roots', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.set_ylim(-3, 8)
        
        # Right: Different types
        y2 = x**2 - 4*x + 4
        y3 = x**2 + 1
        ax2.plot(x, y1, 'b-', linewidth=2, label='Two roots (Δ > 0)')
        ax2.plot(x, y2, 'g-', linewidth=2, label='One root (Δ = 0)')
        ax2.plot(x, y3, 'r-', linewidth=2, label='No real roots (Δ < 0)')
        ax2.axhline(y=0, color='k', linewidth=0.8)
        ax2.axvline(x=0, color='k', linewidth=0.8)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('x', fontsize=12)
        ax2.set_ylabel('y', fontsize=12)
        ax2.set_title('Nature of Roots (Discriminant)', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.set_ylim(-2, 10)
        
        plt.tight_layout()
        diagram_path = os.path.join(self.diagrams_dir, f"{topic_id}_parabola.png")
        plt.savefig(diagram_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Generate content
        content = {
            "id": topic_id,
            "title": "Quadratic Equations: Complete Guide with Solutions",
            "subject": "Mathematics",
            "topic": "Quadratic Equations",
            "subtopic": "Solving Methods and Applications",
            "content_type": "study_guide",
            "difficulty": "intermediate",
            "exam_board": "WAEC",
            "content": self._generate_quadratic_content(),
            "diagrams": [diagram_path],
            "worked_examples": self._generate_quadratic_examples(),
            "practice_problems": self._generate_quadratic_practice(),
            "nigerian_context": "In Lagos, a projectile launcher costs ₦15,000...",
            "estimated_read_time": 25,
            "prerequisites": ["Factorization", "Basic algebra"],
            "learning_objectives": [
                "Solve quadratic equations using three methods",
                "Determine nature of roots using discriminant",
                "Apply quadratic equations to real-world problems",
                "Sketch parabolas and identify key features"
            ],
            "created_at": datetime.now().isoformat(),
            "status": "published"
        }
        
        return content
    
    def _generate_quadratic_content(self) -> str:
        """Generate comprehensive quadratic equations content"""
        return """# Quadratic Equations: Mastery Guide

## 1. Introduction

A **quadratic equation** is a polynomial equation of degree 2, written in the standard form:

**ax² + bx + c = 0**

Where:
- a, b, c are constants (a ≠ 0)
- x is the variable
- a is the coefficient of x²
- b is the coefficient of x
- c is the constant term

## 2. Methods of Solving Quadratic Equations

### Method 1: Factorization

**When to use**: When the equation can be easily factored

**Steps**:
1. Write equation in standard form (ax² + bx + c = 0)
2. Factor the left side into two binomials
3. Set each factor equal to zero
4. Solve for x

**Example**: x² - 5x + 6 = 0
- Factor: (x - 2)(x - 3) = 0
- Solutions: x = 2 or x = 3

### Method 2: Completing the Square

**When to use**: When factorization is difficult, or to derive the quadratic formula

**Steps**:
1. Move constant to right side
2. Make coefficient of x² equal to 1
3. Add (b/2)² to both sides
4. Take square root of both sides
5. Solve for x

**Example**: x² + 6x + 5 = 0
- x² + 6x = -5
- x² + 6x + 9 = -5 + 9
- (x + 3)² = 4
- x + 3 = ±2
- x = -3 ± 2
- Solutions: x = -1 or x = -5

### Method 3: Quadratic Formula (Most Powerful!)

For any quadratic equation ax² + bx + c = 0:

**x = [-b ± √(b² - 4ac)] / 2a**

**Discriminant (Δ)**: b² - 4ac

Nature of roots:
- If Δ > 0: Two distinct real roots
- If Δ = 0: One repeated real root
- If Δ < 0: No real roots (complex roots)

## 3. Nigerian Context Examples

### Example 1: Market Pricing (Lagos)
A trader at Idumota Market sells phones. The profit P (in Naira) is given by:
P = -2x² + 120x - 1000

Where x is the number of phones sold per day.

**Question**: How many phones should be sold to break even (P = 0)?

**Solution**:
-2x² + 120x - 1000 = 0
Divide by -2: x² - 60x + 500 = 0

Using quadratic formula:
x = [60 ± √(3600 - 2000)] / 2
x = [60 ± √1600] / 2
x = [60 ± 40] / 2

x = 50 or x = 10

**Answer**: The trader breaks even by selling either 10 or 50 phones per day.

### Example 2: Construction (Abuja)
A rectangular plot in Abuja has length 5m more than its width. The area is 300m².

**Find**: The dimensions of the plot.

**Solution**:
Let width = x meters
Length = (x + 5) meters
Area: x(x + 5) = 300
x² + 5x - 300 = 0

Factor or use formula:
x = [-5 ± √(25 + 1200)] / 2
x = [-5 ± 35] / 2

x = 15 or x = -20 (reject negative)

**Answer**: Width = 15m, Length = 20m

## 4. Graphing Quadratic Functions

The graph of y = ax² + bx + c is a **parabola**.

**Key Features**:
- **Vertex**: Turning point at x = -b/2a
- **Axis of symmetry**: Vertical line through vertex
- **Y-intercept**: Point (0, c)
- **X-intercepts**: Roots of the equation

**Direction**:
- If a > 0: Opens upward (U-shape)
- If a < 0: Opens downward (∩-shape)

## 5. Exam Tips for WAEC

✅ **Always check your discriminant first** - it tells you how many solutions to expect

✅ **Show all working** - even if you use calculator, write down the formula and substitution

✅ **Check your solutions** by substituting back into the original equation

✅ **Watch for word problems** - translate Nigerian context into equations carefully

✅ **Remember units** - if the problem mentions Naira (₦), meters, or time, include units in your answer

## 6. Common Mistakes to Avoid

❌ Forgetting the ± sign in the quadratic formula
❌ Arithmetic errors when calculating discriminant
❌ Dividing by 2a instead of 2 in the formula
❌ Not writing equation in standard form first
❌ Accepting negative solutions for length, time, or quantity problems

## 7. Practice Problems (Self-Check)

Solve using any method:

1. x² - 7x + 12 = 0
2. 2x² + 5x - 3 = 0
3. x² - 6x + 9 = 0
4. x² + 4x + 5 = 0 (Find nature of roots)

**Challenge Problem**: 
A ball is thrown upward from ground level in Port Harcourt. Its height h (in meters) after t seconds is:
h = -5t² + 20t

Find: (a) Maximum height reached
      (b) Time when ball hits the ground

## Summary

- Three main solving methods: Factorization, Completing the Square, Quadratic Formula
- Discriminant determines nature of roots
- Real-world applications: projectiles, area, profit maximization
- Always check your work by substitution
"""
    
    def _generate_quadratic_examples(self) -> List[Dict[str, str]]:
        """Generate worked examples"""
        return [
            {
                "problem": "Solve: x² + 7x + 10 = 0",
                "solution": "Step 1: Factor → (x + 2)(x + 5) = 0\nStep 2: Set each factor to zero → x + 2 = 0 or x + 5 = 0\nStep 3: Solve → x = -2 or x = -5",
                "answer": "x = -2 or x = -5"
            },
            {
                "problem": "Solve using quadratic formula: 2x² - 3x - 2 = 0",
                "solution": "a = 2, b = -3, c = -2\nΔ = b² - 4ac = 9 + 16 = 25\nx = [3 ± √25] / 4 = [3 ± 5] / 4\nx = 8/4 or -2/4",
                "answer": "x = 2 or x = -0.5"
            },
            {
                "problem": "A rectangular garden in Kano has area 48m². Length is 2m more than width. Find dimensions.",
                "solution": "Let width = x\nLength = x + 2\nArea: x(x + 2) = 48\nx² + 2x - 48 = 0\nFactor: (x + 8)(x - 6) = 0\nx = 6 (reject -8)",
                "answer": "Width = 6m, Length = 8m"
            }
        ]
    
    def _generate_quadratic_practice(self) -> List[Dict[str, Any]]:
        """Generate practice problems"""
        return [
            {
                "question": "Solve: x² - 9 = 0",
                "difficulty": "basic",
                "answer": "x = 3 or x = -3",
                "hint": "This is a difference of squares"
            },
            {
                "question": "Solve: x² + 10x + 25 = 0",
                "difficulty": "basic",
                "answer": "x = -5 (repeated root)",
                "hint": "Perfect square trinomial"
            },
            {
                "question": "Find the discriminant and nature of roots: 3x² - 2x + 5 = 0",
                "difficulty": "intermediate",
                "answer": "Δ = -56 (no real roots)",
                "hint": "Calculate b² - 4ac"
            },
            {
                "question": "A phone seller in Aba has profit function P = -x² + 40x - 300 (in thousands of ₦). Find break-even points.",
                "difficulty": "advanced",
                "answer": "x = 10 or x = 30 phones",
                "hint": "Set P = 0 and solve"
            }
        ]
    
    def generate_circuit_diagram_lesson(self) -> Dict[str, Any]:
        """Generate Physics lesson on Current Electricity with circuit diagrams"""
        topic_id = "physics_current_electricity_enhanced"
        
        # Create circuit diagrams
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # Circuit 1: Simple series circuit
        ax = axes[0, 0]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Series Circuit', fontsize=14, fontweight='bold')
        
        # Battery
        ax.plot([2, 2], [2, 4], 'k-', linewidth=3)
        ax.plot([2, 2], [4.2, 6], 'k-', linewidth=1)
        ax.text(1.3, 4, '+', fontsize=16, fontweight='bold')
        ax.text(1.3, 2.5, '−', fontsize=16, fontweight='bold')
        ax.text(0.5, 3, '6V', fontsize=12)
        
        # Wires
        ax.plot([2, 2, 8, 8, 2], [6, 8, 8, 2, 2], 'b-', linewidth=2)
        
        # Resistors
        for i, (x, y, r) in enumerate([(4, 8, '2Ω'), (8, 5, '3Ω')]):
            rect = mpatches.Rectangle((x-0.3, y-0.2), 0.6, 0.4, 
                                      linewidth=2, edgecolor='red', facecolor='yellow')
            ax.add_patch(rect)
            ax.text(x, y-0.8, r, fontsize=11, ha='center')
        
        ax.text(5, 9, 'Total R = 5Ω, I = 1.2A', fontsize=11, bbox=dict(boxstyle='round', facecolor='wheat'))
        
        # Circuit 2: Parallel circuit
        ax = axes[0, 1]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Parallel Circuit', fontsize=14, fontweight='bold')
        
        # Battery
        ax.plot([2, 2], [3, 5], 'k-', linewidth=3)
        ax.plot([2, 2], [5.2, 7], 'k-', linewidth=1)
        ax.text(1.3, 5, '+', fontsize=16, fontweight='bold')
        ax.text(1.3, 3.5, '−', fontsize=16, fontweight='bold')
        ax.text(0.5, 4, '12V', fontsize=12)
        
        # Main wires
        ax.plot([2, 2, 4, 4], [7, 8, 8, 2], 'b-', linewidth=2)
        ax.plot([2, 2, 4], [3, 2, 2], 'b-', linewidth=2)
        ax.plot([4, 8, 8, 4], [8, 8, 2, 2], 'b-', linewidth=2)
        
        # Branch 1
        ax.plot([4, 5], [8, 8], 'b-', linewidth=1.5)
        ax.plot([5, 5], [8, 5], 'b-', linewidth=1.5)
        rect1 = mpatches.Rectangle((4.7, 6), 0.6, 0.4, linewidth=2, edgecolor='red', facecolor='yellow')
        ax.add_patch(rect1)
        ax.text(5, 5.5, '4Ω', fontsize=10, ha='center')
        ax.plot([5, 5], [5, 2], 'b-', linewidth=1.5)
        ax.plot([5, 4], [2, 2], 'b-', linewidth=1.5)
        
        # Branch 2
        ax.plot([4, 6.5], [8, 8], 'b-', linewidth=1.5)
        ax.plot([6.5, 6.5], [8, 5], 'b-', linewidth=1.5)
        rect2 = mpatches.Rectangle((6.2, 6), 0.6, 0.4, linewidth=2, edgecolor='red', facecolor='yellow')
        ax.add_patch(rect2)
        ax.text(6.5, 5.5, '6Ω', fontsize=10, ha='center')
        ax.plot([6.5, 6.5], [5, 2], 'b-', linewidth=1.5)
        ax.plot([6.5, 4], [2, 2], 'b-', linewidth=1.5)
        
        ax.text(5, 9, '1/Rtotal = 1/4 + 1/6 = 0.42\nRtotal = 2.4Ω', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat'))
        
        # Ohm's Law Triangle
        ax = axes[1, 0]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title("Ohm's Law Triangle", fontsize=14, fontweight='bold')
        
        triangle = mpatches.Polygon([[5, 2], [2, 7], [8, 7]], closed=True, 
                                    edgecolor='blue', facecolor='lightblue', linewidth=3)
        ax.add_patch(triangle)
        ax.plot([2, 8], [5, 5], 'k-', linewidth=2)
        ax.text(5, 6, 'V', fontsize=24, fontweight='bold', ha='center')
        ax.text(3.5, 3.5, 'I', fontsize=24, fontweight='bold')
        ax.text(6.5, 3.5, 'R', fontsize=24, fontweight='bold')
        
        ax.text(5, 1, 'V = IR    I = V/R    R = V/I', fontsize=12, ha='center',
                bbox=dict(boxstyle='round', facecolor='yellow'))
        
        # Power formulas
        ax = axes[1, 1]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        ax.set_title('Power in Electrical Circuits', fontsize=14, fontweight='bold')
        
        formulas = [
            "Power (P) = Electrical Energy / Time",
            "",
            "P = VI  (most common)",
            "P = I²R  (when you know I and R)",
            "P = V²/R  (when you know V and R)",
            "",
            "Units:",
            "Power (P) → Watts (W)",
            "Voltage (V) → Volts (V)",
            "Current (I) → Amperes (A)",
            "Resistance (R) → Ohms (Ω)",
            "",
            "1 kilowatt (kW) = 1000 W",
            "Energy (kWh) = Power (kW) × Time (h)"
        ]
        
        y_pos = 9
        for formula in formulas:
            if formula == "":
                y_pos -= 0.3
            else:
                ax.text(5, y_pos, formula, fontsize=11, ha='center',
                       bbox=dict(boxstyle='round', facecolor='lightyellow' if '=' in formula else 'white'))
                y_pos -= 0.6
        
        plt.tight_layout()
        diagram_path = os.path.join(self.diagrams_dir, f"{topic_id}_circuits.png")
        plt.savefig(diagram_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        content = {
            "id": topic_id,
            "title": "Current Electricity: Circuits and Ohm's Law",
            "subject": "Physics",
            "topic": "Current Electricity",
            "subtopic": "Series and Parallel Circuits",
            "content_type": "study_guide",
            "difficulty": "intermediate",
            "exam_board": "WAEC",
            "content": self._generate_electricity_content(),
            "diagrams": [diagram_path],
            "worked_examples": self._generate_electricity_examples(),
            "practice_problems": self._generate_electricity_practice(),
            "nigerian_context": "NEPA/PHCN power calculations for Nigerian homes...",
            "estimated_read_time": 30,
            "prerequisites": ["Basic electricity", "Mathematics"],
            "learning_objectives": [
                "Apply Ohm's Law to calculate V, I, and R",
                "Analyze series and parallel circuits",
                "Calculate power consumption and cost",
                "Solve WAEC-style circuit problems"
            ],
            "created_at": datetime.now().isoformat(),
            "status": "published"
        }
        
        return content
    
    def _generate_electricity_content(self) -> str:
        """Generate electricity content"""
        return """# Current Electricity: Complete Guide

## 1. Fundamental Concepts

### Electric Current (I)
- **Definition**: Rate of flow of electric charge
- **Formula**: I = Q/t
- **Unit**: Ampere (A) or Coulomb per second (C/s)
- **Direction**: Conventional current flows from positive to negative

### Potential Difference/Voltage (V)
- **Definition**: Work done per unit charge
- **Formula**: V = W/Q
- **Unit**: Volt (V) or Joule per Coulomb (J/C)
- **Meaning**: "Electrical pressure" that pushes charges

### Resistance (R)
- **Definition**: Opposition to current flow
- **Formula**: R = ρL/A (where ρ = resistivity, L = length, A = area)
- **Unit**: Ohm (Ω)
- **Factors**: Material, length, cross-sectional area, temperature

## 2. Ohm's Law ⭐⭐⭐

**V = IR**

Most important formula in electricity!

If you know any two quantities, you can find the third:
- V = IR (voltage equals current times resistance)
- I = V/R (current equals voltage divided by resistance)
- R = V/I (resistance equals voltage divided by current)

## 3. Series Circuits

**Characteristics**:
- Current is **same** through all components: I = I₁ = I₂ = I₃
- Voltage is **shared**: V = V₁ + V₂ + V₃
- Total resistance **adds up**: Rtotal = R₁ + R₂ + R₃

**When to use**: Christmas lights, simple torch circuits

## 4. Parallel Circuits

**Characteristics**:
- Voltage is **same** across all branches: V = V₁ = V₂ = V₃
- Current is **shared**: I = I₁ + I₂ + I₃
- Reciprocal of total resistance: 1/Rtotal = 1/R₁ + 1/R₂ + 1/R₃

**When to use**: Home wiring, appliances that need same voltage

## 5. Electrical Power and Energy

**Power Formulas**:
- P = VI (most common)
- P = I²R (useful when you know current and resistance)
- P = V²/R (useful when you know voltage and resistance)

**Energy**: E = Pt (Energy = Power × Time)

**Cost of Electricity** (Nigerian Context):
Cost = Energy (kWh) × Tariff (₦/kWh)

## 6. Nigerian Context: NEPA/PHCN Calculations

### Example: Monthly Electricity Bill in Lagos

**Appliances in a home**:
- 5 LED bulbs (10W each) × 6 hours/day
- 1 Fan (75W) × 8 hours/day
- 1 TV (100W) × 4 hours/day
- 1 Fridge (150W) × 24 hours/day

**Monthly consumption**:
- Bulbs: 5 × 10W × 6h × 30 days = 9 kWh
- Fan: 75W × 8h × 30 = 18 kWh
- TV: 100W × 4h × 30 = 12 kWh
- Fridge: 150W × 24h × 30 = 108 kWh
- **Total**: 147 kWh/month

**Cost** (at ₦68/kWh):
147 kWh × ₦68 = ₦9,996 per month

## 7. WAEC Exam Tips

✅ **Always write formulas first** - shows you know the concept

✅ **List given values** - helps you organize your solution

✅ **Show unit conversions** - mA to A, kW to W, etc.

✅ **Draw circuit diagrams** when asked - label all components

✅ **Check your answer** - Does the current make sense? Is resistance positive?

## 8. Common Mistakes

❌ Forgetting to convert units (mA to A, kW to W)
❌ Using series formulas for parallel circuits (and vice versa)
❌ Mixing up voltage division vs current division
❌ Not showing working - even if you use calculator
❌ Wrong formula for parallel resistance (don't just add!)

## Summary

- Ohm's Law: V = IR (memorize this!)
- Series: Same current, voltage adds
- Parallel: Same voltage, current adds
- Power: P = VI = I²R = V²/R
- Practice with Nigerian context problems
"""
    
    def _generate_electricity_examples(self) -> List[Dict[str, str]]:
        """Generate electricity examples"""
        return [
            {
                "problem": "A bulb has resistance 240Ω and is connected to 240V mains. Calculate current.",
                "solution": "Given: V = 240V, R = 240Ω\nUsing Ohm's Law: I = V/R\nI = 240/240 = 1A",
                "answer": "Current = 1A"
            },
            {
                "problem": "Three resistors 2Ω, 3Ω, and 5Ω are connected in series to a 20V battery. Find total resistance and current.",
                "solution": "Series: Rtotal = R₁ + R₂ + R₃\nRtotal = 2 + 3 + 5 = 10Ω\nI = V/R = 20/10 = 2A",
                "answer": "Rtotal = 10Ω, I = 2A"
            },
            {
                "problem": "A Nigerian home uses a 1.5kW heater for 3 hours daily. If electricity costs ₦65/kWh, find monthly cost (30 days).",
                "solution": "Daily energy = 1.5kW × 3h = 4.5kWh\nMonthly energy = 4.5 × 30 = 135kWh\nCost = 135 × ₦65 = ₦8,775",
                "answer": "Monthly cost = ₦8,775"
            }
        ]
    
    def _generate_electricity_practice(self) -> List[Dict[str, Any]]:
        """Generate electricity practice problems"""
        return [
            {
                "question": "Calculate the voltage across a 50Ω resistor when 0.5A flows through it.",
                "difficulty": "basic",
                "answer": "V = 25V",
                "hint": "Use Ohm's Law: V = IR"
            },
            {
                "question": "Two resistors 4Ω and 6Ω are in parallel. Find the equivalent resistance.",
                "difficulty": "intermediate",
                "answer": "Req = 2.4Ω",
                "hint": "Use 1/Req = 1/R₁ + 1/R₂"
            },
            {
                "question": "A NEPA prepaid meter shows 50 kWh remaining. How many hours can you run a 2kW air conditioner?",
                "difficulty": "intermediate",
                "answer": "25 hours",
                "hint": "Time = Energy / Power"
            }
        ]
    
    def generate_all_pilot_content(self, count: int = 5) -> List[Dict[str, Any]]:
        """Generate all pilot lessons"""
        print("=" * 70)
        print("ENHANCED CONTENT GENERATOR")
        print("=" * 70)
        print()
        
        generated_content = []
        
        # Generate specific lessons
        print("📝 Generating enhanced lessons with diagrams...")
        print()
        
        print("  1/2 Mathematics: Quadratic Equations...")
        content1 = self.generate_quadratic_equations_lesson()
        generated_content.append(content1)
        print("      ✓ Generated with parabola diagrams")
        
        print("  2/2 Physics: Current Electricity...")
        content2 = self.generate_circuit_diagram_lesson()
        generated_content.append(content2)
        print("      ✓ Generated with circuit diagrams")
        
        print()
        print(f"✅ Generated {len(generated_content)} enhanced lessons")
        print(f"📊 Total diagrams created: {sum(len(c.get('diagrams', [])) for c in generated_content)}")
        
        # Save to JSON
        self.save_generated_content(generated_content)
        
        return generated_content
    
    def save_generated_content(self, content_list: List[Dict[str, Any]]):
        """Save generated content to JSON"""
        output_file = os.path.join(self.output_dir, "pilot_content.json")
        
        output_data = {
            "metadata": {
                "version": "1.0",
                "generated_at": datetime.now().isoformat(),
                "total_items": len(content_list),
                "generator": "EnhancedContentGenerator"
            },
            "content": content_list
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print()
        print(f"💾 Content saved to: {output_file}")
        print(f"📁 Diagrams saved to: {self.diagrams_dir}")
        print()
        print("Next steps:")
        print("1. Review generated content in generated_content/")
        print("2. Check diagram quality in generated_content/diagrams/")
        print("3. Import into wave3_content_database.json")
        print("4. Deploy to platform")

    def generate_batch(
        self,
        topics: List[Tuple[str, str, str]],
        *,
        generate_images: bool = False,
        image_negative_prompt: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Generate a batch of lessons; optionally attach SDXL images."""
        lessons = []
        self.total_duration = 0
        
        for subject, topic, difficulty in topics:
            logger.info(f"📚 Generating: {subject} - {topic} ({difficulty})")
            
            try:
                lesson = {
                    "id": f"{subject.lower()}_{topic.replace(' ', '_').lower()}",
                    "title": topic,
                    "subject": subject,
                    "topic": topic,
                    "difficulty": difficulty,
                    "duration_minutes": 25 + (5 if difficulty == "Intermediate" else 0),
                    "learningObjectives": self._generate_objectives(topic, difficulty),
                    "keyConceptsList": self._generate_concepts(topic),
                    "sections": self._generate_sections(topic, subject),
                    "assessment": self._generate_assessment(topic),
                    "waecCoverage": {
                        "percentCovered": 85,
                        "alignedTopics": [topic],
                        "examinationWeight": "12-15%"
                    },
                    "nigerianContext": self._generate_nigerian_context(subject, topic),
                    "createdAt": datetime.now().isoformat(),
                    "status": "draft"
                }
                
                if generate_images:
                    img_path = self._generate_image_asset(subject, topic, image_negative_prompt)
                    if img_path:
                        lesson["image"] = {
                            "path": img_path,
                            "prompt": self._build_image_prompt(subject, topic)
                        }
                
                lessons.append(lesson)
                self.total_duration += lesson["duration_minutes"]
                self.generated_count += 1
                
            except Exception as e:
                logger.error(f"❌ Failed to generate {topic}: {e}")
                continue
        
        return lessons

    def generate(
        self,
        *,
        subject: str,
        topic: str,
        difficulty: str = "Intermediate",
        use_mcp: bool = False,
        include_nigerian_context: bool = True,
        exam_board: str = "WAEC",
        generate_image: bool = False,
        image_negative_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a single lesson (lightweight path used by batch scripts)."""

        lesson = {
            "id": f"{subject.lower()}_{topic.replace(' ', '_').lower()}",
            "title": topic,
            "subject": subject,
            "topic": topic,
            "difficulty": difficulty,
            "duration_minutes": 25 + (5 if difficulty == "Intermediate" else 0),
            "learningObjectives": self._generate_objectives(topic, difficulty),
            "keyConceptsList": self._generate_concepts(topic),
            "sections": self._generate_sections(topic, subject),
            "assessment": self._generate_assessment(topic),
            "waecCoverage": {
                "percentCovered": 85,
                "alignedTopics": [topic],
                "examinationWeight": "12-15%"
            },
            "nigerianContext": self._generate_nigerian_context(subject, topic) if include_nigerian_context else {},
            "exam_board": exam_board,
            "createdAt": datetime.now().isoformat(),
            "status": "draft",
        }

        # Optional MCP hook (no-op if wrapper missing)
        if use_mcp and self.mcp_wrapper:
            try:
                research = self.mcp_wrapper.search(query=f"{topic} WAEC {subject}")
                if research:
                    lesson["research"] = research
            except Exception as exc:
                logger.warning(f"⚠️ MCP search failed for {topic}: {exc}")

        if generate_image:
            img_path = self._generate_image_asset(subject, topic, image_negative_prompt)
            if img_path:
                lesson["image"] = {
                    "path": img_path,
                    "prompt": self._build_image_prompt(subject, topic)
                }

        self.total_duration += lesson["duration_minutes"]
        self.generated_count += 1
        return lesson

    def _build_image_prompt(self, subject: str, topic: str) -> str:
        return (
            f"Educational illustration of {topic} for WAEC {subject} students in Nigeria, "
            "clear diagrams, classroom context, readable labels, 4k, crisp, high contrast"
        )

    def _generate_image_asset(
        self,
        subject: str,
        topic: str,
        image_negative_prompt: Optional[str] = None,
    ) -> Optional[str]:
        try:
            from stable_image_client import generate_image, StableImageClientError
        except ImportError:
            logger.warning("⚠️ stable_image_client not available; skipping image generation")
            return None

        prompt = self._build_image_prompt(subject, topic)
        seed = random.randint(1, 1_000_000)
        output_path = Path(self.images_dir) / f"{subject.lower()}_{topic.replace(' ', '_').lower()}_{seed}.png"

        try:
            _, saved = generate_image(
                prompt,
                negative_prompt=image_negative_prompt,
                output_path=str(output_path),
                guidance_scale=7.0,
                num_inference_steps=20,
                seed=seed,
            )
            logger.info(f"🖼️  Image generated for {topic}: {saved}")
            return saved
        except StableImageClientError as exc:
            logger.warning(f"⚠️ Image generation failed for {topic}: {exc}")
            return None
    
    def _generate_objectives(self, topic: str, difficulty: str) -> List[str]:
        """Generate learning objectives for a topic"""
        
        objectives = [
            f"Understand the fundamental concepts of {topic.lower()}",
            f"Apply {topic.lower()} to real-world scenarios",
            f"Analyze and solve problems related to {topic.lower()}",
        ]
        
        if difficulty == "Advanced":
            objectives.append(f"Evaluate and compare different approaches to {topic.lower()}")
        
        return objectives
    
    def _generate_concepts(self, topic: str) -> List[str]:
        """Generate key concepts for a topic"""
        
        concept_map = {
            "Quadratic Equations": ["quadratic formula", "discriminant", "roots", "vertex", "parabola"],
            "Coordinate Geometry": ["distance formula", "slope", "line equations", "circles", "transformations"],
            "Electricity and Magnetism": ["electric field", "magnetic force", "circuits", "resistance", "power"],
            "Waves and Oscillations": ["wavelength", "frequency", "amplitude", "interference", "resonance"],
            "Atomic Structure": ["electrons", "protons", "neutrons", "orbitals", "periodic table"],
            "Cell Structure": ["nucleus", "mitochondria", "ribosomes", "cell membrane", "organelles"],
            "Microeconomics": ["supply", "demand", "equilibrium", "elasticity", "consumer behavior"],
            "Geomorphology": ["erosion", "weathering", "landforms", "plate tectonics", "soil formation"],
        }
        
        return concept_map.get(topic, ["concept 1", "concept 2", "concept 3"])
    
    def _generate_sections(self, topic: str, subject: str) -> List[Dict[str, str]]:
        """Generate content sections for a topic"""
        
        sections = [
            {
                "id": f"intro_{topic.replace(' ', '_').lower()}",
                "title": "Introduction",
                "content": f"This section introduces the key concepts of {topic} and their importance in {subject}."
            },
            {
                "id": f"main_{topic.replace(' ', '_').lower()}",
                "title": "Core Concepts",
                "content": f"The main theories, principles, and applications of {topic}. This section covers the fundamental understanding required for WAEC examinations."
            },
            {
                "id": f"application_{topic.replace(' ', '_').lower()}",
                "title": "Real-World Applications",
                "content": f"Practical examples and Nigerian context applications of {topic}. Understanding how {topic} applies in everyday life and professional contexts."
            }
        ]
        
        return sections
    
    def _generate_assessment(self, topic: str) -> Dict[str, Any]:
        """Generate assessment questions for a topic"""
        
        return {
            "questions": [
                {
                    "id": f"q1_{topic.replace(' ', '_').lower()}",
                    "type": "multiple_choice",
                    "question": f"What is the definition of {topic}?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "answer": "Option A",
                    "explanation": f"This is the correct definition of {topic}."
                },
                {
                    "id": f"q2_{topic.replace(' ', '_').lower()}",
                    "type": "short_answer",
                    "question": f"Explain how {topic} is used in practical situations.",
                    "answer": f"{topic} is used in many practical applications...",
                    "marks": 5
                }
            ],
            "totalMarks": 10
        }
    
    def _generate_nigerian_context(self, subject: str, topic: str) -> Dict[str, Any]:
        """Generate Nigerian-specific examples and context"""
        
        contexts = {
            ("Mathematics", "Quadratic Equations"): {
                "examples": ["Agricultural profit optimization", "Building construction calculations"],
                "realWorldScenario": "Nigerian farmers use quadratic equations to maximize crop yields"
            },
            ("Physics", "Electricity"): {
                "examples": ["National grid distribution", "Transformer efficiency"],
                "realWorldScenario": "NEPA electricity distribution uses principles of circuit theory"
            },
            ("Biology", "Cell Structure"): {
                "examples": ["Medical diagnostics", "Disease treatment"],
                "realWorldScenario": "Nigerian hospitals use cell biology to treat diseases"
            }
        }
        
        return contexts.get(
            (subject, topic),
            {
                "examples": [f"Nigerian context example 1", f"Nigerian context example 2"],
                "realWorldScenario": f"How {topic} applies in Nigeria"
            }
        )
    
    def save_to_file(self, lessons: List[Dict[str, Any]], filename: str) -> bool:
        """
        Save generated lessons to a JSON file
        
        Args:
            lessons: List of lesson dictionaries
            filename: Output filename
        
        Returns:
            Success status
        """
        
        try:
            Path("generated_content").mkdir(parents=True, exist_ok=True)
            
            output_path = Path("generated_content") / filename
            
            data = {
                "metadata": {
                    "generatedAt": datetime.now().isoformat(),
                    "count": len(lessons),
                    "totalDuration": self.total_duration,
                    "generatedCount": self.generated_count
                },
                "lessons": lessons
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Saved {len(lessons)} lessons to {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error saving to file: {e}")
            return False


def main():
    """Main execution"""
    generator = EnhancedContentGenerator()
    
    # Generate pilot content
    content_items = generator.generate_all_pilot_content(count=5)
    
    print()
    print("🎉 Pilot content generation complete!")
    print()
    print("📈 Statistics:")
    for item in content_items:
        print(f"  • {item['subject']}: {item['title']}")
        print(f"    - Difficulty: {item['difficulty']}")
        print(f"    - Read time: {item['estimated_read_time']} min")
        print(f"    - Diagrams: {len(item.get('diagrams', []))}")
        print()


if __name__ == "__main__":
    main()
