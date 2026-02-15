#!/usr/bin/env python3
"""
Bulk Content Generator for Akulearn
Generates educational content for multiple subjects and topics using templates
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

# Add the connected_stack/backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'connected_stack', 'backend'))

try:
    from content_service import content_service
    from content_templates import CONTENT_TEMPLATES, SUBJECT_GENERATORS
except ImportError as e:
    print(f"ERROR: Could not import required modules: {e}")
    sys.exit(1)

class BulkContentGenerator:
    """Generate content for multiple subjects and topics"""

    def __init__(self):
        self.content_service = content_service
        self.templates = CONTENT_TEMPLATES
        self.subject_generators = SUBJECT_GENERATORS

    def generate_topic_content(self, subject: str, topic: str, subtopics: List[str]) -> List[Dict[str, Any]]:
        """Generate content for a specific topic with multiple subtopics"""
        generated_content = []

        # Find appropriate template for the subject/topic
        template_key = self._find_template(subject, topic)
        if not template_key:
            print(f"Warning: No template found for {subject}/{topic}, using generic")
            template_key = "math_algebra_study_guide"  # fallback

        template = self.templates[template_key]

        for subtopic in subtopics:
            try:
                content = self._generate_single_content(template, subject, topic, subtopic)
                if content:
                    generated_content.append(content)
                    print(f"✓ Generated: {content['title']}")
            except Exception as e:
                print(f"✗ Failed to generate {subtopic}: {e}")

        return generated_content

    def _find_template(self, subject: str, topic: str) -> Optional[str]:
        """Find the most appropriate template for subject/topic"""
        subject_lower = subject.lower()
        topic_lower = topic.lower()

        # Direct matches
        for key, template in self.templates.items():
            if (template["subject"].lower() == subject_lower and
                template["topic"].lower() == topic_lower):
                return key

        # Subject matches
        subject_templates = [k for k, t in self.templates.items()
                           if t["subject"].lower() == subject_lower]
        if subject_templates:
            return subject_templates[0]

        return None

    def _generate_single_content(self, template: Dict[str, Any], subject: str, topic: str, subtopic: str) -> Dict[str, Any]:
        """Generate a single piece of content"""
        # Generate unique ID
        content_id = f"{subject.lower()}_{topic.lower()}_{subtopic.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Generate title
        title = f"{subtopic.title()} in {topic}"

        # Generate content based on template structure
        content_parts = []

        # Introduction
        content_parts.append(f"# {title}\n")

        # Learning objectives
        if "learning_objectives" in template.get("structure", {}):
            content_parts.append("## Learning Objectives\n")
            content_parts.append(f"By the end of this {template['content_type'].replace('_', ' ')}, you should be able to:\n")
            objectives = self._generate_objectives(subject, topic, subtopic)
            content_parts.append(objectives + "\n")

        # Main content
        content_parts.append("## Key Concepts\n")
        main_content = self._generate_main_content(subject, topic, subtopic)
        content_parts.append(main_content + "\n")

        # Examples/Practice
        if template["content_type"] in ["study_guide", "exercise"]:
            content_parts.append("## Examples and Practice\n")
            examples = self._generate_examples(subject, topic, subtopic)
            content_parts.append(examples + "\n")

        # Formulas (for math/science)
        if subject.lower() in ["mathematics", "physics", "chemistry"]:
            content_parts.append("## Important Formulas\n")
            formulas = self._generate_formulas(subject, topic, subtopic)
            content_parts.append(formulas + "\n")

        # Summary
        content_parts.append("## Summary\n")
        summary = self._generate_summary(subject, topic, subtopic)
        content_parts.append(summary + "\n")

        content_text = "\n".join(content_parts)

        # Create content object
        content_obj = {
            "id": content_id,
            "title": title,
            "subject": subject,
            "topic": topic,
            "content_type": template["content_type"],
            "difficulty": template["difficulty"],
            "exam_board": template["exam_board"],
            "content": content_text,
            "estimated_read_time": self._estimate_read_time(content_text),
            "prerequisites": self._generate_prerequisites(subject, topic),
            "related_questions": self._generate_related_questions(subject, topic, subtopic),
            "tags": self._generate_tags(subject, topic, subtopic),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "author": f"{subject} Expert",
            "version": 1
        }

        return content_obj

    def _generate_objectives(self, subject: str, topic: str, subtopic: str) -> str:
        """Generate learning objectives"""
        objectives = {
            "mathematics": {
                "algebra": ["- Solve equations and inequalities", "- Work with polynomials and functions", "- Apply algebraic methods to problems"],
                "geometry": ["- Identify and classify shapes", "- Apply geometric theorems", "- Solve coordinate geometry problems"],
                "trigonometry": ["- Use trigonometric ratios and identities", "- Solve triangles", "- Apply trigonometry to real-world problems"],
                "calculus": ["- Understand differentiation and integration", "- Apply calculus to rates of change", "- Solve optimization problems"],
                "statistics": ["- Calculate mean, median, and mode", "- Understand probability concepts", "- Analyze data distributions"]
            },
            "physics": {
                "mechanics": ["- Apply Newton's laws of motion", "- Solve problems involving forces and energy", "- Understand momentum and collisions"],
                "electricity": ["- Analyze electric circuits", "- Understand magnetism and electromagnetism", "- Apply electrical principles"],
                "waves": ["- Understand wave properties", "- Analyze sound and light waves", "- Apply wave principles"],
                "modern_physics": ["- Understand atomic structure", "- Learn about radioactivity", "- Apply modern physics concepts"]
            },
            "chemistry": {
                "physical_chemistry": ["- Understand atomic structure and bonding", "- Study states of matter", "- Apply physical chemistry principles"],
                "inorganic_chemistry": ["- Use the periodic table", "- Understand chemical reactions", "- Study acids, bases, and salts"],
                "organic_chemistry": ["- Study hydrocarbons and functional groups", "- Understand organic reactions", "- Apply organic chemistry"]
            },
            "biology": {
                "cell_biology": ["- Understand cell structure and function", "- Study cell organelles", "- Learn about cell processes"],
                "genetics": ["- Understand inheritance patterns", "- Study DNA and genetic processes", "- Learn about reproduction"],
                "ecology": ["- Understand ecosystems and interactions", "- Study environmental biology", "- Learn about conservation"],
                "physiology": ["- Study human body systems", "- Understand homeostasis", "- Learn about physiological processes"]
            },
            "english": {
                "grammar": ["- Identify parts of speech", "- Understand sentence structure", "- Apply grammar rules correctly"],
                "literature": ["- Analyze literary works", "- Understand literary devices", "- Develop comprehension skills"],
                "writing": ["- Write effective essays", "- Improve comprehension skills", "- Master writing techniques"]
            }
        }

        subject_key = subject.lower().replace(" ", "_")
        topic_key = topic.lower().replace(" ", "_")

        if subject_key in objectives and topic_key in objectives[subject_key]:
            return "\n".join(objectives[subject_key][topic_key])

        return "- Understand the fundamental concepts\n- Apply knowledge to solve problems\n- Develop critical thinking skills"

    def _generate_main_content(self, subject: str, topic: str, subtopic: str) -> str:
        """Generate main content for the topic"""
        content_map = {
            "mathematics": {
                "equations": "Equations are mathematical statements that assert the equality of two expressions. They can be solved by isolating the variable using inverse operations.",
                "inequalities": "Inequalities show the relationship between two expressions using symbols like <, >, ≤, ≥. They represent ranges of values rather than single solutions.",
                "polynomials": "Polynomials are expressions consisting of variables and coefficients, combined using addition, subtraction, and multiplication.",
                "functions": "Functions are relations where each input has exactly one output. They can be represented algebraically, graphically, or in tables.",
                "shapes": "Geometric shapes have specific properties and formulas for area, perimeter, and volume calculations.",
                "theorems": "Geometric theorems are proven statements about relationships between different geometric elements.",
                "coordinate_geometry": "Coordinate geometry combines algebra and geometry to study geometric figures using coordinates.",
                "identities": "Trigonometric identities are equations that are true for all values of the variables involved.",
                "triangles": "Triangles are three-sided polygons with specific properties and trigonometric relationships.",
                "applications": "Trigonometry has applications in navigation, physics, engineering, and surveying.",
                "differentiation": "Differentiation is the process of finding the derivative, which represents the rate of change.",
                "integration": "Integration is the reverse process of differentiation, used to find areas and solve differential equations.",
                "mean": "The mean is the average of a set of numbers, calculated by summing all values and dividing by the count.",
                "median": "The median is the middle value in an ordered set of numbers.",
                "probability": "Probability is the measure of how likely an event is to occur, expressed as a number between 0 and 1."
            },
            "physics": {
                "motion": "Motion is the change in position of an object over time. It can be described using displacement, velocity, and acceleration.",
                "forces": "Forces are pushes or pulls that can change an object's motion. They have magnitude and direction.",
                "energy": "Energy is the capacity to do work. It exists in various forms including kinetic, potential, and thermal.",
                "momentum": "Momentum is the product of mass and velocity. It is conserved in collisions.",
                "circuits": "Electric circuits consist of components connected by conductors to allow current flow.",
                "magnetism": "Magnetism is a force exerted by magnets, caused by moving electric charges.",
                "electromagnetism": "Electromagnetism is the interaction between electric and magnetic fields.",
                "sound": "Sound waves are mechanical waves that require a medium for propagation.",
                "light": "Light is an electromagnetic wave that can travel through vacuum and exhibits wave-particle duality.",
                "wave_properties": "Waves have properties like wavelength, frequency, amplitude, and speed.",
                "atomic_structure": "Atoms consist of protons, neutrons, and electrons arranged in specific energy levels.",
                "radioactivity": "Radioactivity is the spontaneous emission of radiation from unstable atomic nuclei."
            },
            "chemistry": {
                "atomic_structure": "Atoms are the basic units of matter, consisting of protons, neutrons, and electrons.",
                "bonding": "Chemical bonding involves the interaction of atoms to form compounds through various types of bonds.",
                "states_of_matter": "Matter exists in three main states: solid, liquid, and gas, each with distinct properties.",
                "periodic_table": "The periodic table organizes elements by atomic number and shows trends in properties.",
                "chemical_reactions": "Chemical reactions involve the transformation of substances into new substances with different properties.",
                "hydrocarbons": "Hydrocarbons are organic compounds containing only hydrogen and carbon atoms.",
                "functional_groups": "Functional groups are specific atom groupings that determine the chemical properties of organic compounds."
            },
            "biology": {
                "cell_structure": "Cells are the basic structural and functional units of life, with various organelles performing specific functions.",
                "functions": "Cell functions include energy production, protein synthesis, waste removal, and reproduction.",
                "inheritance": "Inheritance is the transmission of genetic information from parents to offspring.",
                "dna": "DNA is the molecule that carries genetic information and directs cellular activities.",
                "reproduction": "Reproduction is the process by which organisms produce offspring, either sexually or asexually.",
                "ecosystems": "Ecosystems are communities of living organisms interacting with their physical environment.",
                "environmental_biology": "Environmental biology studies the relationships between organisms and their environment.",
                "systems": "Human body systems work together to maintain homeostasis and ensure proper functioning.",
                "homeostasis": "Homeostasis is the maintenance of stable internal conditions despite external changes."
            },
            "english": {
                "parts_of_speech": "Parts of speech are categories of words based on their grammatical function: nouns, verbs, adjectives, etc.",
                "sentence_structure": "Sentence structure refers to the arrangement of words and phrases to create meaningful sentences.",
                "comprehension": "Comprehension involves understanding and interpreting written or spoken language.",
                "analysis": "Literary analysis examines the elements, themes, and techniques used in literary works.",
                "criticism": "Literary criticism evaluates and interprets literature using various theoretical approaches.",
                "essay_writing": "Essay writing involves organizing ideas into coherent, well-structured arguments."
            }
        }

        subject_key = subject.lower()
        subtopic_key = subtopic.lower().replace(" ", "_")

        if subject_key in content_map and subtopic_key in content_map[subject_key]:
            return content_map[subject_key][subtopic_key]

        return f"{subtopic} is an important concept in {topic} that forms the foundation for understanding more advanced topics in {subject}."

    def _generate_examples(self, subject: str, topic: str, subtopic: str) -> str:
        """Generate examples and practice problems"""
        examples = {
            "mathematics": {
                "equations": "**Example:** Solve 2x + 3 = 7\n**Solution:** 2x = 4, x = 2\n\n**Practice:** Solve 3x - 5 = 10",
                "inequalities": "**Example:** Solve x + 2 > 5\n**Solution:** x > 3\n\n**Practice:** Solve 2x - 1 ≤ 7",
                "polynomials": "**Example:** Expand (x + 2)(x + 3) = x² + 5x + 6\n\n**Practice:** Expand (x - 1)(x + 4)",
                "functions": "**Example:** f(x) = 2x + 1, find f(3) = 7\n\n**Practice:** g(x) = x² - 4, find g(-2)",
                "shapes": "**Example:** Area of rectangle = length × width\n\n**Practice:** Calculate area of circle with radius 5cm",
                "theorems": "**Example:** Pythagoras: 3-4-5 triangle\n\n**Practice:** Verify Pythagoras for 5-12-13 triangle",
                "coordinate_geometry": "**Example:** Distance between (1,2) and (4,6) = √[(4-1)² + (6-2)²] = √[9 + 16] = 5\n\n**Practice:** Find distance between (0,0) and (3,4)",
                "identities": "**Example:** sin²θ + cos²θ = 1\n\n**Practice:** Verify for θ = 30°",
                "triangles": "**Example:** In right triangle, sin A = opposite/hypotenuse\n\n**Practice:** Find missing side using Pythagoras",
                "applications": "**Example:** Height of building using angle of elevation\n\n**Practice:** Calculate distance using trigonometry",
                "differentiation": "**Example:** d/dx(x²) = 2x\n\n**Practice:** d/dx(x³ + 2x) = ?",
                "integration": "**Example:** ∫x dx = x²/2 + C\n\n**Practice:** ∫(2x + 1) dx = ?",
                "mean": "**Example:** Mean of 2, 4, 6, 8 = (2+4+6+8)/4 = 5\n\n**Practice:** Find mean of 1, 3, 5, 7, 9",
                "median": "**Example:** Median of 1, 3, 5, 7, 9 = 5\n\n**Practice:** Find median of 2, 4, 6, 8, 10",
                "probability": "**Example:** P(heads) = 1/2 for fair coin\n\n**Practice:** P(rolling 4 on die) = ?"
            },
            "physics": {
                "motion": "**Example:** Car accelerates from 0 to 60 km/h in 10s\n\n**Practice:** Calculate average velocity",
                "forces": "**Example:** F = ma, 10N force on 2kg mass gives 5 m/s² acceleration\n\n**Practice:** Find force needed for given acceleration",
                "energy": "**Example:** KE = ½mv², m=2kg, v=3m/s, KE=9J\n\n**Practice:** Calculate PE for 5kg mass at 10m height",
                "momentum": "**Example:** p = mv, 2kg mass at 4m/s has momentum 8 kg·m/s\n\n**Practice:** Find change in momentum",
                "circuits": "**Example:** Series circuit: R_total = R1 + R2\n\n**Practice:** Calculate total resistance",
                "magnetism": "**Example:** Magnetic field around current-carrying wire\n\n**Practice:** Determine field direction",
                "electromagnetism": "**Example:** Motor effect: F = BIL sinθ\n\n**Practice:** Calculate force on wire",
                "sound": "**Example:** Speed of sound = 343 m/s at 20°C\n\n**Practice:** Calculate wavelength for 440Hz",
                "light": "**Example:** Refractive index n = c/v\n\n**Practice:** Find angle of refraction",
                "wave_properties": "**Example:** v = fλ, f=100Hz, λ=2m, v=200m/s\n\n**Practice:** Find frequency for given speed and wavelength",
                "atomic_structure": "**Example:** Carbon has 6 protons, 6 neutrons, 6 electrons\n\n**Practice:** Find atomic number and mass number",
                "radioactivity": "**Example:** Half-life of radioactive substance\n\n**Practice:** Calculate remaining amount after 2 half-lives"
            },
            "chemistry": {
                "atomic_structure": "**Example:** Sodium: 11 protons, 12 neutrons, 11 electrons\n\n**Practice:** Draw Bohr diagram for magnesium",
                "bonding": "**Example:** Ionic bond: Na⁺ + Cl⁻ → NaCl\n\n**Practice:** Predict bond type between Mg and O",
                "states_of_matter": "**Example:** Gas particles move freely, liquid particles touch, solid particles fixed\n\n**Practice:** Compare densities of states",
                "periodic_table": "**Example:** Group 1 elements are highly reactive metals\n\n**Practice:** Predict properties of Group 17 elements",
                "chemical_reactions": "**Example:** 2H₂ + O₂ → 2H₂O (synthesis)\n\n**Practice:** Balance: C + O₂ → CO₂",
                "hydrocarbons": "**Example:** Methane CH₄, Ethane C₂H₆\n\n**Practice:** Draw structural formula for propane",
                "functional_groups": "**Example:** -OH is alcohol group\n\n**Practice:** Identify functional group in CH₃COOH"
            },
            "biology": {
                "cell_structure": "**Example:** Nucleus contains DNA and controls cell activities\n\n**Practice:** Label cell organelles",
                "functions": "**Example:** Mitochondria produce energy (ATP)\n\n**Practice:** Explain ribosome function",
                "inheritance": "**Example:** Tall (T) dominant over short (t)\n\n**Practice:** Predict offspring from Tt × tt",
                "dna": "**Example:** DNA structure: double helix with base pairs A-T, C-G\n\n**Practice:** Explain DNA replication",
                "reproduction": "**Example:** Mitosis produces identical cells, meiosis produces gametes\n\n**Practice:** Compare mitosis and meiosis",
                "ecosystems": "**Example:** Food chain: grass → rabbit → fox\n\n**Practice:** Draw energy pyramid",
                "environmental_biology": "**Example:** Deforestation reduces biodiversity\n\n**Practice:** Explain greenhouse effect",
                "systems": "**Example:** Digestive system breaks down food\n\n**Practice:** Describe circulatory system",
                "homeostasis": "**Example:** Body temperature regulation\n\n**Practice:** Explain osmoregulation in kidneys"
            },
            "english": {
                "parts_of_speech": "**Example:** The big dog (adjective) ran (verb) quickly (adverb).\n\n**Practice:** Identify parts of speech in a sentence",
                "sentence_structure": "**Example:** Subject + Verb + Object = Complete sentence\n\n**Practice:** Correct sentence fragments",
                "comprehension": "**Example:** Read passage and answer questions\n\n**Practice:** Summarize main ideas",
                "analysis": "**Example:** Identify theme, character, setting in a story\n\n**Practice:** Analyze author's purpose",
                "criticism": "**Example:** Evaluate literary merit and techniques\n\n**Practice:** Write critical review",
                "essay_writing": "**Example:** Introduction, body paragraphs, conclusion\n\n**Practice:** Outline an argumentative essay"
            }
        }

        subject_key = subject.lower()
        subtopic_key = subtopic.lower().replace(" ", "_")

        if subject_key in examples and subtopic_key in examples[subject_key]:
            return examples[subject_key][subtopic_key]

        return f"**Example:** Study the concept of {subtopic} in {topic}\n\n**Practice:** Apply the concepts learned to solve related problems"

    def _generate_formulas(self, subject: str, topic: str, subtopic: str) -> str:
        """Generate important formulas"""
        formulas = {
            "mathematics": {
                "equations": "**Linear:** ax + b = 0 → x = -b/a\n**Quadratic:** ax² + bx + c = 0 → x = [-b ± √(b²-4ac)]/2a",
                "inequalities": "**Linear:** ax + b > 0 → x > -b/a\n**Quadratic:** ax² + bx + c > 0 → solve using discriminant",
                "polynomials": "**Addition:** (a + b)(c + d) = ac + ad + bc + bd\n**Difference:** (a + b)(a - b) = a² - b²",
                "functions": "**Linear:** f(x) = mx + c\n**Quadratic:** f(x) = ax² + bx + c",
                "shapes": "**Circle Area:** A = πr²\n**Rectangle Area:** A = l × w\n**Triangle Area:** A = ½ × b × h",
                "theorems": "**Pythagoras:** a² + b² = c²\n**Triangle Sum:** A + B + C = 180°",
                "coordinate_geometry": "**Distance:** d = √[(x₂-x₁)² + (y₂-y₁)²]\n**Midpoint:** ((x₁+x₂)/2, (y₁+y₂)/2)",
                "identities": "**sin²θ + cos²θ = 1**\n**tanθ = sinθ/cosθ**\n**1 + tan²θ = sec²θ**",
                "triangles": "**Sine Rule:** a/sinA = b/sinB = c/sinC\n**Cosine Rule:** c² = a² + b² - 2ab cosC",
                "differentiation": "**Power Rule:** d/dx(xⁿ) = nxⁿ⁻¹\n**Sum Rule:** d/dx(f+g) = f' + g'",
                "integration": "**Power Rule:** ∫xⁿ dx = xⁿ⁺¹/(n+1) + C\n**∫k dx = kx + C**",
                "mean": "**Arithmetic Mean:** μ = Σxᵢ/n\n**Weighted Mean:** μ = Σ(wᵢxᵢ)/Σwᵢ",
                "median": "**For odd n:** median = middle value\n**For even n:** median = average of two middle values",
                "probability": "**P(A) = n(A)/n(S)**\n**P(A∪B) = P(A) + P(B) - P(A∩B)**"
            },
            "physics": {
                "motion": "**v = u + at**\n**s = ut + ½at²**\n**v² = u² + 2as**",
                "forces": "**F = ma**\n**W = mg**\n**F = kx (Hooke's law)**",
                "energy": "**KE = ½mv²**\n**PE = mgh**\n**W = Fd cosθ**",
                "momentum": "**p = mv**\n**Conservation:** m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂",
                "circuits": "**V = IR (Ohm's law)**\n**Series R_total = R₁ + R₂ + R₃**\n**Parallel 1/R_total = 1/R₁ + 1/R₂ + 1/R₃**",
                "magnetism": "**F = BIL sinθ**\n**Φ = BA cosθ**\n**F = qvB sinθ**",
                "electromagnetism": "**ε = -dΦ/dt**\n**F = BIL sinθ**\n**Motor effect applications**",
                "sound": "**v = fλ**\n**Doppler: f' = f(v ± v₀)/(v ± vₛ)**",
                "light": "**n = c/v**\n**Snell's law: n₁sinθ₁ = n₂sinθ₂**\n**Lens: 1/f = 1/u + 1/v**",
                "wave_properties": "**v = fλ**\n**T = 1/f**\n**I ∝ A²**",
                "atomic_structure": "**E = hc/λ**\n**Bohr: mvr = nh/2π**\n**Quantum numbers**",
                "radioactivity": "**λ = ln2/t½**\n**N = N₀e^(-λt)**\n**Decay constant relationships**"
            },
            "chemistry": {
                "atomic_structure": "**Atomic number = protons**\n**Mass number = protons + neutrons**\n**Isotopes have same Z, different A**",
                "bonding": "**Ionic:** Metal + non-metal\n**Covalent:** Non-metal + non-metal\n**Metallic:** Metal atoms**",
                "states_of_matter": "**Gas:** PV = nRT\n**Kinetic theory**\n**Phase changes**",
                "periodic_table": "**Atomic radius decreases across period**\n**Ionization energy increases across period**\n**Electronegativity increases across period**",
                "chemical_reactions": "**Conservation of mass**\n**Balancing equations**\n**Reaction types**",
                "hydrocarbons": "**Alkanes: CₙH₂ₙ₊₂**\n**Alkenes: CₙH₂ₙ**\n**Alkynes: CₙH₂ₙ₋₂**",
                "functional_groups": "**-OH: Alcohol**\n**-COOH: Carboxylic acid**\n**-NH₂: Amine**"
            }
        }

        subject_key = subject.lower()
        subtopic_key = subtopic.lower().replace(" ", "_")

        if subject_key in formulas and subtopic_key in formulas[subject_key]:
            return formulas[subject_key][subtopic_key]

        return "Key formulas and equations will be provided in the detailed study guide."

    def _generate_summary(self, subject: str, topic: str, subtopic: str) -> str:
        """Generate summary for the topic"""
        summaries = {
            "mathematics": f"{subtopic} is a fundamental concept in {topic} that provides the foundation for more advanced mathematical studies. Practice regularly to master the techniques and applications.",
            "physics": f"Understanding {subtopic} in {topic} is crucial for explaining natural phenomena and technological applications. Focus on both theoretical concepts and practical problem-solving.",
            "chemistry": f"{subtopic} forms the basis for understanding chemical behavior and reactions. Regular practice with examples will help master these important concepts.",
            "biology": f"{subtopic} is essential for understanding living organisms and biological processes. Connect these concepts with real-world observations for better comprehension.",
            "english": f"Mastering {subtopic} in {topic} will improve your communication skills and analytical abilities. Practice regularly with various texts and writing exercises."
        }

        subject_key = subject.lower()
        return summaries.get(subject_key, f"{subtopic} is an important topic that requires careful study and regular practice.")

    def _estimate_read_time(self, content: str) -> int:
        """Estimate reading time in minutes"""
        words = len(content.split())
        # Average reading speed: 200 words per minute
        return max(1, round(words / 200))

    def _generate_prerequisites(self, subject: str, topic: str) -> List[str]:
        """Generate prerequisite knowledge"""
        prereqs = {
            "mathematics": ["basic_arithmetic", "algebra_fundamentals"],
            "physics": ["mathematics", "basic_physics_concepts"],
            "chemistry": ["basic_chemistry", "periodic_table_basics"],
            "biology": ["basic_biology", "cell_structure"],
            "english": ["basic_english", "reading_comprehension"]
        }
        return prereqs.get(subject.lower(), [])

    def _generate_related_questions(self, subject: str, topic: str, subtopic: str) -> List[str]:
        """Generate related question IDs"""
        return [f"waec_{subject.lower()}_2020_q1", f"waec_{subject.lower()}_2021_q2"]

    def _generate_tags(self, subject: str, topic: str, subtopic: str) -> List[str]:
        """Generate content tags"""
        return [subject.lower(), topic.lower(), subtopic.lower().replace(" ", "_")]

    def generate_all_content(self, content_plan: Dict[str, Dict[str, List[str]]]) -> List[Dict[str, Any]]:
        """Generate content for all subjects and topics in the plan"""
        all_content = []

        for subject, topics in content_plan.items():
            print(f"\n📚 Generating content for {subject}...")
            for topic, subtopics in topics.items():
                print(f"  📖 Processing {topic}...")
                topic_content = self.generate_topic_content(subject, topic, subtopics)
                all_content.extend(topic_content)

        return all_content

    def save_content(self, content_list: List[Dict[str, Any]]) -> None:
        """Save generated content to the content service"""
        saved_count = 0
        for content in content_list:
            try:
                self.content_service.add_content(content)
                saved_count += 1
            except Exception as e:
                print(f"Failed to save content '{content['title']}': {e}")

        print(f"\n✅ Successfully saved {saved_count} content items")

def main():
    """Main function to generate content"""
    generator = BulkContentGenerator()

    # Content generation plan based on user's request
    content_plan = {
        "Mathematics": {
            "Algebra": ["Equations", "Inequalities", "Polynomials", "Functions"],
            "Geometry": ["Shapes", "Theorems", "Coordinate Geometry"],
            "Trigonometry": ["Identities", "Triangles", "Applications"],
            "Calculus": ["Differentiation", "Integration"],
            "Statistics": ["Mean", "Median", "Probability"]
        },
        "Physics": {
            "Mechanics": ["Motion", "Forces", "Energy", "Momentum"],
            "Electricity": ["Circuits", "Magnetism", "Electromagnetism"],
            "Waves": ["Sound", "Light", "Wave Properties"],
            "Modern Physics": ["Atomic Structure", "Radioactivity"]
        },
        "Chemistry": {
            "Physical Chemistry": ["Atomic Structure", "Bonding", "States of Matter"],
            "Inorganic Chemistry": ["Periodic Table", "Chemical Reactions"],
            "Organic Chemistry": ["Hydrocarbons", "Functional Groups"]
        },
        "Biology": {
            "Cell Biology": ["Cell Structure", "Functions"],
            "Genetics": ["Inheritance", "DNA", "Reproduction"],
            "Ecology": ["Ecosystems", "Environmental Biology"],
            "Human Physiology": ["Systems", "Homeostasis"]
        },
        "English Language": {
            "Grammar": ["Parts of Speech", "Sentence Structure"],
            "Literature": ["Comprehension", "Analysis", "Criticism"],
            "Writing": ["Essay Writing", "Comprehension"]
        }
    }

    print("🚀 Starting bulk content generation...")
    print(f"Planning to generate content for {sum(len(subtopics) for topics in content_plan.values() for subtopics in topics.values())} topics")

    # Generate all content
    all_content = generator.generate_all_content(content_plan)

    # Save content
    generator.save_content(all_content)

    print(f"\n🎉 Content generation complete! Generated {len(all_content)} content items.")

    # Show statistics
    subject_counts = {}
    for content in all_content:
        subject = content["subject"]
        subject_counts[subject] = subject_counts.get(subject, 0) + 1

    print("\n📊 Content Generation Statistics:")
    for subject, count in subject_counts.items():
        print(f"  {subject}: {count} items")

if __name__ == "__main__":
    main()