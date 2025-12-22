#!/usr/bin/env python3
"""
Encyclopedia System Module
Provides comprehensive subject-specific encyclopedias with multimedia support.
"""

import json
from typing import Dict, List, Any, Optional

class EncyclopediaManager:
    """
    Manages subject-specific encyclopedias with search and multimedia support.
    """

    def __init__(self):
        self.encyclopedias = {}
        self.load_encyclopedias()

    def load_encyclopedias(self):
        """Load all subject encyclopedias."""
        self.encyclopedias = {
            "mathematics": self.create_mathematics_encyclopedia(),
            "physics": self.create_physics_encyclopedia(),
            "chemistry": self.create_chemistry_encyclopedia(),
            "biology": self.create_biology_encyclopedia(),
            "economics": self.create_economics_encyclopedia(),
            "geography": self.create_geography_encyclopedia()
        }

    def create_mathematics_encyclopedia(self) -> Dict[str, Any]:
        """Create comprehensive mathematics encyclopedia."""
        return {
            "title": "Mathematics Encyclopedia",
            "description": "Comprehensive guide to mathematical concepts, theorems, and applications",
            "entries": {
                "calculus": {
                    "title": "Calculus",
                    "definition": "Branch of mathematics concerned with rates of change and accumulation",
                    "key_concepts": ["Limits", "Derivatives", "Integrals", "Differential Equations"],
                    "applications": ["Physics", "Engineering", "Economics", "Biology"],
                    "formulas": {
                        "derivative": "d/dx[f(x)] = lim(h→0) [f(x+h) - f(x)]/h",
                        "integral": "∫f(x)dx = F(x) + C",
                        "chain_rule": "d/dx[f(g(x))] = f'(g(x)) * g'(x)"
                    },
                    "examples": [
                        "Position-velocity-acceleration relationships",
                        "Area under curves",
                        "Optimization problems"
                    ]
                },
                "probability": {
                    "title": "Probability Theory",
                    "definition": "Study of random events and uncertainty",
                    "key_concepts": ["Sample Space", "Events", "Probability Axioms", "Conditional Probability"],
                    "distributions": {
                        "normal": "Bell-shaped curve, μ = mean, σ = standard deviation",
                        "binomial": "n trials, p success probability",
                        "poisson": "Events in fixed interval"
                    },
                    "theorems": {
                        "bayes": "P(A|B) = P(B|A)P(A)/P(B)",
                        "central_limit": "Sample means approach normal distribution"
                    },
                    "applications": ["Statistics", "Risk Assessment", "Quality Control"]
                },
                "linear_algebra": {
                    "title": "Linear Algebra",
                    "definition": "Study of vectors, matrices, and linear transformations",
                    "key_concepts": ["Vectors", "Matrices", "Determinants", "Eigenvalues"],
                    "operations": {
                        "matrix_multiplication": "AB where columns of A = rows of B",
                        "determinant": "det(A) = measure of matrix scaling",
                        "inverse": "A⁻¹ such that AA⁻¹ = I"
                    },
                    "applications": ["Computer Graphics", "Data Science", "Quantum Mechanics"]
                }
            }
        }

    def create_physics_encyclopedia(self) -> Dict[str, Any]:
        """Create comprehensive physics encyclopedia."""
        return {
            "title": "Physics Encyclopedia",
            "description": "Comprehensive guide to physical laws, principles, and phenomena",
            "entries": {
                "newtonian_mechanics": {
                    "title": "Newtonian Mechanics",
                    "definition": "Classical mechanics based on Newton's laws of motion",
                    "laws": {
                        "first_law": "An object at rest stays at rest, and an object in motion stays in motion unless acted upon by an unbalanced force",
                        "second_law": "F = ma (Force equals mass times acceleration)",
                        "third_law": "For every action, there is an equal and opposite reaction"
                    },
                    "key_concepts": ["Force", "Mass", "Acceleration", "Momentum", "Energy"],
                    "applications": ["Engineering", "Sports", "Transportation", "Astronautics"]
                },
                "electromagnetism": {
                    "title": "Electromagnetism",
                    "definition": "Study of electric and magnetic fields and their interactions",
                    "laws": {
                        "coulomb": "F = kq₁q₂/r² (Electric force between charges)",
                        "faraday": "Changing magnetic field induces electric field",
                        "ampere": "Current produces magnetic field"
                    },
                    "key_concepts": ["Electric Field", "Magnetic Field", "Electromagnetic Waves", "Circuits"],
                    "applications": ["Electronics", "Power Generation", "Communications", "Medical Imaging"]
                },
                "thermodynamics": {
                    "title": "Thermodynamics",
                    "definition": "Study of heat, work, and energy transfer",
                    "laws": {
                        "zeroth": "Thermal equilibrium and temperature",
                        "first": "Energy conservation in thermodynamic processes",
                        "second": "Entropy increases in isolated systems",
                        "third": "Absolute zero is unattainable"
                    },
                    "key_concepts": ["Heat", "Work", "Internal Energy", "Entropy", "Heat Engines"],
                    "applications": ["Power Plants", "Refrigeration", "Chemical Processes", "Climate Science"]
                }
            }
        }

    def create_chemistry_encyclopedia(self) -> Dict[str, Any]:
        """Create comprehensive chemistry encyclopedia."""
        return {
            "title": "Chemistry Encyclopedia",
            "description": "Comprehensive guide to chemical principles, reactions, and applications",
            "entries": {
                "organic_chemistry": {
                    "title": "Organic Chemistry",
                    "definition": "Study of carbon-containing compounds",
                    "functional_groups": {
                        "alkanes": "C-C and C-H bonds only",
                        "alkenes": "C=C double bonds",
                        "alkynes": "C≡C triple bonds",
                        "alcohols": "-OH groups",
                        "carboxylic_acids": "-COOH groups"
                    },
                    "reactions": {
                        "substitution": "One atom/group replaces another",
                        "addition": "Atoms add across double/triple bonds",
                        "elimination": "Small molecule removed, double bond formed"
                    },
                    "applications": ["Pharmaceuticals", "Polymers", "Fuels", "Materials Science"]
                },
                "inorganic_chemistry": {
                    "title": "Inorganic Chemistry",
                    "definition": "Study of non-carbon compounds",
                    "periodic_trends": {
                        "atomic_radius": "Increases down group, decreases across period",
                        "ionization_energy": "Increases across period, decreases down group",
                        "electronegativity": "Increases across period, decreases down group"
                    },
                    "bonding": {
                        "ionic": "Transfer of electrons",
                        "covalent": "Sharing of electrons",
                        "metallic": "Delocalized electrons"
                    },
                    "applications": ["Catalysis", "Materials", "Environmental Chemistry", "Geochemistry"]
                },
                "physical_chemistry": {
                    "title": "Physical Chemistry",
                    "definition": "Study of physical properties and behavior of chemical systems",
                    "thermodynamics": {
                        "enthalpy": "Heat content of system",
                        "entropy": "Measure of disorder",
                        "free_energy": "Energy available for work"
                    },
                    "kinetics": {
                        "rate_law": "Rate = k[A]^m[B]^n",
                        "activation_energy": "Minimum energy for reaction",
                        "catalysts": "Speed up reactions without being consumed"
                    },
                    "applications": ["Reaction Engineering", "Electrochemistry", "Spectroscopy", "Quantum Chemistry"]
                }
            }
        }

    def create_biology_encyclopedia(self) -> Dict[str, Any]:
        """Create comprehensive biology encyclopedia."""
        return {
            "title": "Biology Encyclopedia",
            "description": "Comprehensive guide to living organisms and biological processes",
            "entries": {
                "cell_biology": {
                    "title": "Cell Biology",
                    "definition": "Study of cell structure and function",
                    "organelles": {
                        "nucleus": "Control center, contains DNA",
                        "mitochondria": "Energy production (ATP)",
                        "endoplasmic_reticulum": "Protein synthesis and transport",
                        "golgi_apparatus": "Protein modification and packaging",
                        "lysosomes": "Cellular digestion",
                        "vacuoles": "Storage and waste management"
                    },
                    "processes": ["Cell division", "Protein synthesis", "Energy metabolism", "Cell signaling"],
                    "applications": ["Medicine", "Biotechnology", "Drug Development", "Genetic Engineering"]
                },
                "genetics": {
                    "title": "Genetics",
                    "definition": "Study of genes, heredity, and genetic variation",
                    "key_concepts": {
                        "dna": "Deoxyribonucleic acid, genetic material",
                        "genes": "Units of heredity on chromosomes",
                        "alleles": "Different forms of same gene",
                        "genotype": "Genetic makeup",
                        "phenotype": "Observable characteristics"
                    },
                    "inheritance": {
                        "mendelian": "Dominant/recessive traits",
                        "codominance": "Both alleles expressed",
                        "incomplete_dominance": "Intermediate phenotype",
                        "sex_linked": "Genes on sex chromosomes"
                    },
                    "applications": ["Genetic Counseling", "Forensic Science", "Agriculture", "Medicine"]
                },
                "ecology": {
                    "title": "Ecology",
                    "definition": "Study of organisms and their environment",
                    "levels": {
                        "organism": "Individual living thing",
                        "population": "Group of same species",
                        "community": "Different species in area",
                        "ecosystem": "Community plus environment",
                        "biosphere": "All ecosystems on Earth"
                    },
                    "concepts": {
                        "food_chains": "Energy transfer between organisms",
                        "food_webs": "Interconnected food chains",
                        "energy_pyramid": "Energy decreases at each level",
                        "biogeochemical_cycles": "Nutrient cycling (carbon, nitrogen, water)"
                    },
                    "applications": ["Conservation", "Environmental Management", "Climate Change", "Biodiversity"]
                }
            }
        }

    def create_economics_encyclopedia(self) -> Dict[str, Any]:
        """Create comprehensive economics encyclopedia."""
        return {
            "title": "Economics Encyclopedia",
            "description": "Comprehensive guide to economic principles and Nigerian context",
            "entries": {
                "microeconomics": {
                    "title": "Microeconomics",
                    "definition": "Study of individual economic units and markets",
                    "key_concepts": {
                        "demand": "Quantity consumers want at different prices",
                        "supply": "Quantity producers offer at different prices",
                        "equilibrium": "Price where quantity demanded equals supplied",
                        "elasticity": "Responsiveness of quantity to price changes"
                    },
                    "market_structures": {
                        "perfect_competition": "Many buyers/sellers, identical products",
                        "monopoly": "Single seller, no close substitutes",
                        "oligopoly": "Few large sellers",
                        "monopolistic_competition": "Many sellers, differentiated products"
                    },
                    "nigerian_context": ["Agricultural markets", "Oil market dynamics", "Telecommunications competition"]
                },
                "macroeconomics": {
                    "title": "Macroeconomics",
                    "definition": "Study of economy as a whole",
                    "indicators": {
                        "gdp": "Total value of goods and services produced",
                        "inflation": "General price level increase",
                        "unemployment": "Percentage of labor force without work",
                        "balance_of_payments": "Record of economic transactions with rest of world"
                    },
                    "policies": {
                        "fiscal": "Government spending and taxation",
                        "monetary": "Central bank control of money supply",
                        "exchange_rate": "Value of domestic currency in terms of foreign currencies"
                    },
                    "nigerian_context": ["Oil-dependent economy", "Inflation management", "Foreign exchange challenges"]
                },
                "development_economics": {
                    "title": "Development Economics",
                    "definition": "Study of economic development in developing countries",
                    "theories": {
                        "modernization": "Traditional to modern society transition",
                        "dependency": "Rich countries exploit poor countries",
                        "human_capital": "Investment in education and health",
                        "structural_change": "Economy shifts from agriculture to industry"
                    },
                    "challenges": ["Poverty", "Inequality", "Unemployment", "Infrastructure deficits"],
                    "nigerian_context": ["Agricultural transformation", "Industrial development", "Human capital investment"]
                }
            }
        }

    def create_geography_encyclopedia(self) -> Dict[str, Any]:
        """Create comprehensive geography encyclopedia."""
        return {
            "title": "Geography Encyclopedia",
            "description": "Comprehensive guide to geographical concepts and Nigerian context",
            "entries": {
                "physical_geography": {
                    "title": "Physical Geography",
                    "definition": "Study of Earth's physical features and processes",
                    "landforms": {
                        "mountains": "Elevated landforms from tectonic forces",
                        "plains": "Flat or gently rolling land",
                        "plateaus": "Elevated flat land",
                        "valleys": "Low areas between hills/mountains",
                        "rivers": "Natural water channels"
                    },
                    "processes": {
                        "erosion": "Wearing away of land by water, wind, ice",
                        "weathering": "Breakdown of rocks at surface",
                        "deposition": "Sediment accumulation",
                        "tectonics": "Movement of Earth's crustal plates"
                    },
                    "nigerian_context": ["Niger River system", "Plateau regions", "Coastal geography"]
                },
                "human_geography": {
                    "title": "Human Geography",
                    "definition": "Study of human activities and their spatial organization",
                    "population": {
                        "distribution": "Where people live",
                        "density": "People per unit area",
                        "growth": "Population increase over time",
                        "migration": "Movement of people"
                    },
                    "settlement": {
                        "rural": "Agricultural communities",
                        "urban": "City-based communities",
                        "urbanization": "Growth of urban areas"
                    },
                    "nigerian_context": ["Northern population concentration", "Urban growth in Lagos", "Rural-urban migration"]
                },
                "economic_geography": {
                    "title": "Economic Geography",
                    "definition": "Study of spatial aspects of economic activities",
                    "sectors": {
                        "primary": "Resource extraction (agriculture, mining)",
                        "secondary": "Manufacturing and processing",
                        "tertiary": "Services (trade, transport, finance)",
                        "quaternary": "Information and knowledge services"
                    },
                    "trade": {
                        "imports": "Goods brought into country",
                        "exports": "Goods sent out of country",
                        "balance_of_trade": "Difference between exports and imports"
                    },
                    "nigerian_context": ["Oil export dominance", "Agricultural trade", "Manufacturing development"]
                }
            }
        }

    def search_entries(self, query: str, subject: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search encyclopedia entries by query."""
        results = []
        subjects_to_search = [subject] if subject else self.encyclopedias.keys()

        for subj in subjects_to_search:
            if subj in self.encyclopedias:
                encyclopedia = self.encyclopedias[subj]
                for entry_id, entry in encyclopedia.get("entries", {}).items():
                    if query.lower() in entry.get("title", "").lower() or \
                       query.lower() in entry.get("definition", "").lower():
                        results.append({
                            "subject": subj,
                            "entry_id": entry_id,
                            "title": entry.get("title", ""),
                            "definition": entry.get("definition", ""),
                            "snippet": entry.get("definition", "")[:200] + "..."
                        })

        return results

    def get_entry(self, subject: str, entry_id: str) -> Dict[str, Any]:
        """Get specific encyclopedia entry."""
        if subject in self.encyclopedias:
            return self.encyclopedias[subject].get("entries", {}).get(entry_id, {})
        return {}

    def get_subject_entries(self, subject: str) -> List[str]:
        """Get all entry IDs for a subject."""
        if subject in self.encyclopedias:
            return list(self.encyclopedias[subject].get("entries", {}).keys())
        return []

    def get_all_subjects(self) -> List[str]:
        """Get all available subjects."""
        return list(self.encyclopedias.keys())

# Global instance
encyclopedia_manager = EncyclopediaManager()

def get_encyclopedia_data():
    """Get all encyclopedia data for API integration."""
    return encyclopedia_manager.encyclopedias

def search_encyclopedia(query: str, subject: Optional[str] = None):
    """Search encyclopedia entries."""
    return encyclopedia_manager.search_entries(query, subject)

if __name__ == "__main__":
    print("📚 Testing Encyclopedia System...")

    # Test loading encyclopedias
    subjects = encyclopedia_manager.get_all_subjects()
    print(f"✅ Loaded {len(subjects)} subject encyclopedias: {', '.join(subjects)}")

    # Test getting entries
    math_entries = encyclopedia_manager.get_subject_entries("mathematics")
    print(f"✅ Mathematics encyclopedia has {len(math_entries)} entries: {', '.join(math_entries)}")

    # Test searching
    search_results = encyclopedia_manager.search_entries("calculus")
    print(f"✅ Found {len(search_results)} entries for 'calculus'")

    # Test getting specific entry
    calculus_entry = encyclopedia_manager.get_entry("mathematics", "calculus")
    print(f"✅ Retrieved entry: {calculus_entry.get('title', 'N/A')}")

    print("🎉 Encyclopedia system ready!")