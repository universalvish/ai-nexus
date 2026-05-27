#!/bin/bash
# ============================================
# AI NEXUS - ONE-CLICK DEPLOY SCRIPT
# ============================================
# Run this on your LOCAL machine to:
# 1. Create GitHub repo
# 2. Push all code
# 3. Enable automatic deployment
# ============================================

echo "=============================================="
echo "  AI NEXUS - DEPLOY TO GITHUB"
echo "=============================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Install from: https://git-scm.com"
    exit 1
fi

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI not found."
    echo "   Install from: https://cli.github.com/"
    echo "   Or press Enter to use HTTPS (manual auth)"
    read -p ""
fi

echo "Step 1: Authenticate with GitHub"
echo "==============================="

if command -v gh &> /dev/null; then
    gh auth status || gh auth login
else
    echo "Will use HTTPS for Git operations"
fi

echo ""
echo "Step 2: Create Repository"
echo "==============================="

REPO_NAME="ai-nexus"

if gh repo view "$REPO_NAME" &> /dev/null; then
    echo "✓ Repository already exists: github.com/universalvish/$REPO_NAME"
else
    echo "Creating repository..."
    gh repo create "$REPO_NAME" --private --gitignore Node --license MIT --push
    echo "✓ Repository created and pushed!"
fi

echo ""
echo "Step 3: Add GitHub Secrets (Manual)"
echo "==============================="
echo "Go to: https://github.com/universalvish/$REPO_NAME/settings/secrets/actions"
echo ""
echo "Add these secrets:"
echo "  VERCEL_TOKEN=your_vercel_token"
echo "  VERCEL_ORG_ID=your_vercel_org_id"
echo "  VERCEL_PROJECT_ID=your_vercel_project_id"
echo "  RENDER_API_KEY=your_render_api_key"
echo ""

echo ""
echo "=============================================="
echo "  ✓ Deployment setup complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Add GitHub Secrets (link above)"
echo "2. Import repo in Vercel: https://vercel.com/new"
echo "3. Deploy backend to Render: https://dashboard.render.com/"
echo ""
echo "Documentation: docs/DEPLOYMENT.md"