# Multi-Agent Collaboration Framework

## Overview

This module provides a comprehensive framework for AI agents to collaborate, communicate, and coordinate on complex projects. It enables agents with different roles to work together efficiently while tracking interactions and dependencies.

## Architecture

### Components

1. **Agent Communication Protocol** - Message format and types for inter-agent communication
2. **Message Queue Service** - Redis/RabbitMQ integration for reliable message passing
3. **Context Sharing** - Mechanism for agents to share context and state
4. **Dependency Tracker** - Tracks task dependencies and coordination
5. **Conflict Resolver** - Handles conflicts in agent decisions
6. **Audit Logger** - Records all inter-agent interactions

## Module Structure

```
src/
├── collaboration/
│   ├── __init__.py
│   ├── protocol.py              # Agent communication protocol
│   ├── message_queue.py         # Message queue service
│   ├── context_manager.py       # Context sharing and state
│   ├── dependency_tracker.py    # Dependency management
│   ├── conflict_resolver.py     # Conflict resolution
│   └── audit_logger.py          # Audit trail
├── agents/
│   ├── base_agent.py            # Base agent class with collaboration
│   └── agent_registry.py        # Agent discovery and registration
└── examples/
    └── multi_agent_workflow.py  # Example workflows
```

## Quick Start

```python
from src.collaboration import Agent, MessageBus, ContextManager

# Initialize collaboration system
message_bus = MessageBus(redis_url="redis://localhost:6379")
context_mgr = ContextManager()

# Create agents
pm = Agent(name="ProjectManager", role="project_leader", message_bus=message_bus)
po = Agent(name="ProductOwner", role="product_owner", message_bus=message_bus)

# Agents can now communicate and coordinate
pm.send_message(to=po, subject="roadmap_review", data={...})
```

## Key Features

- **Message-Driven Communication** - Async message passing between agents
- **Context Propagation** - Seamless sharing of context across agents
- **Dependency Management** - Track and validate task dependencies
- **Conflict Resolution** - Automated conflict handling strategies
- **Audit Trail** - Complete record of all agent interactions
- **Error Handling** - Robust error recovery and fallback mechanisms

## Usage Examples

### Example 1: Simple Communication

```python
# Project Leader sends update to Product Owner
pm.send_message(
    to=po,
    subject="sprint_update",
    priority="high",
    data={
        "sprint": "Sprint 25",
        "status": "on_track",
        "velocity": 28
    }
)

# Product Owner receives and processes
po.receive_message()
```

### Example 2: Dependency Coordination

```python
# Define task dependencies
code_review = Task("code_review", assigned_to="CodeReviewer")
deployment = Task("deployment", assigned_to="DevOps", depends_on=[code_review])

# Tracker ensures proper sequencing
tracker.add_dependency(code_review, deployment)
tracker.validate_ready(deployment)  # False until code_review completes
```

### Example 3: Conflict Resolution

```python
# When agents disagree on a decision
conflict = Conflict(
    agent_a=designer,
    agent_b=developer,
    topic="component_design",
    options={"option_a": {...}, "option_b": {...}}
)

# Resolver suggests resolution
resolution = conflict_resolver.resolve(conflict)
```

## Configuration

### Environment Variables

```env
# Message Queue
MESSAGE_QUEUE_TYPE=redis  # redis or rabbitmq
REDIS_URL=redis://localhost:6379
RABBITMQ_URL=amqp://user:pass@localhost/

# Logging
AUDIT_LOG_LEVEL=INFO
AUDIT_LOG_FILE=logs/agent_interactions.log

# Collaboration
CONTEXT_PERSISTENCE=true
DEPENDENCY_VALIDATION=true
CONFLICT_AUTO_RESOLVE=true
```

### Configuration File

```yaml
collaboration:
  message_queue:
    type: redis
    host: localhost
    port: 6379
    db: 0
  
  context:
    persistence: true
    ttl: 86400  # 24 hours
    max_size: 10MB
  
  dependencies:
    validation: true
    timeout: 3600  # 1 hour
  
  conflict_resolution:
    enabled: true
    strategies:
      - majority_vote
      - priority_based
      - escalate_to_human
```

## Installation

```bash
# Clone the repository
git clone git@github.com:christerjohansson/ai-agent-workspace.git
cd ai-agent-workspace

# Install dependencies
pip install -r requirements.txt

# Install optional message queue backends
pip install redis  # For Redis
pip install pika   # For RabbitMQ

# Run tests
pytest tests/collaboration/
```

## Testing

```bash
# Run all collaboration tests
pytest tests/collaboration/ -v

# Run specific test
pytest tests/collaboration/test_protocol.py -v

# Run with coverage
pytest tests/collaboration/ --cov=src/collaboration --cov-report=html
```

## API Reference

### Agent Class

```python
class Agent:
    def __init__(self, name: str, role: str, message_bus: MessageBus)
    def send_message(self, to: Agent, subject: str, data: dict) -> Message
    def receive_message(self, timeout: int = None) -> Message
    def broadcast(self, subject: str, data: dict) -> List[Message]
    def get_context(self) -> Context
    def share_context(self, agents: List[Agent]) -> None
```

### MessageBus Class

```python
class MessageBus:
    def __init__(self, backend: str = "redis", **config)
    def publish(self, message: Message) -> str
    def subscribe(self, agent: Agent, subject: str) -> None
    def unsubscribe(self, agent: Agent, subject: str) -> None
    def get_messages(self, agent: Agent, limit: int = 10) -> List[Message]
```

### DependencyTracker Class

```python
class DependencyTracker:
    def add_dependency(self, task: Task, depends_on: Task) -> None
    def remove_dependency(self, task: Task, depends_on: Task) -> None
    def validate_ready(self, task: Task) -> bool
    def get_blockers(self, task: Task) -> List[Task]
    def on_task_complete(self, task: Task) -> None
```

## Best Practices

1. **Message Design**: Keep messages focused and include all needed context
2. **Error Handling**: Always handle message failures gracefully
3. **Dependency Management**: Validate dependencies before task execution
4. **Audit Logging**: Ensure all critical interactions are logged
5. **Context Sharing**: Be explicit about what context is shared
6. **Timeout Management**: Set appropriate timeouts for message waiting
7. **Scalability**: Use message batching for high-volume communication

## Troubleshooting

### Messages Not Being Delivered

1. Check message queue is running
2. Verify agent subscriptions
3. Review audit logs for errors
4. Check network connectivity

### Dependency Deadlock

1. Review dependency graph
2. Identify circular dependencies
3. Resolve conflicts manually if needed
4. Update dependency configuration

### High Latency

1. Check message queue performance
2. Monitor network latency
3. Review context size
4. Consider message batching

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Related Issues

- #1 - Multi-Agent Collaboration and Communication Framework
- #3 - Agent Orchestration Dashboard
- #2 - Agent Learning and Feedback System

## Resources

- [Redis Documentation](https://redis.io/documentation)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Event-Driven Architecture](https://en.wikipedia.org/wiki/Event-driven_architecture)
- [Microservices Communication Patterns](https://microservices.io/patterns/communication-style/index.html)

---

**Last Updated**: December 10, 2025
