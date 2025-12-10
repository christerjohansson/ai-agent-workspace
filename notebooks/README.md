# Notebooks

This directory contains Jupyter notebooks for exploration, experimentation, and analysis.

## Structure

- `01_getting_started.ipynb` - Introduction to the framework
- `02_agent_communication.ipynb` - Message passing examples
- `03_task_coordination.ipynb` - Dependency management
- `04_context_sharing.ipynb` - Context and access control
- `05_conflict_resolution.ipynb` - Resolution strategies
- `06_audit_trails.ipynb` - Event tracking and analysis

## Running Notebooks

```bash
jupyter notebook
```

## Common Notebook Patterns

### Import Framework

```python
from src.collaboration import (
    BaseAgent, DeveloperAgent, DesignerAgent,
    MessageType, ContextType, AccessLevel,
    ResolutionStrategy
)
```

### Create Agents

```python
dev = DeveloperAgent("dev1")
designer = DesignerAgent("designer1")
```

### Send Messages

```python
dev.send_message(
    to_agent="designer1",
    msg_type=MessageType.TASK_REQUEST,
    subject="Design needed",
    data={"component": "form"}
)
```

### Analyze Results

```python
# Query audit logs
report = dev.audit_logger.generate_report("task1")
print(report)

# Export for analysis
events_json = dev.audit_logger.export_events()
```

## Using Notebooks for Development

Notebooks are great for:
- Learning the framework
- Prototyping new agents
- Testing workflow scenarios
- Analyzing agent interactions
- Debugging issues
- Creating documentation
