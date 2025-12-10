# Configurations

This directory contains configuration files for the agentic project.

## Structure

- `agents.yaml` - Agent definitions and settings
- `tools.yaml` - Tool configurations
- `framework.yaml` - Collaboration framework settings
- `logging.yaml` - Logging configuration
- `environment.yaml` - Environment-specific settings

## Configuration Formats

### agents.yaml

```yaml
agents:
  - name: developer1
    type: Developer
    capabilities:
      - task_management
      - code_review
    settings:
      max_concurrent_tasks: 5
      timeout: 300
  
  - name: designer1
    type: Designer
    capabilities:
      - design
      - conflict_resolution
```

### framework.yaml

```yaml
message_queue:
  backend: redis
  url: redis://localhost:6379

context_manager:
  persistence_enabled: true
  max_contexts: 1000

conflict_resolver:
  default_strategy: majority_vote
  escalation_timeout: 600
```

## Loading Configuration

```python
from configs import config_loader

config = config_loader.load_config("agents.yaml")
agents = config_loader.get_agents_config()
```

## Environment-Specific Configuration

```python
import os
from configs import config_loader

env = os.getenv("AGENTIC_ENV", "development")
config = config_loader.load_config(f"environment-{env}.yaml")
```
