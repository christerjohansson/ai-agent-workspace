# SSH & GitHub Authentication Setup Guide

## Overview
This guide explains how to securely configure SSH authentication for GitHub without storing passphrases in `.env` files.

## ⚠️ Security Warning
**Never store SSH passphrases in `.env` files or any version-controlled files.** Use SSH agent instead.

## Method 1: SSH Agent (Recommended for Local Development) ✅

### Windows Setup

#### Step 1: Verify OpenSSH is installed
```powershell
# Check if ssh is available
ssh -V

# If not installed, add OpenSSH via Settings
# Settings > Apps > Apps & features > Optional features > Add a feature
# Search for "OpenSSH Client" and install
```

#### Step 2: Start SSH Agent
```powershell
# Start the agent (run PowerShell as Administrator)
Start-Service ssh-agent

# Make it start automatically
Set-Service -Name ssh-agent -StartupType Automatic
```

#### Step 3: Add Your SSH Key
```powershell
# Add your SSH key to the agent
# It will prompt you for the passphrase once
ssh-add C:\Users\chris\.ssh\id_ed25519

# Verify key was added
ssh-add -L
```

#### Step 4: Test Connection
```powershell
# Test GitHub connection
ssh -T git@github.com

# Expected output:
# Hi christerjohansson! You've successfully authenticated...
```

### Mac/Linux Setup

```bash
# Start SSH agent
eval "$(ssh-agent -s)"

# Add your key
ssh-add ~/.ssh/id_ed25519

# Add to ~/.ssh/config for auto-loading (optional)
# Add these lines to ~/.ssh/config:
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  AddKeysToAgent yes
```

---

## Method 2: GitHub CLI (Recommended for Easy Setup)

### Installation

#### Windows (using Chocolatey)
```powershell
choco install gh
```

#### Windows (using Scoop)
```powershell
scoop install gh
```

#### Mac
```bash
brew install gh
```

#### Linux (Ubuntu/Debian)
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### Setup
```bash
# Authenticate with GitHub
gh auth login

# Choose:
# - GitHub.com
# - HTTPS or SSH
# - Authenticate with your browser

# Verify authentication
gh auth status
```

---

## Method 3: Personal Access Token (GitHub_TOKEN)

Already configured in your `.env` file (keep it secret, never commit):
```
GITHUB_TOKEN=your_personal_access_token_here
```

### Creating a New Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Set expiration (90 days recommended)
4. Select scopes:
   - ✅ repo (full)
   - ✅ gist
   - ✅ read:user
   - ✅ workflow
5. Click "Generate token"
6. Copy token to `.env` as `GITHUB_TOKEN=`

### Using Token with Git
```bash
# Clone using token
git clone https://github.com/christerjohansson/ai-agent-workspace.git

# When prompted for password, use the token
# Username: your-username
# Password: your-personal-access-token
```

---

## Method 4: GitHub Desktop

Download: https://desktop.github.com/

Benefits:
- Handles authentication automatically
- GUI for Git operations
- No terminal required

---

## For GitHub Actions (CI/CD)

### Recommended Approach: Deploy Keys

Create a deploy key for your repository:
```bash
# Generate a key for CI/CD
ssh-keygen -t ed25519 -f deploy_key -N ""

# Add public key to repo settings
# Settings > Deploy keys > Add deploy key
cat deploy_key.pub

# Add private key as GitHub secret
# Settings > Secrets and variables > Actions > New repository secret
# Name: SSH_DEPLOY_KEY
# Value: contents of deploy_key
```

### Use in Workflow
```yaml
- name: Checkout code
  uses: actions/checkout@v3
  with:
    ssh-key: ${{ secrets.SSH_DEPLOY_KEY }}
```

---

## Troubleshooting

### Git still asking for password
```bash
# Change remote from HTTPS to SSH
git remote set-url origin git@github.com:christerjohansson/ai-agent-workspace.git

# Verify
git remote -v
```

### SSH agent not working
```bash
# Check if agent is running
ssh-add -L

# If it says "Connection refused":
# Restart the agent (Windows)
Stop-Service ssh-agent
Start-Service ssh-agent

# Linux/Mac
ssh-agent -k
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Permission denied (publickey)
```bash
# Debug SSH connection
ssh -vvv git@github.com

# Ensure your public key is added to GitHub
# https://github.com/settings/keys

# Verify key permissions (Linux/Mac)
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

### Wrong key being used
```bash
# Check which keys are loaded
ssh-add -L

# Remove all keys
ssh-add -D

# Add specific key
ssh-add C:\Users\chris\.ssh\id_ed25519
```

---

## Best Practices Summary

| Method | Best For | Security | Ease |
|--------|----------|----------|------|
| SSH Agent | Local development | ✅✅✅ | ✅✅✅ |
| GitHub CLI | New users | ✅✅✅ | ✅✅✅ |
| Personal Token | REST API, alternatives | ✅✅ | ✅✅ |
| GitHub Desktop | GUI users | ✅✅✅ | ✅✅✅✅ |
| Deploy Keys | CI/CD pipelines | ✅✅✅ | ✅✅ |

---

## Next Steps

1. **Choose your authentication method** (SSH Agent recommended)
2. **Follow the setup steps** for your platform
3. **Test the connection**: `ssh -T git@github.com`
4. **Update remote if needed**: `git remote set-url origin git@github.com:christerjohansson/ai-agent-workspace.git`
5. **Start using Git** without password prompts!

---

**Last Updated**: December 10, 2025
