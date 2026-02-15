#!/usr/bin/env python3
"""
Flashcard System Module
Implements spaced repetition flashcard system with SM-2 algorithm for optimal learning.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum

class Difficulty(Enum):
    """Flashcard difficulty levels."""
    EASY = 1
    GOOD = 2
    HARD = 3
    AGAIN = 4

class Flashcard:
    """Individual flashcard with spaced repetition data."""

    def __init__(self, front: str, back: str, subject: str, topic: str, card_id: Optional[str] = None):
        self.card_id = card_id or f"{subject}_{topic}_{hash(front + back) % 10000}"
        self.front = front
        self.back = back
        self.subject = subject
        self.topic = topic

        # SM-2 algorithm parameters
        self.repetitions = 0
        self.interval = 1  # days
        self.ease_factor = 2.5
        self.next_review = datetime.now()
        self.last_reviewed = None
        self.correct_streak = 0

    def review(self, difficulty: Difficulty) -> bool:
        """Update card based on review difficulty using SM-2 algorithm."""
        self.last_reviewed = datetime.now()

        if difficulty == Difficulty.AGAIN:
            self.repetitions = 0
            self.interval = 1
            self.correct_streak = 0
        else:
            if difficulty == Difficulty.EASY:
                self.correct_streak += 1
                self.ease_factor = max(1.3, self.ease_factor + 0.15)
            elif difficulty == Difficulty.GOOD:
                self.correct_streak += 1
                # ease_factor unchanged
            elif difficulty == Difficulty.HARD:
                self.correct_streak = 0
                self.ease_factor = max(1.3, self.ease_factor - 0.2)

            self.repetitions += 1

            if self.repetitions == 1:
                self.interval = 1
            elif self.repetitions == 2:
                self.interval = 6
            else:
                self.interval = round(self.interval * self.ease_factor)

        self.next_review = self.last_reviewed + timedelta(days=self.interval)
        return difficulty != Difficulty.AGAIN

    def is_due(self) -> bool:
        """Check if card is due for review."""
        return datetime.now() >= self.next_review

    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary for serialization."""
        return {
            "card_id": self.card_id,
            "front": self.front,
            "back": self.back,
            "subject": self.subject,
            "topic": self.topic,
            "repetitions": self.repetitions,
            "interval": self.interval,
            "ease_factor": self.ease_factor,
            "next_review": self.next_review.isoformat(),
            "last_reviewed": self.last_reviewed.isoformat() if self.last_reviewed else None,
            "correct_streak": self.correct_streak
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Flashcard':
        """Create card from dictionary."""
        card = cls(
            front=data["front"],
            back=data["back"],
            subject=data["subject"],
            topic=data["topic"],
            card_id=data["card_id"]
        )
        card.repetitions = data["repetitions"]
        card.interval = data["interval"]
        card.ease_factor = data["ease_factor"]
        card.next_review = datetime.fromisoformat(data["next_review"])
        card.last_reviewed = datetime.fromisoformat(data["last_reviewed"]) if data["last_reviewed"] else None
        card.correct_streak = data["correct_streak"]
        return card

class FlashcardDeck:
    """Collection of flashcards for a specific topic or subject."""

    def __init__(self, name: str, subject: str, description: str = ""):
        self.name = name
        self.subject = subject
        self.description = description
        self.cards: Dict[str, Flashcard] = {}
        self.created_date = datetime.now()
        self.last_studied = None

    def add_card(self, card: Flashcard):
        """Add a flashcard to the deck."""
        self.cards[card.card_id] = card

    def remove_card(self, card_id: str):
        """Remove a flashcard from the deck."""
        if card_id in self.cards:
            del self.cards[card_id]

    def get_due_cards(self) -> List[Flashcard]:
        """Get cards that are due for review."""
        return [card for card in self.cards.values() if card.is_due()]

    def get_new_cards(self, limit: int = 20) -> List[Flashcard]:
        """Get new cards that haven't been reviewed yet."""
        new_cards = [card for card in self.cards.values() if card.repetitions == 0]
        return new_cards[:limit]

    def get_cards_by_difficulty(self) -> Dict[str, List[Flashcard]]:
        """Categorize cards by learning difficulty."""
        easy = []
        medium = []
        hard = []

        for card in self.cards.values():
            if card.correct_streak >= 3:
                easy.append(card)
            elif card.correct_streak >= 1:
                medium.append(card)
            else:
                hard.append(card)

        return {
            "easy": easy,
            "medium": medium,
            "hard": hard
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get deck statistics."""
        total_cards = len(self.cards)
        due_cards = len(self.get_due_cards())
        new_cards = len(self.get_new_cards())
        mastered_cards = len([c for c in self.cards.values() if c.correct_streak >= 5])

        return {
            "total_cards": total_cards,
            "due_cards": due_cards,
            "new_cards": new_cards,
            "mastered_cards": mastered_cards,
            "completion_rate": mastered_cards / total_cards if total_cards > 0 else 0,
            "average_interval": sum(c.interval for c in self.cards.values()) / total_cards if total_cards > 0 else 0
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert deck to dictionary for serialization."""
        return {
            "name": self.name,
            "subject": self.subject,
            "description": self.description,
            "cards": {card_id: card.to_dict() for card_id, card in self.cards.items()},
            "created_date": self.created_date.isoformat(),
            "last_studied": self.last_studied.isoformat() if self.last_studied else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FlashcardDeck':
        """Create deck from dictionary."""
        deck = cls(
            name=data["name"],
            subject=data["subject"],
            description=data.get("description", "")
        )
        deck.created_date = datetime.fromisoformat(data["created_date"])
        deck.last_studied = datetime.fromisoformat(data["last_studied"]) if data.get("last_studied") else None

        for card_data in data["cards"].values():
            card = Flashcard.from_dict(card_data)
            deck.add_card(card)

        return deck

class FlashcardManager:
    """
    Manages multiple flashcard decks with spaced repetition system.
    """

    def __init__(self):
        self.decks: Dict[str, FlashcardDeck] = {}
        self.load_decks()

    def load_decks(self):
        """Load all flashcard decks."""
        self.decks = {
            "mathematics_ss1": self.create_mathematics_ss1_deck(),
            "physics_ss1": self.create_physics_ss1_deck(),
            "chemistry_ss1": self.create_chemistry_ss1_deck(),
            "biology_ss1": self.create_biology_ss1_deck(),
            "economics_ss1": self.create_economics_ss1_deck(),
            "geography_ss1": self.create_geography_ss1_deck()
        }

    def create_mathematics_ss1_deck(self) -> FlashcardDeck:
        """Create SS1 Mathematics flashcard deck."""
        deck = FlashcardDeck("SS1 Mathematics", "mathematics", "Senior Secondary 1 Mathematics flashcards")

        cards_data = [
            ("What is the formula for the area of a circle?", "A = πr²", "geometry", "circles"),
            ("What is the Pythagorean theorem?", "a² + b² = c² for right-angled triangles", "geometry", "triangles"),
            ("What is the quadratic formula?", "x = [-b ± √(b² - 4ac)] / 2a", "algebra", "equations"),
            ("What is the slope-intercept form of a line?", "y = mx + c", "algebra", "linear_equations"),
            ("What is the formula for compound interest?", "A = P(1 + r/n)^(nt)", "algebra", "financial_math"),
            ("What is the sum of angles in a triangle?", "180 degrees", "geometry", "triangles"),
            ("What is the formula for the circumference of a circle?", "C = 2πr", "geometry", "circles"),
            ("What is the distributive property?", "a(b + c) = ab + ac", "algebra", "properties"),
            ("What is the formula for simple interest?", "I = PRT/100", "algebra", "financial_math"),
            ("What is the area of a rectangle?", "A = length × width", "geometry", "rectangles")
        ]

        for front, back, topic, subtopic in cards_data:
            card = Flashcard(front, back, "mathematics", f"{topic}_{subtopic}")
            deck.add_card(card)

        return deck

    def create_physics_ss1_deck(self) -> FlashcardDeck:
        """Create SS1 Physics flashcard deck."""
        deck = FlashcardDeck("SS1 Physics", "physics", "Senior Secondary 1 Physics flashcards")

        cards_data = [
            ("What is Newton's First Law?", "An object at rest stays at rest, and an object in motion stays in motion unless acted upon by an unbalanced force", "mechanics", "newton_laws"),
            ("What is the formula for force?", "F = ma (Force = mass × acceleration)", "mechanics", "force"),
            ("What is the unit of energy?", "Joule (J)", "energy", "units"),
            ("What is the speed of light in vacuum?", "3 × 10⁸ m/s", "waves", "light"),
            ("What is the formula for work done?", "W = F × d × cosθ", "energy", "work"),
            ("What is the unit of power?", "Watt (W)", "energy", "power"),
            ("What is the formula for density?", "ρ = m/V", "properties", "density"),
            ("What is the acceleration due to gravity on Earth?", "9.8 m/s²", "mechanics", "gravity"),
            ("What is the formula for pressure?", "P = F/A", "properties", "pressure"),
            ("What is the unit of electric current?", "Ampere (A)", "electricity", "current")
        ]

        for front, back, topic, subtopic in cards_data:
            card = Flashcard(front, back, "physics", f"{topic}_{subtopic}")
            deck.add_card(card)

        return deck

    def create_chemistry_ss1_deck(self) -> FlashcardDeck:
        """Create SS1 Chemistry flashcard deck."""
        deck = FlashcardDeck("SS1 Chemistry", "chemistry", "Senior Secondary 1 Chemistry flashcards")

        cards_data = [
            ("What is the atomic number?", "Number of protons in an atom", "atomic_structure", "atom"),
            ("What is the chemical symbol for gold?", "Au", "periodic_table", "elements"),
            ("What is the pH of pure water?", "7 (neutral)", "acids_bases", "ph_scale"),
            ("What is the formula for water?", "H₂O", "compounds", "water"),
            ("What is the molar mass of carbon?", "12 g/mol", "stoichiometry", "molar_mass"),
            ("What is the chemical symbol for sodium?", "Na", "periodic_table", "elements"),
            ("What is the formula for carbon dioxide?", "CO₂", "compounds", "gases"),
            ("What is the valency of oxygen?", "2", "chemical_bonding", "valency"),
            ("What is the chemical symbol for iron?", "Fe", "periodic_table", "elements"),
            ("What is the formula for sodium chloride?", "NaCl", "compounds", "salts")
        ]

        for front, back, topic, subtopic in cards_data:
            card = Flashcard(front, back, "chemistry", f"{topic}_{subtopic}")
            deck.add_card(card)

        return deck

    def create_biology_ss1_deck(self) -> FlashcardDeck:
        """Create SS1 Biology flashcard deck."""
        deck = FlashcardDeck("SS1 Biology", "biology", "Senior Secondary 1 Biology flashcards")

        cards_data = [
            ("What is the basic unit of life?", "Cell", "cell_biology", "cell_theory"),
            ("What is photosynthesis?", "Process by which plants make food using sunlight", "plant_biology", "photosynthesis"),
            ("What is the powerhouse of the cell?", "Mitochondria", "cell_biology", "organelles"),
            ("What is the genetic material in cells?", "DNA", "genetics", "dna"),
            ("What is the process of cell division in somatic cells?", "Mitosis", "cell_biology", "cell_division"),
            ("What is the control center of the cell?", "Nucleus", "cell_biology", "organelles"),
            ("What is the process by which plants lose water?", "Transpiration", "plant_biology", "transpiration"),
            ("What is the study of inheritance?", "Genetics", "genetics", "inheritance"),
            ("What is the basic structural unit of nervous system?", "Neuron", "human_biology", "nervous_system"),
            ("What is the process of converting food into energy?", "Respiration", "physiology", "respiration")
        ]

        for front, back, topic, subtopic in cards_data:
            card = Flashcard(front, back, "biology", f"{topic}_{subtopic}")
            deck.add_card(card)

        return deck

    def create_economics_ss1_deck(self) -> FlashcardDeck:
        """Create SS1 Economics flashcard deck."""
        deck = FlashcardDeck("SS1 Economics", "economics", "Senior Secondary 1 Economics flashcards")

        cards_data = [
            ("What is economics?", "Study of how people use scarce resources to satisfy unlimited wants", "basic_concepts", "definition"),
            ("What is opportunity cost?", "The value of the next best alternative forgone", "basic_concepts", "opportunity_cost"),
            ("What is demand?", "Quantity of a good consumers are willing and able to buy at different prices", "market_forces", "demand"),
            ("What is supply?", "Quantity of a good producers are willing and able to sell at different prices", "market_forces", "supply"),
            ("What is inflation?", "Sustained increase in general price level", "macroeconomics", "inflation"),
            ("What is GDP?", "Total value of goods and services produced within a country in a year", "macroeconomics", "gdp"),
            ("What is unemployment?", "Situation where people who are willing and able to work cannot find jobs", "macroeconomics", "unemployment"),
            ("What is a market?", "Place or system where buyers and sellers interact", "market_structures", "market"),
            ("What is taxation?", "Compulsory payment made by citizens to government", "public_finance", "taxation"),
            ("What is budget?", "Financial plan of government for a fiscal year", "public_finance", "budget")
        ]

        for front, back, topic, subtopic in cards_data:
            card = Flashcard(front, back, "economics", f"{topic}_{subtopic}")
            deck.add_card(card)

        return deck

    def create_geography_ss1_deck(self) -> FlashcardDeck:
        """Create SS1 Geography flashcard deck."""
        deck = FlashcardDeck("SS1 Geography", "geography", "Senior Secondary 1 Geography flashcards")

        cards_data = [
            ("What is geography?", "Study of the Earth and its features, inhabitants, and phenomena", "basic_concepts", "definition"),
            ("What is the largest continent?", "Asia", "world_geography", "continents"),
            ("What is the longest river in the world?", "Nile River", "physical_geography", "rivers"),
            ("What is the highest mountain?", "Mount Everest", "physical_geography", "mountains"),
            ("What is the largest ocean?", "Pacific Ocean", "physical_geography", "oceans"),
            ("What is latitude?", "Angular distance north or south of the equator", "map_work", "coordinates"),
            ("What is longitude?", "Angular distance east or west of the Prime Meridian", "map_work", "coordinates"),
            ("What is the capital of Nigeria?", "Abuja", "nigerian_geography", "capitals"),
            ("What is the largest state in Nigeria by area?", "Niger State", "nigerian_geography", "states"),
            ("What is the climate of Nigeria?", "Tropical climate with wet and dry seasons", "nigerian_geography", "climate")
        ]

        for front, back, topic, subtopic in cards_data:
            card = Flashcard(front, back, "geography", f"{topic}_{subtopic}")
            deck.add_card(card)

        return deck

    def get_deck(self, deck_name: str) -> Optional[FlashcardDeck]:
        """Get a specific deck."""
        return self.decks.get(deck_name)

    def get_all_decks(self) -> List[str]:
        """Get all deck names."""
        return list(self.decks.keys())

    def get_study_session(self, deck_name: str, session_length: int = 20) -> List[Flashcard]:
        """Get a study session with due and new cards."""
        deck = self.get_deck(deck_name)
        if not deck:
            return []

        due_cards = deck.get_due_cards()
        new_cards = deck.get_new_cards(session_length - len(due_cards))

        session_cards = due_cards + new_cards
        random.shuffle(session_cards)

        return session_cards[:session_length]

    def get_overall_statistics(self) -> Dict[str, Any]:
        """Get overall statistics across all decks."""
        total_cards = 0
        total_due = 0
        total_mastered = 0

        for deck in self.decks.values():
            stats = deck.get_statistics()
            total_cards += stats["total_cards"]
            total_due += stats["due_cards"]
            total_mastered += stats["mastered_cards"]

        return {
            "total_decks": len(self.decks),
            "total_cards": total_cards,
            "total_due": total_due,
            "total_mastered": total_mastered,
            "overall_completion": total_mastered / total_cards if total_cards > 0 else 0
        }

# Global instance
flashcard_manager = FlashcardManager()

def get_flashcard_data():
    """Get all flashcard data for API integration."""
    return {name: deck.to_dict() for name, deck in flashcard_manager.decks.items()}

def get_study_session(deck_name: str, session_length: int = 20):
    """Get a study session for a deck."""
    return [card.to_dict() for card in flashcard_manager.get_study_session(deck_name, session_length)]

if __name__ == "__main__":
    print("🃏 Testing Flashcard System...")

    # Test loading decks
    decks = flashcard_manager.get_all_decks()
    print(f"✅ Loaded {len(decks)} flashcard decks: {', '.join(decks)}")

    # Test getting deck statistics
    math_deck = flashcard_manager.get_deck("mathematics_ss1")
    if math_deck:
        stats = math_deck.get_statistics()
        print(f"✅ Mathematics deck: {stats['total_cards']} cards, {stats['new_cards']} new, {stats['due_cards']} due")

    # Test study session
    session = flashcard_manager.get_study_session("mathematics_ss1", 5)
    print(f"✅ Generated study session with {len(session)} cards")

    # Test overall statistics
    overall_stats = flashcard_manager.get_overall_statistics()
    print(f"✅ Overall: {overall_stats['total_cards']} total cards across {overall_stats['total_decks']} decks")

    print("🎉 Flashcard system ready!")