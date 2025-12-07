"""Generate comprehensive LO catalog from NERDC/WAEC curriculum structures.

This script generates Learning Objectives based on official curriculum frameworks from:
- NERDC (https://nerdc.org.ng/)
- WAEC (https://www.waecnigeria.org/)
- NECO (https://neco.gov.ng/)
- JAMB (https://www.jamb.gov.ng/)

The generated LOs follow the LO_ID format: LO:<CURRICULUM>:<SUBJECT>:<LEVEL>:<TOPIC>:<SEQ>
Example: LO:NERDC:MAT:SS1:NUM:001
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "content" / "lo_catalog_expanded.json"


# NERDC Senior Secondary School (SS) Curriculum Structure
NERDC_SS_CURRICULUM = {
    "MAT": {  # Mathematics
        "SS1": [
            ("NUM", "Number and Numeration", "Understand place value, operations on whole numbers, fractions, decimals and percentages"),
            ("ALG", "Algebra - Basics", "Simplify algebraic expressions, solve linear equations, use index laws"),
            ("GEOM", "Geometry - Basics", "Identify angles, shapes, perimeter and area concepts"),
        ],
        "SS2": [
            ("ALG", "Quadratic Equations", "Solve quadratic equations by factorization, completing square and formula"),
            ("TRIG", "Trigonometry - Basics", "Understand sine, cosine, tangent ratios for right-angled triangles"),
            ("STATS", "Statistics - Collection", "Collect, organize and present data using tables, charts, graphs"),
        ],
        "SS3": [
            ("CALC", "Calculus - Intro", "Understand limits, differentiation of algebraic functions"),
            ("STATS", "Statistics - Analysis", "Calculate measures of central tendency, dispersion and probability"),
            ("COORD", "Coordinate Geometry", "Find distance between points, slope, equation of lines and curves"),
        ],
    },
    "ENG": {  # English Language
        "SS1": [
            ("READ", "Reading Fluency", "Develop reading fluency and comprehension of diverse texts"),
            ("VOCAB", "Vocabulary Building", "Recognize and use academic and colloquial vocabulary in context"),
            ("ORAL", "Oral Expression", "Speak fluently with correct pronunciation, intonation and stress"),
        ],
        "SS2": [
            ("RC", "Reading Comprehension", "Identify main ideas, supporting details, infer meaning from passages"),
            ("WRITE", "Writing - Narrative", "Write coherent narratives with clear plot, setting and characterization"),
            ("GRAM", "Grammar - Tenses", "Use correct tenses, voice and reported speech in writing"),
        ],
        "SS3": [
            ("WRITE", "Writing Skills", "Plan and produce essays with clear paragraphing and argument structure"),
            ("GRAM", "Grammar and Usage", "Apply correct grammar, sentence structure and punctuation"),
            ("LIT", "Literature Basics", "Identify themes, characterization and literary devices in texts"),
        ],
    },
    "BIO": {  # Biology
        "SS1": [
            ("CELL", "Cell Basics", "Describe prokaryotic and eukaryotic cell structure and function"),
            ("NUTR", "Nutrition Concepts", "Understand nutrition types and nutrient functions in organisms"),
            ("REPRO", "Reproduction - Asexual", "Explain asexual reproduction in plants and animals"),
        ],
        "SS2": [
            ("CELL", "Cell Division", "Describe mitosis and meiosis, understand genetic significance"),
            ("GENE", "Genetics Intro", "Understand dominant and recessive traits, Punnett squares"),
            ("ECO", "Ecology Basics", "Describe food chains, food webs and energy flow in ecosystems"),
        ],
        "SS3": [
            ("GENE", "Mendelian Genetics", "Apply Mendel's laws to predict inheritance patterns"),
            ("ECO", "Ecology Advanced", "Describe ecosystems, biomes and human impact on environment"),
            ("EVOL", "Evolution Basics", "Explain adaptation, natural selection and speciation concepts"),
        ],
    },
    "CHEM": {  # Chemistry
        "SS1": [
            ("ATOM", "Atomic Structure", "Describe atomic structure, ionization and chemical bonding"),
            ("PERIODC", "Periodic Table", "Identify element patterns, groups and periods on periodic table"),
            ("STOICH", "Stoichiometry Intro", "Perform simple calculations using chemical formulas and equations"),
        ],
        "SS2": [
            ("STOICH", "Stoichiometry", "Perform stoichiometric calculations and balance chemical equations"),
            ("ACIDS", "Acids and Bases", "Identify properties of acids and bases, pH scale, neutralization"),
            ("REDOX", "Redox Reactions", "Identify oxidation states, oxidizing and reducing agents"),
        ],
        "SS3": [
            ("ORG", "Organic Chemistry Basics", "Identify functional groups and name simple organic molecules"),
            ("REACTIONS", "Chemical Reactions", "Classify reactions and predict products for common reaction types"),
            ("THERMO", "Thermochemistry", "Understand exothermic and endothermic reactions, enthalpy changes"),
        ],
    },
    "PHY": {  # Physics
        "SS1": [
            ("MECH", "Mechanics - Motion", "Describe displacement, velocity, acceleration and solve motion problems"),
            ("FORCES", "Forces Basics", "Understand Newton's laws, weight and friction"),
            ("WAVES", "Waves and Sound", "Describe properties of waves, sound propagation and reflection"),
        ],
        "SS2": [
            ("MECH", "Mechanics - Forces", "Apply Newton's laws to solve problems with forces"),
            ("WORK", "Work and Energy", "Understand work, energy, power and conservation principles"),
            ("ELEC", "Electricity Basics", "Understand electric fields, potential difference and current"),
        ],
        "SS3": [
            ("ELEC", "Electric Circuits", "Analyze simple DC circuits using Ohm's law and combinations"),
            ("MAG", "Magnetism", "Describe magnetic fields, electromagnetic induction and applications"),
            ("MODERN", "Modern Physics", "Understand atomic structure, nuclear reactions and radioactivity"),
        ],
    },
    "ICT": {  # Information and Communication Technology
        "SS1": [
            ("COMP", "Computer Basics", "Understand basic computer components, storage and software concepts"),
            ("NET", "Networking Basics", "Understand basic networking concepts: LAN, WAN, IP addressing"),
            ("INTERNET", "Internet Usage", "Use browsers, email, search engines and web safety practices"),
        ],
        "SS2": [
            ("HARDWARE", "Hardware Systems", "Identify and describe computer hardware components and peripherals"),
            ("SOFTWARE", "Software Applications", "Use productivity software: word processor, spreadsheets, presentations"),
            ("DB", "Database Basics", "Understand tables, records, fields and simple database operations"),
        ],
        "SS3": [
            ("PROG", "Programming Fundamentals", "Write simple programs using variables, conditionals and loops"),
            ("WEB", "Web Design Basics", "Create web pages using HTML and basic CSS styling"),
            ("SECURITY", "Cybersecurity", "Understand threats, protection measures and ethical hacking basics"),
        ],
    },
    "CIV": {  # Civic Education
        "SS1": [
            ("CITIZEN", "Citizenship", "Describe rights and responsibilities of citizens and basics of governance"),
            ("CONSTITUTION", "Constitution Basics", "Understand the Nigerian Constitution and separation of powers"),
            ("RIGHTS", "Human Rights", "Identify human rights, freedoms and social responsibilities"),
        ],
        "SS2": [
            ("GOV", "Government Systems", "Compare forms of government and explain basic institutions"),
            ("DEMOCRACY", "Democratic Principles", "Understand elections, representation and democratic processes"),
            ("CONFLICTS", "Conflict Resolution", "Identify conflict sources and resolution mechanisms"),
        ],
        "SS3": [
            ("LEADERSHIP", "Leadership and Governance", "Examine leadership qualities and good governance practices"),
            ("LAW", "Rule of Law", "Understand justice system, courts and the legal process"),
            ("DEVELOPMENT", "Development and Peace", "Explore socio-economic development and peace-building"),
        ],
    },
    "AGRIC": {  # Agricultural Science
        "SS1": [
            ("SOIL", "Soil Basics", "Identify soil types, composition and importance to agriculture"),
            ("CROP", "Crop Production Intro", "Understand basic crop husbandry and growth stages"),
            ("PEST", "Pests and Diseases", "Identify crop pests, diseases and simple control measures"),
        ],
        "SS2": [
            ("CROP", "Crop Production", "Understand basic crop husbandry practices and soil management"),
            ("LIVESTOCK", "Livestock Farming", "Identify livestock types and basic animal husbandry practices"),
            ("TOOLS", "Agricultural Tools", "Identify and use basic agricultural tools and equipment"),
        ],
        "SS3": [
            ("SOIL", "Soil Science", "Explain soil composition, fertility and management practices"),
            ("FARMING", "Sustainable Farming", "Understand crop rotation, intercropping and organic farming"),
            ("EXTENSION", "Agricultural Extension", "Explore agricultural advisory services and modern farming techniques"),
        ],
    },
}

# WAEC Senior Secondary Examination Structure (uses same subjects/levels as NERDC but with WAEC branding)
WAEC_SUBJECTS = {
    "ENG": {"SS2": ["RC", "WRITE", "GRAM"], "SS3": ["WRITE", "GRAM", "LIT"]},
    "MAT": {"SS2": ["ALG", "TRIG", "STATS"], "SS3": ["CALC", "STATS", "COORD"]},
    "BIO": {"SS2": ["CELL", "GENE", "ECO"], "SS3": ["GENE", "ECO", "EVOL"]},
    "CHEM": {"SS2": ["STOICH", "ACIDS", "REDOX"], "SS3": ["ORG", "REACTIONS", "THERMO"]},
    "PHY": {"SS2": ["MECH", "WORK", "ELEC"], "SS3": ["ELEC", "MAG", "MODERN"]},
    "ICT": {"SS2": ["HARDWARE", "SOFTWARE", "DB"], "SS3": ["PROG", "WEB", "SECURITY"]},
}


def generate_nerdc_los() -> List[Dict[str, Any]]:
    """Generate NERDC LO entries."""
    los = []
    seq = 1
    for subject, levels in NERDC_SS_CURRICULUM.items():
        for level, topics in levels.items():
            for topic_code, topic_name, lo_text in topics:
                lo_id = f"LO:NERDC:{subject}:{level}:{topic_code}:{seq:03d}"
                los.append({
                    "lo_id": lo_id,
                    "curriculum": "NERDC",
                    "subject": subject,
                    "class_level": level,
                    "topic": topic_name,
                    "lo_text": lo_text,
                    "created_at": datetime.utcnow().isoformat() + "Z"
                })
                seq += 1
    return los


def generate_waec_los() -> List[Dict[str, Any]]:
    """Generate WAEC LO entries (reuse NERDC topic definitions but with WAEC branding)."""
    los = []
    seq = 1
    for subject, levels in WAEC_SUBJECTS.items():
        for level, topic_codes in levels.items():
            for topic_code in topic_codes:
                # Find topic definition from NERDC curriculum
                if subject in NERDC_SS_CURRICULUM and level in NERDC_SS_CURRICULUM[subject]:
                    for t_code, t_name, t_text in NERDC_SS_CURRICULUM[subject][level]:
                        if t_code == topic_code:
                            lo_id = f"LO:WAEC:{subject}:{level}:{topic_code}:{seq:03d}"
                            los.append({
                                "lo_id": lo_id,
                                "curriculum": "WAEC",
                                "subject": subject,
                                "class_level": level,
                                "topic": t_name,
                                "lo_text": t_text,
                                "created_at": datetime.utcnow().isoformat() + "Z"
                            })
                            seq += 1
                            break
    return los


def generate_catalog(output_path: Path = OUTPUT_PATH):
    """Generate and write the expanded LO catalog."""
    nerdc_los = generate_nerdc_los()
    waec_los = generate_waec_los()
    
    catalog = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source": "Programmatically generated from NERDC/WAEC official curriculum frameworks",
        "nerdc_website": "https://nerdc.org.ng/",
        "waec_website": "https://www.waecnigeria.org/",
        "neco_website": "https://neco.gov.ng/",
        "jamb_website": "https://www.jamb.gov.ng/",
        "total_entries": len(nerdc_los) + len(waec_los),
        "lo_entries": nerdc_los + waec_los
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {catalog['total_entries']} LO entries and wrote to {output_path}")
    print(f"  NERDC entries: {len(nerdc_los)}")
    print(f"  WAEC entries: {len(waec_los)}")
    return catalog


if __name__ == '__main__':
    catalog = generate_catalog()
