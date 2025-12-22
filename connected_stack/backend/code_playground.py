#!/usr/bin/env python3
"""
Code Playground Integration Module
Provides interactive coding environments and code examples for Akulearn platform.
"""

import json
import os
from typing import Dict, List, Any

class CodePlaygroundManager:
    """
    Manages interactive code playgrounds and coding challenges.
    """

    def __init__(self):
        self.code_examples = {}
        self.playgrounds = {}
        self.challenges = {}
        self.load_code_assets()

    def load_code_assets(self):
        """Load code examples and playground configurations."""
        self.code_examples = self.generate_code_examples()
        self.playgrounds = self.create_playgrounds()
        self.challenges = self.create_coding_challenges()

    def generate_code_examples(self) -> Dict[str, Any]:
        """Generate comprehensive code examples database."""
        return {
            "python": {
                "basic_syntax": {
                    "title": "Python Basic Syntax",
                    "description": "Fundamental Python programming concepts",
                    "code": """
# Variables and Data Types
name = "Alice"
age = 16
height = 5.6
is_student = True

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height}m")
print(f"Is student: {is_student}")

# Lists and Loops
subjects = ["Mathematics", "Physics", "Chemistry", "Biology"]
for subject in subjects:
    print(f"Studying: {subject}")

# Functions
def calculate_average(scores):
    return sum(scores) / len(scores)

math_scores = [85, 92, 78, 96, 88]
average = calculate_average(math_scores)
print(f"Average score: {average:.2f}")
                    """,
                    "language": "python",
                    "difficulty": "beginner",
                    "tags": ["variables", "loops", "functions", "lists"],
                    "subject": "Computer Science",
                    "level": "SS1"
                },
                "quadratic_solver": {
                    "title": "Quadratic Equation Solver",
                    "description": "Solve quadratic equations using Python",
                    "code": """
import math

def solve_quadratic(a, b, c):
    \"\"\"Solve quadratic equation ax² + bx + c = 0\"\"\"
    discriminant = b**2 - 4*a*c

    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        return f"Two real roots: {root1:.2f}, {root2:.2f}"
    elif discriminant == 0:
        root = -b / (2*a)
        return f"One real root: {root:.2f}"
    else:
        real_part = -b / (2*a)
        imag_part = math.sqrt(-discriminant) / (2*a)
        return f"Complex roots: {real_part:.2f} ± {imag_part:.2f}i"

# Test the function
print("Solving x² - 5x + 6 = 0:")
print(solve_quadratic(1, -5, 6))

print("\\nSolving x² - 4x + 4 = 0:")
print(solve_quadratic(1, -4, 4))

print("\\nSolving x² + 2x + 5 = 0:")
print(solve_quadratic(1, 2, 5))
                    """,
                    "language": "python",
                    "difficulty": "intermediate",
                    "tags": ["mathematics", "equations", "functions"],
                    "subject": "Computer Science",
                    "level": "SS2"
                }
            },
            "javascript": {
                "dom_manipulation": {
                    "title": "DOM Manipulation Basics",
                    "description": "Interact with web page elements using JavaScript",
                    "code": """
// DOM Manipulation Example
// This code demonstrates basic DOM operations

// Get elements by ID
const heading = document.getElementById('main-heading');
const button = document.getElementById('action-btn');

// Change text content
heading.textContent = 'Welcome to Akulearn!';

// Add event listener
button.addEventListener('click', function() {
    // Create new element
    const newParagraph = document.createElement('p');
    newParagraph.textContent = 'Button was clicked!';
    newParagraph.style.color = 'green';

    // Append to document
    document.body.appendChild(newParagraph);

    // Change button text
    button.textContent = 'Clicked!';
    button.disabled = true;
});

// Array operations with DOM
const subjects = ['Math', 'Physics', 'Chemistry', 'Biology'];
const subjectList = document.getElementById('subject-list');

subjects.forEach(subject => {
    const listItem = document.createElement('li');
    listItem.textContent = subject;
    subjectList.appendChild(listItem);
});
                    """,
                    "language": "javascript",
                    "difficulty": "intermediate",
                    "tags": ["dom", "events", "elements", "web"],
                    "subject": "Computer Science",
                    "level": "SS2"
                }
            }
        }

    def create_playgrounds(self) -> Dict[str, Any]:
        """Create interactive playground configurations."""
        return {
            "python_playground": {
                "id": "python-interactive",
                "title": "Python Interactive Playground",
                "description": "Write and execute Python code in real-time",
                "language": "python",
                "features": [
                    "Syntax highlighting",
                    "Auto-completion",
                    "Error highlighting",
                    "Variable inspector",
                    "Output console",
                    "Code sharing"
                ],
                "default_code": """
# Welcome to Python Playground!
# Try writing some code below:

print("Hello, Akulearn!")

# Calculate area of a circle
radius = 5
area = 3.14159 * radius ** 2
print(f"Area of circle with radius {radius} = {area:.2f}")

# Work with lists
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers]
print(f"Original: {numbers}")
print(f"Squared: {squared}")
                """,
                "libraries": ["math", "random", "datetime"],
                "max_execution_time": 10,
                "memory_limit": "50MB"
            },
            "javascript_playground": {
                "id": "javascript-interactive",
                "title": "JavaScript Interactive Playground",
                "description": "Create interactive web applications",
                "language": "javascript",
                "features": [
                    "Live HTML preview",
                    "CSS styling",
                    "DOM manipulation",
                    "Event handling",
                    "Console output",
                    "Code collaboration"
                ],
                "default_code": """
// JavaScript Playground
// This code runs in your browser!

// Basic DOM manipulation
document.body.style.backgroundColor = '#f0f8ff';

const heading = document.createElement('h1');
heading.textContent = 'Welcome to JavaScript Playground!';
heading.style.color = '#2e8b57';
document.body.appendChild(heading);

// Interactive button
const button = document.createElement('button');
button.textContent = 'Click me!';
button.style.padding = '10px 20px';
button.style.backgroundColor = '#4CAF50';
button.style.color = 'white';
button.style.border = 'none';
button.style.borderRadius = '5px';
button.style.cursor = 'pointer';

button.addEventListener('click', function() {
    alert('Hello from Akulearn! 🎓');
    button.textContent = 'Clicked! ✅';
});

document.body.appendChild(button);
                """,
                "libraries": ["jquery", "lodash", "moment"],
                "max_execution_time": 15,
                "memory_limit": "100MB"
            }
        }

    def create_coding_challenges(self) -> Dict[str, Any]:
        """Create coding challenges for different skill levels."""
        return {
            "beginner": [
                {
                    "id": "hello-world",
                    "title": "Hello World Program",
                    "description": "Write a program that prints 'Hello, World!'",
                    "difficulty": "beginner",
                    "language": "python",
                    "starter_code": "print()",
                    "solution": "print('Hello, World!')",
                    "test_cases": [
                        {"input": "", "expected": "Hello, World!"}
                    ],
                    "hints": [
                        "Use the print() function",
                        "Put your text inside quotes"
                    ]
                },
                {
                    "id": "simple-calculator",
                    "title": "Simple Calculator",
                    "description": "Create a program that adds two numbers",
                    "difficulty": "beginner",
                    "language": "python",
                    "starter_code": """
# Write code to add two numbers
num1 =
num2 =

result =
print(result)
                    """,
                    "solution": """
num1 = 5
num2 = 3
result = num1 + num2
print(result)
                    """,
                    "test_cases": [
                        {"input": "5, 3", "expected": "8"}
                    ],
                    "hints": [
                        "Store numbers in variables",
                        "Use the + operator for addition",
                        "Print the result"
                    ]
                }
            ],
            "intermediate": [
                {
                    "id": "quadratic-formula",
                    "title": "Quadratic Formula Solver",
                    "description": "Implement the quadratic formula to solve equations",
                    "difficulty": "intermediate",
                    "language": "python",
                    "starter_code": """
import math

def solve_quadratic(a, b, c):
    # Calculate discriminant
    discriminant =

    # Calculate roots
    if discriminant > 0:
        root1 =
        root2 =
        return f"Roots: {root1}, {root2}"
    elif discriminant == 0:
        root =
        return f"Root: {root}"
    else:
        return "No real roots"

# Test your function
print(solve_quadratic(1, -5, 6))  # Should give roots: 3, 2
                    """,
                    "solution": """
import math

def solve_quadratic(a, b, c):
    discriminant = b**2 - 4*a*c

    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        return f"Roots: {root1:.2f}, {root2:.2f}"
    elif discriminant == 0:
        root = -b / (2*a)
        return f"Root: {root:.2f}"
    else:
        return "No real roots"

print(solve_quadratic(1, -5, 6))
                    """,
                    "test_cases": [
                        {"input": "1, -5, 6", "expected": "Roots: 3.00, 2.00"},
                        {"input": "1, -4, 4", "expected": "Root: 2.00"}
                    ],
                    "hints": [
                        "Discriminant = b² - 4ac",
                        "Use math.sqrt() for square root",
                        "Handle three cases: two roots, one root, no real roots"
                    ]
                }
            ]
        }

    def get_code_example(self, language: str, topic: str) -> Dict[str, Any]:
        """Get a specific code example."""
        return self.code_examples.get(language, {}).get(topic, {})

    def get_playground_config(self, playground_id: str) -> Dict[str, Any]:
        """Get playground configuration."""
        return self.playgrounds.get(playground_id, {})

    def get_challenges_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """Get coding challenges by difficulty level."""
        return self.challenges.get(difficulty, [])

    def validate_code(self, code: str, language: str) -> Dict[str, Any]:
        """Basic code validation (syntax check)."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        if language == "python":
            # Basic Python validation
            if "print(" not in code and "return" not in code:
                result["warnings"].append("Code doesn't produce output")

            if "import" in code and "as" not in code:
                result["warnings"].append("Consider using 'as' for import aliases")

        elif language == "javascript":
            if "console.log(" not in code and "alert(" not in code:
                result["warnings"].append("Code doesn't produce visible output")

        return result

# Global instance
code_playground = CodePlaygroundManager()

def get_code_playground_data():
    """Get all code playground data for API integration."""
    return {
        "code_examples": code_playground.code_examples,
        "playgrounds": code_playground.playgrounds,
        "challenges": code_playground.challenges
    }

if __name__ == "__main__":
    # Test the code playground
    print("🧪 Testing Code Playground Integration...")

    # Test code examples
    python_example = code_playground.get_code_example("python", "basic_syntax")
    print(f"✅ Loaded Python example: {python_example.get('title', 'N/A')}")

    # Test playgrounds
    python_playground = code_playground.get_playground_config("python-interactive")
    print(f"✅ Loaded playground: {python_playground.get('title', 'N/A')}")

    # Test challenges
    beginner_challenges = code_playground.get_challenges_by_difficulty("beginner")
    print(f"✅ Loaded {len(beginner_challenges)} beginner challenges")

    # Test validation
    test_code = "print('Hello, World!')"
    validation = code_playground.validate_code(test_code, "python")
    print(f"✅ Code validation: {'Valid' if validation['valid'] else 'Invalid'}")

    print("🎉 Code playground integration ready!")