# Documentation

This directory contains project documentation.

## Structure

- `AGENTS.md` - Agent types and implementations
- `TOOLS.md` - Available tools and tool creation guide
- `WORKFLOWS.md` - Common workflow patterns
- `ARCHITECTURE.md` - System architecture
- `API.md` - API reference
- `DEPLOYMENT.md` - Deployment guide

## Quick Links

### For Users
- [Getting Started](#getting-started)
- [Creating Agents](AGENTS.md)
- [Using Tools](TOOLS.md)
- [Common Workflows](WORKFLOWS.md)

### For Developers
- [System Architecture](ARCHITECTURE.md)
- [API Reference](API.md)
- [Contributing Guidelines](CONTRIBUTING.md)

### For Operations
- [Deployment](DEPLOYMENT.md)
- [Configuration](../configs/README.md)
- [Monitoring](#monitoring)

## Getting Started

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Explore the framework**
   ```bash
   jupyter notebook notebooks/01_getting_started.ipynb
   ```

3. **Run example workflows**
   ```bash
   python src/collaboration/example_workflows.py
   ```

4. **Create your first agent**
   - See [Creating Agents](AGENTS.md)

## Architecture Overview

```
Agentic Project
├── src/collaboration/          - Core framework
│   ├── protocol.py             - Message protocol
│   ├── message_queue.py        - Message bus
│   ├── dependency_tracker.py   - Task coordination
│   ├── context_manager.py      - Context sharing
│   ├── conflict_resolver.py    - Conflict resolution
│   ├── audit_logger.py         - Event tracking
│   └── base_agent.py           - Agent base class
│
├── agents/                      - Agent implementations
│   ├── specialized_agents.py   - Custom agents
│   └── agent_registry.py       - Agent management
│
├── tools/                       - Tool definitions
│   ├── base_tool.py            - Tool interface
│   └── tool_registry.py        - Tool management
│
├── configs/                     - Configuration files
│   ├── agents.yaml             - Agent config
│   └── framework.yaml          - Framework config
│
├── notebooks/                   - Jupyter notebooks
│   └── *.ipynb                 - Exploration & examples
│
├── tests/                       - Unit & integration tests
│   └── collaboration/          - Framework tests
│
└── docs/                        - Documentation
    └── *.md                    - Various guides
```

## Key Features

- **Agent Communication**: Standardized messaging protocol
- **Task Coordination**: Dependency tracking with cycle detection
- **Context Management**: Shared state with access control
- **Conflict Resolution**: Multiple resolution strategies
- **Audit Logging**: Complete event tracking for compliance
- **Extensible Design**: Easy to add custom agents and tools

## Resources

- [Collaboration Framework Documentation](../src/collaboration/FRAMEWORK_DOCUMENTATION.md)
- [Example Workflows](../src/collaboration/example_workflows.py)
- [API Reference](../src/collaboration/README.md)

## Support

For issues, questions, or contributions:
1. Check the documentation
2. Review existing notebooks
3. Check framework README
4. Open an issue with details

## License

See LICENSE file in repository root.
