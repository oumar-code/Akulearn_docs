#!/usr/bin/env python3
"""
Dataset Integration Module
Provides Nigerian economic and scientific data for analysis and visualization.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

class DatasetManager:
    """
    Manages educational datasets for Nigerian context.
    """

    def __init__(self):
        self.economic_data = {}
        self.scientific_data = {}
        self.geographic_data = {}
        self.load_datasets()

    def load_datasets(self):
        """Load all educational datasets."""
        self.economic_data = self.generate_economic_data()
        self.scientific_data = self.generate_scientific_data()
        self.geographic_data = self.generate_geographic_data()

    def generate_economic_data(self) -> Dict[str, Any]:
        """Generate Nigerian economic indicators dataset."""
        return {
            "gdp_data": {
                "title": "Nigeria GDP Growth (2015-2024)",
                "description": "Annual GDP growth rates for Nigeria",
                "unit": "Percentage (%)",
                "source": "National Bureau of Statistics (NBS)",
                "data": {
                    "years": list(range(2015, 2025)),
                    "growth_rates": [2.7, -1.6, -1.8, 0.8, 2.3, 3.4, 2.9, 3.6, 2.8, 3.2]
                },
                "analysis_questions": [
                    "What was Nigeria's highest GDP growth year?",
                    "Calculate the average growth rate from 2015-2024",
                    "Compare growth rates before and after COVID-19"
                ]
            },
            "inflation_data": {
                "title": "Nigeria Inflation Rates (2015-2024)",
                "description": "Annual inflation rates for Nigeria",
                "unit": "Percentage (%)",
                "source": "Central Bank of Nigeria (CBN)",
                "data": {
                    "years": list(range(2015, 2025)),
                    "rates": [9.0, 15.6, 16.5, 11.4, 11.4, 13.3, 15.6, 16.9, 21.5, 24.1]
                },
                "analysis_questions": [
                    "What trend do you observe in inflation rates?",
                    "How does inflation affect purchasing power?",
                    "Compare inflation rates with GDP growth"
                ]
            },
            "employment_data": {
                "title": "Nigeria Employment by Sector (2023)",
                "description": "Employment distribution across economic sectors",
                "unit": "Percentage (%)",
                "source": "National Bureau of Statistics (NBS)",
                "data": {
                    "sectors": ["Agriculture", "Services", "Industry", "Trade", "Others"],
                    "employment": [35.2, 28.1, 15.8, 12.4, 8.5]
                },
                "analysis_questions": [
                    "Which sector employs the most people?",
                    "Why is agriculture still dominant in Nigeria?",
                    "What are the implications for economic development?"
                ]
            },
            "oil_prices": {
                "title": "Crude Oil Prices and Nigeria's Revenue (2018-2024)",
                "description": "Brent crude oil prices and Nigeria's oil revenue",
                "unit": "USD per barrel / Billion USD",
                "source": "NNPC, OPEC",
                "data": {
                    "years": list(range(2018, 2025)),
                    "oil_prices": [71.3, 64.3, 41.5, 68.2, 76.1, 83.2, 79.4],
                    "revenue": [8.2, 7.1, 4.3, 6.8, 8.9, 9.2, 8.7]
                },
                "analysis_questions": [
                    "How do oil prices affect Nigeria's revenue?",
                    "What happened to revenue during the COVID-19 period?",
                    "Calculate the correlation between oil prices and revenue"
                ]
            }
        }

    def generate_scientific_data(self) -> Dict[str, Any]:
        """Generate scientific research data for educational use."""
        return {
            "physics_experiments": {
                "pendulum_data": {
                    "title": "Simple Pendulum Experiment Data",
                    "description": "Relationship between pendulum length and period",
                    "variables": {
                        "length": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],  # meters
                        "period": [0.89, 1.10, 1.27, 1.42, 1.55, 1.67, 1.79]  # seconds
                    },
                    "theory": "T = 2π√(L/g) where T is period, L is length, g is gravity",
                    "analysis_questions": [
                        "Plot length vs period squared",
                        "Calculate the value of g from the data",
                        "Explain why longer pendulums swing slower"
                    ]
                },
                "resistance_data": {
                    "title": "Electrical Resistance Experiment",
                    "description": "Ohm's law verification with different materials",
                    "materials": ["Nichrome", "Copper", "Iron", "Aluminum"],
                    "data": {
                        "nichrome": {"voltage": [2, 4, 6, 8, 10], "current": [0.4, 0.8, 1.2, 1.6, 2.0]},
                        "copper": {"voltage": [2, 4, 6, 8, 10], "current": [2.0, 4.0, 6.0, 8.0, 10.0]},
                        "iron": {"voltage": [2, 4, 6, 8, 10], "current": [1.3, 2.6, 3.9, 5.2, 6.5]},
                        "aluminum": {"voltage": [2, 4, 6, 8, 10], "current": [1.8, 3.6, 5.4, 7.2, 9.0]}
                    },
                    "analysis_questions": [
                        "Calculate resistance for each material",
                        "Which material is best conductor? Why?",
                        "Verify Ohm's law (V = IR) for each material"
                    ]
                }
            },
            "chemistry_experiments": {
                "reaction_rates": {
                    "title": "Chemical Reaction Rates",
                    "description": "Effect of concentration on reaction rate",
                    "reaction": "2H₂O₂ → 2H₂O + O₂ (catalyzed by MnO₂)",
                    "data": {
                        "concentration": [0.5, 1.0, 1.5, 2.0, 2.5],  # M
                        "time": [120, 85, 65, 50, 40]  # seconds for 50mL O₂
                    },
                    "analysis_questions": [
                        "Plot concentration vs 1/time",
                        "How does concentration affect reaction rate?",
                        "Calculate reaction rate constants"
                    ]
                },
                "periodic_trends": {
                    "title": "Periodic Table Trends",
                    "description": "Atomic radius and ionization energy trends",
                    "elements": ["Li", "Be", "B", "C", "N", "O", "F"],
                    "atomic_radius": [152, 112, 88, 77, 70, 66, 64],  # pm
                    "ionization_energy": [520, 900, 801, 1086, 1402, 1314, 1681],  # kJ/mol
                    "analysis_questions": [
                        "Plot atomic radius vs atomic number",
                        "Explain the trend in atomic radius",
                        "How does ionization energy change across the period?"
                    ]
                }
            },
            "biology_experiments": {
                "population_growth": {
                    "title": "Population Growth Study",
                    "description": "Bacterial growth in nutrient broth",
                    "data": {
                        "time": [0, 2, 4, 6, 8, 10, 12],  # hours
                        "population": [100, 150, 280, 650, 1200, 1800, 1900]  # cells/mL
                    },
                    "phases": ["Lag", "Log", "Stationary", "Death"],
                    "analysis_questions": [
                        "Identify the different growth phases",
                        "Calculate growth rate during log phase",
                        "Explain what happens in stationary phase"
                    ]
                }
            }
        }

    def generate_geographic_data(self) -> Dict[str, Any]:
        """Generate geographic data for Nigerian context."""
        return {
            "population_data": {
                "title": "Nigeria Population by State (2023)",
                "description": "Population distribution across Nigerian states",
                "source": "National Population Commission",
                "data": {
                    "states": ["Lagos", "Kano", "Oyo", "Rivers", "Kaduna", "Delta", "Ogun", "Niger", "Abia", "Others"],
                    "population": [14200000, 10200000, 7800000, 7200000, 6900000, 5600000, 5200000, 4100000, 3700000, 65000000]
                },
                "analysis_questions": [
                    "Which state has the highest population?",
                    "Calculate the percentage of total population in Lagos",
                    "Compare northern vs southern states population"
                ]
            },
            "climate_data": {
                "title": "Nigeria Climate Data by Region",
                "description": "Temperature and rainfall patterns",
                "regions": ["Northern", "Central", "Southern"],
                "data": {
                    "temperature": {
                        "northern": {"min": 20, "max": 40, "average": 30},
                        "central": {"min": 18, "max": 35, "average": 26},
                        "southern": {"min": 22, "max": 32, "average": 27}
                    },
                    "rainfall": {
                        "northern": {"annual": 500, "wet_season": "June-September"},
                        "central": {"annual": 1500, "wet_season": "April-October"},
                        "southern": {"annual": 2500, "wet_season": "March-November"}
                    }
                },
                "analysis_questions": [
                    "Explain the rainfall distribution pattern",
                    "Why is the north hotter than the south?",
                    "How does climate affect agriculture in different regions?"
                ]
            },
            "resources_data": {
                "title": "Nigeria Natural Resources by State",
                "description": "Major natural resources distribution",
                "data": {
                    "oil_states": ["Rivers", "Delta", "Bayelsa", "Akwa Ibom", "Abia", "Imo", "Ondo", "Edo"],
                    "mineral_states": {
                        "coal": ["Enugu", "Benue", "Kogi"],
                        "tin": ["Jos Plateau", "Bauchi"],
                        "limestone": ["Cross River", "Benue", "Sokoto"],
                        "gold": ["Edo", "Ekwiti", "Kebbi"]
                    },
                    "agricultural_zones": {
                        "cocoa": ["Ondo", "Osun", "Oyo", "Ekiti"],
                        "groundnut": ["Kano", "Kaduna", "Bauchi", "Sokoto"],
                        "rubber": ["Cross River", "Edo", "Delta"],
                        "cotton": ["Kano", "Kaduna", "Katsina"]
                    }
                },
                "analysis_questions": [
                    "Why is oil concentrated in the Niger Delta?",
                    "How do natural resources affect state economies?",
                    "Discuss the environmental impact of resource extraction"
                ]
            }
        }

    def get_economic_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """Get specific economic dataset."""
        return self.economic_data.get(dataset_id, {})

    def get_scientific_dataset(self, category: str, dataset_id: str) -> Dict[str, Any]:
        """Get specific scientific dataset."""
        return self.scientific_data.get(category, {}).get(dataset_id, {})

    def get_geographic_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """Get specific geographic dataset."""
        return self.geographic_data.get(dataset_id, {})

    def get_all_datasets(self) -> Dict[str, Any]:
        """Get all datasets for API integration."""
        return {
            "economic": self.economic_data,
            "scientific": self.scientific_data,
            "geographic": self.geographic_data
        }

    def create_data_visualization(self, dataset: Dict[str, Any]) -> Dict[str, Any]:
        """Create visualization configuration for a dataset."""
        viz_config = {
            "type": "line",  # default
            "title": dataset.get("title", ""),
            "x_label": "",
            "y_label": dataset.get("unit", ""),
            "data": dataset.get("data", {})
        }

        # Determine chart type based on data structure
        data = dataset.get("data", {})
        if isinstance(data.get("sectors"), list):
            viz_config["type"] = "pie"
        elif len(data) > 2:
            viz_config["type"] = "multi-line"
        elif "latitude" in str(data).lower():
            viz_config["type"] = "map"

        return viz_config

# Global instance
dataset_manager = DatasetManager()

def get_dataset_data():
    """Get all dataset data for API integration."""
    return dataset_manager.get_all_datasets()

def get_data_analysis_tools():
    """Get data analysis tools configuration."""
    return {
        "pandas_operations": [
            "df.head() - View first rows",
            "df.describe() - Statistical summary",
            "df.groupby() - Group data",
            "df.plot() - Create visualizations"
        ],
        "matplotlib_charts": [
            "plt.plot() - Line charts",
            "plt.bar() - Bar charts",
            "plt.scatter() - Scatter plots",
            "plt.pie() - Pie charts"
        ],
        "analysis_templates": {
            "correlation": "Analyze relationship between two variables",
            "trend": "Identify patterns over time",
            "comparison": "Compare different categories",
            "distribution": "Understand data spread"
        }
    }

if __name__ == "__main__":
    print("🧪 Testing Dataset Integration...")

    # Test economic data
    gdp_data = dataset_manager.get_economic_dataset("gdp_data")
    print(f"✅ Loaded GDP data: {len(gdp_data.get('data', {}).get('years', []))} years")

    # Test scientific data
    pendulum_data = dataset_manager.get_scientific_dataset("physics_experiments", "pendulum_data")
    print(f"✅ Loaded pendulum data: {len(pendulum_data.get('variables', {}).get('length', []))} measurements")

    # Test geographic data
    population_data = dataset_manager.get_geographic_dataset("population_data")
    print(f"✅ Loaded population data: {len(population_data.get('data', {}).get('states', []))} states")

    print("🎉 Dataset integration ready!")