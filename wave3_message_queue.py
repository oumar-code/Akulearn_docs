"""
Wave 3 Message Queue (RabbitMQ) Integration
Scalable WebSocket broadcasting and async task processing
"""

import pika
import json
from typing import Dict, List, Callable, Optional, Any
from functools import wraps
import threading
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageQueue:
    """
    RabbitMQ message queue manager for Wave 3
    """
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 5672,
        username: str = 'guest',
        password: str = 'guest',
        virtual_host: str = '/'
    ):
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(username, password)
        self.connection_params = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=virtual_host,
            credentials=self.credentials
        )
        
        self.connection = None
        self.channel = None
        self.consumers = {}
        
        # Standard exchanges and queues for Wave 3
        self.exchanges = {
            'websocket': 'websocket_broadcast',  # WebSocket messages
            'notifications': 'user_notifications',  # User notifications
            'analytics': 'analytics_events',  # Analytics processing
            'tasks': 'async_tasks'  # Background tasks
        }
        
        self.connect()
        self.setup_exchanges()
    
    def connect(self):
        """Establish connection to RabbitMQ"""
        try:
            self.connection = pika.BlockingConnection(self.connection_params)
            self.channel = self.connection.channel()
            logger.info("✓ Connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    def setup_exchanges(self):
        """Setup standard exchanges"""
        for exchange_name in self.exchanges.values():
            self.channel.exchange_declare(
                exchange=exchange_name,
                exchange_type='topic',
                durable=True
            )
    
    def ensure_connection(self):
        """Ensure connection is alive, reconnect if needed"""
        if self.connection is None or self.connection.is_closed:
            self.connect()
            self.setup_exchanges()
    
    # === WebSocket Broadcasting ===
    
    def broadcast_websocket_message(
        self,
        topic: str,
        message: Dict,
        student_ids: Optional[List[str]] = None
    ):
        """
        Broadcast message to WebSocket clients
        
        Args:
            topic: Message topic (e.g., 'lesson_update', 'badge_earned')
            message: Message payload
            student_ids: Optional list of specific students to notify
        """
        self.ensure_connection()
        
        routing_key = f"ws.{topic}"
        
        payload = {
            'topic': topic,
            'data': message,
            'timestamp': datetime.now().isoformat(),
            'student_ids': student_ids  # None = broadcast to all
        }
        
        self.channel.basic_publish(
            exchange=self.exchanges['websocket'],
            routing_key=routing_key,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Persistent
                content_type='application/json'
            )
        )
        
        logger.info(f"Broadcast WebSocket message: {topic}")
    
    def subscribe_websocket_broadcast(
        self,
        callback: Callable[[Dict], None],
        topics: List[str] = ['*']
    ):
        """
        Subscribe to WebSocket broadcast messages
        
        Args:
            callback: Function to call with message data
            topics: List of topics to subscribe to (supports wildcards)
        """
        queue_name = f"ws_subscriber_{id(callback)}"
        
        self.channel.queue_declare(queue=queue_name, exclusive=True)
        
        for topic in topics:
            routing_key = f"ws.{topic}"
            self.channel.queue_bind(
                exchange=self.exchanges['websocket'],
                queue=queue_name,
                routing_key=routing_key
            )
        
        def on_message(ch, method, properties, body):
            try:
                message = json.loads(body)
                callback(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing WebSocket broadcast: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message
        )
        
        logger.info(f"Subscribed to WebSocket topics: {topics}")
    
    # === User Notifications ===
    
    def send_notification(
        self,
        student_id: str,
        notification_type: str,
        data: Dict,
        priority: int = 5
    ):
        """
        Send notification to user
        
        Args:
            student_id: Target student
            notification_type: Type of notification
            data: Notification data
            priority: Priority (0-9, higher = more important)
        """
        self.ensure_connection()
        
        routing_key = f"notification.{student_id}.{notification_type}"
        
        payload = {
            'student_id': student_id,
            'type': notification_type,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'priority': priority
        }
        
        self.channel.basic_publish(
            exchange=self.exchanges['notifications'],
            routing_key=routing_key,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,
                priority=priority,
                content_type='application/json'
            )
        )
    
    def subscribe_notifications(
        self,
        callback: Callable[[Dict], None],
        student_id: Optional[str] = None
    ):
        """
        Subscribe to user notifications
        
        Args:
            callback: Function to process notifications
            student_id: Optional specific student (None = all students)
        """
        queue_name = f"notifications_{student_id or 'all'}"
        
        self.channel.queue_declare(queue=queue_name, durable=True)
        
        routing_key = f"notification.{student_id or '#'}.#"
        self.channel.queue_bind(
            exchange=self.exchanges['notifications'],
            queue=queue_name,
            routing_key=routing_key
        )
        
        def on_message(ch, method, properties, body):
            try:
                notification = json.loads(body)
                callback(notification)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing notification: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message
        )
    
    # === Analytics Events ===
    
    def publish_analytics_event(
        self,
        event_type: str,
        data: Dict
    ):
        """
        Publish analytics event for async processing
        
        Args:
            event_type: Type of event (e.g., 'lesson_completed', 'quiz_taken')
            data: Event data
        """
        self.ensure_connection()
        
        routing_key = f"analytics.{event_type}"
        
        payload = {
            'event_type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        self.channel.basic_publish(
            exchange=self.exchanges['analytics'],
            routing_key=routing_key,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
    
    def subscribe_analytics_events(
        self,
        callback: Callable[[Dict], None],
        event_types: List[str] = ['#']
    ):
        """Subscribe to analytics events"""
        queue_name = "analytics_processor"
        
        self.channel.queue_declare(queue=queue_name, durable=True)
        
        for event_type in event_types:
            routing_key = f"analytics.{event_type}"
            self.channel.queue_bind(
                exchange=self.exchanges['analytics'],
                queue=queue_name,
                routing_key=routing_key
            )
        
        def on_message(ch, method, properties, body):
            try:
                event = json.loads(body)
                callback(event)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing analytics event: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message
        )
    
    # === Background Tasks ===
    
    def enqueue_task(
        self,
        task_name: str,
        args: List = None,
        kwargs: Dict = None,
        priority: int = 5,
        delay: int = 0
    ):
        """
        Enqueue background task
        
        Args:
            task_name: Name of task to execute
            args: Positional arguments
            kwargs: Keyword arguments
            priority: Task priority (0-9)
            delay: Delay in seconds before processing
        """
        self.ensure_connection()
        
        routing_key = f"task.{task_name}"
        
        payload = {
            'task_name': task_name,
            'args': args or [],
            'kwargs': kwargs or {},
            'enqueued_at': datetime.now().isoformat(),
            'delay': delay
        }
        
        properties = pika.BasicProperties(
            delivery_mode=2,
            priority=priority,
            content_type='application/json'
        )
        
        if delay > 0:
            # Use delayed message plugin or DLX
            properties.expiration = str(delay * 1000)
        
        self.channel.basic_publish(
            exchange=self.exchanges['tasks'],
            routing_key=routing_key,
            body=json.dumps(payload),
            properties=properties
        )
    
    def subscribe_tasks(
        self,
        task_handlers: Dict[str, Callable],
        prefetch_count: int = 1
    ):
        """
        Subscribe to background tasks
        
        Args:
            task_handlers: Dict mapping task names to handler functions
            prefetch_count: Number of messages to prefetch
        """
        queue_name = "task_worker"
        
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=prefetch_count)
        
        for task_name in task_handlers.keys():
            routing_key = f"task.{task_name}"
            self.channel.queue_bind(
                exchange=self.exchanges['tasks'],
                queue=queue_name,
                routing_key=routing_key
            )
        
        def on_message(ch, method, properties, body):
            try:
                task = json.loads(body)
                task_name = task['task_name']
                
                if task_name in task_handlers:
                    handler = task_handlers[task_name]
                    result = handler(*task['args'], **task['kwargs'])
                    logger.info(f"Task {task_name} completed: {result}")
                else:
                    logger.warning(f"No handler for task: {task_name}")
                
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error executing task: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message
        )
    
    # === Worker Thread ===
    
    def start_consuming(self):
        """Start consuming messages (blocking)"""
        logger.info("Starting message queue consumer...")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
            self.channel.stop_consuming()
            self.connection.close()
    
    def start_consuming_thread(self):
        """Start consuming in background thread"""
        consumer_thread = threading.Thread(target=self.start_consuming, daemon=True)
        consumer_thread.start()
        return consumer_thread
    
    def close(self):
        """Close connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("Closed RabbitMQ connection")


# Decorator for async task processing
def async_task(queue_manager: MessageQueue, task_name: str = None):
    """
    Decorator to make function an async task
    
    Usage:
        @async_task(queue, task_name="send_email")
        def send_email(recipient: str, subject: str, body: str):
            ...
    """
    def decorator(func: Callable):
        nonlocal task_name
        if task_name is None:
            task_name = func.__name__
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Enqueue instead of executing directly
            queue_manager.enqueue_task(
                task_name=task_name,
                args=args,
                kwargs=kwargs
            )
        
        # Attach original function for direct execution
        wrapper._original = func
        wrapper._task_name = task_name
        
        return wrapper
    
    return decorator


# Example task handlers
def process_recommendation_update(student_id: str, lesson_id: str):
    """Example: Update recommendations after lesson completion"""
    logger.info(f"Processing recommendation update for {student_id}")
    # ... recommendation logic ...
    return {'status': 'updated'}


def send_achievement_notification(student_id: str, achievement_id: str):
    """Example: Send notification for new achievement"""
    logger.info(f"Sending achievement notification to {student_id}")
    # ... notification logic ...
    return {'status': 'sent'}


def calculate_leaderboard(leaderboard_id: str):
    """Example: Recalculate leaderboard rankings"""
    logger.info(f"Calculating leaderboard: {leaderboard_id}")
    # ... leaderboard logic ...
    return {'status': 'calculated'}


# Example usage
if __name__ == "__main__":
    # Initialize queue
    queue = MessageQueue()
    
    # Example 1: WebSocket Broadcasting
    queue.broadcast_websocket_message(
        topic='lesson_update',
        message={
            'lesson_id': 'math_101',
            'action': 'new_content',
            'title': 'New practice problems added'
        }
    )
    
    # Example 2: Send notification
    queue.send_notification(
        student_id='student_123',
        notification_type='badge_earned',
        data={
            'badge_id': 'math_master',
            'title': 'Math Master',
            'description': 'Complete 50 math lessons'
        },
        priority=8
    )
    
    # Example 3: Analytics event
    queue.publish_analytics_event(
        event_type='lesson_completed',
        data={
            'student_id': 'student_123',
            'lesson_id': 'physics_201',
            'score': 95,
            'time_spent': 1200
        }
    )
    
    # Example 4: Background task
    queue.enqueue_task(
        task_name='send_achievement_notification',
        kwargs={
            'student_id': 'student_123',
            'achievement_id': 'first_perfect_score'
        },
        priority=7
    )
    
    # Example 5: Setup workers
    task_handlers = {
        'process_recommendation_update': process_recommendation_update,
        'send_achievement_notification': send_achievement_notification,
        'calculate_leaderboard': calculate_leaderboard
    }
    
    # Start worker in background thread
    # worker_thread = queue.start_consuming_thread()
    
    print("✓ Message queue examples executed")
    
    # Close connection
    queue.close()
