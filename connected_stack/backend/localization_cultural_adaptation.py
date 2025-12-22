#!/usr/bin/env python3
"""
Localization and Cultural Adaptation Module
Ensures content relevance to Nigerian context and cultural sensitivity.
"""

import json
from typing import Dict, List, Any, Optional

class LocalizationManager:
    """
    Manages cultural adaptation and localization of educational content.
    """

    def __init__(self):
        self.cultural_contexts = {}
        self.regional_variations = {}
        self.language_adaptations = {}
        self.cultural_sensitivity = {}
        self.load_localization_data()

    def load_localization_data(self):
        """Load all localization and cultural adaptation data."""
        self.cultural_contexts = self.create_cultural_contexts()
        self.regional_variations = self.create_regional_variations()
        self.language_adaptations = self.create_language_adaptations()
        self.cultural_sensitivity = self.create_cultural_sensitivity_guide()

    def create_cultural_contexts(self) -> Dict[str, Any]:
        """Create cultural context data for Nigerian education."""
        return {
            "economics_nigeria": {
                "title": "Nigerian Economic Context",
                "cultural_elements": {
                    "informal_sector": {
                        "description": "Significant portion of economy is informal/unregulated",
                        "examples": ["Market trading", "Artisan services", "Transportation"],
                        "teaching_approach": "Include informal sector in economic analysis"
                    },
                    "oil_economy": {
                        "description": "Heavy dependence on oil exports",
                        "examples": ["Dutch disease effects", "Resource curse", "Revenue volatility"],
                        "teaching_approach": "Discuss economic diversification strategies"
                    },
                    "agricultural_society": {
                        "description": "Agriculture remains backbone despite urbanization",
                        "examples": ["Subsistence farming", "Cash crops", "Food security"],
                        "teaching_approach": "Connect economic theory to agricultural realities"
                    }
                },
                "case_studies": [
                    {
                        "title": "Impact of Fuel Subsidy Removal",
                        "context": "2012 and 2020 subsidy removals",
                        "economic_concepts": ["Price elasticity", "Inflation", "Government intervention"],
                        "cultural_insights": "Effects on transportation and food costs"
                    },
                    {
                        "title": "Naira Devaluation Effects",
                        "context": "Multiple devaluations since 2016",
                        "economic_concepts": ["Exchange rates", "Imports", "Balance of payments"],
                        "cultural_insights": "Impact on imported goods and education costs"
                    }
                ]
            },
            "biology_nigeria": {
                "title": "Biology in Nigerian Context",
                "cultural_elements": {
                    "tropical_diseases": {
                        "description": "Prevalent tropical diseases affect health education",
                        "examples": ["Malaria", "Typhoid", "Cholera", "HIV/AIDS"],
                        "teaching_approach": "Include local disease prevention strategies"
                    },
                    "biodiversity": {
                        "description": "Rich biodiversity in different ecosystems",
                        "examples": ["Rainforest zones", "Savanna regions", "Mangrove swamps"],
                        "teaching_approach": "Use local examples for ecological concepts"
                    },
                    "traditional_medicine": {
                        "description": "Integration of traditional and modern medicine",
                        "examples": ["Herbal remedies", "Local healing practices"],
                        "teaching_approach": "Discuss evidence-based traditional medicine"
                    }
                },
                "case_studies": [
                    {
                        "title": "Malaria Control Programs",
                        "context": "National malaria elimination strategy",
                        "biological_concepts": ["Parasite life cycle", "Vector control", "Immunity"],
                        "cultural_insights": "Community participation in control efforts"
                    }
                ]
            },
            "geography_nigeria": {
                "title": "Geography of Nigeria",
                "cultural_elements": {
                    "regional_diversity": {
                        "description": "Three distinct geo-political zones",
                        "examples": ["Northern savanna", "Southern rainforest", "Middle belt"],
                        "teaching_approach": "Explain regional economic specializations"
                    },
                    "urban_rural_divide": {
                        "description": "Significant urban-rural population distribution",
                        "examples": ["Lagos megacity", "Rural subsistence communities"],
                        "teaching_approach": "Discuss urbanization challenges and opportunities"
                    },
                    "resource_distribution": {
                        "description": "Uneven distribution of natural resources",
                        "examples": ["Oil in Niger Delta", "Minerals in Middle Belt", "Agriculture nationwide"],
                        "teaching_approach": "Analyze resource curse and development implications"
                    }
                }
            }
        }

    def create_regional_variations(self) -> Dict[str, Any]:
        """Create regional variation data for content adaptation."""
        return {
            "northern_nigeria": {
                "climate_adaptations": {
                    "agricultural_practices": ["Irrigation farming", "Drought-resistant crops", "Nomadic pastoralism"],
                    "housing": ["Mud houses with thatched roofs", "Protection from sandstorms"],
                    "economic_activities": ["Groundnut production", "Cotton farming", "Cattle rearing"]
                },
                "cultural_considerations": {
                    "religious_practices": "Predominantly Muslim communities",
                    "social_structure": "Extended family systems",
                    "education": "Islamic education alongside formal schooling"
                },
                "content_adaptations": {
                    "economics": "Include Islamic banking concepts",
                    "biology": "Focus on desert ecosystem adaptations",
                    "geography": "Emphasize Sahel climate patterns"
                }
            },
            "southern_nigeria": {
                "climate_adaptations": {
                    "agricultural_practices": ["Tropical crop farming", "Tree crop cultivation", "Fishery development"],
                    "housing": ["Wooden structures", "Protection from heavy rainfall"],
                    "economic_activities": ["Oil production", "Cocoa farming", "Rubber plantations"]
                },
                "cultural_considerations": {
                    "religious_practices": "Christian and traditional religion mix",
                    "social_structure": "Community-based decision making",
                    "education": "Emphasis on technical and vocational skills"
                },
                "content_adaptations": {
                    "economics": "Include petroleum economics",
                    "biology": "Focus on rainforest biodiversity",
                    "geography": "Emphasize coastal and river systems"
                }
            },
            "middle_belt": {
                "climate_adaptations": {
                    "agricultural_practices": ["Mixed farming systems", "Root crop cultivation", "Livestock integration"],
                    "housing": ["Mixed construction materials", "Adaptable to varying rainfall"],
                    "economic_activities": ["Mining", "Food crop production", "Small-scale manufacturing"]
                },
                "cultural_considerations": {
                    "religious_practices": "Religious diversity and tolerance",
                    "social_structure": "Multi-ethnic communities",
                    "education": "Focus on conflict resolution and peace education"
                },
                "content_adaptations": {
                    "economics": "Include solid minerals economics",
                    "biology": "Focus on savanna-forest transition zones",
                    "geography": "Emphasize plateau and mining regions"
                }
            }
        }

    def create_language_adaptations(self) -> Dict[str, Any]:
        """Create language adaptation data for multilingual education."""
        return {
            "pidgin_english": {
                "usage_context": "Common lingua franca in urban areas",
                "educational_value": "Bridge language for complex concepts",
                "examples": {
                    "economics": {
                        "standard": "The law of demand states that...",
                        "adapted": "Demand law talk say...",
                        "purpose": "Make economic concepts accessible"
                    },
                    "science": {
                        "standard": "Photosynthesis is the process by which...",
                        "adapted": "Photosynthesis na di process wey...",
                        "purpose": "Explain biological processes clearly"
                    }
                }
            },
            "local_languages": {
                "hausa": {
                    "regions": ["Northern Nigeria"],
                    "educational_terms": {
                        "economics": {"money": "kuɗi", "market": "kasuwa", "trade": "ciniki"},
                        "biology": {"cell": "tantanin halitta", "plant": "shuka", "animal": "dabbobi"},
                        "physics": {"force": "karfi", "energy": "makamashi", "motion": "motsi"}
                    }
                },
                "yoruba": {
                    "regions": ["South-Western Nigeria"],
                    "educational_terms": {
                        "economics": {"money": "owo", "market": "oja", "trade": "isowo"},
                        "biology": {"cell": "sẹẹli", "plant": "ewéko", "animal": "ẹranko"},
                        "physics": {"force": "agbara", "energy": "agbara", "motion": "iṣipopada"}
                    }
                },
                "igbo": {
                    "regions": ["South-Eastern Nigeria"],
                    "educational_terms": {
                        "economics": {"money": "ego", "market": "ahịa", "trade": "azụmahịa"},
                        "biology": {"cell": "sẹl", "plant": "osisi", "animal": "anụmanụ"},
                        "physics": {"force": "ike", "energy": "ike", "motion": "mbugharị"}
                    }
                }
            },
            "multilingual_strategies": {
                "code_switching": "Use familiar local terms to explain concepts",
                "bilingual_glossaries": "Provide translations for key terms",
                "cultural_bridging": "Connect new concepts to familiar cultural practices",
                "visual_supports": "Use diagrams and images to transcend language barriers"
            }
        }

    def create_cultural_sensitivity_guide(self) -> Dict[str, Any]:
        """Create cultural sensitivity guidelines for content development."""
        return {
            "gender_sensitivity": {
                "avoid_stereotypes": [
                    "Women as only homemakers",
                    "Men as only breadwinners",
                    "Gender-specific career choices"
                ],
                "inclusive_examples": [
                    "Women in STEM careers",
                    "Men in caregiving roles",
                    "Equal participation in all subjects"
                ],
                "teaching_approaches": [
                    "Use gender-neutral language",
                    "Include diverse role models",
                    "Address gender-based challenges"
                ]
            },
            "religious_sensitivity": {
                "respect_all_faiths": [
                    "Christianity, Islam, Traditional religions",
                    "Religious holidays and observances",
                    "Faith-based community practices"
                ],
                "educational_balance": [
                    "Present scientific facts objectively",
                    "Respect religious beliefs",
                    "Avoid religious controversies in science"
                ],
                "inclusive_practices": [
                    "Flexible scheduling for religious obligations",
                    "Multifaith prayer/meditation spaces",
                    "Religious diversity in examples"
                ]
            },
            "ethnic_sensitivity": {
                "cultural_diversity": [
                    "250+ ethnic groups in Nigeria",
                    "Respect for all cultural practices",
                    "Avoid ethnic stereotypes"
                ],
                "inclusive_content": [
                    "Examples from different regions",
                    "Celebration of cultural diversity",
                    "National unity themes"
                ],
                "conflict_avoidance": [
                    "Neutral presentation of history",
                    "Focus on shared Nigerian identity",
                    "Avoid regional rivalries"
                ]
            },
            "socioeconomic_sensitivity": {
                "class_awareness": [
                    "Wide socioeconomic disparities",
                    "Access to educational resources",
                    "Economic pressures on families"
                ],
                "equitable_content": [
                    "Examples relevant to all income levels",
                    "Low-cost educational activities",
                    "Realistic career aspirations"
                ],
                "supportive_approaches": [
                    "Encourage achievement at all levels",
                    "Address economic barriers",
                    "Promote social mobility"
                ]
            }
        }

    def get_cultural_context(self, subject: str) -> Dict[str, Any]:
        """Get cultural context for a specific subject."""
        return self.cultural_contexts.get(f"{subject.lower()}_nigeria", {})

    def get_regional_adaptation(self, region: str) -> Dict[str, Any]:
        """Get regional adaptation data."""
        return self.regional_variations.get(region.lower().replace(" ", "_"), {})

    def get_language_support(self, language: str) -> Dict[str, Any]:
        """Get language adaptation support."""
        return self.language_adaptations.get("local_languages", {}).get(language.lower(), {})

    def check_cultural_sensitivity(self, content: str, subject: str) -> Dict[str, Any]:
        """Check content for cultural sensitivity issues."""
        issues = []
        suggestions = []

        # Check for gender stereotypes
        gender_stereotypes = ["girls should", "boys should", "women only", "men only"]
        for stereotype in gender_stereotypes:
            if stereotype in content.lower():
                issues.append(f"Potential gender stereotype: '{stereotype}'")
                suggestions.append("Use gender-neutral language and inclusive examples")

        # Check for regional bias
        regional_bias = ["only in the north", "only in the south", "better in"]
        for bias in regional_bias:
            if bias in content.lower():
                issues.append(f"Potential regional bias: '{bias}'")
                suggestions.append("Include examples from all Nigerian regions")

        # Check for socioeconomic assumptions
        economic_assumptions = ["everyone has", "all families can", "rich families"]
        for assumption in economic_assumptions:
            if assumption in content.lower():
                issues.append(f"Socioeconomic assumption: '{assumption}'")
                suggestions.append("Ensure examples are accessible to all economic levels")

        return {
            "content_length": len(content),
            "issues_found": len(issues),
            "issues": issues,
            "suggestions": suggestions,
            "sensitivity_score": max(0, 100 - (len(issues) * 20))
        }

    def adapt_content_for_region(self, content: Dict[str, Any], region: str) -> Dict[str, Any]:
        """Adapt content for a specific Nigerian region."""
        region_data = self.get_regional_adaptation(region)
        if not region_data:
            return content

        adapted_content = content.copy()

        # Add regional examples
        if "examples" not in adapted_content:
            adapted_content["examples"] = []

        regional_examples = region_data.get("content_adaptations", {}).get(content.get("subject", ""), [])
        adapted_content["examples"].extend(regional_examples)

        # Add regional context
        adapted_content["regional_context"] = {
            "region": region,
            "cultural_considerations": region_data.get("cultural_considerations", {}),
            "local_examples": region_data.get("climate_adaptations", {})
        }

        return adapted_content

    def generate_localized_assessment(self, subject: str, level: str, region: str) -> Dict[str, Any]:
        """Generate culturally appropriate assessment questions."""
        cultural_context = self.get_cultural_context(subject)
        regional_data = self.get_regional_adaptation(region)

        assessment = {
            "subject": subject,
            "level": level,
            "region": region,
            "questions": []
        }

        # Generate contextually relevant questions
        if subject.lower() == "economics":
            assessment["questions"] = [
                {
                    "question": f"How does {regional_data.get('economic_activities', ['agricultural practices'])[0]} in {region} demonstrate economic principles?",
                    "type": "application",
                    "cultural_relevance": "local economic activities"
                },
                {
                    "question": "How can traditional trading practices in Nigerian markets be analyzed using modern economic theory?",
                    "type": "analysis",
                    "cultural_relevance": "informal sector economics"
                }
            ]
        elif subject.lower() == "biology":
            assessment["questions"] = [
                {
                    "question": f"How do organisms in {region}'s {regional_data.get('climate_adaptations', {}).get('agricultural_practices', ['local environment'])[0]} adapt to environmental conditions?",
                    "type": "application",
                    "cultural_relevance": "local biodiversity"
                }
            ]
        elif subject.lower() == "geography":
            assessment["questions"] = [
                {
                    "question": f"Analyze how {regional_data.get('cultural_considerations', {}).get('social_structure', 'community structure')} in {region} affects resource management.",
                    "type": "analysis",
                    "cultural_relevance": "regional geography"
                }
            ]

        return assessment

    def create_inclusive_content_guidelines(self) -> Dict[str, Any]:
        """Create guidelines for developing inclusive educational content."""
        return {
            "content_development": {
                "diversity_representation": [
                    "Include examples from all Nigerian regions",
                    "Represent different socioeconomic backgrounds",
                    "Show diverse family structures",
                    "Include various abilities and disabilities"
                ],
                "language_accessibility": [
                    "Use clear, simple language",
                    "Provide multilingual glossaries",
                    "Include visual supports",
                    "Avoid idioms and cultural references"
                ],
                "cultural_relevance": [
                    "Connect to students' lived experiences",
                    "Include local examples and case studies",
                    "Respect cultural practices and values",
                    "Address local challenges and opportunities"
                ]
            },
            "assessment_design": {
                "fair_assessment": [
                    "Multiple assessment formats",
                    "Consider cultural context in responses",
                    "Allow for different communication styles",
                    "Provide appropriate time accommodations"
                ],
                "inclusive_questioning": [
                    "Use culturally familiar contexts",
                    "Include diverse perspectives",
                    "Avoid culturally biased questions",
                    "Provide context for abstract concepts"
                ]
            },
            "teaching_strategies": {
                "differentiated_instruction": [
                    "Adapt to different learning styles",
                    "Provide multiple means of engagement",
                    "Offer various levels of challenge",
                    "Use flexible grouping strategies"
                ],
                "cultural_responsiveness": [
                    "Build on students' cultural knowledge",
                    "Create welcoming classroom environments",
                    "Incorporate student interests and experiences",
                    "Maintain high expectations for all students"
                ]
            }
        }

# Global instance
localization_manager = LocalizationManager()

def get_cultural_context(subject: str):
    """Get cultural context for a subject."""
    return localization_manager.get_cultural_context(subject)

def check_content_sensitivity(content: str, subject: str):
    """Check content for cultural sensitivity."""
    return localization_manager.check_cultural_sensitivity(content, subject)

def adapt_content_for_region(content: Dict[str, Any], region: str):
    """Adapt content for a specific region."""
    return localization_manager.adapt_content_for_region(content, region)

if __name__ == "__main__":
    print("🌍 Testing Localization and Cultural Adaptation...")

    # Test cultural contexts
    economics_context = localization_manager.get_cultural_context("economics")
    print(f"✅ Loaded cultural context for economics: {len(economics_context.get('cultural_elements', {}))} elements")

    # Test regional adaptations
    northern_adaptations = localization_manager.get_regional_adaptation("northern_nigeria")
    print(f"✅ Loaded regional adaptations for Northern Nigeria: {len(northern_adaptations)} categories")

    # Test language support
    hausa_terms = localization_manager.get_language_support("hausa")
    print(f"✅ Loaded Hausa language support: {len(hausa_terms.get('educational_terms', {}))} subjects")

    # Test cultural sensitivity check
    test_content = "All girls should study home economics while boys study physics."
    sensitivity_check = localization_manager.check_cultural_sensitivity(test_content, "general")
    print(f"✅ Cultural sensitivity check: {sensitivity_check['issues_found']} issues found")

    # Test content adaptation
    sample_content = {"subject": "economics", "title": "Supply and Demand"}
    adapted_content = localization_manager.adapt_content_for_region(sample_content, "southern_nigeria")
    print("✅ Adapted content for Southern Nigeria region")

    print("🎉 Localization and cultural adaptation ready!")