"""
Agent Communication Protocol

Defines the message format and types for inter-agent communication.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4


class MessageType(Enum):
    """Types of messages agents can send."""
    
    # Task-related messages
    TASK_REQUEST = "task_request"
    TASK_UPDATE = "task_update"
    TASK_COMPLETE = "task_complete"
    TASK_FAILED = "task_failed"
    
    # Coordination messages
    DEPENDENCY_CHECK = "dependency_check"
    CONTEXT_SHARE = "context_share"
    STATE_SYNC = "state_sync"
    
    # Decision messages
    REQUEST_FEEDBACK = "request_feedback"
    PROVIDE_FEEDBACK = "provide_feedback"
    CONFLICT_NOTIFICATION = "conflict_notification"
    DECISION_NEEDED = "decision_needed"
    
    # Acknowledgment
    ACK = "ack"
    NACK = "nack"


class MessagePriority(Enum):
    """Message priority levels."""
    
    LOW = 3
    NORMAL = 2
    HIGH = 1
    CRITICAL = 0


class MessageStatus(Enum):
    """Status of a message."""
    
    PENDING = "pending"
    DELIVERED = "delivered"
    PROCESSED = "processed"
    FAILED = "failed"
    EXPIRED = "expired"


@dataclass
class Message:
    """
    Standard message format for agent communication.
    
    Attributes:
        id: Unique message identifier
        from_agent: Sender agent name
        to_agent: Recipient agent name(s)
        msg_type: Type of message
        subject: Subject line for the message
        data: Message payload
        priority: Message priority level
        timestamp: When message was created
        status: Current message status
        reply_to: ID of message this is replying to
        context: Shared context metadata
        signature: Digital signature for verification
    """
    
    id: str
    from_agent: str
    to_agent: str | list[str]
    msg_type: MessageType
    subject: str
    data: Dict[str, Any]
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: datetime = None
    status: MessageStatus = MessageStatus.PENDING
    reply_to: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    signature: Optional[str] = None
    ttl: Optional[int] = None  # Time to live in seconds
    
    def __post_init__(self):
        """Initialize default values."""
        if self.id is None:
            self.id = str(uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        data = asdict(self)
        data['msg_type'] = self.msg_type.value
        data['priority'] = self.priority.value
        data['status'] = self.status.value
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    def is_expired(self) -> bool:
        """Check if message has expired."""
        if self.ttl is None:
            return False
        elapsed = (datetime.utcnow() - self.timestamp).total_seconds()
        return elapsed > self.ttl
    
    def is_critical(self) -> bool:
        """Check if message is critical priority."""
        return self.priority == MessagePriority.CRITICAL


@dataclass
class Response:
    """
    Response to a message.
    
    Attributes:
        message_id: ID of the message being responded to
        status: Response status
        data: Response payload
        error: Error message if response failed
    """
    
    message_id: str
    status: str  # "success", "error", "pending"
    data: Dict[str, Any]
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return asdict(self)


class ProtocolValidator:
    """Validates messages against protocol specifications."""
    
    REQUIRED_FIELDS = {'id', 'from_agent', 'to_agent', 'msg_type', 'subject', 'data'}
    
    @classmethod
    def validate_message(cls, message: Message) -> tuple[bool, Optional[str]]:
        """
        Validate a message.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if not hasattr(message, field) or getattr(message, field) is None:
                return False, f"Missing required field: {field}"
        
        # Validate message type
        if not isinstance(message.msg_type, MessageType):
            return False, f"Invalid message type: {message.msg_type}"
        
        # Validate priority
        if not isinstance(message.priority, MessagePriority):
            return False, f"Invalid priority: {message.priority}"
        
        # Validate status
        if not isinstance(message.status, MessageStatus):
            return False, f"Invalid status: {message.status}"
        
        # Validate recipient
        if isinstance(message.to_agent, list):
            if not message.to_agent:
                return False, "to_agent list cannot be empty"
        elif not isinstance(message.to_agent, str):
            return False, f"to_agent must be string or list, got {type(message.to_agent)}"
        
        # Validate expiration
        if message.is_expired():
            return False, "Message has expired"
        
        return True, None


# Protocol Examples

def create_task_request(
    from_agent: str,
    to_agent: str,
    task_id: str,
    task_description: str,
    deadline: str,
    priority: str = "normal"
) -> Message:
    """Create a task request message."""
    return Message(
        id=None,
        from_agent=from_agent,
        to_agent=to_agent,
        msg_type=MessageType.TASK_REQUEST,
        subject=f"New task: {task_id}",
        data={
            "task_id": task_id,
            "description": task_description,
            "deadline": deadline,
            "priority": priority
        },
        priority=MessagePriority.HIGH
    )


def create_task_complete(
    from_agent: str,
    to_agent: str,
    task_id: str,
    result: Dict[str, Any]
) -> Message:
    """Create a task completion message."""
    return Message(
        id=None,
        from_agent=from_agent,
        to_agent=to_agent,
        msg_type=MessageType.TASK_COMPLETE,
        subject=f"Task completed: {task_id}",
        data={
            "task_id": task_id,
            "result": result,
            "completed_at": datetime.utcnow().isoformat()
        }
    )


def create_feedback_request(
    from_agent: str,
    to_agent: str,
    topic: str,
    options: Dict[str, Any]
) -> Message:
    """Create a feedback request message."""
    return Message(
        id=None,
        from_agent=from_agent,
        to_agent=to_agent,
        msg_type=MessageType.REQUEST_FEEDBACK,
        subject=f"Feedback needed on: {topic}",
        data={
            "topic": topic,
            "options": options,
            "requested_at": datetime.utcnow().isoformat()
        },
        priority=MessagePriority.HIGH
    )
