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

## Using This Workspace for Web Projects (Backend + Frontend)

### Quick Setup for New Web Projects

This workspace is designed to coordinate multi-agent development for full-stack web applications. Here's how to use it:

#### Step 1: Set Up Project Structure

```powershell
# Initialize your web project
mkdir my-web-app
cd my-web-app

# Create backend and frontend directories
mkdir backend frontend

# Initialize backend (Python example)
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy pytest

# Initialize frontend (Next.js per AGENT_INSTRUCTIONS)
cd ../frontend
npx create-next-app@latest . --typescript --tailwind --app
npx shadcn-ui@latest init
```

#### Step 2: Integrate the Agentic Framework

```powershell
# From your web project root, copy the framework
Copy-Item -Path "C:\projects\agentic-workspace\src" -Destination ".\src" -Recurse
Copy-Item -Path "C:\projects\agentic-workspace\agents" -Destination ".\agents" -Recurse
```

#### Step 3: Assign Agent Roles to Your Team

| Role | Responsibility | Reference |
|------|-----------------|-----------|
| **Product Owner** | Define features, requirements | `agents/AGENT_PRODUCT_OWNER.md` |
| **Frontend Developer** | React/Next.js implementation | `agents/AGENT_INSTRUCTIONS.md` |
| **Backend Developer** | API & database implementation | `agents/AGENT_INSTRUCTIONS.md` |
| **Designer** | UI/UX, component design | `agents/AGENT_DESIGN.md` |
| **Code Reviewer** | Quality assurance | `agents/AGENT_CODE_REVIEW.md` |
| **DevOps Engineer** | Deployment & infrastructure | `agents/AGENT_DEVOPS.md` |
| **Project Leader** | Timeline & coordination | `agents/AGENT_PROJECT_LEADER.md` |

#### Step 4: Multi-Agent Feature Development Workflow

**Example: Building a User Dashboard Feature**

```python
from src.collaboration.base_agent import DeveloperAgent, DesignerAgent
from src.collaboration.message_queue import MessageBus
from src.collaboration.dependency_tracker import DependencyTracker

# Initialize agents
product_owner = Agent("PO_Alice", role="ProductOwner")
designer = DesignerAgent("Designer_Bob")
frontend_dev = DeveloperAgent("Dev_Carol")
backend_dev = DeveloperAgent("Dev_David")
code_reviewer = Agent("Reviewer_Eve", role="CodeReviewer")
devops = Agent("DevOps_Frank", role="DevOps")

# Step 1: Product Owner defines requirements
product_owner.send_message(
    to_agent="Designer_Bob",
    msg_type=MessageType.TASK_REQUEST,
    subject="Design user dashboard",
    data={"priority": "high"}
)

# Step 2: Designer creates and shares design specs
design_context = designer.create_context(
    context_id="dashboard-design",
    context_type=ContextType.DESIGN,
    data={"components": ["UserCard", "StatsPanel", "Charts"]}
)
designer.share_context("dashboard-design", ["Dev_Carol", "Dev_David"])

# Step 3: Frontend Dev implements UI (parallel with backend)
frontend_task = frontend_dev.assign_task(
    "implement-dashboard-ui",
    "Create dashboard components"
)
frontend_dev.create_context(
    context_id="frontend-impl",
    context_type=ContextType.TASK,
    data={"branch": "feature/dashboard-ui"}
)

# Step 4: Backend Dev implements API (parallel)
backend_task = backend_dev.assign_task(
    "implement-dashboard-api",
    "Create API endpoints"
)
backend_dev.create_context(
    context_id="backend-impl",
    context_type=ContextType.TASK,
    data={"endpoints": ["/api/users", "/api/stats"]}
)

# Step 5: Code Reviewer validates quality
code_reviewer.propose_resolution(
    conflict_id="implementation-approval",
    resolution="approved",
    rationale="Code meets standards"
)

# Step 6: DevOps deploys to staging/production
devops.send_message(
    to_agent="PO_Alice",
    msg_type=MessageType.TASK_COMPLETE,
    subject="Dashboard deployed to staging"
)
```

#### Step 5: Configuration for Your Project

**Create `configs/project-config.yaml`:**

```yaml
project:
  name: "My Web App"
  backend:
    language: python
    framework: fastapi
    port: 8000
  frontend:
    framework: nextjs
    typescript: true
    port: 3000
    styling: tailwind
    ui_library: shadcn/ui

agents:
  message_queue:
    backend: redis
    url: "redis://localhost:6379"
  audit:
    enabled: true
    storage: "postgresql"

team:
  roles:
    - product_owner
    - frontend_developer
    - backend_developer
    - designer
    - code_reviewer
    - devops_engineer
```

#### Step 6: Key Framework Features for Web Projects

**1. Message-Based Coordination** (for async team work)
```python
# Frontend sends API requirements to Backend
msg = Message(
    from_agent="FrontendDev",
    to_agent="BackendDev",
    type=MessageType.TASK_REQUEST,
    data={"endpoint": "/api/users", "method": "GET"}
)
message_bus.publish(msg)
```

**2. Dependency Tracking** (for sprint planning)
```python
tracker = DependencyTracker()
tracker.add_task("design_dashboard", "UI Design")
tracker.add_task("implement_frontend", "Frontend Dev",
    dependencies=["design_dashboard"])
tracker.add_task("implement_backend", "Backend Dev",
    dependencies=["design_dashboard"])

ready_tasks = tracker.get_ready_tasks()  # Parallel execution ready
```

**3. Conflict Resolution** (for design disagreements)
```python
# When Designer disagrees with Frontend Dev on component approach
conflict = resolver.create_conflict(
    type=ConflictType.DESIGN_CONFLICT,
    agents_involved=["Designer", "FrontendDev"],
    topic="Component architecture",
    options=[
        ConflictOption("opt1", "Monolithic component"),
        ConflictOption("opt2", "Micro-components")
    ]
)
# Resolve via team voting
result = resolver.resolve(conflict.id, ResolutionStrategy.MAJORITY_VOTE)
```

**4. Audit Trail** (for compliance & debugging)
```python
audit = AuditLogger()
# Track all development activities
audit.log_task_completed("FrontendDev", "implement-dashboard-ui",
    {"time": "2h30m", "pr": "#123"})

# Generate team activity reports
report = audit.generate_report("dashboard-feature")
```

#### Step 7: Development Workflow

```powershell
# Start developing with agentic profile
code . --profile Agentic

# Create feature branch
git checkout -b feature/user-dashboard

# Coordinate work using framework:
# - Designer creates specs
# - Frontend & Backend Devs work in parallel
# - Code Reviewer validates implementation
# - DevOps prepares deployment
# (All coordinated through messages & dependencies)

# Merge when team consensus reached
git merge --no-ff feature/user-dashboard
```

#### Step 8: Testing & Quality

```powershell
# Run backend tests
cd backend
pytest tests/ -v

# Run frontend tests
cd ../frontend
npm test

# Run framework tests (coordination, messaging, etc.)
pytest ../tests/collaboration/ -v

# View audit trail of team activities
python -c "from src.collaboration.audit_logger import AuditLogger; 
a = AuditLogger(); 
print(a.get_timeline())"
```

### Why This Workspace Excels for Web Projects

✅ **Multi-role coordination** - Product Owner, Designers, Frontend/Backend Devs work in sync  
✅ **Async collaboration** - Message queue for distributed/remote teams  
✅ **Dependency tracking** - Sprint planning with automatic ready-state validation  
✅ **Parallel execution** - Frontend and Backend can work simultaneously  
✅ **Conflict resolution** - Handle design/implementation disagreements systematically  
✅ **Audit trail** - Complete history of all decisions and work  
✅ **AI-powered** - GitHub Copilot Chat for code generation and problem-solving  
✅ **Next.js ready** - Pre-configured frontend stack (TypeScript, Tailwind, shadcn/ui)  
✅ **DevOps included** - Deployment & infrastructure as code support  
✅ **Extensible** - Add custom agents and tools for your specific needs  

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
