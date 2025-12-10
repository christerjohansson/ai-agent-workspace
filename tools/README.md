# Tools

This directory contains tool definitions and utility functions for agents.

## Structure

- `__init__.py` - Package initialization
- `base_tool.py` - Base tool interface
- `tool_registry.py` - Tool discovery and registration
- `utilities.py` - Common utility functions
- `integrations.py` - External service integrations

## Tool Interface

```python
from tools.base_tool import BaseTool

class CustomTool(BaseTool):
    """Custom tool implementation."""
    
    name = "custom_tool"
    description = "What this tool does"
    input_schema = {
        "type": "object",
        "properties": {
            "param1": {"type": "string"}
        }
    }
    
    def execute(self, **kwargs):
        """Execute the tool."""
        # Implement tool logic
        return {"result": "output"}
```

## Registering Tools

```python
from tools import tool_registry

registry = tool_registry.ToolRegistry()
registry.register(CustomTool())

tool = registry.get("custom_tool")
result = tool.execute(param1="value")
```

## Available Tools

Tools can be created for:
- File operations
- API calls
- Data processing
- Code generation
- System commands
- And more...
