#!/usr/bin/env python3
"""
Content Creation Templates and Manual Entry System for Akulearn
Provides structured templates and forms for manual content creation
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Add the connected_stack/backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'connected_stack', 'backend'))

try:
    from content_service import content_service
except ImportError:
    print("ERROR: Could not import content_service. Make sure connected_stack/backend/content_service.py exists.")
    sys.exit(1)

@dataclass
class ContentTemplate:
    """Template for content creation"""
    subject: str
    topic: str
    content_type: str
    difficulty: str
    exam_board: str
    title_template: str
    content_structure: Dict[str, Any]
    required_sections: List[str]
    example_content: Dict[str, str]

class ContentCreator:
    """Manual content creation system"""

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, ContentTemplate]:
        """Load content creation templates"""
        return {
            "math_study_guide": ContentTemplate(
                subject="Mathematics",
                topic="Algebra",
                content_type="study_guide",
                difficulty="intermediate",
                exam_board="WAEC",
                title_template="Understanding {topic} in {subject}",
                content_structure={
                    "introduction": {"type": "heading", "level": 2, "required": True},
                    "learning_objectives": {"type": "list", "required": True},
                    "main_content": {"type": "paragraph", "required": True},
                    "worked_examples": {"type": "numbered_list", "required": True},
                    "key_formulas": {"type": "code_block", "required": True},
                    "common_mistakes": {"type": "list", "required": False},
                    "practice_problems": {"type": "exercise", "required": True},
                    "summary": {"type": "quote", "required": True}
                },
                required_sections=["introduction", "learning_objectives", "main_content", "worked_examples", "key_formulas", "practice_problems", "summary"],
                example_content={
                    "introduction": "## Introduction to Quadratic Equations\n\nQuadratic equations are polynomial equations of degree 2 with the general form ax² + bx + c = 0.",
                    "learning_objectives": "- Define quadratic equations\n- Solve quadratic equations using factoring, completing the square, and quadratic formula\n- Apply quadratic equations to real-world problems",
                    "main_content": "A quadratic equation is any equation that can be written in the form ax² + bx + c = 0, where a, b, and c are real numbers and a ≠ 0.",
                    "worked_examples": "1. Solve x² + 5x + 6 = 0\n   (x + 2)(x + 3) = 0\n   x = -2 or x = -3",
                    "key_formulas": "Quadratic Formula: x = [-b ± √(b² - 4ac)] / 2a",
                    "practice_problems": "Solve the following quadratic equations:\n1. x² - 4x - 5 = 0\n2. 2x² + 3x - 2 = 0",
                    "summary": "> Quadratic equations can be solved using factoring, completing the square, or the quadratic formula. Always check your solutions by substitution."
                }
            ),

            "physics_reference": ContentTemplate(
                subject="Physics",
                topic="Electricity",
                content_type="reference",
                difficulty="basic",
                exam_board="WAEC",
                title_template="{topic} Fundamentals - {subject} Reference",
                content_structure={
                    "key_concepts": {"type": "list", "required": True},
                    "important_formulas": {"type": "code_block", "required": True},
                    "units": {"type": "table", "required": True},
                    "diagrams": {"type": "description", "required": False},
                    "common_values": {"type": "list", "required": False}
                },
                required_sections=["key_concepts", "important_formulas", "units"],
                example_content={
                    "key_concepts": "- **Current**: Rate of flow of electric charge\n- **Voltage**: Electric potential difference\n- **Resistance**: Opposition to current flow\n- **Power**: Rate of energy transfer",
                    "important_formulas": "V = IR\nP = VI\nP = I²R\nP = V²/R",
                    "units": "| Quantity | Symbol | Unit |\n|----------|--------|------|\n| Current | I | Ampere (A) |\n| Voltage | V | Volt (V) |\n| Resistance | R | Ohm (Ω) |\n| Power | P | Watt (W) |",
                    "common_values": "- 1 kW = 1000 W\n- Standard voltage = 220 V\n- Fuse rating = 13 A (typical household)"
                }
            ),

            "chemistry_summary": ContentTemplate(
                subject="Chemistry",
                topic="Periodic Table",
                content_type="summary",
                difficulty="basic",
                exam_board="WAEC",
                title_template="{topic} - Key Points Summary",
                content_structure={
                    "overview": {"type": "paragraph", "required": True},
                    "key_points": {"type": "bullet_list", "required": True},
                    "important_trends": {"type": "list", "required": True},
                    "memory_aids": {"type": "quote", "required": False},
                    "exam_focus": {"type": "highlight", "required": True}
                },
                required_sections=["overview", "key_points", "important_trends", "exam_focus"],
                example_content={
                    "overview": "The periodic table organizes elements by atomic number and groups them by similar chemical properties.",
                    "key_points": "- Elements arranged by increasing atomic number\n- Groups (vertical) have similar properties\n- Periods (horizontal) show electron shell filling\n- Metals on left, non-metals on right",
                    "important_trends": "- Atomic radius decreases across period, increases down group\n- Ionization energy increases across period, decreases down group\n- Electronegativity increases across period, decreases down group",
                    "memory_aids": "> Remember: \"Please Send Cats Monkeys And Zebras In Lovely Happy Xylophone Jokes\" for element groups 1-8",
                    "exam_focus": "**Key exam topics**: Group properties, periodic trends, element identification, chemical reactivity patterns"
                }
            ),

            "biology_exercise": ContentTemplate(
                subject="Biology",
                topic="Cell Biology",
                content_type="exercise",
                difficulty="intermediate",
                exam_board="WAEC",
                title_template="{topic} Practice Questions - {subject}",
                content_structure={
                    "instructions": {"type": "paragraph", "required": True},
                    "questions": {"type": "numbered_list", "required": True},
                    "answer_key": {"type": "section", "required": True},
                    "explanations": {"type": "detailed_list", "required": True}
                },
                required_sections=["instructions", "questions", "answer_key", "explanations"],
                example_content={
                    "instructions": "Answer all questions. Each question carries equal marks. Show all working where necessary.",
                    "questions": "1. State three differences between plant and animal cells.\n2. Describe the function of mitochondria in a cell.\n3. Explain how the cell membrane controls the movement of substances.",
                    "answer_key": "1. (a) Plant cells have cell walls, animal cells do not\n   (b) Plant cells have chloroplasts, animal cells do not\n   (c) Plant cells have large vacuoles, animal cells have small vacuoles\n\n2. Mitochondria are the powerhouse of the cell, responsible for cellular respiration and ATP production.\n\n3. The cell membrane is selectively permeable, allowing some substances to pass through while restricting others through processes like diffusion, osmosis, and active transport.",
                    "explanations": "1. **Cell wall**: Provides structural support and protection\n   **Chloroplasts**: Site of photosynthesis in plant cells\n   **Vacuoles**: Storage organelles, larger in plant cells for maintaining turgor pressure\n\n2. **Mitochondria**: Double-membraned organelles containing enzymes for aerobic respiration, producing ATP energy.\n\n3. **Selective permeability**: Controls internal environment, maintains homeostasis, protects cell contents."
                }
            )
        }

    def create_content_from_template(self, template_name: str, custom_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create content using a template"""
        if template_name not in self.templates:
            print(f"❌ Template '{template_name}' not found")
            return None

        template = self.templates[template_name]

        # Generate content ID
        content_id = f"{template.subject.lower()}_{template.topic.lower()}_{template.content_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Build content from template structure
        content_parts = []

        for section_name, section_config in template.content_structure.items():
            if section_config.get("required", False) or section_name in custom_data:
                section_content = custom_data.get(section_name, template.example_content.get(section_name, ""))

                if section_config["type"] == "heading":
                    content_parts.append(f"## {section_content}")
                elif section_config["type"] == "paragraph":
                    content_parts.append(section_content)
                elif section_config["type"] == "list":
                    content_parts.append(section_content)
                elif section_config["type"] == "code_block":
                    content_parts.append(f"```\n{section_content}\n```")
                elif section_config["type"] == "quote":
                    content_parts.append(f"> {section_content}")
                elif section_config["type"] == "table":
                    content_parts.append(section_content)
                else:
                    content_parts.append(section_content)

                content_parts.append("")  # Add spacing

        full_content = "\n".join(content_parts)

        # Create content object
        content = {
            "id": content_id,
            "title": custom_data.get("title", template.title_template.format(
                topic=template.topic,
                subject=template.subject
            )),
            "subject": template.subject,
            "topic": template.topic,
            "content_type": template.content_type,
            "difficulty": template.difficulty,
            "exam_board": template.exam_board,
            "content": full_content,
            "estimated_read_time": custom_data.get("estimated_read_time", 15),
            "prerequisites": custom_data.get("prerequisites", []),
            "related_questions": custom_data.get("related_questions", []),
            "tags": custom_data.get("tags", [template.topic.lower(), template.subject.lower()]),
            "author": custom_data.get("author", "Content Creator"),
            "version": 1,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        return content

    def interactive_content_creation(self):
        """Interactive content creation wizard"""
        print("🎯 Akulearn Content Creation Wizard")
        print("=" * 40)

        # Show available templates
        print("\n📋 Available Templates:")
        for i, (template_name, template) in enumerate(self.templates.items(), 1):
            print(f"{i}. {template_name}: {template.subject} - {template.topic} ({template.content_type})")

        # Get template choice
        while True:
            try:
                choice = input("\nSelect template (number or name): ").strip()
                if choice.isdigit():
                    template_names = list(self.templates.keys())
                    template_name = template_names[int(choice) - 1]
                else:
                    template_name = choice

                if template_name in self.templates:
                    break
                else:
                    print("❌ Invalid template selection")
            except (ValueError, IndexError):
                print("❌ Invalid input")

        template = self.templates[template_name]
        print(f"\n✅ Selected: {template.subject} - {template.topic} ({template.content_type})")

        # Collect custom data
        custom_data = {}

        # Title
        default_title = template.title_template.format(topic=template.topic, subject=template.subject)
        title = input(f"Title [{default_title}]: ").strip()
        if title:
            custom_data["title"] = title
        else:
            custom_data["title"] = default_title

        # Author
        author = input("Author [Content Creator]: ").strip()
        if author:
            custom_data["author"] = author

        # Estimated read time
        while True:
            read_time = input("Estimated read time (minutes) [15]: ").strip()
            if not read_time:
                custom_data["estimated_read_time"] = 15
                break
            try:
                custom_data["estimated_read_time"] = int(read_time)
                break
            except ValueError:
                print("❌ Please enter a valid number")

        # Tags
        tags_input = input(f"Tags (comma-separated) [{template.topic.lower()}, {template.subject.lower()}]: ").strip()
        if tags_input:
            custom_data["tags"] = [tag.strip() for tag in tags_input.split(",")]
        else:
            custom_data["tags"] = [template.topic.lower(), template.subject.lower()]

        # Prerequisites
        prereqs = input("Prerequisites (comma-separated, optional): ").strip()
        if prereqs:
            custom_data["prerequisites"] = [p.strip() for p in prereqs.split(",")]

        # Related questions
        questions = input("Related question IDs (comma-separated, optional): ").strip()
        if questions:
            custom_data["related_questions"] = [q.strip() for q in questions.split(",")]

        print("\n📝 Content Sections:")
        for section_name, section_config in template.content_structure.items():
            required = section_config.get("required", False)
            status = "(Required)" if required else "(Optional)"

            print(f"\n{section_name.upper()} {status}")
            print("-" * 30)

            # Show example
            example = template.example_content.get(section_name, "")
            if example:
                print("Example:")
                print(example[:200] + "..." if len(example) > 200 else example)
                print()

            # Get user input
            if required:
                content = input(f"Enter {section_name} content: ").strip()
                while not content:
                    print("❌ This section is required")
                    content = input(f"Enter {section_name} content: ").strip()
                custom_data[section_name] = content
            else:
                content = input(f"Enter {section_name} content (or press Enter to skip): ").strip()
                if content:
                    custom_data[section_name] = content

        # Create content
        print("\n🔄 Creating content...")
        content = self.create_content_from_template(template_name, custom_data)

        if content:
            print("✅ Content created successfully!")
            print(f"📄 Title: {content['title']}")
            print(f"🏷️  ID: {content['id']}")
            print(f"📊 Subject: {content['subject']} - {content['topic']}")

            # Save option
            save = input("\n💾 Save content to database? (y/n): ").strip().lower()
            if save == 'y':
                success = content_service.add_content(content)
                if success:
                    print("✅ Content saved to database!")
                else:
                    print("❌ Failed to save content")

            # Export option
            export = input("📤 Export content to JSON file? (y/n): ").strip().lower()
            if export == 'y':
                filename = f"{content['id']}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump([content], f, indent=2, ensure_ascii=False)
                print(f"✅ Content exported to {filename}")

        return content

def main():
    """Main content creation interface"""
    creator = ContentCreator()

    print("🎯 Akulearn Manual Content Creation System")
    print("=" * 50)
    print("1. Interactive content creation wizard")
    print("2. List available templates")
    print("3. Create content from template (batch)")
    print("4. Exit")

    while True:
        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            creator.interactive_content_creation()

        elif choice == "2":
            print("\n📋 Available Templates:")
            for name, template in creator.templates.items():
                print(f"• {name}: {template.subject} - {template.topic} ({template.content_type})")

        elif choice == "3":
            print("Batch creation not yet implemented")

        elif choice == "4":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()