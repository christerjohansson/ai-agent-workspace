"""
Message Queue Service

Provides abstraction for message queue operations.
Supports Redis and RabbitMQ backends.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import json
from datetime import datetime
from src.collaboration.protocol import Message, MessageStatus


class MessageQueueBackend(ABC):
    """Abstract base class for message queue implementations."""
    
    @abstractmethod
    def connect(self) -> None:
        """Connect to message queue service."""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from message queue service."""
        pass
    
    @abstractmethod
    def publish(self, channel: str, message: Message) -> str:
        """Publish a message to a channel."""
        pass
    
    @abstractmethod
    def subscribe(self, channel: str, callback) -> None:
        """Subscribe to a channel with callback."""
        pass
    
    @abstractmethod
    def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from a channel."""
        pass
    
    @abstractmethod
    def get_messages(self, channel: str, count: int = 10) -> List[Message]:
        """Get messages from a channel."""
        pass
    
    @abstractmethod
    def acknowledge(self, message_id: str) -> None:
        """Acknowledge a message was processed."""
        pass


class RedisBackend(MessageQueueBackend):
    """Redis-based message queue implementation."""
    
    def __init__(self, url: str = "redis://localhost:6379"):
        """Initialize Redis backend."""
        self.url = url
        self.redis = None
        self.pubsub = None
    
    def connect(self) -> None:
        """Connect to Redis."""
        try:
            import redis
            self.redis = redis.from_url(self.url, decode_responses=True)
            self.redis.ping()
            print("✓ Connected to Redis")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redis: {e}")
    
    def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self.redis:
            self.redis.close()
    
    def publish(self, channel: str, message: Message) -> str:
        """Publish message to Redis channel."""
        if not self.redis:
            raise RuntimeError("Not connected to Redis")
        
        message_json = json.dumps(message.to_dict())
        self.redis.publish(channel, message_json)
        
        # Also store in message log
        log_key = f"messages:{channel}"
        self.redis.lpush(log_key, message_json)
        self.redis.ltrim(log_key, 0, 999)  # Keep last 1000 messages
        
        return message.id
    
    def subscribe(self, channel: str, callback) -> None:
        """Subscribe to Redis channel."""
        if not self.redis:
            raise RuntimeError("Not connected to Redis")
        
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel)
        
        # This is blocking - should be used in separate thread
        for message in pubsub.listen():
            if message['type'] == 'message':
                msg_data = json.loads(message['data'])
                callback(msg_data)
    
    def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from Redis channel."""
        if self.pubsub:
            self.pubsub.unsubscribe(channel)
    
    def get_messages(self, channel: str, count: int = 10) -> List[Message]:
        """Get messages from Redis channel history."""
        if not self.redis:
            raise RuntimeError("Not connected to Redis")
        
        log_key = f"messages:{channel}"
        messages = self.redis.lrange(log_key, 0, count - 1)
        
        return [
            Message(**json.loads(msg))
            for msg in messages
        ]
    
    def acknowledge(self, message_id: str) -> None:
        """Mark message as acknowledged."""
        if not self.redis:
            raise RuntimeError("Not connected to Redis")
        
        # Store acknowledgment
        self.redis.sadd("acknowledged_messages", message_id)


class RabbitMQBackend(MessageQueueBackend):
    """RabbitMQ-based message queue implementation."""
    
    def __init__(self, url: str = "amqp://guest:guest@localhost/"):
        """Initialize RabbitMQ backend."""
        self.url = url
        self.connection = None
        self.channel = None
    
    def connect(self) -> None:
        """Connect to RabbitMQ."""
        try:
            import pika
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.url)
            )
            self.channel = self.connection.channel()
            print("✓ Connected to RabbitMQ")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to RabbitMQ: {e}")
    
    def disconnect(self) -> None:
        """Disconnect from RabbitMQ."""
        if self.connection:
            self.connection.close()
    
    def publish(self, channel: str, message: Message) -> str:
        """Publish message to RabbitMQ."""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        # Declare queue if not exists
        self.channel.queue_declare(queue=channel, durable=True)
        
        message_json = json.dumps(message.to_dict())
        self.channel.basic_publish(
            exchange='',
            routing_key=channel,
            body=message_json,
            properties=pika.BasicProperties(
                delivery_mode=2  # Make message persistent
            )
        )
        
        return message.id
    
    def subscribe(self, channel: str, callback) -> None:
        """Subscribe to RabbitMQ queue."""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        # Declare queue
        self.channel.queue_declare(queue=channel, durable=True)
        
        def message_callback(ch, method, properties, body):
            msg_data = json.loads(body)
            callback(msg_data)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        self.channel.basic_consume(
            queue=channel,
            on_message_callback=message_callback,
            auto_ack=False
        )
        
        self.channel.start_consuming()
    
    def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from RabbitMQ queue."""
        if self.channel:
            self.channel.stop_consuming()
    
    def get_messages(self, channel: str, count: int = 10) -> List[Message]:
        """Get messages from RabbitMQ queue."""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        messages = []
        for _ in range(count):
            method, properties, body = self.channel.basic_get(channel)
            if body:
                msg_data = json.loads(body)
                messages.append(Message(**msg_data))
        
        return messages
    
    def acknowledge(self, message_id: str) -> None:
        """Mark message as acknowledged."""
        pass


class MessageBus:
    """
    Central message bus for agent communication.
    
    Abstracts away the underlying message queue implementation.
    """
    
    def __init__(self, backend_type: str = "redis", **config):
        """
        Initialize message bus.
        
        Args:
            backend_type: "redis" or "rabbitmq"
            **config: Backend-specific configuration
        """
        if backend_type.lower() == "redis":
            url = config.get("url", "redis://localhost:6379")
            self.backend = RedisBackend(url)
        elif backend_type.lower() == "rabbitmq":
            url = config.get("url", "amqp://guest:guest@localhost/")
            self.backend = RabbitMQBackend(url)
        else:
            raise ValueError(f"Unknown backend type: {backend_type}")
        
        self.backend.connect()
        self.subscriptions: Dict[str, Any] = {}
    
    def send_message(self, message: Message) -> str:
        """Send a message."""
        # Determine channel from recipient
        if isinstance(message.to_agent, list):
            channel = f"agents:{message.to_agent[0]}"
        else:
            channel = f"agents:{message.to_agent}"
        
        return self.backend.publish(channel, message)
    
    def broadcast_message(self, message: Message) -> List[str]:
        """Broadcast a message to multiple recipients."""
        message_ids = []
        if isinstance(message.to_agent, list):
            for recipient in message.to_agent:
                msg_copy = Message(
                    id=None,
                    from_agent=message.from_agent,
                    to_agent=recipient,
                    msg_type=message.msg_type,
                    subject=message.subject,
                    data=message.data,
                    priority=message.priority
                )
                msg_id = self.send_message(msg_copy)
                message_ids.append(msg_id)
        
        return message_ids
    
    def subscribe(self, agent_name: str, callback) -> None:
        """Subscribe an agent to messages."""
        channel = f"agents:{agent_name}"
        self.backend.subscribe(channel, callback)
        self.subscriptions[agent_name] = callback
    
    def unsubscribe(self, agent_name: str) -> None:
        """Unsubscribe an agent from messages."""
        channel = f"agents:{agent_name}"
        self.backend.unsubscribe(channel)
        del self.subscriptions[agent_name]
    
    def get_messages_for_agent(
        self,
        agent_name: str,
        count: int = 10
    ) -> List[Message]:
        """Retrieve messages for an agent."""
        channel = f"agents:{agent_name}"
        return self.backend.get_messages(channel, count)
    
    def acknowledge_message(self, message_id: str) -> None:
        """Acknowledge a message was processed."""
        self.backend.acknowledge(message_id)
    
    def close(self) -> None:
        """Close the message bus."""
        self.backend.disconnect()
