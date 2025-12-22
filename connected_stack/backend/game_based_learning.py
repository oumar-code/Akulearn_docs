#!/usr/bin/env python3
"""
Game-Based Learning Module
Implements educational games for engagement and retention across subjects.
"""

import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class GameManager:
    """
    Manages educational games with scoring, progression, and analytics.
    """

    def __init__(self):
        self.games = {}
        self.player_progress = {}
        self.leaderboards = {}
        self.load_games()

    def load_games(self):
        """Load all educational games."""
        self.games = {
            "math_puzzles": self.create_math_puzzles(),
            "physics_simulator": self.create_physics_simulator(),
            "chemistry_lab": self.create_chemistry_lab(),
            "biology_quiz": self.create_biology_quiz(),
            "economics_trading": self.create_economics_trading(),
            "geography_explorer": self.create_geography_explorer()
        }

    def create_math_puzzles(self) -> Dict[str, Any]:
        """Create mathematics puzzle games."""
        return {
            "title": "Math Master Puzzles",
            "description": "Solve mathematical puzzles and challenges",
            "subject": "mathematics",
            "difficulty_levels": ["beginner", "intermediate", "advanced"],
            "game_types": {
                "number_sequences": {
                    "title": "Number Sequence Puzzles",
                    "description": "Find the next number in the sequence",
                    "examples": [
                        {"sequence": [2, 4, 8, 16], "answer": 32, "pattern": "multiply by 2"},
                        {"sequence": [1, 4, 9, 16], "answer": 25, "pattern": "square numbers"},
                        {"sequence": [1, 1, 2, 3, 5], "answer": 8, "pattern": "Fibonacci sequence"}
                    ]
                },
                "algebra_solver": {
                    "title": "Algebra Equation Solver",
                    "description": "Solve algebraic equations step by step",
                    "examples": [
                        {"equation": "2x + 5 = 13", "solution": "x = 4", "steps": ["Subtract 5", "Divide by 2"]},
                        {"equation": "3(x - 2) = 12", "solution": "x = 6", "steps": ["Divide by 3", "Add 2"]},
                        {"equation": "x² - 9 = 0", "solution": "x = ±3", "steps": ["Add 9", "Take square root"]}
                    ]
                },
                "geometry_challenges": {
                    "title": "Geometry Challenges",
                    "description": "Solve geometry problems and puzzles",
                    "examples": [
                        {"problem": "Area of circle with radius 5cm", "answer": "78.5 cm²", "formula": "πr²"},
                        {"problem": "Pythagorean theorem: sides 3,4", "answer": "5", "formula": "a² + b² = c²"},
                        {"problem": "Volume of sphere radius 3cm", "answer": "113.1 cm³", "formula": "4/3πr³"}
                    ]
                }
            },
            "scoring": {
                "correct_answer": 10,
                "speed_bonus": 5,  # for answers under 30 seconds
                "streak_bonus": 2,  # per consecutive correct answer
                "hint_penalty": -3
            }
        }

    def create_physics_simulator(self) -> Dict[str, Any]:
        """Create physics simulation games."""
        return {
            "title": "Physics Simulator",
            "description": "Explore physics concepts through interactive simulations",
            "subject": "physics",
            "simulations": {
                "projectile_motion": {
                    "title": "Projectile Motion Simulator",
                    "description": "Launch projectiles and analyze trajectories",
                    "variables": ["initial_velocity", "launch_angle", "gravity"],
                    "challenges": [
                        {"objective": "Hit target at 50m", "constraints": "angle ≤ 45°"},
                        {"objective": "Maximize range", "constraints": "velocity ≤ 30 m/s"},
                        {"objective": "Calculate landing time", "constraints": "height = 10m"}
                    ]
                },
                "circuit_builder": {
                    "title": "Circuit Builder",
                    "description": "Build and test electrical circuits",
                    "components": ["battery", "resistor", "capacitor", "switch", "bulb"],
                    "challenges": [
                        {"objective": "Light bulb with minimum power", "components": ["battery", "resistor", "bulb"]},
                        {"objective": "Create series circuit", "components": ["battery", "3 resistors", "bulb"]},
                        {"objective": "Measure current flow", "tools": ["ammeter", "voltmeter"]}
                    ]
                },
                "force_balancer": {
                    "title": "Force Balance Simulator",
                    "description": "Balance forces on objects",
                    "forces": ["gravity", "friction", "tension", "normal_force"],
                    "challenges": [
                        {"objective": "Balance box on incline", "forces": ["gravity", "friction"]},
                        {"objective": "Calculate net force", "forces": ["push", "pull", "friction"]},
                        {"objective": "Find equilibrium point", "forces": ["weight", "tension"]}
                    ]
                }
            },
            "scoring": {
                "simulation_accuracy": 15,
                "prediction_correct": 10,
                "calculation_correct": 5,
                "time_bonus": 5
            }
        }

    def create_chemistry_lab(self) -> Dict[str, Any]:
        """Create chemistry laboratory simulations."""
        return {
            "title": "Virtual Chemistry Lab",
            "description": "Conduct chemistry experiments in a virtual laboratory",
            "subject": "chemistry",
            "experiments": {
                "acid_base_titration": {
                    "title": "Acid-Base Titration",
                    "description": "Determine concentration of unknown acid/base",
                    "equipment": ["burette", "pipette", "flask", "indicator"],
                    "procedure": [
                        "Measure acid sample",
                        "Add indicator",
                        "Titrate with base",
                        "Record volume at endpoint"
                    ],
                    "challenges": [
                        {"objective": "Find acid concentration", "precision": "0.01M"},
                        {"objective": "Determine pH at equivalence", "indicator": "phenolphthalein"},
                        {"objective": "Calculate molar mass", "data": "volume, concentration"}
                    ]
                },
                "periodic_table_explorer": {
                    "title": "Periodic Table Explorer",
                    "description": "Explore element properties and trends",
                    "features": ["element_lookup", "property_comparison", "trend_analysis"],
                    "challenges": [
                        {"objective": "Find elements with similar properties", "group": "alkali_metals"},
                        {"objective": "Predict element reactivity", "period": 3},
                        {"objective": "Calculate atomic mass trend", "group": "halogens"}
                    ]
                },
                "reaction_simulator": {
                    "title": "Chemical Reaction Simulator",
                    "description": "Simulate and balance chemical reactions",
                    "reaction_types": ["synthesis", "decomposition", "combustion", "precipitation"],
                    "challenges": [
                        {"objective": "Balance combustion reaction", "reactants": ["C₃H₈", "O₂"]},
                        {"objective": "Predict products", "reactants": ["Na", "Cl₂"]},
                        {"objective": "Calculate reaction yield", "limiting_reactant": "given"}
                    ]
                }
            },
            "scoring": {
                "experiment_success": 20,
                "accuracy_bonus": 10,
                "safety_compliance": 5,
                "time_efficiency": 5
            }
        }

    def create_biology_quiz(self) -> Dict[str, Any]:
        """Create biology quiz games."""
        return {
            "title": "Biology Challenge Quiz",
            "description": "Test your knowledge of biological concepts",
            "subject": "biology",
            "quiz_categories": {
                "cell_biology": {
                    "title": "Cell Biology Quiz",
                    "questions": [
                        {"question": "What is the control center of the cell?", "options": ["Nucleus", "Mitochondria", "Ribosome", "Vacuole"], "answer": "Nucleus"},
                        {"question": "Which organelle produces ATP?", "options": ["Golgi", "Lysosome", "Mitochondria", "Endoplasmic Reticulum"], "answer": "Mitochondria"},
                        {"question": "What is the process of cell division in body cells?", "options": ["Mitosis", "Meiosis", "Binary fission", "Budding"], "answer": "Mitosis"}
                    ]
                },
                "genetics": {
                    "title": "Genetics Quiz",
                    "questions": [
                        {"question": "What carries genetic information?", "options": ["DNA", "RNA", "Protein", "Carbohydrate"], "answer": "DNA"},
                        {"question": "How many chromosomes do humans have?", "options": ["23", "46", "92", "138"], "answer": "46"},
                        {"question": "What is the probability of getting a dominant trait?", "options": ["25%", "50%", "75%", "100%"], "answer": "75%"}
                    ]
                },
                "ecology": {
                    "title": "Ecology Quiz",
                    "questions": [
                        {"question": "What is the study of ecosystems?", "options": ["Ecology", "Biology", "Zoology", "Botany"], "answer": "Ecology"},
                        {"question": "What is the first organism in a food chain?", "options": ["Producer", "Consumer", "Decomposer", "Herbivore"], "answer": "Producer"},
                        {"question": "What is the top consumer in a food chain?", "options": ["Primary", "Secondary", "Tertiary", "Quaternary"], "answer": "Tertiary"}
                    ]
                }
            },
            "scoring": {
                "correct_answer": 10,
                "speed_bonus": 5,
                "category_completion": 25,
                "perfect_score": 50
            }
        }

    def create_economics_trading(self) -> Dict[str, Any]:
        """Create economics trading simulation games."""
        return {
            "title": "Economics Trading Simulator",
            "description": "Simulate economic decisions and market dynamics",
            "subject": "economics",
            "scenarios": {
                "market_simulation": {
                    "title": "Market Supply & Demand",
                    "description": "Manage a business in a competitive market",
                    "decisions": ["pricing", "production", "marketing", "investment"],
                    "challenges": [
                        {"objective": "Maximize profit in competitive market", "constraints": "market_demand"},
                        {"objective": "Break even within 5 rounds", "resources": "limited"},
                        {"objective": "Achieve market leadership", "competitors": "3"}
                    ]
                },
                "budget_management": {
                    "title": "Government Budget Simulator",
                    "description": "Allocate government budget for development",
                    "sectors": ["education", "health", "infrastructure", "security", "agriculture"],
                    "challenges": [
                        {"objective": "Balance budget deficit", "constraints": "revenue_limits"},
                        {"objective": "Maximize GDP growth", "timeframe": "4_years"},
                        {"objective": "Reduce unemployment", "target": "5%_reduction"}
                    ]
                },
                "trade_game": {
                    "title": "International Trade Game",
                    "description": "Manage imports, exports, and trade relations",
                    "factors": ["tariffs", "quotas", "exchange_rates", "comparative_advantage"],
                    "challenges": [
                        {"objective": "Achieve trade surplus", "partners": "5_countries"},
                        {"objective": "Optimize export portfolio", "resources": "limited"},
                        {"objective": "Negotiate favorable terms", "bargaining": "required"}
                    ]
                }
            },
            "scoring": {
                "profit_earned": 10,  # per 1000 units
                "efficiency_bonus": 15,
                "strategy_score": 20,
                "sustainability": 10
            }
        }

    def create_geography_explorer(self) -> Dict[str, Any]:
        """Create geography exploration games."""
        return {
            "title": "Geography Explorer",
            "description": "Explore geographical concepts and Nigerian geography",
            "subject": "geography",
            "exploration_modes": {
                "nigeria_map_quiz": {
                    "title": "Nigeria Map Quiz",
                    "description": "Test knowledge of Nigerian states and capitals",
                    "regions": ["North_West", "North_Central", "North_East", "South_West", "South_South", "South_East"],
                    "challenges": [
                        {"objective": "Identify all state capitals", "time_limit": "5_minutes"},
                        {"objective": "Locate all major cities", "accuracy": "required"},
                        {"objective": "Match states to regions", "score": "perfect_match"}
                    ]
                },
                "climate_simulator": {
                    "title": "Climate Pattern Simulator",
                    "description": "Understand climate patterns and their effects",
                    "factors": ["latitude", "altitude", "ocean_currents", "wind_patterns"],
                    "challenges": [
                        {"objective": "Predict rainfall patterns", "region": "Nigeria"},
                        {"objective": "Explain seasonal changes", "hemisphere": "Northern"},
                        {"objective": "Analyze climate impact", "agriculture": "crop_yields"}
                    ]
                },
                "resource_management": {
                    "title": "Resource Management Game",
                    "description": "Manage natural resources sustainably",
                    "resources": ["oil", "minerals", "forests", "fisheries", "agricultural_land"],
                    "challenges": [
                        {"objective": "Sustainable oil extraction", "environment": "protected"},
                        {"objective": "Forest conservation", "biodiversity": "maintained"},
                        {"objective": "Fisheries management", "stocks": "sustainable"}
                    ]
                }
            },
            "scoring": {
                "accuracy_points": 10,
                "exploration_bonus": 5,
                "knowledge_test": 15,
                "sustainability_score": 20
            }
        }

    def get_game(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific game."""
        return self.games.get(game_id)

    def get_games_by_subject(self, subject: str) -> List[Dict[str, Any]]:
        """Get all games for a subject."""
        return [game for game in self.games.values() if game.get("subject") == subject]

    def get_all_games(self) -> List[str]:
        """Get all game IDs."""
        return list(self.games.keys())

    def calculate_score(self, game_id: str, performance: Dict[str, Any]) -> int:
        """Calculate score based on game performance."""
        game = self.get_game(game_id)
        if not game:
            return 0

        scoring = game.get("scoring", {})
        score = 0

        for metric, value in performance.items():
            if metric in scoring:
                score += value * scoring[metric]

        return score

    def update_player_progress(self, player_id: str, game_id: str, score: int, level: str):
        """Update player progress and achievements."""
        if player_id not in self.player_progress:
            self.player_progress[player_id] = {}

        if game_id not in self.player_progress[player_id]:
            self.player_progress[player_id][game_id] = {
                "high_score": 0,
                "levels_completed": [],
                "total_plays": 0,
                "achievements": []
            }

        progress = self.player_progress[player_id][game_id]
        progress["total_plays"] += 1

        if score > progress["high_score"]:
            progress["high_score"] = score

        if level not in progress["levels_completed"]:
            progress["levels_completed"].append(level)

        # Check for achievements
        achievements = self.check_achievements(progress, score)
        progress["achievements"].extend(achievements)

    def check_achievements(self, progress: Dict[str, Any], recent_score: int) -> List[str]:
        """Check for new achievements."""
        achievements = []

        if progress["total_plays"] >= 10:
            achievements.append("Dedicated Player")
        if progress["high_score"] >= 500:
            achievements.append("High Scorer")
        if len(progress["levels_completed"]) >= 3:
            achievements.append("Level Master")
        if recent_score >= 300:
            achievements.append("Perfect Game")

        return achievements

    def get_leaderboard(self, game_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get leaderboard for a game."""
        if game_id not in self.leaderboards:
            self.leaderboards[game_id] = []

        # Sort by score descending
        leaderboard = sorted(self.leaderboards[game_id], key=lambda x: x["score"], reverse=True)
        return leaderboard[:limit]

    def get_player_stats(self, player_id: str) -> Dict[str, Any]:
        """Get comprehensive player statistics."""
        if player_id not in self.player_progress:
            return {"total_games": 0, "total_score": 0, "achievements": []}

        progress = self.player_progress[player_id]
        total_games = len(progress)
        total_score = sum(game["high_score"] for game in progress.values())
        all_achievements = []

        for game in progress.values():
            all_achievements.extend(game["achievements"])

        unique_achievements = list(set(all_achievements))

        return {
            "total_games": total_games,
            "total_score": total_score,
            "achievements": unique_achievements,
            "achievement_count": len(unique_achievements),
            "games_mastered": len([g for g in progress.values() if len(g["levels_completed"]) >= 3])
        }

# Global instance
game_manager = GameManager()

def get_game_data():
    """Get all game data for API integration."""
    return game_manager.games

def get_player_progress(player_id: str):
    """Get player progress data."""
    return game_manager.get_player_stats(player_id)

def update_game_score(player_id: str, game_id: str, score: int, level: str):
    """Update player score and progress."""
    game_manager.update_player_progress(player_id, game_id, score, level)
    return {"success": True, "new_achievements": game_manager.check_achievements(
        game_manager.player_progress[player_id][game_id], score
    )}

if __name__ == "__main__":
    print("🎮 Testing Game-Based Learning System...")

    # Test loading games
    games = game_manager.get_all_games()
    print(f"✅ Loaded {len(games)} educational games: {', '.join(games)}")

    # Test getting games by subject
    math_games = game_manager.get_games_by_subject("mathematics")
    print(f"✅ Found {len(math_games)} mathematics games")

    # Test score calculation
    performance = {"correct_answer": 8, "speed_bonus": 3, "streak_bonus": 5}
    score = game_manager.calculate_score("math_puzzles", performance)
    print(f"✅ Calculated score: {score} points")

    # Test player progress
    game_manager.update_player_progress("student_001", "math_puzzles", 150, "intermediate")
    stats = game_manager.get_player_stats("student_001")
    print(f"✅ Player stats: {stats['total_games']} games, {stats['total_score']} total score")

    print("🎉 Game-based learning system ready!")