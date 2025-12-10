# AI Agentic Workspace

This is a dedicated VS Code workspace configured for AI agentic development and experimentation.

## Workspace Profile Features

- **Color Theme**: Winter is Coming (Dark Black)
- **Icon Theme**: VSCode Icons
- **Language Support**: Python, TypeScript, JavaScript, Rust, C++
- **AI Tools**: GitHub Copilot, Copilot Chat, Sourcegraph Cody
- **Development Tools**: Remote containers, SSH, WSL support
- **Version Control**: GitLens for enhanced Git integration
- **Database Tools**: MSSQL, REST Client

## Recommended Extensions

### AI & Code Generation
- **GitHub Copilot** - AI-powered code completion
- **GitHub Copilot Chat** - Conversational AI in editor
- **Sourcegraph Cody** - AI code search and generation

### Python Development
- **Python** - Core Python support
- **Pylance** - Type checking and IntelliSense
- **Ruff** - Fast Python linter and formatter

### Code Quality
- **Prettier** - Code formatter
- **ESLint** - JavaScript linting
- **GitLens** - Enhanced Git history and blame

### Remote Development
- **Remote - Containers** - Develop in Docker containers
- **Remote - SSH** - Connect to remote machines
- **Remote - WSL** - Use Windows Subsystem for Linux

### Utilities
- **REST Client** - Test HTTP endpoints
- **Docker** - Docker container management
- **PowerShell** - PowerShell language support
- **YAML** - YAML file support
- **Live Server** - Local development server

## Getting Started

1. Open this workspace with: `code agentic-workspace.code-workspace`
2. Install recommended extensions when prompted
3. Configure your AI tools (Copilot, API keys, etc.)
4. Explore the project structure: `cat PROJECT_STRUCTURE.md`
5. Start building agentic applications!

## Quick Navigation

**Framework & Examples:**
- 📚 [Framework Documentation](src/collaboration/FRAMEWORK_DOCUMENTATION.md) - Complete API reference
- 🔄 [Example Workflows](src/collaboration/example_workflows.py) - Real-world scenarios
- ✅ [Completion Summary](ISSUE_1_COMPLETION_SUMMARY.md) - Phase status

**Agent Roles & Instructions:**
- 👨‍💻 [Development Setup](agents/AGENT_INSTRUCTIONS.md)
- 🔍 [Code Review](agents/AGENT_CODE_REVIEW.md)
- 🎨 [Design Patterns](agents/AGENT_DESIGN.md)
- 🚀 [DevOps & Deployment](agents/AGENT_DEVOPS.md)
- 📊 [Product Strategy](agents/AGENT_PRODUCT_OWNER.md)
- 👥 [Team Coordination](agents/AGENT_PROJECT_LEADER.md)

**Setup & Configuration:**
- 🔐 [SSH GitHub Authentication](docs/SSH_GITHUB_AUTH_SETUP.md)
- 📋 [Configuration Guide](configs/README.md)

## Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for comprehensive directory overview.

**Key Directories:**
- `src/collaboration/` - Core framework (4,000+ LOC, production-ready)
- `agents/` - Agent implementations and role instructions
- `tools/` - Tool definitions and utilities
- `configs/` - Configuration management
- `notebooks/` - Jupyter notebooks for exploration
- `docs/` - Documentation and guides
- `tests/` - Unit and integration tests

## VS Code Profiles

To use this as a dedicated profile:

1. Open VS Code
2. Click the profile icon (bottom-left)
3. Select "Create Profile"
4. Name it "Agentic"
5. Choose to copy settings from this workspace
6. Switch to the profile anytime using the profile dropdown

## Environment Setup

### Python Projects
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Node.js Projects
```bash
npm install
npm run dev
```

## Projects & Frameworks

### Multi-Agent Collaboration Framework (Issue #1) ✅
A complete framework for building collaborative AI agents with:
- Standardized message protocol for agent communication
- Task dependency tracking with cycle detection
- Shared context management with fine-grained access control
- Multi-strategy conflict resolution system
- Comprehensive audit logging and compliance tracking
- Base agent implementation with 5 specialized agent types

**Location**: `src/collaboration/`
**Status**: Production Ready (~4,000 LOC, 5 phases complete)
**Documentation**: `src/collaboration/FRAMEWORK_DOCUMENTATION.md`

See [Collaboration Framework Overview](#collaboration-framework-overview) below.

## Collaboration Framework Overview

### Framework Components

1. **Phase 1: Core Communication**
   - Message protocol with validation
   - Message queue abstraction (Redis/RabbitMQ)
   - Dependency tracking with cycle detection
   - ✅ Complete with tests

2. **Phase 2: Advanced Features**
   - Context management with versioning
   - Conflict resolution (6+ strategies)
   - Audit logging and reporting
   - ✅ Complete with 40+ tests

3. **Phase 3: Example Workflows**
   - Roadmap planning workflow
   - Feature development workflow
   - Design conflict resolution workflow
   - ✅ Complete and runnable

4. **Phase 4: Base Agent**
   - Unified agent interface
   - Agent state management
   - Integrated framework access
   - 5 specialized agent types
   - ✅ Complete

5. **Phase 5: Documentation**
   - Architecture and API reference
   - Testing guide
   - Best practices
   - Troubleshooting
   - ✅ Complete

### Quick Start

```python
from src.collaboration import DeveloperAgent, DesignerAgent, MessageType

# Create agents
dev = DeveloperAgent("dev1")
designer = DesignerAgent("designer1")

# Send message
dev.send_message(
    to_agent="designer1",
    msg_type=MessageType.TASK_REQUEST,
    subject="Need UI design",
    data={"component": "form-input"}
)

# Create task with dependencies
task = dev.assign_task("feat-001", "Implement feature")

# Share context
context = dev.create_context(
    context_id="impl-details",
    context_type=ContextType.TASK,
    data={"branch": "feature/form-input"}
)
dev.share_context("impl-details", ["designer1"])
```

### Testing

```bash
# Run all tests
pytest tests/collaboration/ -v

# Run example workflows
python src/collaboration/example_workflows.py
```

### Documentation

Complete documentation available in:
- `src/collaboration/FRAMEWORK_DOCUMENTATION.md` - Full reference
- `src/collaboration/README.md` - Framework overview
- `src/collaboration/example_workflows.py` - Working examples

## Tips for Agentic Development

- Use GitHub Copilot Chat for interactive problem-solving
- Leverage Remote Containers for isolated development environments
- Check out the collaboration framework for multi-agent patterns
- Review example workflows for real-world usage patterns
- Use REST Client for testing API calls during agent development
- Enable Python type checking for better code quality
- Use GitLens for tracking code evolution

## Theme Customization

Your current settings preserve your preferred "Winter is Coming (Dark Black)" theme.
To customize further, adjust settings in `.vscode/settings.json`
