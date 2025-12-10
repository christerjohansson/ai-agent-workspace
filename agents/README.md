# Agents

This directory contains agent implementations for the agentic project.

## Structure

- `__init__.py` - Package initialization
- `specialized_agents.py` - Custom agent implementations
- `agent_registry.py` - Agent discovery and registration

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

## Integration with Collaboration Framework

All agents inherit from `BaseAgent` and automatically get:
- Message passing capabilities
- Task dependency management
- Context sharing and access control
- Conflict resolution participation
- Comprehensive audit logging

See `src/collaboration/FRAMEWORK_DOCUMENTATION.md` for complete API reference.
