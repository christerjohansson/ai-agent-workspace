# Phase 5: Comprehensive Documentation and Testing Guide

## Overview

This document provides comprehensive documentation for the Multi-Agent Collaboration Framework (Issue #1) and a complete testing guide for all phases.

## Framework Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Multi-Agent System                          │
└─────────────────────────────────────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
      ┌────▼────┐        ┌────▼────┐       ┌────▼────┐
      │ Agent 1  │        │ Agent 2  │       │ Agent N  │
      │ (Developer) │      │ (Designer)│     │(DevOps)  │
      └────┬────┘        └────┬────┘       └────┬────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        │    Collaboration Framework Layer          │
        ├─────────────────────────────────────────┤
        │  ┌─────────────────────────────────┐   │
        │  │ Message Bus (Phase 1)           │   │
        │  │ - Protocol validation           │   │
        │  │ - Redis/RabbitMQ backends       │   │
        │  └─────────────────────────────────┘   │
        │                                         │
        │  ┌─────────────────────────────────┐   │
        │  │ Dependency Tracker (Phase 1)    │   │
        │  │ - Task management               │   │
        │  │ - Cycle detection               │   │
        │  │ - Ready-state validation        │   │
        │  └─────────────────────────────────┘   │
        │                                         │
        │  ┌─────────────────────────────────┐   │
        │  │ Context Manager (Phase 2)       │   │
        │  │ - Shared context with access    │   │
        │  │ - Versioning and TTL            │   │
        │  │ - Subscriptions                 │   │
        │  └─────────────────────────────────┘   │
        │                                         │
        │  ┌─────────────────────────────────┐   │
        │  │ Conflict Resolver (Phase 2)     │   │
        │  │ - Multiple strategies           │   │
        │  │ - Voting and consensus          │   │
        │  │ - Escalation                    │   │
        │  └─────────────────────────────────┘   │
        │                                         │
        │  ┌─────────────────────────────────┐   │
        │  │ Audit Logger (Phase 2)          │   │
        │  │ - Event tracking                │   │
        │  │ - Timeline queries              │   │
        │  │ - Report generation             │   │
        │  └─────────────────────────────────┘   │
        │                                         │
        │  ┌─────────────────────────────────┐   │
        │  │ BaseAgent (Phase 4)             │   │
        │  │ - Unified agent interface       │   │
        │  │ - State management              │   │
        │  │ - Capability registration       │   │
        │  └─────────────────────────────────┘   │
        │                                         │
        └─────────────────────────────────────────┘
```

## Phase Breakdown

### Phase 1: Core Communication & Dependency Management

**Components:**
- `protocol.py` - Message protocol with validation
- `message_queue.py` - Message bus abstraction (Redis + RabbitMQ)
- `dependency_tracker.py` - Task dependencies with cycle detection

**Key Classes:**
- `Message` - Standard message format
- `ProtocolValidator` - Message validation
- `MessageBus` - Unified message interface
- `DependencyTracker` - Task coordination

**Lines of Code:** ~1,000+ LOC
**Test Coverage:** Basic protocol, messaging, dependency tracking

**Example:**
```python
from src.collaboration import MessageBus, DependencyTracker

# Create message bus
bus = MessageBus("redis", url="redis://localhost:6379")

# Send message
msg = Message(
    from_agent="Agent1",
    to_agent="Agent2",
    msg_type=MessageType.TASK_REQUEST,
    subject="Start feature",
    data={"feature_id": "feat-001"}
)
bus.send_message(msg)

# Track dependencies
tracker = DependencyTracker()
task1 = tracker.add_task("design", "Design UI", "Designer")
task2 = tracker.add_task("dev", "Implement", "Developer")
tracker.add_dependency(task2, task1)  # dev depends on design

# Check ready state
print(tracker.is_ready(task2))  # False until task1 completed
```

### Phase 2: Advanced Collaboration Features

**Components:**
- `context_manager.py` - Shared context with access control
- `conflict_resolver.py` - Multi-strategy conflict resolution
- `audit_logger.py` - Comprehensive audit trail

**Key Classes:**
- `ContextManager` - Context lifecycle management
- `ConflictResolver` - Conflict resolution strategies
- `AuditLogger` - Event tracking and reporting

**Lines of Code:** ~980+ LOC
**Test Coverage:** 40+ test cases

**Example:**
```python
from src.collaboration import ContextManager, ConflictResolver

# Create shared context
context_mgr = ContextManager()
context = context_mgr.create_context(
    context_id="project-scope",
    context_type=ContextType.PROJECT,
    owner="ProductOwner",
    data={"features": [...]},
    access_level=AccessLevel.TEAM
)

# Share with team
context_mgr.share_context("project-scope", ["Developer", "Designer"])

# Resolve conflict
resolver = ConflictResolver()
conflict = resolver.create_conflict(
    conflict_id="scope-conflict",
    conflict_type=ConflictType.DECISION_CONFLICT,
    agents_involved=["Developer", "ProductOwner"],
    topic="Feature scope",
    options=[...]
)

# Vote and resolve
conflict.vote("Developer", "option1")
conflict.vote("ProductOwner", "option2")
result = resolver.resolve("scope-conflict", ResolutionStrategy.MAJORITY_VOTE)
```

### Phase 3: Example Workflows

**Components:**
- `example_workflows.py` - 3 complete workflow examples

**Workflows:**
1. **Roadmap Planning** - ProductOwner + ProjectLeader coordination
2. **Feature Development** - Multi-agent handoff workflow
3. **Design Conflict** - Resolution with voting

**Lines of Code:** 600+ LOC
**Purpose:** Demonstrate real-world framework usage

### Phase 4: Base Agent Implementation

**Components:**
- `base_agent.py` - Unified agent interface

**Key Classes:**
- `BaseAgent` - Base class for all agents
- `DeveloperAgent` - Developer specialization
- `DesignerAgent` - Designer specialization
- `CodeReviewerAgent` - Review specialization
- `DevOpsAgent` - Deployment specialization
- `ProjectLeaderAgent` - Coordination specialization

**Lines of Code:** 600+ LOC
**Features:** Capabilities, state management, integrated framework access

## Running the Framework

### Installation

```bash
# Install dependencies
pip install redis pika pytest

# Or use in-memory message queue (no dependencies)
```

### Usage

```python
from src.collaboration import (
    BaseAgent, DeveloperAgent, DesignerAgent, DevOpsAgent,
    ProjectLeaderAgent, CodeReviewerAgent
)

# Create agents
developer = DeveloperAgent("dev1")
designer = DesignerAgent("designer1")
reviewer = CodeReviewerAgent("reviewer1")

# Send messages
developer.send_message(
    to_agent="designer1",
    msg_type=MessageType.TASK_REQUEST,
    subject="Need design specs",
    data={"component": "form-input"}
)

# Manage tasks
task = developer.assign_task("feat-001", "Implement form")
developer.mark_task_in_progress("feat-001")
developer.mark_task_completed("feat-001", {"pr": "#123"})

# Share contexts
context = developer.create_context(
    context_id="implementation-details",
    context_type=ContextType.TASK,
    data={"branch": "feature/form-input"},
    access_level=AccessLevel.TEAM
)
developer.share_context("implementation-details", ["designer1", "reviewer1"])

# Participate in conflicts
developer.propose_resolution("design-conflict", "opt1", "Better performance")
resolution = developer.resolve_conflict(
    "design-conflict",
    ResolutionStrategy.MAJORITY_VOTE
)
```

## Testing Guide

### Phase 1 Tests
Located in `tests/collaboration/test_framework.py`

**Test Categories:**
1. Protocol validation
2. Message creation and expiration
3. Dependency tracking and ready-state
4. Cycle detection
5. Blocker analysis

**Run Tests:**
```bash
pytest tests/collaboration/test_framework.py -v
```

### Phase 2 Tests
Located in `tests/collaboration/test_phase2.py`

**Test Categories:**
1. Context creation and access control
2. Context sharing and updates
3. Context versioning and history
4. TTL-based expiration
5. Conflict creation and resolution
6. Conflict voting strategies
7. Audit event logging and reporting

**Run Tests:**
```bash
pytest tests/collaboration/test_phase2.py -v
```

### Example Workflows
Located in `src/collaboration/example_workflows.py`

**Run Examples:**
```bash
python src/collaboration/example_workflows.py
```

**Output:**
```
================================================================================
MULTI-AGENT WORKFLOW EXAMPLES
================================================================================

[Example 1] Roadmap Planning Workflow
--------------------------------------------------------------------------------
✓ Roadmap created: q1-roadmap
✓ Priority conflict resolved: prioritize-auth

[Example 2] Feature Development & Handoff Workflow
--------------------------------------------------------------------------------
✓ Created 4 interdependent tasks
✓ Created 3 shared contexts
✓ HandOff message: Review implementation

[Example 3] Design Conflict Resolution Workflow
--------------------------------------------------------------------------------
✓ Conflict created: form-component-design-conflict
✓ Resolution: controlled-component

================================================================================
AUDIT TRAIL
================================================================================
Subject: form-component-decision
Total events: 15
Agents involved: Designer, Developer, CodeReviewer

================================================================================
✓ All workflows completed successfully!
================================================================================
```

## API Reference

### Message API

```python
from src.collaboration.protocol import Message, MessageType, MessagePriority

# Create message
msg = Message(
    from_agent="Agent1",
    to_agent="Agent2",
    msg_type=MessageType.TASK_REQUEST,
    subject="Task subject",
    data={"key": "value"},
    priority=MessagePriority.HIGH
)

# Validate message
validator = ProtocolValidator()
is_valid = validator.validate_message(msg)

# Check expiration
is_expired = msg.is_expired()

# Get response
response_msg = msg.create_response(
    from_agent="Agent2",
    response_text="Task completed"
)
```

### Dependency Tracking API

```python
from src.collaboration.dependency_tracker import DependencyTracker, TaskStatus

tracker = DependencyTracker()

# Add tasks
task1 = tracker.add_task("task1", "Task 1", "Agent1", priority=1)
task2 = tracker.add_task("task2", "Task 2", "Agent2", priority=2)

# Add dependency
tracker.add_dependency(task2, task1)

# Check ready state
if tracker.is_ready(task2):
    print("Task 2 is ready to start")

# Get blockers
blockers = tracker.get_blockers(task2)

# Mark completed
tracker.mark_completed(task1)

# Get ready tasks
ready = tracker.get_ready_tasks()
```

### Context Management API

```python
from src.collaboration.context_manager import (
    ContextManager, ContextType, AccessLevel
)

mgr = ContextManager()

# Create context
ctx = mgr.create_context(
    context_id="ctx1",
    context_type=ContextType.PROJECT,
    owner="Agent1",
    data={"key": "value"},
    access_level=AccessLevel.TEAM,
    ttl=3600  # 1 hour
)

# Share context
mgr.share_context("ctx1", ["Agent2", "Agent3"])

# Get context
ctx = mgr.get_context("ctx1", "Agent2")

# Update context
mgr.update_context("ctx1", "Agent1", {"new_key": "new_value"})

# Find contexts
contexts = mgr.find_contexts(
    "Agent1",
    context_type=ContextType.PROJECT,
    tags={"important"}
)

# Get related contexts
related = mgr.get_related_contexts("ctx1")
```

### Conflict Resolution API

```python
from src.collaboration.conflict_resolver import (
    ConflictResolver, ConflictType, ResolutionStrategy
)

resolver = ConflictResolver()

# Create conflict
conflict = resolver.create_conflict(
    conflict_id="conflict1",
    conflict_type=ConflictType.DECISION_CONFLICT,
    agents_involved=["Agent1", "Agent2", "Agent3"],
    topic="Decision topic",
    options=[...]
)

# Vote
conflict.vote("Agent1", "option1")
conflict.vote("Agent2", "option2")
conflict.vote("Agent3", "option1")

# Resolve with strategy
result = resolver.resolve(
    "conflict1",
    ResolutionStrategy.MAJORITY_VOTE
)

# Escalate if needed
resolver.escalate_conflict(
    "conflict1",
    "Unable to reach agreement"
)

# Get status
status = resolver.get_conflict_status("conflict1")
```

### Audit Logging API

```python
from src.collaboration.audit_logger import AuditLogger, AuditEventType

logger = AuditLogger()

# Log event
event = logger.log_event(
    event_type=AuditEventType.MESSAGE_SENT,
    agent="Agent1",
    subject="msg-123",
    action="Sent message"
)

# Specialized logging
logger.log_task_completed("Agent1", "task1", {"status": "done"})
logger.log_context_shared("Agent1", "ctx1", ["Agent2", "Agent3"])
logger.log_conflict_resolved("Agent1", "conflict1", "option1", "majority_vote")

# Query events
events = logger.get_events_for_subject("task1")
events = logger.get_events_by_agent("Agent1")
events = logger.get_events_by_type(AuditEventType.TASK_COMPLETED)

# Generate report
report = logger.generate_report("task1")

# Export
json_data = logger.export_events()
```

### Base Agent API

```python
from src.collaboration import BaseAgent, DeveloperAgent, AgentCapability

# Create agent
agent = DeveloperAgent("dev1")

# Register capability
agent.register_capability(AgentCapability.CODE_REVIEW)

# Send message
msg = agent.send_message(
    to_agent="designer1",
    msg_type=MessageType.REQUEST_FEEDBACK,
    subject="Design review",
    data={"component": "form"}
)

# Assign task
task = agent.assign_task("feat-001", "Implement feature")

# Check ready
is_ready = agent.check_ready("feat-001")

# Mark task progress
agent.mark_task_in_progress("feat-001")
agent.mark_task_completed("feat-001", {"pr": "#123"})

# Context operations
ctx = agent.create_context(
    context_id="impl-details",
    context_type=ContextType.TASK,
    data={"branch": "feature/form"},
    access_level=AccessLevel.TEAM
)
agent.share_context("impl-details", ["reviewer1"])
ctx = agent.get_context("impl-details")

# Conflict operations
agent.propose_resolution("conflict1", "opt1", "Better approach")
result = agent.resolve_conflict("conflict1", ResolutionStrategy.MAJORITY_VOTE)

# Get status
status = agent.get_status()
```

## Best Practices

### 1. Message Design
- Use specific message types (TASK_REQUEST, TASK_UPDATE, etc.)
- Include complete data in the message
- Set appropriate priority levels
- Use TTL for time-sensitive messages

### 2. Dependency Management
- Add dependencies before marking tasks ready
- Check for cycles before complex workflows
- Use ready-state checks before starting tasks
- Track blockers for debugging

### 3. Context Sharing
- Create contexts with appropriate access levels
- Share only necessary information
- Version contexts for audit trails
- Use TTL to prevent stale contexts

### 4. Conflict Resolution
- Define clear options with rationale
- Use appropriate resolution strategies
- Document escalation reasons
- Archive resolved conflicts

### 5. Auditing
- Log all significant events
- Generate reports for compliance
- Export audit trails for external systems
- Track interaction patterns

## Troubleshooting

### Message Queue Connection Issues
```python
# Check if Redis is running
$ redis-cli ping
# Should return: PONG

# Test connection
bus = MessageBus("redis", url="redis://localhost:6379")
bus.send_message(test_message)
```

### Dependency Cycle Detection
```python
from src.collaboration import DependencyTracker

tracker = DependencyTracker()
# If add_dependency fails with error, cycle would be created
try:
    tracker.add_dependency(task_a, task_b)
except ValueError as e:
    print(f"Cycle detected: {e}")
```

### Context Access Control
```python
# Verify access level
ctx = mgr.get_context("ctx1", "Agent1")
if ctx is None:
    print(f"Access denied or context not found")

# Check permissions
has_access = "Agent1" in ctx.access_permissions
```

## Performance Considerations

- **Message Queue**: Redis for high throughput, RabbitMQ for reliability
- **Context Storage**: In-memory for development, persistent storage for production
- **Audit Logging**: Cleanup old events periodically (default 10% when max reached)
- **Conflict Resolution**: Escalate unresolved conflicts automatically

## Future Enhancements

1. **Phase 5 (Current)**: Documentation and testing
2. **Learning System**: Agent feedback and improvement
3. **Dashboard**: Real-time monitoring and visualization
4. **Advanced Scheduling**: Task prioritization and resource allocation
5. **Integration**: With external systems and APIs

## Contributing

To extend the framework:

1. Create specialized agent types by subclassing `BaseAgent`
2. Add new conflict resolution strategies to `ConflictResolver`
3. Extend audit event types in `AuditLogger`
4. Implement new message types in `protocol.py`
5. Add tests in `tests/collaboration/`

## License

See LICENSE file in repository root.

---

**Framework Status**: Phase 5 - Production Ready
**Total Lines of Code**: ~4,000+
**Test Coverage**: 40+ Phase 2 tests, basic Phase 1 tests
**Last Updated**: 2024
