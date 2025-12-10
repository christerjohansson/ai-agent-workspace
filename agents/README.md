# Agents

This directory contains agent implementations and role-specific instructions for the agentic project.

## Structure

- `__init__.py` - Package initialization
- `specialized_agents.py` - Custom agent implementations
- `agent_registry.py` - Agent discovery and registration
- `AGENT_INSTRUCTIONS.md` - NextJS development setup guide
- `AGENT_CODE_REVIEW.md` - Code review guidelines and practices
- `AGENT_DESIGN.md` - UX/UI design patterns and principles
- `AGENT_DEVOPS.md` - DevOps and infrastructure management
- `AGENT_PRODUCT_OWNER.md` - Product strategy and roadmapping
- `AGENT_PROJECT_LEADER.md` - Project coordination and team leadership

## Usage

### Creating a Custom Agent

```python
from src.collaboration import BaseAgent, AgentCapability, MessageType

class CustomAgent(BaseAgent):
    """Example custom agent."""
    
    def __init__(self, name: str):
        super().__init__(name, "CustomAgent")
        self.register_capability(AgentCapability.TASK_MANAGEMENT)
    
    def get_capabilities(self):
        return self.metadata.capabilities
    
    def handle_task_request(self, message):
        # Handle task requests
        pass
```

### Registering Agents

```python
from agents import agent_registry

registry = agent_registry.AgentRegistry()
registry.register(CustomAgent("agent1"))
registry.register(CustomAgent("agent2"))

agents = registry.get_all()
```

## Agent Role Instructions

The following agent role guides are available:

- **AGENT_INSTRUCTIONS.md** - Core development setup and NextJS configuration
- **AGENT_CODE_REVIEW.md** - Code review standards and practices
- **AGENT_DESIGN.md** - Design patterns, UX/UI principles, and component design
- **AGENT_DEVOPS.md** - Infrastructure, deployment, and operations
- **AGENT_PRODUCT_OWNER.md** - Product strategy, roadmapping, and feature prioritization
- **AGENT_PROJECT_LEADER.md** - Team coordination, timelines, and project management

Each guide provides:
- Role-specific responsibilities
- Best practices and standards
- Workflow integration points
- Collaboration guidelines

## Integration with Collaboration Framework

All agents inherit from `BaseAgent` and automatically get:
- Message passing capabilities
- Task dependency management
- Context sharing and access control
- Conflict resolution participation
- Comprehensive audit logging

See `src/collaboration/FRAMEWORK_DOCUMENTATION.md` for complete API reference.
