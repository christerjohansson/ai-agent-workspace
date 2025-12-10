"""
Audit Logger

Provides comprehensive audit trail for all multi-agent interactions.
"""

from dataclasses import dataclass, asdict, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import json


class AuditEventType(Enum):
    """Types of events that can be audited."""
    
    # Message events
    MESSAGE_SENT = "message_sent"
    MESSAGE_RECEIVED = "message_received"
    MESSAGE_FAILED = "message_failed"
    
    # Context events
    CONTEXT_CREATED = "context_created"
    CONTEXT_UPDATED = "context_updated"
    CONTEXT_SHARED = "context_shared"
    CONTEXT_ACCESSED = "context_accessed"
    CONTEXT_DELETED = "context_deleted"
    
    # Task/Dependency events
    TASK_CREATED = "task_created"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    DEPENDENCY_ADDED = "dependency_added"
    DEPENDENCY_REMOVED = "dependency_removed"
    
    # Conflict events
    CONFLICT_CREATED = "conflict_created"
    CONFLICT_RESOLVED = "conflict_resolved"
    CONFLICT_ESCALATED = "conflict_escalated"
    
    # Decision events
    DECISION_MADE = "decision_made"
    DECISION_REVIEWED = "decision_reviewed"
    
    # System events
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"


@dataclass
class AuditEvent:
    """
    Represents a single auditable event.
    
    Attributes:
        event_id: Unique event identifier
        event_type: Type of event
        timestamp: When event occurred
        agent: Agent that triggered the event
        subject: What the event is about (context_id, task_id, etc.)
        action: Specific action taken
        details: Event details
        status: Success/failure status
        duration_ms: How long the action took
        metadata: Additional metadata
    """
    
    event_id: str
    event_type: AuditEventType
    timestamp: datetime
    agent: str
    subject: str                          # context_id, task_id, message_id, etc.
    action: str
    details: Dict[str, Any] = field(default_factory=dict)
    status: str = "success"               # success, failure, pending
    duration_ms: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['event_type'] = self.event_type.value
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


class AuditLogger:
    """
    Provides comprehensive audit trail for multi-agent system.
    
    Logs all significant events for compliance, debugging, and analysis.
    """
    
    def __init__(self, max_events: int = 10000):
        """
        Initialize audit logger.
        
        Args:
            max_events: Maximum events to keep in memory
        """
        self.events: List[AuditEvent] = []
        self.max_events = max_events
        self.event_index: Dict[str, List[int]] = {}  # subject -> event indices
    
    def log_event(
        self,
        event_type: AuditEventType,
        agent: str,
        subject: str,
        action: str,
        details: Dict[str, Any] = None,
        status: str = "success",
        duration_ms: Optional[float] = None,
        metadata: Dict[str, Any] = None
    ) -> AuditEvent:
        """
        Log an event.
        
        Args:
            event_type: Type of event
            agent: Agent that triggered event
            subject: Subject of event (context_id, task_id, etc.)
            action: Action taken
            details: Event details
            status: Success or failure
            duration_ms: Duration of action
            metadata: Additional metadata
        
        Returns:
            Created AuditEvent
        """
        from uuid import uuid4
        
        event = AuditEvent(
            event_id=str(uuid4()),
            event_type=event_type,
            timestamp=datetime.utcnow(),
            agent=agent,
            subject=subject,
            action=action,
            details=details or {},
            status=status,
            duration_ms=duration_ms,
            metadata=metadata or {}
        )
        
        # Add to events list
        self.events.append(event)
        
        # Add to index
        if subject not in self.event_index:
            self.event_index[subject] = []
        self.event_index[subject].append(len(self.events) - 1)
        
        # Cleanup if too many events
        if len(self.events) > self.max_events:
            self._cleanup_oldest()
        
        return event
    
    def log_message_sent(
        self,
        agent: str,
        message_id: str,
        recipient: str,
        message_type: str
    ) -> AuditEvent:
        """Log a message being sent."""
        return self.log_event(
            event_type=AuditEventType.MESSAGE_SENT,
            agent=agent,
            subject=message_id,
            action=f"Sent to {recipient}",
            details={"recipient": recipient, "message_type": message_type}
        )
    
    def log_context_created(
        self,
        agent: str,
        context_id: str,
        context_type: str
    ) -> AuditEvent:
        """Log context creation."""
        return self.log_event(
            event_type=AuditEventType.CONTEXT_CREATED,
            agent=agent,
            subject=context_id,
            action="Created context",
            details={"context_type": context_type}
        )
    
    def log_context_shared(
        self,
        agent: str,
        context_id: str,
        shared_with: List[str]
    ) -> AuditEvent:
        """Log context being shared."""
        return self.log_event(
            event_type=AuditEventType.CONTEXT_SHARED,
            agent=agent,
            subject=context_id,
            action="Shared context",
            details={"shared_with": shared_with}
        )
    
    def log_task_completed(
        self,
        agent: str,
        task_id: str,
        result: Dict[str, Any]
    ) -> AuditEvent:
        """Log task completion."""
        return self.log_event(
            event_type=AuditEventType.TASK_COMPLETED,
            agent=agent,
            subject=task_id,
            action="Completed task",
            details={"result": result}
        )
    
    def log_conflict_resolved(
        self,
        agent: str,
        conflict_id: str,
        resolution: str,
        strategy: str
    ) -> AuditEvent:
        """Log conflict resolution."""
        return self.log_event(
            event_type=AuditEventType.CONFLICT_RESOLVED,
            agent=agent,
            subject=conflict_id,
            action="Resolved conflict",
            details={"resolution": resolution, "strategy": strategy}
        )
    
    def get_events_for_subject(self, subject: str, limit: int = 100) -> List[AuditEvent]:
        """Get all events for a subject (context_id, task_id, etc.)."""
        indices = self.event_index.get(subject, [])
        return [self.events[i] for i in indices[-limit:]]
    
    def get_events_by_agent(self, agent: str, limit: int = 100) -> List[AuditEvent]:
        """Get all events triggered by an agent."""
        events = [e for e in self.events if e.agent == agent]
        return events[-limit:]
    
    def get_events_by_type(
        self,
        event_type: AuditEventType,
        limit: int = 100
    ) -> List[AuditEvent]:
        """Get all events of a specific type."""
        events = [e for e in self.events if e.event_type == event_type]
        return events[-limit:]
    
    def get_timeline(
        self,
        subject: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[AuditEvent]:
        """Get timeline of events for a subject within time range."""
        events = self.get_events_for_subject(subject)
        
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]
        
        return events
    
    def get_agent_interactions(
        self,
        agent1: str,
        agent2: str,
        limit: int = 100
    ) -> List[AuditEvent]:
        """Get interactions between two agents."""
        events = [
            e for e in self.events
            if (e.agent == agent1 and agent2 in str(e.details)) or
               (e.agent == agent2 and agent1 in str(e.details))
        ]
        return events[-limit:]
    
    def generate_report(
        self,
        subject: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Generate audit report for a subject."""
        events = self.get_timeline(subject, start_time, end_time)
        
        # Aggregate statistics
        agents_involved = set(e.agent for e in events)
        event_types = {}
        status_counts = {"success": 0, "failure": 0}
        
        for event in events:
            event_type = event.event_type.value
            event_types[event_type] = event_types.get(event_type, 0) + 1
            
            if event.status in status_counts:
                status_counts[event.status] += 1
        
        total_duration = sum(e.duration_ms or 0 for e in events)
        
        return {
            "subject": subject,
            "total_events": len(events),
            "agents_involved": list(agents_involved),
            "event_types": event_types,
            "status": status_counts,
            "total_duration_ms": total_duration,
            "average_duration_ms": total_duration / len(events) if events else 0,
            "time_range": {
                "start": events[0].timestamp.isoformat() if events else None,
                "end": events[-1].timestamp.isoformat() if events else None
            },
            "events": [e.to_dict() for e in events]
        }
    
    def export_events(self, subject: Optional[str] = None) -> str:
        """Export events as JSON."""
        if subject:
            events = self.get_events_for_subject(subject)
        else:
            events = self.events
        
        data = [e.to_dict() for e in events]
        return json.dumps(data, indent=2)
    
    def clear_events(self) -> None:
        """Clear all events (use with caution)."""
        self.events = []
        self.event_index = {}
    
    def _cleanup_oldest(self) -> None:
        """Remove oldest 10% of events."""
        remove_count = self.max_events // 10
        removed_events = self.events[:remove_count]
        self.events = self.events[remove_count:]
        
        # Rebuild index
        self.event_index = {}
        for idx, event in enumerate(self.events):
            if event.subject not in self.event_index:
                self.event_index[event.subject] = []
            self.event_index[event.subject].append(idx)
