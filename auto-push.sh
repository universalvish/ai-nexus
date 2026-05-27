#!/bin/bash
# ============================================
# AI NEXUS - AUTO PUSH SCRIPT
# ============================================
# This script will automatically push all code
# to GitHub using your Personal Access Token
# ============================================

set -e

echo "=============================================="
echo "  AI NEXUS - AUTO PUSH TO GITHUB"
echo "=============================================="
echo ""

# Check if PAT is provided
if [ -z "$1" ]; then
    echo "Usage: $0 YOUR_GITHUB_PAT"
    echo ""
    echo "To get a Personal Access Token:"
    echo "1. Go to: https://github.com/settings/tokens/new"
    echo "2. Note: Select 'Fine-grained tokens'"
    echo "3. Permissions:"
    echo "   - Repository access: All repositories"
    echo "   - Permissions: Contents: Read and write"
    echo "4. Generate token and copy it"
    echo "5. Run: $0 YOUR_TOKEN"
    exit 1
fi

PAT="$1"
REPO_URL="https://github.com/universalvish/ai-nexus.git"

echo "Step 1: Creating repository on GitHub..."
echo "============================================"

# Create repo using curl with PAT
RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $PAT" \
    -H "Content-Type: application/json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/user/repos" \
    -d '{"name":"ai-nexus","private":true,"auto_init":false,"description":"AI Nexus - Enterprise AI SaaS Platform"}')

HTML_URL=$(echo "$RESPONSE" | jq -r '.html_url // empty')
ERROR=$(echo "$RESPONSE" | jq -r '.message // empty')

if [ -n "$HTML_URL" ] && [ "$HTML_URL" != "null" ]; then
    echo "✅ Repository created: $HTML_URL"
elif echo "$RESPONSE" | jq -r '.errors[0].message // empty' | grep -q "already exists"; then
    echo "✅ Repository already exists"
    HTML_URL="$REPO_URL"
else
    echo "⚠️ Could not create repo (may already exist)"
    echo "Error: $ERROR"
    HTML_URL="$REPO_URL"
fi

echo ""
echo "Step 2: Pushing code to GitHub..."
echo "============================================"

# Set remote with PAT
git remote remove origin 2>/dev/null || true
git remote add origin "https://$PAT@github.com/universalvish/ai-nexus.git"

# Push
if git push -u origin master --force 2>&1; then
    echo ""
    echo "=============================================="
    echo "  ✅ PUSH SUCCESSFUL!"
    echo "=============================================="
    echo ""
    echo "🌐 Repository: https://github.com/universalvish/ai-nexus"
    echo ""
    echo "NEXT STEPS:"
    echo "1. Go to repository Settings > Secrets > Actions"
    echo "2. Add these secrets:"
    echo "   - VERCEL_TOKEN"
    echo "   - VERCEL_ORG_ID"
    echo "   - VERCEL_PROJECT_ID"
    echo "   - RENDER_API_KEY"
    echo "3. Import repo in Vercel"
    echo "4. Deploy backend to Render"
else
    echo ""
    echo "❌ Push failed. Please check your token permissions."
fi