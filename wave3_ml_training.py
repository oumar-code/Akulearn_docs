"""
Wave 3 ML Training Module
Custom ML models for enhanced recommendations and predictions
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import pickle
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any
from pathlib import Path


class MasteryPredictor:
    """
    ML model to predict student mastery level based on activity patterns
    """
    
    def __init__(self, model_path: str = "models/mastery_predictor.pkl"):
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.model_path = model_path
        self.feature_names = [
            'quiz_attempts', 'quiz_avg_score', 'time_spent_hours',
            'practice_problems_completed', 'video_views',
            'consecutive_days', 'avg_session_length',
            'problem_accuracy', 'help_requests', 'hints_used'
        ]
        
    def extract_features(self, student_data: Dict) -> np.ndarray:
        """Extract features from student activity data"""
        features = [
            student_data.get('quiz_attempts', 0),
            student_data.get('quiz_avg_score', 0),
            student_data.get('time_spent_hours', 0),
            student_data.get('practice_problems_completed', 0),
            student_data.get('video_views', 0),
            student_data.get('consecutive_days', 0),
            student_data.get('avg_session_length', 0),
            student_data.get('problem_accuracy', 0),
            student_data.get('help_requests', 0),
            student_data.get('hints_used', 0)
        ]
        return np.array(features).reshape(1, -1)
    
    def train(self, training_data: List[Dict], labels: List[float]) -> Dict[str, float]:
        """
        Train the mastery prediction model
        
        Args:
            training_data: List of student activity dictionaries
            labels: Mastery scores (0-100)
            
        Returns:
            Training metrics
        """
        # Extract features
        X = np.array([self.extract_features(data).flatten() for data in training_data])
        y = np.array(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5)
        
        # Save model
        self.save_model()
        
        return {
            'train_r2': train_score,
            'test_r2': test_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_importance': dict(zip(
                self.feature_names,
                self.model.feature_importances_
            ))
        }
    
    def predict(self, student_data: Dict) -> float:
        """Predict mastery level (0-100)"""
        features = self.extract_features(student_data)
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        return max(0, min(100, prediction))  # Clamp to 0-100
    
    def save_model(self):
        """Save model and scaler to disk"""
        Path(self.model_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler}, f)
    
    def load_model(self):
        """Load model and scaler from disk"""
        with open(self.model_path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']


class DifficultyClassifier:
    """
    ML model to classify content difficulty based on features
    """
    
    def __init__(self, model_path: str = "models/difficulty_classifier.pkl"):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.model_path = model_path
        self.difficulty_levels = ['beginner', 'intermediate', 'advanced', 'expert']
        
    def extract_features(self, content: Dict) -> np.ndarray:
        """Extract features from content"""
        features = [
            len(content.get('text', '')),  # Content length
            content.get('num_formulas', 0),
            content.get('num_diagrams', 0),
            content.get('vocabulary_complexity', 0),  # 0-10 scale
            content.get('prerequisite_count', 0),
            content.get('avg_word_length', 0),
            content.get('sentence_complexity', 0),  # 0-10 scale
            content.get('concept_density', 0),  # concepts per 100 words
        ]
        return np.array(features).reshape(1, -1)
    
    def train(self, training_data: List[Dict], labels: List[str]) -> Dict[str, float]:
        """Train difficulty classifier"""
        X = np.array([self.extract_features(data).flatten() for data in training_data])
        y = np.array([self.difficulty_levels.index(label) for label in labels])
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model.fit(X_train_scaled, y_train)
        
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average='weighted'
        )
        
        self.save_model()
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
    
    def predict(self, content: Dict) -> str:
        """Predict difficulty level"""
        features = self.extract_features(content)
        features_scaled = self.scaler.transform(features)
        prediction_idx = self.model.predict(features_scaled)[0]
        return self.difficulty_levels[prediction_idx]
    
    def save_model(self):
        """Save model to disk"""
        Path(self.model_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler}, f)
    
    def load_model(self):
        """Load model from disk"""
        with open(self.model_path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']


class ModelTrainingPipeline:
    """
    Complete training pipeline for Wave 3 ML models
    """
    
    def __init__(self, data_dir: str = "training_data/"):
        self.data_dir = Path(data_dir)
        self.mastery_predictor = MasteryPredictor()
        self.difficulty_classifier = DifficultyClassifier()
        self.training_history = []
        
    def load_training_data(self) -> Tuple[List[Dict], List[Any]]:
        """Load training data from files"""
        mastery_data_path = self.data_dir / "mastery_training.json"
        difficulty_data_path = self.data_dir / "difficulty_training.json"
        
        mastery_data = []
        mastery_labels = []
        difficulty_data = []
        difficulty_labels = []
        
        if mastery_data_path.exists():
            with open(mastery_data_path, 'r') as f:
                data = json.load(f)
                mastery_data = data['features']
                mastery_labels = data['labels']
        
        if difficulty_data_path.exists():
            with open(difficulty_data_path, 'r') as f:
                data = json.load(f)
                difficulty_data = data['features']
                difficulty_labels = data['labels']
        
        return (mastery_data, mastery_labels, difficulty_data, difficulty_labels)
    
    def train_all_models(self) -> Dict[str, Dict]:
        """Train all ML models"""
        mastery_data, mastery_labels, difficulty_data, difficulty_labels = self.load_training_data()
        
        results = {}
        
        # Train mastery predictor
        if mastery_data:
            print("Training mastery predictor...")
            mastery_metrics = self.mastery_predictor.train(mastery_data, mastery_labels)
            results['mastery_predictor'] = mastery_metrics
            print(f"Mastery predictor trained - Test R²: {mastery_metrics['test_r2']:.3f}")
        
        # Train difficulty classifier
        if difficulty_data:
            print("Training difficulty classifier...")
            difficulty_metrics = self.difficulty_classifier.train(difficulty_data, difficulty_labels)
            results['difficulty_classifier'] = difficulty_metrics
            print(f"Difficulty classifier trained - Accuracy: {difficulty_metrics['accuracy']:.3f}")
        
        # Save training history
        self.training_history.append({
            'timestamp': datetime.now().isoformat(),
            'results': results
        })
        
        self._save_training_history()
        
        return results
    
    def _save_training_history(self):
        """Save training history to file"""
        history_path = self.data_dir / "training_history.json"
        with open(history_path, 'w') as f:
            json.dump(self.training_history, f, indent=2)
    
    def generate_sample_data(self, num_samples: int = 1000):
        """Generate synthetic training data for testing"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate mastery prediction data
        mastery_features = []
        mastery_labels = []
        
        for _ in range(num_samples):
            # Simulate student activity
            quiz_attempts = np.random.randint(1, 20)
            quiz_avg_score = np.random.uniform(30, 100)
            time_spent = np.random.uniform(0.5, 50)
            problems_completed = np.random.randint(0, 100)
            
            # Create target mastery based on activity (with noise)
            mastery_score = (
                quiz_avg_score * 0.4 +
                min(time_spent * 2, 30) +
                min(problems_completed * 0.3, 20) +
                np.random.normal(0, 5)
            )
            mastery_score = max(0, min(100, mastery_score))
            
            features = {
                'quiz_attempts': quiz_attempts,
                'quiz_avg_score': quiz_avg_score,
                'time_spent_hours': time_spent,
                'practice_problems_completed': problems_completed,
                'video_views': np.random.randint(0, 30),
                'consecutive_days': np.random.randint(0, 30),
                'avg_session_length': np.random.uniform(5, 120),
                'problem_accuracy': np.random.uniform(0, 1),
                'help_requests': np.random.randint(0, 20),
                'hints_used': np.random.randint(0, 50)
            }
            
            mastery_features.append(features)
            mastery_labels.append(mastery_score)
        
        # Save mastery data
        with open(self.data_dir / "mastery_training.json", 'w') as f:
            json.dump({
                'features': mastery_features,
                'labels': mastery_labels
            }, f, indent=2)
        
        # Generate difficulty classification data
        difficulty_features = []
        difficulty_labels = []
        difficulty_levels = ['beginner', 'intermediate', 'advanced', 'expert']
        
        for _ in range(num_samples):
            level = np.random.choice(difficulty_levels)
            level_idx = difficulty_levels.index(level)
            
            # Features correlated with difficulty
            features = {
                'text': 'x' * np.random.randint(500 + level_idx * 500, 1500 + level_idx * 1000),
                'num_formulas': np.random.randint(level_idx, level_idx * 5 + 5),
                'num_diagrams': np.random.randint(0, level_idx + 2),
                'vocabulary_complexity': level_idx + np.random.uniform(0, 2),
                'prerequisite_count': level_idx + np.random.randint(0, 3),
                'avg_word_length': 4 + level_idx * 0.5 + np.random.uniform(0, 1),
                'sentence_complexity': level_idx * 2 + np.random.uniform(0, 2),
                'concept_density': level_idx + np.random.uniform(0, 2)
            }
            
            difficulty_features.append(features)
            difficulty_labels.append(level)
        
        # Save difficulty data
        with open(self.data_dir / "difficulty_training.json", 'w') as f:
            json.dump({
                'features': difficulty_features,
                'labels': difficulty_labels
            }, f, indent=2)
        
        print(f"Generated {num_samples} training samples for each model")


# Example usage
if __name__ == "__main__":
    # Initialize pipeline
    pipeline = ModelTrainingPipeline()
    
    # Generate sample data
    pipeline.generate_sample_data(num_samples=1000)
    
    # Train models
    results = pipeline.train_all_models()
    
    print("\n=== Training Complete ===")
    print(json.dumps(results, indent=2))
    
    # Test predictions
    test_student = {
        'quiz_attempts': 10,
        'quiz_avg_score': 85,
        'time_spent_hours': 20,
        'practice_problems_completed': 50,
        'video_views': 15,
        'consecutive_days': 14,
        'avg_session_length': 45,
        'problem_accuracy': 0.80,
        'help_requests': 5,
        'hints_used': 10
    }
    
    predicted_mastery = pipeline.mastery_predictor.predict(test_student)
    print(f"\nPredicted mastery for test student: {predicted_mastery:.1f}%")
    
    test_content = {
        'text': 'x' * 2000,
        'num_formulas': 10,
        'num_diagrams': 3,
        'vocabulary_complexity': 7,
        'prerequisite_count': 5,
        'avg_word_length': 6.5,
        'sentence_complexity': 8,
        'concept_density': 6
    }
    
    predicted_difficulty = pipeline.difficulty_classifier.predict(test_content)
    print(f"Predicted difficulty for test content: {predicted_difficulty}")
