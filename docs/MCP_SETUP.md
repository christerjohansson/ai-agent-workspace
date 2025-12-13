# MCP Configuration Setup Guide

## Quick Setup

1. **Copy example files**:
   ```powershell
   Copy-Item .mcp-config.example.json .mcp-config.json
   Copy-Item .env.example .env
   ```

2. **Edit with your credentials**:
   ```powershell
   # Edit .mcp-config.json with your actual settings
   code .mcp-config.json
   
   # Edit .env with your tokens and passwords
   code .env
   ```

3. **Add to .gitignore** (already configured):
   ```
   .mcp-config.json
   .env
   .env.local
   ```

## Configuration Files

### .mcp-config.example.json
- Shareable MCP configuration template
- Shows all available settings without secrets
- Contains placeholders like `${GITHUB_TOKEN}` that reference environment variables
- Safe to commit to repository

### .env.example
- Environment variables template for all MCP services
- Placeholder values for tokens and passwords
- Organized by service section
- Safe to commit to repository

### .mcp-config.json (DO NOT COMMIT)
- Your actual MCP configuration file
- Created locally from .mcp-config.example.json
- Contains references to environment variables
- Should be in .gitignore

### .env (DO NOT COMMIT)
- Your actual environment variables
- Contains real tokens and passwords
- Should be in .gitignore
- Never share with team

## For New Team Members

1. **Clone the repository**
2. **Copy example files**:
   ```powershell
   Copy-Item .mcp-config.example.json .mcp-config.json
   Copy-Item .env.example .env
   ```
3. **Ask team lead for shared secrets** or generate your own:
   - GitHub Personal Access Token: https://github.com/settings/tokens
   - PostgreSQL credentials: from team database admin
   - Redis credentials: from infrastructure team
4. **Update .env with your credentials**
5. **Verify setup**: Run validation commands

## Validation

Test your MCP configuration:

```powershell
# Test GitHub connection
python -c "from src.collaboration import MessageBus; print('GitHub MCP: OK')"

# Test PostgreSQL connection (if enabled)
psql -h $env:DB_HOST -U $env:DB_USER -d $env:DB_NAME -c 'SELECT version();'

# Verify configuration loaded
python -c "import json; f=open('.mcp-config.json'); c=json.load(f); print(f'Enabled servers: {[k for k,v in c[\"mcp_servers\"].items() if v.get(\"enabled\")]}')"
```

## Troubleshooting

### "GITHUB_TOKEN not found"
- Verify `GITHUB_TOKEN` is set in `.env`
- Check `.mcp-config.json` references `${GITHUB_TOKEN}`
- Restart your terminal/IDE

### PostgreSQL connection fails
- Verify `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` in `.env`
- Check PostgreSQL server is running
- Verify credentials have database access

### MCP servers not loading
- Check `.mcp-config.json` syntax (valid JSON)
- Verify all required environment variables are set
- Check logs: `tail logs/mcp.log`

## Security Best Practices

✅ **DO:**
- Use `.mcp-config.example.json` as template
- Store secrets in `.env` file
- Add `.mcp-config.json` and `.env` to `.gitignore`
- Rotate tokens regularly
- Use environment-specific configurations

❌ **DON'T:**
- Commit `.mcp-config.json` with real secrets
- Commit `.env` with passwords
- Share real `.env` files
- Store tokens in code comments
- Use same token for multiple environments
