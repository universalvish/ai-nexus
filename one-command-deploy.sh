#!/bin/bash
# ============================================
# AI NEXUS - ONE COMMAND DEPLOY
# ============================================
# Copy/paste this entire script to run
# ============================================

echo "=============================================="
echo "  AI NEXUS - DEPLOYING TO GITHUB"
echo "=============================================="
echo ""

# Check if token is available
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN not set"
    echo ""
    echo "Please run these commands first:"
    echo ""
    echo "1. Create GitHub Personal Access Token:"
    echo "   https://github.com/settings/tokens/new"
    echo "   Scopes: repo, admin:org"
    echo ""
    echo "2. Export the token:"
    echo "   export GITHUB_TOKEN='your_token_here'"
    echo ""
    echo "3. Run this script again"
    exit 1
fi

# Create repo
echo "Creating GitHub repository..."
RESPONSE=$(curl -s -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.github.com/user/repos" \
    -d '{"name":"ai-nexus","private":true,"auto_init":false}')

REPO_URL=$(echo "$RESPONSE" | jq -r '.html_url // empty')
ERROR=$(echo "$RESPONSE" | jq -r '.message // empty')

if [ -n "$REPO_URL" ] && [ "$REPO_URL" != "null" ]; then
    echo "✅ Repository created: $REPO_URL"
    
    # Push code
    echo "Pushing code to GitHub..."
    git remote add origin "$REPO_URL" 2>/dev/null || true
    git remote set-url origin "$REPO_URL"
    git push -u origin master --force
    
    echo ""
    echo "=============================================="
    echo "  ✅ DEPLOYMENT COMPLETE!"
    echo "=============================================="
    echo ""
    echo "Repository: $REPO_URL"
    echo ""
    echo "Next steps:"
    echo "1. Add GitHub Secrets"
    echo "2. Deploy to Vercel & Render"
else
    echo "❌ Failed to create repository"
    echo "Error: $ERROR"
    echo ""
    echo "The repository might already exist. Try:"
    echo "git remote set-url origin https://github.com/universalvish/ai-nexus.git"
    echo "git push -u origin master --force"
fi