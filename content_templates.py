#!/usr/bin/env python3
"""
Content Templates for Akulearn
Structured templates for different subjects and content types
"""

from typing import Dict, List, Any

# Content Templates Database
CONTENT_TEMPLATES = {
    # MATHEMATICS TEMPLATES
    "math_algebra_study_guide": {
        "subject": "Mathematics",
        "topic": "Algebra",
        "content_type": "study_guide",
        "difficulty": "intermediate",
        "exam_board": "WAEC",
        "title_template": "Mastering {topic}: {specific_topic}",
        "structure": {
            "introduction": {
                "type": "heading",
                "level": 2,
                "required": True,
                "description": "Brief overview of the topic"
            },
            "learning_objectives": {
                "type": "bullet_list",
                "required": True,
                "description": "What students should learn"
            },
            "key_concepts": {
                "type": "definition_list",
                "required": True,
                "description": "Important definitions and concepts"
            },
            "worked_examples": {
                "type": "numbered_examples",
                "required": True,
                "description": "Step-by-step solved problems"
            },
            "important_formulas": {
                "type": "formula_box",
                "required": True,
                "description": "Key formulas with explanations"
            },
            "common_mistakes": {
                "type": "warning_list",
                "required": False,
                "description": "Common errors to avoid"
            },
            "practice_exercises": {
                "type": "exercise_list",
                "required": True,
                "description": "Practice problems for students"
            },
            "exam_tips": {
                "type": "highlight_box",
                "required": False,
                "description": "Tips for exam success"
            },
            "summary": {
                "type": "summary_quote",
                "required": True,
                "description": "Key takeaways"
            }
        },
        "examples": {
            "introduction": "## Solving Quadratic Equations\n\nQuadratic equations are fundamental to algebra and appear frequently in science and engineering applications.",
            "learning_objectives": "- Solve quadratic equations by factoring\n- Apply the quadratic formula\n- Complete the square method\n- Determine nature of roots using discriminant",
            "key_concepts": "**Quadratic Equation**: ax² + bx + c = 0 where a ≠ 0\n**Discriminant**: D = b² - 4ac\n**Roots**: Solutions to the equation",
            "worked_examples": "Solve x² - 5x + 6 = 0\n\n**Step 1:** Factor: (x - 2)(x - 3) = 0\n**Step 2:** x - 2 = 0 or x - 3 = 0\n**Step 3:** x = 2 or x = 3",
            "important_formulas": "**Quadratic Formula:**\n\\[ x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a} \\]\n\n**Discriminant:**\n\\[ D = b^2 - 4ac \\]",
            "practice_exercises": "1. Solve: x² + 7x + 12 = 0\n2. Find roots: 2x² - 8x + 6 = 0\n3. Determine nature of roots: x² - 6x + 9 = 0",
            "summary": "> Master the three methods: factoring for simple equations, quadratic formula for all cases, and completing square for theory problems."
        }
    },

    "math_geometry_reference": {
        "subject": "Mathematics",
        "topic": "Geometry",
        "content_type": "reference",
        "difficulty": "intermediate",
        "exam_board": "WAEC",
        "title_template": "{topic} Quick Reference: {specific_topic}",
        "structure": {
            "key_theorems": {
                "type": "theorem_list",
                "required": True,
                "description": "Important theorems and postulates"
            },
            "important_formulas": {
                "type": "formula_table",
                "required": True,
                "description": "Area, perimeter, volume formulas"
            },
            "properties": {
                "type": "property_list",
                "required": True,
                "description": "Shape properties and rules"
            },
            "common_constructions": {
                "type": "step_list",
                "required": False,
                "description": "Geometric construction methods"
            },
            "memory_aids": {
                "type": "mnemonic_list",
                "required": False,
                "description": "Mnemonics for remembering concepts"
            }
        },
        "examples": {
            "key_theorems": "**Pythagoras Theorem:** In a right-angled triangle, a² + b² = c²\n\n**Triangle Inequality:** Sum of any two sides > third side",
            "important_formulas": "| Shape | Area | Perimeter |\n|-------|------|-----------|\n| Circle | πr² | 2πr |\n| Rectangle | l×w | 2(l+w) |\n| Triangle | ½×b×h | a+b+c |",
            "properties": "- **Circle**: All points equidistant from center\n- **Square**: Equal sides, right angles\n- **Equilateral Triangle**: Equal sides, equal angles (60°)",
            "memory_aids": "**SOHCAHTOA** for trigonometry ratios\n**Please Excuse My Dear Aunt Sally** for order of operations"
        }
    },

    # PHYSICS TEMPLATES
    "physics_mechanics_study_guide": {
        "subject": "Physics",
        "topic": "Mechanics",
        "content_type": "study_guide",
        "difficulty": "intermediate",
        "exam_board": "WAEC",
        "title_template": "Understanding {topic}: {specific_topic}",
        "structure": {
            "core_principles": {
                "type": "principle_list",
                "required": True,
                "description": "Fundamental laws and principles"
            },
            "key_equations": {
                "type": "equation_set",
                "required": True,
                "description": "Important physics equations"
            },
            "problem_solving": {
                "type": "method_steps",
                "required": True,
                "description": "Step-by-step problem solving approach"
            },
            "real_world_applications": {
                "type": "application_list",
                "required": False,
                "description": "Practical applications of concepts"
            },
            "common_misconceptions": {
                "type": "myth_list",
                "required": False,
                "description": "Common wrong ideas to avoid"
            }
        },
        "examples": {
            "core_principles": "**Newton's First Law:** An object at rest stays at rest, and an object in motion stays in uniform motion unless acted upon by an unbalanced force.\n\n**Newton's Second Law:** F = ma\n\n**Newton's Third Law:** For every action, there is an equal and opposite reaction.",
            "key_equations": "**Force:** F = ma\n**Work:** W = Fd cosθ\n**Power:** P = W/t\n**Kinetic Energy:** KE = ½mv²\n**Potential Energy:** PE = mgh",
            "problem_solving": "1. **Read** the problem carefully\n2. **Identify** known and unknown quantities\n3. **Select** appropriate formula\n4. **Substitute** values and solve\n5. **Check** units and reasonableness",
            "real_world_applications": "- Car safety features (seat belts, airbags)\n- Rocket propulsion\n- Sports equipment design\n- Bridge construction",
            "common_misconceptions": "- Heavy objects fall faster than light ones\n- Force equals weight\n- Work is only done when tired"
        }
    },

    "physics_electricity_reference": {
        "subject": "Physics",
        "topic": "Electricity",
        "content_type": "reference",
        "difficulty": "intermediate",
        "exam_board": "WAEC",
        "title_template": "Electricity Quick Reference: {specific_topic}",
        "structure": {
            "fundamental_concepts": {
                "type": "concept_grid",
                "required": True,
                "description": "Basic electrical quantities"
            },
            "circuit_laws": {
                "type": "law_summaries",
                "required": True,
                "description": "Ohm's law and Kirchhoff's laws"
            },
            "component_characteristics": {
                "type": "component_table",
                "required": True,
                "description": "Resistor, capacitor, inductor properties"
            },
            "safety_guidelines": {
                "type": "safety_list",
                "required": False,
                "description": "Electrical safety precautions"
            }
        },
        "examples": {
            "fundamental_concepts": "**Charge (Q):** Fundamental property of matter\n**Current (I):** Rate of charge flow (C/s = A)\n**Voltage (V):** Electric potential difference (J/C = V)\n**Resistance (R):** Opposition to current flow (V/A = Ω)\n**Power (P):** Rate of energy transfer (W)",
            "circuit_laws": "**Ohm's Law:** V = IR\n**Kirchhoff's Current Law:** ΣI = 0 at junction\n**Kirchhoff's Voltage Law:** ΣV = 0 around loop",
            "component_characteristics": "| Component | Symbol | Function |\n|-----------|--------|----------|\n| Resistor | R | Limits current |\n| Capacitor | C | Stores charge |\n| Inductor | L | Stores energy in magnetic field |\n| Diode | D | Allows current one way |",
            "safety_guidelines": "- Never work on live circuits\n- Use insulated tools\n- Know location of circuit breakers\n- Avoid water near electrical equipment"
        }
    },

    # CHEMISTRY TEMPLATES
    "chemistry_periodic_table_summary": {
        "subject": "Chemistry",
        "topic": "Periodic Table",
        "content_type": "summary",
        "difficulty": "basic",
        "exam_board": "WAEC",
        "title_template": "Periodic Table Summary: {specific_topic}",
        "structure": {
            "table_structure": {
                "type": "structure_description",
                "required": True,
                "description": "How the periodic table is organized"
            },
            "group_characteristics": {
                "type": "group_profiles",
                "required": True,
                "description": "Properties of different groups"
            },
            "periodic_trends": {
                "type": "trend_analysis",
                "required": True,
                "description": "Atomic radius, ionization energy, etc."
            },
            "element_identification": {
                "type": "identification_guide",
                "required": False,
                "description": "How to identify unknown elements"
            },
            "exam_focus_areas": {
                "type": "priority_list",
                "required": True,
                "description": "Key areas for examinations"
            }
        },
        "examples": {
            "table_structure": "Elements arranged by increasing atomic number in rows (periods) and columns (groups). Groups have similar chemical properties. Periods show electron shell filling patterns.",
            "group_characteristics": "**Group 1 (Alkali Metals):** Highly reactive, soft metals, react with water\n**Group 7 (Halogens):** Reactive non-metals, form salts with metals\n**Group 8 (Noble Gases):** Unreactive, stable electron configuration",
            "periodic_trends": "**Atomic Radius:** Decreases across period, increases down group\n**Ionization Energy:** Increases across period, decreases down group\n**Electronegativity:** Increases across period, decreases down group",
            "element_identification": "Use atomic number, group number, period number, and properties to identify elements. Check reactivity patterns and physical state at room temperature.",
            "exam_focus_areas": "- Group properties and reactions\n- Periodic trends explanations\n- Element classification\n- Electronic configuration patterns"
        }
    },

    # BIOLOGY TEMPLATES
    "biology_cell_biology_exercise": {
        "subject": "Biology",
        "topic": "Cell Biology",
        "content_type": "exercise",
        "difficulty": "intermediate",
        "exam_board": "WAEC",
        "title_template": "Cell Biology Practice: {specific_topic}",
        "structure": {
            "question_set": {
                "type": "mixed_questions",
                "required": True,
                "description": "Multiple choice, short answer, and essay questions"
            },
            "answer_key": {
                "type": "detailed_answers",
                "required": True,
                "description": "Complete answers with explanations"
            },
            "marking_scheme": {
                "type": "mark_allocation",
                "required": True,
                "description": "How marks are awarded"
            },
            "common_errors": {
                "type": "error_analysis",
                "required": False,
                "description": "Frequent mistakes and how to avoid them"
            }
        },
        "examples": {
            "question_set": "**Section A: Multiple Choice**\n1. Which organelle is responsible for protein synthesis?\n   A) Mitochondria  B) Ribosomes  C) Lysosomes  D) Vacuoles\n\n**Section B: Short Answer**\n2. State three differences between prokaryotic and eukaryotic cells.\n\n**Section C: Essay**\n3. Describe the structure and function of the cell membrane.",
            "answer_key": "1. B) Ribosomes\n\n2. (a) Prokaryotic cells lack a nucleus; eukaryotic cells have a nucleus\n   (b) Prokaryotic cells are smaller; eukaryotic cells are larger\n   (c) Prokaryotic cells lack membrane-bound organelles; eukaryotic cells have them\n\n3. The cell membrane is a phospholipid bilayer with embedded proteins. Its functions include: controlling substance movement, maintaining cell shape, cell signaling, and protecting cell contents.",
            "marking_scheme": "**Question 1:** 1 mark\n**Question 2:** 3 marks (1 mark each point)\n**Question 3:** 8 marks (4 for structure, 4 for function)",
            "common_errors": "- Confusing ribosomes with other organelles\n- Forgetting to mention membrane-bound organelles in eukaryotic cells\n- Not explaining selective permeability of cell membrane"
        }
    },

    # ENGLISH LANGUAGE TEMPLATES
    "english_grammar_reference": {
        "subject": "English Language",
        "topic": "Grammar",
        "content_type": "reference",
        "difficulty": "basic",
        "exam_board": "WAEC",
        "title_template": "Grammar Reference: {specific_topic}",
        "structure": {
            "parts_of_speech": {
                "type": "speech_categories",
                "required": True,
                "description": "Noun, verb, adjective, etc."
            },
            "sentence_structure": {
                "type": "structure_rules",
                "required": True,
                "description": "Subject-verb agreement, tense usage"
            },
            "common_errors": {
                "type": "error_examples",
                "required": True,
                "description": "Frequently made mistakes"
            },
            "practice_sentences": {
                "type": "correction_exercises",
                "required": False,
                "description": "Sentences to correct"
            }
        },
        "examples": {
            "parts_of_speech": "**Noun:** Person, place, thing, idea\n**Verb:** Action or state word\n**Adjective:** Describes noun\n**Adverb:** Describes verb, adjective, or adverb\n**Pronoun:** Replaces noun\n**Preposition:** Shows relationship\n**Conjunction:** Joins words/clauses\n**Interjection:** Expresses emotion",
            "sentence_structure": "**Subject-Verb Agreement:** The subject and verb must agree in number\n**Tense Consistency:** Use consistent verb tenses\n**Parallel Structure:** Similar ideas should have similar structure\n**Active/Passive Voice:** Choose appropriate voice for clarity",
            "common_errors": "- Subject-verb disagreement: *He go* → *He goes*\n- Wrong tense: *I goed* → *I went*\n- Double negatives: *I don't have no money* → *I don't have any money*\n- Wrong preposition: *depend on* vs *depend from*",
            "practice_sentences": "1. She don't like apples. → She doesn't like apples.\n2. The boys plays football. → The boys play football.\n3. I have went to school. → I have gone to school."
        }
    }
}

# Subject-specific content generators
SUBJECT_GENERATORS = {
    "mathematics": {
        "algebra": ["linear_equations", "quadratic_equations", "simultaneous_equations", "inequalities"],
        "geometry": ["triangles", "circles", "coordinate_geometry", "transformations"],
        "trigonometry": ["ratios", "identities", "triangle_solutions", "applications"],
        "statistics": ["mean_median_mode", "probability", "data_representation"]
    },

    "physics": {
        "mechanics": ["newtons_laws", "energy", "momentum", "circular_motion"],
        "electricity": ["circuits", "magnetism", "electromagnetism", "capacitance"],
        "waves": ["wave_properties", "sound", "light", "optics"],
        "modern_physics": ["atomic_structure", "radioactivity", "nuclear_physics"]
    },

    "chemistry": {
        "physical": ["atomic_structure", "bonding", "states_of_matter", "solutions"],
        "inorganic": ["periodic_table", "chemical_reactions", "acids_bases", "salts"],
        "organic": ["hydrocarbons", "functional_groups", "polymers", "biochemistry"]
    },

    "biology": {
        "cell_biology": ["cell_structure", "cell_organelles", "cell_division", "transport"],
        "genetics": ["inheritance", "dna", "genetic_engineering", "evolution"],
        "ecology": ["ecosystems", "food_chains", "pollution", "conservation"],
        "physiology": ["digestion", "respiration", "circulation", "homeostasis"]
    },

    "english": {
        "grammar": ["parts_of_speech", "sentence_structure", "tenses", "punctuation"],
        "literature": ["poetry", "drama", "prose", "literary_devices"],
        "writing": ["essay_writing", "comprehension", "summary_writing", "letter_writing"]
    }
}

def get_template(template_name: str) -> Dict[str, Any]:
    """Get a specific content template"""
    return CONTENT_TEMPLATES.get(template_name)

def get_subject_templates(subject: str) -> List[str]:
    """Get all templates for a specific subject"""
    return [name for name, template in CONTENT_TEMPLATES.items()
            if template["subject"].lower() == subject.lower()]

def get_content_type_templates(content_type: str) -> List[str]:
    """Get all templates for a specific content type"""
    return [name for name, template in CONTENT_TEMPLATES.items()
            if template["content_type"] == content_type]

def generate_content_outline(template_name: str, specific_topic: str = "") -> Dict[str, Any]:
    """Generate a content outline using a template"""
    if template_name not in CONTENT_TEMPLATES:
        return None

    template = CONTENT_TEMPLATES[template_name].copy()

    # Customize title if specific topic provided
    if specific_topic:
        template["title"] = template["title_template"].format(
            topic=template["topic"],
            subject=template["subject"],
            specific_topic=specific_topic
        )
    else:
        template["title"] = template["title_template"].format(
            topic=template["topic"],
            subject=template["subject"],
            specific_topic=template["topic"]
        )

    return template

def list_available_templates() -> None:
    """Print all available templates"""
    print("📋 Available Content Templates:")
    print("=" * 50)

    by_subject = {}
    for name, template in CONTENT_TEMPLATES.items():
        subject = template["subject"]
        if subject not in by_subject:
            by_subject[subject] = []
        by_subject[subject].append((name, template))

    for subject, templates in by_subject.items():
        print(f"\n🎓 {subject}:")
        for name, template in templates:
            print(f"  • {name}: {template['content_type']} - {template['topic']}")

if __name__ == "__main__":
    list_available_templates()