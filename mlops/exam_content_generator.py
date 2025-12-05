"""
AIops Content Generation Pipeline for Secondary School Exams
Supports WAEC, NECO, JAMB exam preparation content

Usage:
    python -m mlops.exam_content_generator --exam waec --subject mathematics --difficulty medium --count 10
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, List

import mlflow
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# 1. DATA MODELS & ENUMS
# ============================================================================

class ExamBoard(str, Enum):
    """Supported exam boards in Nigeria"""
    WAEC = "waec"
    NECO = "neco"
    JAMB = "jamb"


class Difficulty(str, Enum):
    """Question difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionType(str, Enum):
    """Types of questions"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"


@dataclass
class Question:
    """Represents a single question"""
    id: str
    exam_board: ExamBoard
    subject: str
    topic: str
    difficulty: Difficulty
    question_text: str
    options: List[str]
    correct_answer: str
    explanation: str
    question_type: QuestionType = QuestionType.MULTIPLE_CHOICE
    relevance_score: float = 0.0
    quality_score: float = 0.0
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return asdict(self)
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class GenerationRequest:
    """Represents a request to generate content"""
    exam_board: ExamBoard
    subject: str
    topic: str
    difficulty: Difficulty
    question_count: int
    quality_threshold: float = 0.75


# ============================================================================
# 2. QUESTION GENERATOR AGENT
# ============================================================================

class QuestionGeneratorAgent:
    """
    Generates exam questions using HuggingFace transformers
    
    Strategy:
    - Use a prompt-based approach with a language model
    - Validate generated questions for quality
    - Track all operations with MLflow
    """
    
    def __init__(self, model_name: str = "gpt2", mlflow_tracking_uri: str = "runs/mlflow"):
        """Initialize the question generator agent"""
        self.model_name = model_name
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        mlflow.set_experiment("exam-content-generation")
        
        logger.info(f"Initializing QuestionGeneratorAgent with model: {model_name}")
        
        # Load summarization pipeline for extracting key concepts
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Load text classification for quality scoring
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
        self.generated_questions = []
    
    def generate_questions(self, request: GenerationRequest) -> List[Question]:
        """
        Generate questions based on the request
        
        This is where you would integrate:
        - Google Notebook LM for audio guides
        - Hugging Face models for generation
        - LLaMA for more advanced generation
        """
        logger.info(f"Generating {request.question_count} questions for {request.exam_board.value}")
        
        with mlflow.start_run(run_name=f"{request.exam_board.value}-{request.subject}"):
            mlflow.log_params({
                "exam_board": request.exam_board.value,
                "subject": request.subject,
                "topic": request.topic,
                "difficulty": request.difficulty.value,
                "question_count": request.question_count,
            })
            
            questions = []
            
            for i in range(request.question_count):
                try:
                    question = self._generate_single_question(
                        request, i + 1
                    )
                    questions.append(question)
                    
                except Exception as e:
                    logger.error(f"Error generating question {i+1}: {e}")
                    continue
            
            # Log metrics
            successful_count = len(questions)
            mlflow.log_metrics({
                "questions_generated": successful_count,
                "success_rate": successful_count / request.question_count,
                "avg_quality_score": sum(q.quality_score for q in questions) / max(1, len(questions)),
                "avg_relevance_score": sum(q.relevance_score for q in questions) / max(1, len(questions)),
            })
            
            self.generated_questions.extend(questions)
            return questions
    
    def _generate_single_question(self, request: GenerationRequest, index: int) -> Question:
        """Generate a single question"""
        
        # Template-based question generation
        # In production, integrate with LLaMA or fine-tuned GPT model
        
        question_text = self._create_question_text(request, index)
        options = self._create_options(request, index)
        correct_answer = options[0]
        explanation = self._create_explanation(request, question_text, correct_answer)
        
        # Score relevance & quality
        relevance_score = self._score_relevance(question_text, request)
        quality_score = self._score_quality(question_text, options, explanation)
        
        question_id = f"{request.exam_board.value}_{request.subject}_{index:05d}"
        
        question = Question(
            id=question_id,
            exam_board=request.exam_board,
            subject=request.subject,
            topic=request.topic,
            difficulty=request.difficulty,
            question_text=question_text,
            options=options,
            correct_answer=correct_answer,
            explanation=explanation,
            relevance_score=relevance_score,
            quality_score=quality_score,
        )
        
        logger.info(f"Generated question {index}: {question.id} (quality: {quality_score:.2f})")
        
        return question
    
    def _create_question_text(self, request: GenerationRequest, index: int) -> str:
        """Create question text - would be replaced with LLM call"""
        
        templates = {
            Difficulty.EASY: [
                f"What is the basic definition of {request.topic}?",
                f"Which of the following best describes {request.topic}?",
                f"State the formula for calculating {request.topic}",
            ],
            Difficulty.MEDIUM: [
                f"Explain how {request.topic} affects {request.subject} processes",
                f"Apply the concept of {request.topic} to solve this problem",
                f"Compare and contrast {request.topic} with related concepts",
            ],
            Difficulty.HARD: [
                f"Analyze the implications of {request.topic} in advanced {request.subject} scenarios",
                f"Synthesize knowledge of {request.topic} to predict outcomes",
                f"Evaluate different approaches to {request.topic} and justify your choice",
            ]
        }
        
        template_list = templates.get(request.difficulty, templates[Difficulty.MEDIUM])
        question = template_list[index % len(template_list)]
        
        return question
    
    def _create_options(self, request: GenerationRequest, index: int) -> List[str]:
        """Create multiple choice options"""
        
        # Correct answer
        correct = f"Option A: Correct answer for {request.topic} (index {index})"
        
        # Distractors
        distractors = [
            f"Option B: Common misconception about {request.topic}",
            f"Option C: Partially correct but incomplete answer",
            f"Option D: Plausible but incorrect alternative",
        ]
        
        return [correct] + distractors
    
    def _create_explanation(self, request: GenerationRequest, question: str, answer: str) -> str:
        """Create explanation for the answer"""
        
        explanation = f"""
Step 1: Understand the question
- Key concept: {request.topic}
- Difficulty level: {request.difficulty.value}

Step 2: Recall relevant knowledge
- Core principle: The question tests understanding of {request.topic}
- Related concepts: Connected to broader {request.subject} principles

Step 3: Analyze the options
- The correct answer ({answer}) directly addresses the question
- Distractors test common misconceptions

Step 4: Verify your answer
- Double-check against exam syllabus
- Confirm with reference materials
- Consider real-world applications
        """.strip()
        
        return explanation
    
    def _score_relevance(self, question_text: str, request: GenerationRequest) -> float:
        """
        Score relevance to exam syllabus
        Uses zero-shot classification with MLflow tracking
        """
        
        labels = [
            "highly relevant to exam syllabus",
            "somewhat relevant to exam syllabus",
            "not relevant to exam syllabus"
        ]
        
        try:
            result = self.classifier(question_text, labels)
            scores = {label: score for label, score in zip(result['labels'], result['scores'])}
            
            # Weight high relevance as 1.0, medium as 0.5, low as 0.0
            relevance = scores.get(labels[0], 0.5)
            return round(relevance, 3)
        except Exception as e:
            logger.warning(f"Relevance scoring failed: {e}, returning default 0.7")
            return 0.7
    
    def _score_quality(self, question_text: str, options: List[str], explanation: str) -> float:
        """
        Score overall quality of the question
        Factors: clarity, correctness, presence of explanation
        """
        
        score = 0.0
        
        # Factor 1: Question clarity (20%)
        clarity = 1.0 if len(question_text) > 10 else 0.5
        score += clarity * 0.2
        
        # Factor 2: Option diversity (20%)
        option_diversity = 1.0 if len(set(options)) == len(options) else 0.5
        score += option_diversity * 0.2
        
        # Factor 3: Explanation presence (30%)
        explanation_score = 1.0 if len(explanation) > 100 else 0.5
        score += explanation_score * 0.3
        
        # Factor 4: Formatting (30%)
        formatting_score = 1.0
        score += formatting_score * 0.3
        
        return round(score, 3)
    
    def get_statistics(self) -> dict:
        """Get statistics about generated questions"""
        
        if not self.generated_questions:
            return {
                "total_generated": 0,
                "by_exam_board": {},
                "by_difficulty": {},
                "avg_quality_score": 0,
                "avg_relevance_score": 0,
            }
        
        questions = self.generated_questions
        
        return {
            "total_generated": len(questions),
            "by_exam_board": {
                board.value: len([q for q in questions if q.exam_board == board])
                for board in ExamBoard
            },
            "by_difficulty": {
                diff.value: len([q for q in questions if q.difficulty == diff])
                for diff in Difficulty
            },
            "avg_quality_score": round(
                sum(q.quality_score for q in questions) / len(questions), 3
            ),
            "avg_relevance_score": round(
                sum(q.relevance_score for q in questions) / len(questions), 3
            ),
        }


# ============================================================================
# 3. CONTENT VALIDATOR AGENT
# ============================================================================

class ContentValidatorAgent:
    """Validates generated content for quality and correctness"""
    
    def __init__(self):
        self.validation_results = []
    
    def validate_question(self, question: Question) -> dict:
        """Validate a single question"""
        
        validation = {
            "question_id": question.id,
            "passed": True,
            "checks": {}
        }
        
        # Check 1: Question text not empty
        if not question.question_text or len(question.question_text) < 10:
            validation["checks"]["question_text"] = "FAILED: Too short"
            validation["passed"] = False
        else:
            validation["checks"]["question_text"] = "PASSED"
        
        # Check 2: Exactly 4 options (for multiple choice)
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            if len(question.options) != 4:
                validation["checks"]["options_count"] = f"FAILED: Expected 4, got {len(question.options)}"
                validation["passed"] = False
            else:
                validation["checks"]["options_count"] = "PASSED"
        
        # Check 3: Correct answer in options
        if question.correct_answer not in question.options:
            validation["checks"]["correct_answer_in_options"] = "FAILED: Correct answer not in options"
            validation["passed"] = False
        else:
            validation["checks"]["correct_answer_in_options"] = "PASSED"
        
        # Check 4: Explanation exists
        if not question.explanation or len(question.explanation) < 50:
            validation["checks"]["explanation"] = "FAILED: Explanation too short"
            validation["passed"] = False
        else:
            validation["checks"]["explanation"] = "PASSED"
        
        # Check 5: Quality & Relevance scores above threshold
        if question.quality_score < 0.6 or question.relevance_score < 0.6:
            validation["checks"]["quality_relevance"] = (
                f"WARNING: Low scores (Q:{question.quality_score}, R:{question.relevance_score})"
            )
        else:
            validation["checks"]["quality_relevance"] = "PASSED"
        
        self.validation_results.append(validation)
        return validation
    
    def validate_batch(self, questions: List[Question]) -> dict:
        """Validate a batch of questions"""
        
        results = [self.validate_question(q) for q in questions]
        
        passed = sum(1 for r in results if r["passed"])
        total = len(results)
        
        return {
            "total_questions": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": round(passed / total, 3) if total > 0 else 0,
            "details": results
        }


# ============================================================================
# 4. MAIN ORCHESTRATOR
# ============================================================================

class ExamContentOrchestrator:
    """Orchestrates the entire content generation pipeline"""
    
    def __init__(self):
        self.generator = QuestionGeneratorAgent()
        self.validator = ContentValidatorAgent()
        self.storage = []
    
    def generate_content_batch(self, request: GenerationRequest) -> dict:
        """
        Generate a batch of content with validation
        
        Returns: {
            "generated": List[Question],
            "validated": List[Question],
            "statistics": dict,
            "validation_report": dict
        }
        """
        
        logger.info(f"Starting content generation batch: {request}")
        
        # Step 1: Generate questions
        generated_questions = self.generator.generate_questions(request)
        logger.info(f"Generated {len(generated_questions)} questions")
        
        # Step 2: Validate questions
        validation_report = self.validator.validate_batch(generated_questions)
        logger.info(f"Validation report: {validation_report['pass_rate']*100:.1f}% pass rate")
        
        # Step 3: Filter valid questions
        valid_questions = [
            q for q in generated_questions
            if self.validator.validate_question(q)["passed"]
        ]
        logger.info(f"Stored {len(valid_questions)} valid questions")
        
        # Step 4: Store in memory (in production, use database)
        self.storage.extend(valid_questions)
        
        return {
            "generated": generated_questions,
            "validated": valid_questions,
            "statistics": self.generator.get_statistics(),
            "validation_report": validation_report,
        }
    
    def export_to_json(self, questions: List[Question], filename: str) -> str:
        """Export questions to JSON format"""
        
        data = {
            "metadata": {
                "export_date": datetime.now().isoformat(),
                "total_questions": len(questions),
                "exam_boards": list(set(q.exam_board.value for q in questions)),
                "subjects": list(set(q.subject for q in questions)),
            },
            "questions": [q.to_dict() for q in questions]
        }
        
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Exported {len(questions)} questions to {output_path}")
        return str(output_path)


# ============================================================================
# 5. CLI INTERFACE
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate exam content for WAEC, NECO, JAMB"
    )
    parser.add_argument(
        "--exam",
        type=str,
        choices=["waec", "neco", "jamb"],
        default="waec",
        help="Exam board (default: waec)"
    )
    parser.add_argument(
        "--subject",
        type=str,
        default="mathematics",
        help="Subject to generate questions for"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="algebra",
        help="Specific topic within subject"
    )
    parser.add_argument(
        "--difficulty",
        type=str,
        choices=["easy", "medium", "hard"],
        default="medium",
        help="Question difficulty level"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of questions to generate"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="runs/generated_content.json",
        help="Output JSON file"
    )
    
    args = parser.parse_args()
    
    # Create request
    request = GenerationRequest(
        exam_board=ExamBoard(args.exam),
        subject=args.subject,
        topic=args.topic,
        difficulty=Difficulty(args.difficulty),
        question_count=args.count,
    )
    
    # Run orchestrator
    orchestrator = ExamContentOrchestrator()
    result = orchestrator.generate_content_batch(request)
    
    # Export results
    orchestrator.export_to_json(result["validated"], args.output)
    
    # Print summary
    print("\n" + "="*60)
    print("CONTENT GENERATION SUMMARY")
    print("="*60)
    print(f"Generated:  {len(result['generated'])} questions")
    print(f"Valid:      {len(result['validated'])} questions")
    print(f"Pass Rate:  {result['validation_report']['pass_rate']*100:.1f}%")
    print(f"Exported to: {args.output}")
    print("="*60)
