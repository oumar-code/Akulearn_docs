#!/usr/bin/env python3
"""Generate remaining 109 NERDC topics for 100% coverage"""

import json
from datetime import datetime
from enhanced_content_generator import EnhancedContentGenerator

# 109 remaining topics organized by subject and level
NERDC_TOPICS = [
    # Mathematics (15 more needed)
    ("Mathematics", "SS1", "Sets and Operations"),
    ("Mathematics", "SS1", "Number Systems"),
    ("Mathematics", "SS1", "Inequalities"),
    ("Mathematics", "SS1", "Sequences and Series"),
    ("Mathematics", "SS1", "Surds and Radicals"),
    ("Mathematics", "SS2", "Polynomials"),
    ("Mathematics", "SS2", "Rational Expressions"),
    ("Mathematics", "SS2", "Exponential Functions"),
    ("Mathematics", "SS2", "Logarithmic Functions"),
    ("Mathematics", "SS2", "Matrices and Determinants"),
    ("Mathematics", "SS3", "Limits and Continuity"),
    ("Mathematics", "SS3", "Differentiation"),
    ("Mathematics", "SS3", "Integration"),
    ("Mathematics", "SS3", "Differential Equations"),
    ("Mathematics", "SS3", "Vectors and 3D Geometry"),
    
    # Physics (13 more needed)
    ("Physics", "SS1", "Mechanics of Solids"),
    ("Physics", "SS1", "Heat and Thermodynamics"),
    ("Physics", "SS1", "Simple Harmonic Motion"),
    ("Physics", "SS1", "Elasticity and Deformation"),
    ("Physics", "SS2", "Optics"),
    ("Physics", "SS2", "Modern Physics"),
    ("Physics", "SS2", "Quantum Mechanics Basics"),
    ("Physics", "SS2", "Semiconductor Physics"),
    ("Physics", "SS3", "Relativity Basics"),
    ("Physics", "SS3", "Nuclear Physics"),
    ("Physics", "SS3", "Astrophysics"),
    ("Physics", "SS3", "Plasma Physics"),
    ("Physics", "SS3", "Particle Physics"),
    
    # Chemistry (9 more needed)
    ("Chemistry", "SS1", "Periodic Table"),
    ("Chemistry", "SS1", "Mole Concept"),
    ("Chemistry", "SS1", "Chemical Equations"),
    ("Chemistry", "SS2", "Equilibrium"),
    ("Chemistry", "SS2", "Kinetics"),
    ("Chemistry", "SS2", "Electrochemistry"),
    ("Chemistry", "SS3", "Complex Ions"),
    ("Chemistry", "SS3", "Spectroscopy"),
    ("Chemistry", "SS3", "Polymers and Plastics"),
    
    # Biology (9 more needed)
    ("Biology", "SS1", "Photosynthesis"),
    ("Biology", "SS1", "Respiration"),
    ("Biology", "SS1", "Nutrition"),
    ("Biology", "SS2", "Reproduction and Development"),
    ("Biology", "SS2", "Homeostasis"),
    ("Biology", "SS2", "Coordination and Control"),
    ("Biology", "SS3", "Immunity and Disease"),
    ("Biology", "SS3", "Biodiversity"),
    ("Biology", "SS3", "Environmental Biology"),
    
    # English Language (3 more needed)
    ("English Language", "SS1", "Language and Society"),
    ("English Language", "SS2", "Phonetics and Phonology"),
    ("English Language", "SS3", "Stylistics and Discourse"),
    
    # Further Mathematics (15 needed - all new)
    ("Further Mathematics", "SS1", "Advanced Algebra"),
    ("Further Mathematics", "SS1", "Complex Numbers"),
    ("Further Mathematics", "SS1", "Boolean Algebra"),
    ("Further Mathematics", "SS1", "Linear Programming"),
    ("Further Mathematics", "SS1", "Graph Theory"),
    ("Further Mathematics", "SS2", "Advanced Calculus"),
    ("Further Mathematics", "SS2", "Numerical Methods"),
    ("Further Mathematics", "SS2", "Probability Distributions"),
    ("Further Mathematics", "SS2", "Hypothesis Testing"),
    ("Further Mathematics", "SS2", "Decision Theory"),
    ("Further Mathematics", "SS3", "Abstract Algebra"),
    ("Further Mathematics", "SS3", "Real Analysis"),
    ("Further Mathematics", "SS3", "Topology"),
    ("Further Mathematics", "SS3", "Combinatorics"),
    ("Further Mathematics", "SS3", "Game Theory"),
    
    # Geography (15 needed - all new)
    ("Geography", "SS1", "Earth and Atmosphere"),
    ("Geography", "SS1", "Weather and Climate"),
    ("Geography", "SS1", "Landforms and Processes"),
    ("Geography", "SS1", "Soil Formation"),
    ("Geography", "SS1", "Biogeography"),
    ("Geography", "SS2", "Population Geography"),
    ("Geography", "SS2", "Settlement Patterns"),
    ("Geography", "SS2", "Economic Geography"),
    ("Geography", "SS2", "Urban Geography"),
    ("Geography", "SS2", "Resource Management"),
    ("Geography", "SS3", "Geopolitics"),
    ("Geography", "SS3", "Development Geography"),
    ("Geography", "SS3", "Cultural Geography"),
    ("Geography", "SS3", "Environmental Issues"),
    ("Geography", "SS3", "Cartography"),
    
    # Economics (15 needed - all new)
    ("Economics", "SS1", "Microeconomics Basics"),
    ("Economics", "SS1", "Demand and Supply"),
    ("Economics", "SS1", "Consumer Behavior"),
    ("Economics", "SS1", "Production and Costs"),
    ("Economics", "SS1", "Market Structures"),
    ("Economics", "SS2", "National Income"),
    ("Economics", "SS2", "Employment and Inflation"),
    ("Economics", "SS2", "Money and Banking"),
    ("Economics", "SS2", "International Trade"),
    ("Economics", "SS2", "Economic Growth"),
    ("Economics", "SS3", "Fiscal Policy"),
    ("Economics", "SS3", "Monetary Policy"),
    ("Economics", "SS3", "Development Economics"),
    ("Economics", "SS3", "Environmental Economics"),
    ("Economics", "SS3", "Behavioral Economics"),
    
    # Computer Science (15 needed - all new)
    ("Computer Science", "SS1", "Information Systems"),
    ("Computer Science", "SS1", "Data Representation"),
    ("Computer Science", "SS1", "Boolean Logic"),
    ("Computer Science", "SS1", "Number Systems"),
    ("Computer Science", "SS1", "Introduction to Programming"),
    ("Computer Science", "SS2", "Data Structures"),
    ("Computer Science", "SS2", "Algorithms"),
    ("Computer Science", "SS2", "Object-Oriented Programming"),
    ("Computer Science", "SS2", "Database Systems"),
    ("Computer Science", "SS2", "Web Development"),
    ("Computer Science", "SS3", "Artificial Intelligence"),
    ("Computer Science", "SS3", "Cybersecurity"),
    ("Computer Science", "SS3", "Software Engineering"),
    ("Computer Science", "SS3", "Network Protocols"),
    ("Computer Science", "SS3", "Cloud Computing"),
]

def main():
    with open("connected_stack/backend/content_data.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    generator = EnhancedContentGenerator(use_mcp=False)
    
    print(f"\n=== Generating {len(NERDC_TOPICS)} Remaining NERDC Topics ===\n")
    
    success_count = 0
    failed_topics = []
    
    for i, (subject, level, topic) in enumerate(NERDC_TOPICS, 1):
        print(f"[{i:3d}/{len(NERDC_TOPICS)}] {subject:20s} {level:3s}: {topic:30s}...", end=" ", flush=True)
        try:
            lesson = generator.generate(
                subject=subject,
                topic=f"{level} - {topic}",
                difficulty="intermediate" if level in ["SS1", "SS2"] else "advanced",
                use_mcp=False,
                include_nigerian_context=True
            )
            lesson["id"] = f"nerdc_{level.lower()}_{subject.lower().replace(' ','_')}_{topic.lower().replace(' ','_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            lesson["curriculum"] = "NERDC"
            lesson["level"] = level
            lesson["content_type"] = "study_guide"
            db["content"].append(lesson)
            success_count += 1
            print("OK")
        except Exception as e:
            failed_topics.append((subject, level, topic, str(e)[:50]))
            print(f"ERROR")
    
    # Update metadata if it exists
    if "metadata" not in db:
        db["metadata"] = {}
    db["metadata"]["total_items"] = len(db["content"])
    db["metadata"]["last_updated"] = datetime.now().isoformat()
    
    with open("connected_stack/backend/content_data.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"Generated {success_count}/{len(NERDC_TOPICS)} topics")
    print(f"Total NERDC items now: {len(db['content'])}")
    
    if failed_topics:
        print(f"\nFailed topics ({len(failed_topics)}):")
        for subj, level, topic, error in failed_topics:
            print(f"  - {subj} {level}: {topic}")
    
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
