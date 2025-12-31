"""
Wave 3 Performance Monitoring & Observability
Real-time metrics, logging, and APM integration
"""

import time
import psutil
import logging
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from functools import wraps
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import json
from pathlib import Path
import statistics


# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/wave3_performance.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@dataclass
class RequestMetric:
    """Single request performance metric"""
    endpoint: str
    method: str
    status_code: int
    duration_ms: float
    timestamp: str
    user_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class SystemMetric:
    """System resource metrics"""
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_usage_percent: float
    active_connections: int
    timestamp: str


class MetricsCollector:
    """
    Collect and aggregate performance metrics
    """
    
    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self.request_metrics: deque = deque(maxlen=window_size)
        self.system_metrics: deque = deque(maxlen=window_size)
        
        # Real-time counters
        self.endpoint_counters: Dict[str, int] = defaultdict(int)
        self.error_counters: Dict[str, int] = defaultdict(int)
        self.active_requests: int = 0
        
        # Timing buckets for histograms
        self.timing_buckets: Dict[str, List[float]] = defaultdict(list)
        
    def record_request(self, metric: RequestMetric):
        """Record a request metric"""
        self.request_metrics.append(metric)
        self.endpoint_counters[metric.endpoint] += 1
        
        if metric.error:
            self.error_counters[metric.endpoint] += 1
        
        # Store for percentile calculations
        self.timing_buckets[metric.endpoint].append(metric.duration_ms)
        
        # Keep only recent timings
        if len(self.timing_buckets[metric.endpoint]) > self.window_size:
            self.timing_buckets[metric.endpoint] = self.timing_buckets[metric.endpoint][-self.window_size:]
        
        # Log slow requests
        if metric.duration_ms > 1000:
            logger.warning(
                f"Slow request: {metric.method} {metric.endpoint} - {metric.duration_ms:.2f}ms",
                extra={'metric': asdict(metric)}
            )
    
    def record_system_metrics(self):
        """Record current system metrics"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Count network connections (approximation)
        try:
            connections = len(psutil.net_connections())
        except:
            connections = 0
        
        metric = SystemMetric(
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / (1024 * 1024),
            disk_usage_percent=disk.percent,
            active_connections=connections,
            timestamp=datetime.now().isoformat()
        )
        
        self.system_metrics.append(metric)
        
        # Alert on high resource usage
        if cpu_percent > 80:
            logger.warning(f"High CPU usage: {cpu_percent}%")
        if memory.percent > 80:
            logger.warning(f"High memory usage: {memory.percent}%")
    
    def get_endpoint_stats(self, endpoint: str) -> Dict[str, Any]:
        """Get statistics for a specific endpoint"""
        timings = self.timing_buckets.get(endpoint, [])
        
        if not timings:
            return {
                'endpoint': endpoint,
                'total_requests': 0,
                'error_rate': 0
            }
        
        return {
            'endpoint': endpoint,
            'total_requests': self.endpoint_counters[endpoint],
            'errors': self.error_counters[endpoint],
            'error_rate': self.error_counters[endpoint] / self.endpoint_counters[endpoint],
            'avg_duration_ms': statistics.mean(timings),
            'median_duration_ms': statistics.median(timings),
            'p95_duration_ms': self._percentile(timings, 95),
            'p99_duration_ms': self._percentile(timings, 99),
            'min_duration_ms': min(timings),
            'max_duration_ms': max(timings)
        }
    
    def get_all_endpoint_stats(self) -> List[Dict[str, Any]]:
        """Get statistics for all endpoints"""
        return [
            self.get_endpoint_stats(endpoint)
            for endpoint in self.endpoint_counters.keys()
        ]
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get current system health snapshot"""
        if not self.system_metrics:
            self.record_system_metrics()
        
        recent_metrics = list(self.system_metrics)[-10:]  # Last 10 samples
        
        return {
            'current': asdict(self.system_metrics[-1]) if self.system_metrics else {},
            'avg_cpu_percent': statistics.mean(m.cpu_percent for m in recent_metrics),
            'avg_memory_percent': statistics.mean(m.memory_percent for m in recent_metrics),
            'active_requests': self.active_requests,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get complete metrics summary"""
        total_requests = sum(self.endpoint_counters.values())
        total_errors = sum(self.error_counters.values())
        
        all_timings = []
        for timings in self.timing_buckets.values():
            all_timings.extend(timings)
        
        return {
            'overview': {
                'total_requests': total_requests,
                'total_errors': total_errors,
                'error_rate': total_errors / total_requests if total_requests > 0 else 0,
                'unique_endpoints': len(self.endpoint_counters),
                'active_requests': self.active_requests
            },
            'performance': {
                'avg_duration_ms': statistics.mean(all_timings) if all_timings else 0,
                'median_duration_ms': statistics.median(all_timings) if all_timings else 0,
                'p95_duration_ms': self._percentile(all_timings, 95) if all_timings else 0,
                'p99_duration_ms': self._percentile(all_timings, 99) if all_timings else 0
            },
            'system': self.get_system_health(),
            'endpoints': self.get_all_endpoint_stats()
        }
    
    @staticmethod
    def _percentile(data: List[float], percentile: float) -> float:
        """Calculate percentile value"""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]


# Global metrics collector instance
metrics_collector = MetricsCollector()


def monitor_performance(endpoint: str = None):
    """
    Decorator to monitor endpoint performance
    
    Usage:
        @monitor_performance(endpoint="/api/v3/recommendations")
        async def get_recommendations(student_id: str):
            ...
    """
    def decorator(func: Callable):
        nonlocal endpoint
        if endpoint is None:
            endpoint = func.__name__
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            metrics_collector.active_requests += 1
            
            error = None
            status_code = 200
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                error = str(e)
                status_code = 500
                logger.error(
                    f"Error in {endpoint}: {error}",
                    exc_info=True,
                    extra={'endpoint': endpoint}
                )
                raise
            finally:
                duration_ms = (time.time() - start_time) * 1000
                metrics_collector.active_requests -= 1
                
                # Extract user_id if available
                user_id = kwargs.get('student_id') or kwargs.get('user_id')
                
                metric = RequestMetric(
                    endpoint=endpoint,
                    method="ASYNC",
                    status_code=status_code,
                    duration_ms=duration_ms,
                    timestamp=datetime.now().isoformat(),
                    user_id=user_id,
                    error=error
                )
                
                metrics_collector.record_request(metric)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            metrics_collector.active_requests += 1
            
            error = None
            status_code = 200
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error = str(e)
                status_code = 500
                logger.error(
                    f"Error in {endpoint}: {error}",
                    exc_info=True,
                    extra={'endpoint': endpoint}
                )
                raise
            finally:
                duration_ms = (time.time() - start_time) * 1000
                metrics_collector.active_requests -= 1
                
                user_id = kwargs.get('student_id') or kwargs.get('user_id')
                
                metric = RequestMetric(
                    endpoint=endpoint,
                    method="SYNC",
                    status_code=status_code,
                    duration_ms=duration_ms,
                    timestamp=datetime.now().isoformat(),
                    user_id=user_id,
                    error=error
                )
                
                metrics_collector.record_request(metric)
        
        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class AlertManager:
    """
    Manage performance alerts and thresholds
    """
    
    def __init__(self):
        self.alerts: List[Dict] = []
        self.alert_handlers: List[Callable] = []
        
        # Default thresholds
        self.thresholds = {
            'error_rate': 0.05,  # 5% error rate
            'p99_latency_ms': 2000,  # 2 seconds
            'cpu_percent': 80,
            'memory_percent': 85
        }
    
    def add_handler(self, handler: Callable):
        """Add alert handler function"""
        self.alert_handlers.append(handler)
    
    def check_alerts(self, metrics: Dict[str, Any]):
        """Check metrics against thresholds and trigger alerts"""
        alerts_triggered = []
        
        # Check error rate
        if metrics['overview']['error_rate'] > self.thresholds['error_rate']:
            alert = {
                'type': 'error_rate',
                'severity': 'high',
                'message': f"Error rate {metrics['overview']['error_rate']:.2%} exceeds threshold",
                'timestamp': datetime.now().isoformat()
            }
            alerts_triggered.append(alert)
        
        # Check P99 latency
        if metrics['performance']['p99_duration_ms'] > self.thresholds['p99_latency_ms']:
            alert = {
                'type': 'latency',
                'severity': 'medium',
                'message': f"P99 latency {metrics['performance']['p99_duration_ms']:.0f}ms exceeds threshold",
                'timestamp': datetime.now().isoformat()
            }
            alerts_triggered.append(alert)
        
        # Check CPU usage
        if metrics['system']['current'].get('cpu_percent', 0) > self.thresholds['cpu_percent']:
            alert = {
                'type': 'cpu',
                'severity': 'high',
                'message': f"CPU usage {metrics['system']['current']['cpu_percent']:.1f}% exceeds threshold",
                'timestamp': datetime.now().isoformat()
            }
            alerts_triggered.append(alert)
        
        # Check memory usage
        if metrics['system']['current'].get('memory_percent', 0) > self.thresholds['memory_percent']:
            alert = {
                'type': 'memory',
                'severity': 'high',
                'message': f"Memory usage {metrics['system']['current']['memory_percent']:.1f}% exceeds threshold",
                'timestamp': datetime.now().isoformat()
            }
            alerts_triggered.append(alert)
        
        # Trigger handlers for new alerts
        for alert in alerts_triggered:
            self.alerts.append(alert)
            logger.warning(f"Alert triggered: {alert['message']}")
            
            for handler in self.alert_handlers:
                try:
                    handler(alert)
                except Exception as e:
                    logger.error(f"Error in alert handler: {e}")
        
        return alerts_triggered
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Get recent alerts"""
        return self.alerts[-limit:]


# Global alert manager
alert_manager = AlertManager()


# Example alert handler
def log_alert_to_file(alert: Dict):
    """Example: Log alert to dedicated file"""
    alert_log_path = Path("logs/alerts.log")
    alert_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(alert_log_path, 'a') as f:
        f.write(json.dumps(alert) + '\n')


# Export metrics for Prometheus (optional)
def export_prometheus_metrics() -> str:
    """
    Export metrics in Prometheus format
    """
    summary = metrics_collector.get_summary()
    
    lines = [
        "# HELP wave3_requests_total Total number of requests",
        "# TYPE wave3_requests_total counter",
        f"wave3_requests_total {summary['overview']['total_requests']}",
        "",
        "# HELP wave3_errors_total Total number of errors",
        "# TYPE wave3_errors_total counter",
        f"wave3_errors_total {summary['overview']['total_errors']}",
        "",
        "# HELP wave3_request_duration_ms Request duration in milliseconds",
        "# TYPE wave3_request_duration_ms summary",
        f"wave3_request_duration_ms_sum {summary['performance']['avg_duration_ms'] * summary['overview']['total_requests']}",
        f"wave3_request_duration_ms_count {summary['overview']['total_requests']}",
        "",
        "# HELP wave3_active_requests Current active requests",
        "# TYPE wave3_active_requests gauge",
        f"wave3_active_requests {summary['overview']['active_requests']}",
        "",
        "# HELP wave3_cpu_percent CPU usage percentage",
        "# TYPE wave3_cpu_percent gauge",
        f"wave3_cpu_percent {summary['system']['avg_cpu_percent']}",
        "",
        "# HELP wave3_memory_percent Memory usage percentage",
        "# TYPE wave3_memory_percent gauge",
        f"wave3_memory_percent {summary['system']['avg_memory_percent']}",
    ]
    
    return '\n'.join(lines)


# Example usage with FastAPI
"""
from fastapi import FastAPI, Request
from wave3_performance_monitoring import monitor_performance, metrics_collector, alert_manager

app = FastAPI()

@app.middleware("http")
async def performance_middleware(request: Request, call_next):
    start_time = time.time()
    metrics_collector.active_requests += 1
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        error = None
    except Exception as e:
        status_code = 500
        error = str(e)
        raise
    finally:
        duration_ms = (time.time() - start_time) * 1000
        metrics_collector.active_requests -= 1
        
        metric = RequestMetric(
            endpoint=request.url.path,
            method=request.method,
            status_code=status_code,
            duration_ms=duration_ms,
            timestamp=datetime.now().isoformat(),
            error=error
        )
        metrics_collector.record_request(metric)
    
    return response

@app.get("/metrics")
async def get_metrics():
    return metrics_collector.get_summary()

@app.get("/metrics/prometheus")
async def prometheus_metrics():
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(export_prometheus_metrics())

@app.get("/health")
async def health_check():
    return metrics_collector.get_system_health()
"""


if __name__ == "__main__":
    # Example usage
    import asyncio
    
    # Add alert handler
    alert_manager.add_handler(log_alert_to_file)
    
    # Simulate some requests
    @monitor_performance(endpoint="/api/test")
    async def test_endpoint(student_id: str):
        await asyncio.sleep(0.1)
        return {"status": "ok"}
    
    async def main():
        # Simulate traffic
        for i in range(100):
            await test_endpoint(student_id=f"student_{i}")
            metrics_collector.record_system_metrics()
        
        # Get summary
        summary = metrics_collector.get_summary()
        print(json.dumps(summary, indent=2))
        
        # Check alerts
        alerts = alert_manager.check_alerts(summary)
        print(f"\nAlerts triggered: {len(alerts)}")
    
    asyncio.run(main())
