#!/bin/bash
# ============================================
# AI NEXUS - AUTOMATED SETUP SCRIPT
# Complete environment setup and configuration
# ============================================

set -e

echo "=============================================="
echo "  AI NEXUS - AUTOMATED SETUP"
echo "=============================================="
echo ""

# Get user inputs
read -p "GitHub Username: " GITHUB_USER
read -p "Repository Name (default: ai-nexus): " REPO_NAME
REPO_NAME=${REPO_NAME:-ai-nexus}

echo ""
echo "Creating private GitHub repository: $GITHUB_USER/$REPO_NAME"
echo ""

# Create GitHub repo using API
curl -s -X POST "https://api.github.com/user/repos" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"$REPO_NAME\", \"private\": true, \"auto_init\": false}" | jq -r '.html_url // empty'

# Push to GitHub
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git" 2>/dev/null || \
git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"

echo ""
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "=============================================="
echo "  Repository created and code pushed!"
echo "=============================================="
