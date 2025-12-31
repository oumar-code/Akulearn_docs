"""
Wave 3 A/B Testing Framework
Test and compare different algorithms, features, and UI variations
"""

import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from scipy import stats


class TestStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


@dataclass
class Variant:
    """Test variant configuration"""
    id: str
    name: str
    description: str
    traffic_allocation: float  # 0-1, percentage of users
    config: Dict[str, Any]  # Variant-specific configuration
    

@dataclass
class Metric:
    """Metric to track in A/B test"""
    name: str
    type: str  # 'conversion', 'numerical', 'duration'
    goal: str  # 'maximize', 'minimize'
    primary: bool = False  # Is this the primary metric?


@dataclass
class ExperimentResult:
    """Results for a single variant"""
    variant_id: str
    sample_size: int
    metric_values: Dict[str, List[float]]
    aggregated_metrics: Dict[str, float]
    confidence_intervals: Dict[str, tuple]


class ABTest:
    """
    A/B Test experiment manager
    """
    
    def __init__(
        self,
        test_id: str,
        name: str,
        description: str,
        variants: List[Variant],
        metrics: List[Metric],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        self.test_id = test_id
        self.name = name
        self.description = description
        self.variants = variants
        self.metrics = metrics
        self.start_date = start_date or datetime.now()
        self.end_date = end_date
        self.status = TestStatus.DRAFT
        
        # Validate traffic allocation
        total_traffic = sum(v.traffic_allocation for v in variants)
        if not (0.99 <= total_traffic <= 1.01):
            raise ValueError(f"Traffic allocation must sum to 1.0, got {total_traffic}")
        
        # Data storage
        self.events: Dict[str, List[Dict]] = {v.id: [] for v in variants}
        self.assignments: Dict[str, str] = {}  # user_id -> variant_id
        
    def assign_variant(self, user_id: str) -> str:
        """
        Consistently assign user to a variant
        Uses deterministic hashing for consistency
        """
        if user_id in self.assignments:
            return self.assignments[user_id]
        
        # Hash user_id + test_id for deterministic assignment
        hash_input = f"{user_id}:{self.test_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        random_value = (hash_value % 10000) / 10000.0  # 0-1 range
        
        # Assign to variant based on traffic allocation
        cumulative = 0
        for variant in self.variants:
            cumulative += variant.traffic_allocation
            if random_value < cumulative:
                self.assignments[user_id] = variant.id
                return variant.id
        
        # Fallback to first variant
        self.assignments[user_id] = self.variants[0].id
        return self.variants[0].id
    
    def get_variant_config(self, user_id: str) -> Dict[str, Any]:
        """Get configuration for user's assigned variant"""
        variant_id = self.assign_variant(user_id)
        variant = next(v for v in self.variants if v.id == variant_id)
        return variant.config
    
    def track_event(self, user_id: str, metric_name: str, value: Any):
        """Record a metric event for a user"""
        variant_id = self.assign_variant(user_id)
        
        event = {
            'user_id': user_id,
            'metric_name': metric_name,
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        
        self.events[variant_id].append(event)
    
    def get_results(self) -> Dict[str, ExperimentResult]:
        """
        Analyze results for all variants
        """
        results = {}
        
        for variant in self.variants:
            variant_events = self.events[variant.id]
            
            # Organize events by metric
            metric_values = {}
            for metric in self.metrics:
                values = [
                    e['value'] for e in variant_events 
                    if e['metric_name'] == metric.name
                ]
                metric_values[metric.name] = values
            
            # Calculate aggregated metrics
            aggregated = {}
            confidence_intervals = {}
            
            for metric_name, values in metric_values.items():
                if not values:
                    aggregated[metric_name] = 0
                    confidence_intervals[metric_name] = (0, 0)
                    continue
                
                metric = next(m for m in self.metrics if m.name == metric_name)
                
                if metric.type == 'conversion':
                    # Binary metric (0 or 1)
                    conversion_rate = np.mean(values)
                    aggregated[metric_name] = conversion_rate
                    
                    # Wilson score interval for binomial proportion
                    n = len(values)
                    p = conversion_rate
                    z = 1.96  # 95% confidence
                    denominator = 1 + z**2 / n
                    center = (p + z**2 / (2*n)) / denominator
                    margin = z * np.sqrt((p*(1-p)/n + z**2/(4*n**2))) / denominator
                    confidence_intervals[metric_name] = (
                        max(0, center - margin),
                        min(1, center + margin)
                    )
                
                elif metric.type in ['numerical', 'duration']:
                    # Continuous metric
                    mean = np.mean(values)
                    aggregated[metric_name] = mean
                    
                    # Confidence interval for mean
                    sem = stats.sem(values)
                    ci = stats.t.interval(0.95, len(values)-1, loc=mean, scale=sem)
                    confidence_intervals[metric_name] = ci
            
            results[variant.id] = ExperimentResult(
                variant_id=variant.id,
                sample_size=len(set(e['user_id'] for e in variant_events)),
                metric_values=metric_values,
                aggregated_metrics=aggregated,
                confidence_intervals=confidence_intervals
            )
        
        return results
    
    def statistical_significance(
        self,
        control_variant_id: str,
        test_variant_id: str,
        metric_name: str
    ) -> Dict[str, Any]:
        """
        Test statistical significance between control and test variant
        """
        control_events = [
            e['value'] for e in self.events[control_variant_id]
            if e['metric_name'] == metric_name
        ]
        test_events = [
            e['value'] for e in self.events[test_variant_id]
            if e['metric_name'] == metric_name
        ]
        
        if not control_events or not test_events:
            return {
                'significant': False,
                'p_value': 1.0,
                'error': 'Insufficient data'
            }
        
        metric = next(m for m in self.metrics if m.name == metric_name)
        
        if metric.type == 'conversion':
            # Two-proportion z-test
            n1, n2 = len(control_events), len(test_events)
            p1, p2 = np.mean(control_events), np.mean(test_events)
            
            p_pooled = (sum(control_events) + sum(test_events)) / (n1 + n2)
            se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
            
            if se == 0:
                z_score = 0
                p_value = 1.0
            else:
                z_score = (p2 - p1) / se
                p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
            
            return {
                'significant': p_value < 0.05,
                'p_value': p_value,
                'z_score': z_score,
                'control_rate': p1,
                'test_rate': p2,
                'lift': ((p2 - p1) / p1 * 100) if p1 > 0 else 0
            }
        
        else:
            # Two-sample t-test
            t_stat, p_value = stats.ttest_ind(control_events, test_events)
            
            control_mean = np.mean(control_events)
            test_mean = np.mean(test_events)
            
            return {
                'significant': p_value < 0.05,
                'p_value': p_value,
                't_statistic': t_stat,
                'control_mean': control_mean,
                'test_mean': test_mean,
                'lift': ((test_mean - control_mean) / control_mean * 100) if control_mean > 0 else 0
            }
    
    def start(self):
        """Start the experiment"""
        self.status = TestStatus.ACTIVE
        self.start_date = datetime.now()
    
    def pause(self):
        """Pause the experiment"""
        self.status = TestStatus.PAUSED
    
    def complete(self):
        """Complete the experiment"""
        self.status = TestStatus.COMPLETED
        self.end_date = datetime.now()
    
    def to_dict(self) -> Dict:
        """Serialize test to dictionary"""
        return {
            'test_id': self.test_id,
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'variants': [asdict(v) for v in self.variants],
            'metrics': [asdict(m) for m in self.metrics],
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'assignments': self.assignments,
            'events': self.events
        }


class ABTestManager:
    """
    Manage multiple A/B tests
    """
    
    def __init__(self, data_dir: str = "ab_tests/"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.tests: Dict[str, ABTest] = {}
        self.load_tests()
    
    def create_test(
        self,
        test_id: str,
        name: str,
        description: str,
        variants: List[Variant],
        metrics: List[Metric]
    ) -> ABTest:
        """Create a new A/B test"""
        test = ABTest(test_id, name, description, variants, metrics)
        self.tests[test_id] = test
        self.save_test(test)
        return test
    
    def get_test(self, test_id: str) -> Optional[ABTest]:
        """Get test by ID"""
        return self.tests.get(test_id)
    
    def list_active_tests(self) -> List[ABTest]:
        """List all active tests"""
        return [t for t in self.tests.values() if t.status == TestStatus.ACTIVE]
    
    def save_test(self, test: ABTest):
        """Save test to disk"""
        file_path = self.data_dir / f"{test.test_id}.json"
        with open(file_path, 'w') as f:
            json.dump(test.to_dict(), f, indent=2)
    
    def load_tests(self):
        """Load all tests from disk"""
        for file_path in self.data_dir.glob("*.json"):
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                # Reconstruct test object
                variants = [Variant(**v) for v in data['variants']]
                metrics = [Metric(**m) for m in data['metrics']]
                
                test = ABTest(
                    test_id=data['test_id'],
                    name=data['name'],
                    description=data['description'],
                    variants=variants,
                    metrics=metrics,
                    start_date=datetime.fromisoformat(data['start_date']) if data['start_date'] else None,
                    end_date=datetime.fromisoformat(data['end_date']) if data['end_date'] else None
                )
                
                test.status = TestStatus(data['status'])
                test.assignments = data['assignments']
                test.events = data['events']
                
                self.tests[test.test_id] = test


# Example A/B tests for Wave 3 features
def create_recommendation_algorithm_test(manager: ABTestManager) -> ABTest:
    """
    Test different recommendation algorithms
    """
    return manager.create_test(
        test_id="rec_algo_v1",
        name="Recommendation Algorithm Comparison",
        description="Compare collaborative filtering vs. content-based vs. hybrid",
        variants=[
            Variant(
                id="control",
                name="Collaborative Filtering",
                description="Pure collaborative filtering",
                traffic_allocation=0.33,
                config={'algorithm': 'collaborative_filtering'}
            ),
            Variant(
                id="content_based",
                name="Content-Based",
                description="Pure content-based filtering",
                traffic_allocation=0.33,
                config={'algorithm': 'content_based'}
            ),
            Variant(
                id="hybrid",
                name="Hybrid Approach",
                description="Weighted combination of both",
                traffic_allocation=0.34,
                config={'algorithm': 'hybrid', 'cf_weight': 0.6, 'cb_weight': 0.4}
            )
        ],
        metrics=[
            Metric(
                name="lesson_completion",
                type="conversion",
                goal="maximize",
                primary=True
            ),
            Metric(
                name="time_to_completion",
                type="duration",
                goal="minimize",
                primary=False
            ),
            Metric(
                name="quiz_score",
                type="numerical",
                goal="maximize",
                primary=False
            )
        ]
    )


def create_gamification_ui_test(manager: ABTestManager) -> ABTest:
    """
    Test different gamification UI designs
    """
    return manager.create_test(
        test_id="gamification_ui_v1",
        name="Gamification UI Design",
        description="Test badge design and achievement notifications",
        variants=[
            Variant(
                id="control",
                name="Minimal UI",
                description="Simple badge display",
                traffic_allocation=0.5,
                config={'badge_style': 'minimal', 'notification_frequency': 'low'}
            ),
            Variant(
                id="enhanced",
                name="Enhanced UI",
                description="Animated badges with celebrations",
                traffic_allocation=0.5,
                config={'badge_style': 'animated', 'notification_frequency': 'high'}
            )
        ],
        metrics=[
            Metric(
                name="engagement_rate",
                type="conversion",
                goal="maximize",
                primary=True
            ),
            Metric(
                name="daily_active_time",
                type="duration",
                goal="maximize",
                primary=False
            )
        ]
    )


# Example usage
if __name__ == "__main__":
    # Initialize manager
    manager = ABTestManager()
    
    # Create recommendation algorithm test
    rec_test = create_recommendation_algorithm_test(manager)
    rec_test.start()
    
    # Simulate user interactions
    test_users = [f"user_{i}" for i in range(100)]
    
    for user_id in test_users:
        # Assign to variant
        variant_id = rec_test.assign_variant(user_id)
        
        # Simulate metrics
        rec_test.track_event(user_id, "lesson_completion", np.random.choice([0, 1], p=[0.3, 0.7]))
        rec_test.track_event(user_id, "time_to_completion", np.random.uniform(300, 1800))
        rec_test.track_event(user_id, "quiz_score", np.random.uniform(60, 95))
    
    # Get results
    results = rec_test.get_results()
    
    print("=== A/B Test Results ===")
    for variant_id, result in results.items():
        print(f"\nVariant: {variant_id}")
        print(f"Sample size: {result.sample_size}")
        print(f"Metrics: {result.aggregated_metrics}")
    
    # Test significance
    sig_test = rec_test.statistical_significance("control", "hybrid", "lesson_completion")
    print(f"\nSignificance test (control vs hybrid):")
    print(f"Significant: {sig_test['significant']}")
    print(f"P-value: {sig_test['p_value']:.4f}")
    print(f"Lift: {sig_test['lift']:.2f}%")
    
    # Save results
    manager.save_test(rec_test)
