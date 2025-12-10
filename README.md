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
4. Start building agentic applications!

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

## Tips for Agentic Development

- Use GitHub Copilot Chat for interactive problem-solving
- Leverage Remote Containers for isolated development environments
- Use REST Client for testing API calls during agent development
- Enable Python type checking for better code quality
- Use GitLens for tracking code evolution

## Theme Customization

Your current settings preserve your preferred "Winter is Coming (Dark Black)" theme.
To customize further, adjust settings in `.vscode/settings.json`
