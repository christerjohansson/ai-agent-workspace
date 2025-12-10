"""
Package initialization for collaboration module.
"""

from src.collaboration.protocol import (
    Message, MessageType, MessagePriority, MessageStatus,
    Response, ProtocolValidator
)
from src.collaboration.message_queue import MessageBus, MessageQueueBackend
from src.collaboration.dependency_tracker import DependencyTracker, Task, TaskStatus
from src.collaboration.context_manager import (
    ContextManager, Context, ContextMetadata, ContextType, AccessLevel
)
from src.collaboration.conflict_resolver import (
    ConflictResolver, Conflict, ConflictOption,
    ConflictType, ResolutionStrategy, ConflictStatus
)
from src.collaboration.audit_logger import AuditLogger, AuditEventType

__all__ = [
    # Phase 1
    'Message',
    'MessageType',
    'MessagePriority',
    'MessageStatus',
    'Response',
    'ProtocolValidator',
    'MessageBus',
    'MessageQueueBackend',
    'DependencyTracker',
    'Task',
    'TaskStatus',
    # Phase 2
    'ContextManager',
    'Context',
    'ContextMetadata',
    'ContextType',
    'AccessLevel',
    'ConflictResolver',
    'Conflict',
    'ConflictOption',
    'ConflictType',
    'ResolutionStrategy',
    'ConflictStatus',
    'AuditLogger',
    'AuditEventType',
]
