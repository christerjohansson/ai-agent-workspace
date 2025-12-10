"""
Phase 4: Base Agent Implementation
==================================

Provides a unified BaseAgent class that incorporates all collaboration
framework capabilities (messaging, dependencies, context, conflicts, auditing).

This enables agents to:
- Send/receive structured messages
- Manage tasks and dependencies
- Share and access contexts
- Participate in conflict resolution
- Generate audit trails
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from enum import Enum

from src.collaboration.protocol import Message, MessageType, ProtocolValidator
from src.collaboration.message_queue import MessageBus
from src.collaboration.dependency_tracker import DependencyTracker, Task, TaskStatus
from src.collaboration.context_manager import (
    ContextManager, Context, ContextType, AccessLevel
)
from src.collaboration.conflict_resolver import (
    ConflictResolver, Conflict, ConflictType, ResolutionStrategy
)
from src.collaboration.audit_logger import AuditLogger, AuditEventType


class AgentCapability(Enum):
    """Capabilities an agent can have."""
    MESSAGING = "messaging"
    TASK_MANAGEMENT = "task_management"
    CONTEXT_SHARING = "context_sharing"
    CONFLICT_RESOLUTION = "conflict_resolution"
    CODE_REVIEW = "code_review"
    DESIGN = "design"
    DEPLOYMENT = "deployment"
    ORCHESTRATION = "orchestration"


class AgentState(Enum):
    """States an agent can be in."""
    IDLE = "idle"
    BUSY = "busy"
    WAITING = "waiting"
    FAILED = "failed"
    OFFLINE = "offline"


@dataclass
class AgentMetadata:
    """Metadata about an agent."""
    name: str
    agent_type: str
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.utcnow)
    state: AgentState = AgentState.IDLE
    capabilities: List[AgentCapability] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Base class for all collaborative agents in the framework.
    
    Provides unified interface for:
    - Message-based communication
    - Task coordination with dependencies
    - Shared context management
    - Conflict resolution
    - Comprehensive auditing
    
    Subclasses should implement:
    - process_message()
    - handle_task_request()
    - get_capabilities()
    """
    
    def __init__(
        self,
        name: str,
        agent_type: str,
        version: str = "1.0.0",
        use_message_queue: bool = False
    ):
        """
        Initialize base agent.
        
        Args:
            name: Unique agent identifier
            agent_type: Type of agent (Developer, Designer, etc.)
            version: Agent version
            use_message_queue: Whether to use Redis/RabbitMQ (vs in-memory)
        """
        self.metadata = AgentMetadata(name=name, agent_type=agent_type, version=version)
        
        # Collaboration framework components
        self.message_bus = MessageBus("memory") if not use_message_queue else MessageBus("redis")
        self.dependency_tracker = DependencyTracker()
        self.context_manager = ContextManager()
        self.conflict_resolver = ConflictResolver()
        self.audit_logger = AuditLogger()
        
        # Agent state
        self.incoming_messages: List[Message] = []
        self.task_assignments: Dict[str, Task] = {}
        self.message_handlers: Dict[MessageType, Callable] = {}
        
        # Register default message handlers
        self._register_default_handlers()
        
        # Log agent initialization
        self.audit_logger.log_event(
            event_type=AuditEventType.WORKFLOW_STARTED,
            agent=self.name,
            subject=f"{self.agent_type}_initialized",
            action=f"Initialized {self.agent_type} agent"
        )
    
    @property
    def name(self) -> str:
        """Get agent name."""
        return self.metadata.name
    
    @property
    def agent_type(self) -> str:
        """Get agent type."""
        return self.metadata.agent_type
    
    @property
    def state(self) -> AgentState:
        """Get current agent state."""
        return self.metadata.state
    
    @state.setter
    def state(self, value: AgentState) -> None:
        """Set agent state."""
        self.metadata.state = value
        self.audit_logger.log_event(
            event_type=AuditEventType.AGENT_STATE_CHANGED,
            agent=self.name,
            subject=self.name,
            action=f"State changed to {value.value}"
        )
    
    def _register_default_handlers(self) -> None:
        """Register default message handlers."""
        self.message_handlers[MessageType.TASK_REQUEST] = self.handle_task_request
        self.message_handlers[MessageType.TASK_UPDATE] = self.handle_task_update
        self.message_handlers[MessageType.CONTEXT_SHARE] = self.handle_context_share
        self.message_handlers[MessageType.REQUEST_FEEDBACK] = self.handle_feedback_request
    
    def register_capability(self, capability: AgentCapability) -> None:
        """Register an agent capability."""
        if capability not in self.metadata.capabilities:
            self.metadata.capabilities.append(capability)
            self.audit_logger.log_event(
                event_type=AuditEventType.AGENT_CAPABILITY_ADDED,
                agent=self.name,
                subject=self.name,
                action=f"Capability added: {capability.value}"
            )
    
    def send_message(
        self,
        to_agent: str,
        msg_type: MessageType,
        subject: str,
        data: Dict = None
    ) -> Message:
        """
        Send message to another agent.
        
        Args:
            to_agent: Target agent name
            msg_type: Type of message
            subject: Message subject
            data: Message data
        
        Returns:
            The sent message
        """
        message = Message(
            from_agent=self.name,
            to_agent=to_agent,
            msg_type=msg_type,
            subject=subject,
            data=data or {}
        )
        
        # Validate message
        validator = ProtocolValidator()
        if not validator.validate_message(message):
            raise ValueError(f"Invalid message from {self.name}: {message}")
        
        # Send via message bus
        self.message_bus.send_message(message)
        
        # Audit
        self.audit_logger.log_message_sent(
            self.name,
            to_agent,
            msg_type.value,
            subject
        )
        
        return message
    
    def receive_message(self, message: Message) -> None:
        """
        Receive and process a message from another agent.
        
        Args:
            message: The message to process
        """
        self.incoming_messages.append(message)
        self.audit_logger.log_event(
            event_type=AuditEventType.MESSAGE_RECEIVED,
            agent=self.name,
            subject=message.subject,
            action=f"Received {message.msg_type.value} from {message.from_agent}"
        )
        
        # Process the message
        self.process_message(message)
    
    def process_message(self, message: Message) -> None:
        """
        Process incoming message (can be overridden by subclasses).
        
        Args:
            message: The message to process
        """
        handler = self.message_handlers.get(message.msg_type)
        if handler:
            handler(message)
        else:
            self.audit_logger.log_event(
                event_type=AuditEventType.MESSAGE_FAILED,
                agent=self.name,
                subject=message.subject,
                action=f"No handler for message type {message.msg_type.value}"
            )
    
    def assign_task(
        self,
        task_id: str,
        task_name: str,
        dependencies: List[str] = None
    ) -> Task:
        """
        Assign a task to this agent.
        
        Args:
            task_id: Task identifier
            task_name: Task description
            dependencies: List of blocking task IDs
        
        Returns:
            The created task
        """
        task = self.dependency_tracker.add_task(
            task_id,
            task_name,
            self.name,
            priority=1
        )
        
        # Add dependencies
        for dep_id in (dependencies or []):
            dep_task = self.dependency_tracker.tasks.get(dep_id)
            if dep_task:
                self.dependency_tracker.add_dependency(task, dep_task)
        
        self.task_assignments[task_id] = task
        
        self.audit_logger.log_event(
            event_type=AuditEventType.TASK_ASSIGNED,
            agent=self.name,
            subject=task_id,
            action=f"Task assigned: {task_name}"
        )
        
        return task
    
    def check_ready(self, task_id: str) -> bool:
        """
        Check if a task is ready to start (all dependencies met).
        
        Args:
            task_id: Task identifier
        
        Returns:
            True if task is ready
        """
        task = self.task_assignments.get(task_id)
        if task:
            return self.dependency_tracker.is_ready(task)
        return False
    
    def mark_task_in_progress(self, task_id: str) -> None:
        """Mark task as in progress."""
        task = self.task_assignments.get(task_id)
        if task:
            self.dependency_tracker.mark_in_progress(task)
            self.state = AgentState.BUSY
            self.audit_logger.log_event(
                event_type=AuditEventType.TASK_STARTED,
                agent=self.name,
                subject=task_id,
                action="Task started"
            )
    
    def mark_task_completed(self, task_id: str, result: Dict = None) -> None:
        """Mark task as completed."""
        task = self.task_assignments.get(task_id)
        if task:
            self.dependency_tracker.mark_completed(task)
            self.state = AgentState.IDLE
            self.audit_logger.log_task_completed(
                self.name,
                task_id,
                result or {"status": "completed"}
            )
    
    def create_context(
        self,
        context_id: str,
        context_type: ContextType,
        data: Dict,
        access_level: AccessLevel = AccessLevel.TEAM,
        ttl: Optional[int] = None,
        tags: set = None
    ) -> Context:
        """
        Create a shared context.
        
        Args:
            context_id: Context identifier
            context_type: Type of context
            data: Context data
            access_level: Access control level
            ttl: Time to live in seconds
            tags: Optional tags
        
        Returns:
            The created context
        """
        context = self.context_manager.create_context(
            context_id=context_id,
            context_type=context_type,
            owner=self.name,
            data=data,
            access_level=access_level,
            ttl=ttl,
            tags=tags
        )
        
        self.audit_logger.log_context_created(
            self.name,
            context_id,
            context_type.value
        )
        
        return context
    
    def share_context(self, context_id: str, agents: List[str]) -> bool:
        """
        Share a context with other agents.
        
        Args:
            context_id: Context to share
            agents: List of agent names to share with
        
        Returns:
            True if successful
        """
        success = self.context_manager.share_context(context_id, agents)
        
        if success:
            self.audit_logger.log_context_shared(
                self.name,
                context_id,
                agents
            )
        
        return success
    
    def get_context(self, context_id: str) -> Optional[Context]:
        """
        Access a shared context.
        
        Args:
            context_id: Context to retrieve
        
        Returns:
            The context if accessible, None otherwise
        """
        return self.context_manager.get_context(context_id, self.name)
    
    def propose_resolution(
        self,
        conflict_id: str,
        option_id: str,
        rationale: str
    ) -> None:
        """
        Propose a resolution option for a conflict.
        
        Args:
            conflict_id: Conflict identifier
            option_id: Option to propose
            rationale: Rationale for the proposal
        """
        conflict = self.conflict_resolver.conflicts.get(conflict_id)
        if conflict:
            conflict.vote(self.name, option_id)
            self.audit_logger.log_event(
                event_type=AuditEventType.CONFLICT_VOTED,
                agent=self.name,
                subject=conflict_id,
                action=f"Voted for {option_id}",
                details={"rationale": rationale}
            )
    
    def resolve_conflict(
        self,
        conflict_id: str,
        strategy: ResolutionStrategy
    ) -> Optional[str]:
        """
        Attempt to resolve a conflict.
        
        Args:
            conflict_id: Conflict identifier
            strategy: Resolution strategy to use
        
        Returns:
            The selected option ID or None
        """
        resolution = self.conflict_resolver.resolve(conflict_id, strategy)
        
        if resolution:
            self.audit_logger.log_conflict_resolved(
                self.name,
                conflict_id,
                resolution,
                strategy.value
            )
        
        return resolution
    
    def handle_task_request(self, message: Message) -> None:
        """Handle incoming task request."""
        # Subclasses can override
        pass
    
    def handle_task_update(self, message: Message) -> None:
        """Handle incoming task update."""
        # Subclasses can override
        pass
    
    def handle_context_share(self, message: Message) -> None:
        """Handle incoming context share."""
        # Subclasses can override
        pass
    
    def handle_feedback_request(self, message: Message) -> None:
        """Handle incoming feedback request."""
        # Subclasses can override
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[AgentCapability]:
        """Return list of agent capabilities."""
        pass
    
    def get_status(self) -> Dict:
        """Get agent status."""
        return {
            "name": self.name,
            "type": self.agent_type,
            "state": self.state.value,
            "capabilities": [c.value for c in self.metadata.capabilities],
            "pending_messages": len(self.incoming_messages),
            "assigned_tasks": len(self.task_assignments),
            "version": self.metadata.version
        }


# =============================================================================
# Specialized Agent Implementations
# =============================================================================

class DeveloperAgent(BaseAgent):
    """Agent for development tasks."""
    
    def __init__(self, name: str = "Developer"):
        super().__init__(name, "Developer")
        self.register_capability(AgentCapability.TASK_MANAGEMENT)
        self.register_capability(AgentCapability.MESSAGING)
        self.register_capability(AgentCapability.CONTEXT_SHARING)
    
    def get_capabilities(self) -> List[AgentCapability]:
        return self.metadata.capabilities
    
    def handle_task_request(self, message: Message) -> None:
        """Handle task request."""
        task_data = message.data
        if "task_id" in task_data:
            self.assign_task(
                task_data["task_id"],
                task_data.get("task_name", "Development task")
            )


class DesignerAgent(BaseAgent):
    """Agent for design tasks."""
    
    def __init__(self, name: str = "Designer"):
        super().__init__(name, "Designer")
        self.register_capability(AgentCapability.DESIGN)
        self.register_capability(AgentCapability.CONTEXT_SHARING)
        self.register_capability(AgentCapability.CONFLICT_RESOLUTION)
    
    def get_capabilities(self) -> List[AgentCapability]:
        return self.metadata.capabilities


class CodeReviewerAgent(BaseAgent):
    """Agent for code review."""
    
    def __init__(self, name: str = "CodeReviewer"):
        super().__init__(name, "CodeReviewer")
        self.register_capability(AgentCapability.CODE_REVIEW)
        self.register_capability(AgentCapability.MESSAGING)
        self.register_capability(AgentCapability.CONFLICT_RESOLUTION)
    
    def get_capabilities(self) -> List[AgentCapability]:
        return self.metadata.capabilities


class DevOpsAgent(BaseAgent):
    """Agent for deployment and infrastructure."""
    
    def __init__(self, name: str = "DevOps"):
        super().__init__(name, "DevOps")
        self.register_capability(AgentCapability.DEPLOYMENT)
        self.register_capability(AgentCapability.MESSAGING)
        self.register_capability(AgentCapability.TASK_MANAGEMENT)
    
    def get_capabilities(self) -> List[AgentCapability]:
        return self.metadata.capabilities


class ProjectLeaderAgent(BaseAgent):
    """Agent for project coordination."""
    
    def __init__(self, name: str = "ProjectLeader"):
        super().__init__(name, "ProjectLeader")
        self.register_capability(AgentCapability.ORCHESTRATION)
        self.register_capability(AgentCapability.TASK_MANAGEMENT)
        self.register_capability(AgentCapability.CONFLICT_RESOLUTION)
    
    def get_capabilities(self) -> List[AgentCapability]:
        return self.metadata.capabilities


# =============================================================================
# Example: Agent Interaction
# =============================================================================

def demonstrate_base_agents():
    """Demonstrate base agent functionality."""
    
    print("=" * 80)
    print("BASE AGENT DEMONSTRATION")
    print("=" * 80)
    
    # Create agents
    developer = DeveloperAgent("dev1")
    designer = DesignerAgent("designer1")
    reviewer = CodeReviewerAgent("reviewer1")
    devops = DevOpsAgent("devops1")
    leader = ProjectLeaderAgent("leader1")
    
    print("\n[Agent Registration]")
    print(f"✓ Developer: {developer.get_status()['name']}")
    print(f"✓ Designer: {designer.get_status()['name']}")
    print(f"✓ Reviewer: {reviewer.get_status()['name']}")
    print(f"✓ DevOps: {devops.get_status()['name']}")
    print(f"✓ Leader: {leader.get_status()['name']}")
    
    # Task assignment
    print("\n[Task Assignment]")
    task1 = developer.assign_task("feat-001", "Implement feature")
    print(f"✓ Developer assigned task: {task1.name}")
    
    # Message sending
    print("\n[Message Passing]")
    msg = developer.send_message(
        to_agent="reviewer1",
        msg_type=MessageType.TASK_REQUEST,
        subject="Code review needed",
        data={"branch": "feature/new-feature"}
    )
    print(f"✓ Message sent: {msg.subject}")
    
    # Context creation
    print("\n[Context Management]")
    context = designer.create_context(
        context_id="ui-design",
        context_type=ContextType.DESIGN,
        data={"components": ["Button", "Form"]},
        access_level=AccessLevel.TEAM
    )
    print(f"✓ Context created: {context.metadata.context_id}")
    
    designer.share_context("ui-design", ["dev1", "reviewer1"])
    print(f"✓ Context shared with team")
    
    # Agent status
    print("\n[Agent Status]")
    print(f"Developer: {developer.get_status()}")
    
    print("\n" + "=" * 80)
    print("✓ Base agent demonstration complete!")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_base_agents()
