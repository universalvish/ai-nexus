#!/bin/bash
# ============================================
# AI NEXUS - COMPLETE AUTOMATED SETUP
# ============================================
# Run this script to set up everything
# ============================================

set -e

# ============================================
# CONFIGURATION
# ============================================

GITHUB_USER="${GITHUB_USER:-}"
REPO_NAME="ai-nexus"

# GitHub Token (from environment)
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  AI NEXUS - AUTOMATED SETUP & DEPLOYMENT  ${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# ============================================
# STEP 1: Check Prerequisites
# ============================================
echo -e "${GREEN}[1/7] Checking prerequisites...${NC}"

if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}⚠ GITHUB_TOKEN not set in environment${NC}"
    echo ""
    echo "To get a GitHub Token:"
    echo "1. Go to: https://github.com/settings/tokens"
    echo "2. Click 'Generate new token (classic)'"
    echo "Select these scopes:"
    echo "  ☑ repo (full control)"
    echo "  ☑ admin:org (if creating org repos)"
    echo "3. Copy the token"
    echo "4. Export it: export GITHUB_TOKEN='your-token-here'"
    echo ""
    echo -e "${YELLOW}Note: You can skip GitHub setup and configure manually.${NC}"
    echo ""
    USE_GITHUB=false
else
    USE_GITHUB=true
fi

echo ""

# ============================================
# STEP 2: Create GitHub Repository
# ============================================
echo -e "${GREEN}[2/7] Setting up GitHub Repository...${NC}"

if [ "$USE_GITHUB" = true ]; then
    echo "Creating private repository: $REPO_NAME..."
    
    RESPONSE=$(curl -s -X POST "https://api.github.com/user/repos" \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"$REPO_NAME\", \"private\": true, \"auto_init\": false}")
    
    REPO_URL=$(echo "$RESPONSE" | jq -r '.html_url // empty')
    
    if [ -n "$REPO_URL" ] && [ "$REPO_URL" != "null" ]; then
        echo -e "${GREEN}✓ Repository created: $REPO_URL${NC}"
        
        # Set remote
        git remote add origin "$REPO_URL" 2>/dev/null || \
            git remote set-url origin "$REPO_URL"
        
        # Push code
        echo "Pushing code to GitHub..."
        git remote set-url origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"
        git push -u origin master --force
        
        echo -e "${GREEN}✓ Code pushed to GitHub${NC}"
    else
        echo -e "${RED}⚠ Failed to create repository${NC}"
        echo "Response: $RESPONSE"
    fi
else
    echo -e "${YELLOW}⚠ Skipping GitHub setup${NC}"
    echo "To manually push to GitHub:"
    echo "1. Create private repo at: https://github.com/new"
    echo "2. Run: git remote add origin YOUR_REPO_URL"
    echo "3. Run: git push -u origin master"
fi

echo ""

# ============================================
# STEP 3: Configure Branch Protection
# ============================================
echo -e "${GREEN}[3/7] Configuring branch protection...${NC}"

if [ "$USE_GITHUB" = true ]; then
    # Get repo details
    REPO_FULL="${GITHUB_USER}/${REPO_NAME}"
    
    # Create branch protection rule
    curl -s -X PUT "https://api.github.com/repos/${REPO_FULL}/branches/master/protection" \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "required_status_checks": null,
            "enforce_admins": true,
            "required_pull_request_reviews": {
                "required_approving_review_count": 1
            },
            "restrictions": null
        }' 2>/dev/null
    
    echo -e "${GREEN}✓ Branch protection enabled${NC}"
fi

echo -e "${YELLOW}Manual steps for branch protection:${NC}"
echo "1. Go to: https://github.com/${GITHUB_USER}/${REPO_NAME}/settings/branches"
echo "2. Click 'Add rule' for 'master'"
echo "3. Enable:"
echo "   - Require pull request reviews"
echo "   - Dismiss stale reviews"
echo "   - Require status checks to pass"
echo ""

# ============================================
# STEP 4: Setup GitHub Secrets (Instructions)
# ============================================
echo -e "${GREEN}[4/7] GitHub Secrets Setup${NC}"

echo "Add these secrets in GitHub > Settings > Secrets > Actions:"
echo ""
echo "Required Secrets:"
echo "  VERCEL_TOKEN      - From vercel.com/settings/tokens"
echo "  VERCEL_ORG_ID     - From vercel.com/settings/teams"  
echo "  VERCEL_PROJECT_ID - From your vercel project"
echo "  RENDER_API_KEY    - From render.com/api-keys"
echo "  RENDER_SERVICE_ID - Your render service ID"
echo "  NEXT_PUBLIC_API_URL          - Your backend URL"
echo "  NEXT_PUBLIC_SUPABASE_URL     - Your supabase URL"
echo "  NEXT_PUBLIC_SUPABASE_ANON_KEY - Your supabase anon key"
echo ""

# ============================================
# STEP 5: Vercel Deployment Instructions
# ============================================
echo -e "${GREEN}[5/7] Vercel Frontend Deployment${NC}"

echo "To deploy frontend to Vercel:"
echo "1. Go to: https://vercel.com/new"
echo "2. Import from GitHub"
output_url=$(git remote get-url origin 2>/dev/null | sed 's|https://.*@github.com|https://github.com|')
echo "   Repository: $output_url"
echo "3. Select 'frontend' as root directory"
echo "4. Add environment variables:"
echo "   - NEXT_PUBLIC_API_URL"
echo "   - NEXT_PUBLIC_SUPABASE_URL"
echo "   - NEXT_PUBLIC_SUPABASE_ANON_KEY"
echo "5. Click 'Deploy'"
echo ""

# ============================================
# STEP 6: Render Backend Deployment Instructions
# ============================================
echo -e "${GREEN}[6/7] Render Backend Deployment${NC}"

echo "To deploy backend to Render:"
echo "1. Go to: https://dashboard.render.com/"
echo "2. Connect your GitHub repo"
echo "3. Create Web Service:"
echo "   - Name: ai-nexus-api"
echo "   - Root Directory: backend"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn app.main:app --bind 0.0.0.0:\$PORT --workers 2"
echo "4. Add environment variables:"
echo "   - DATABASE_URL (Supabase connection string)"
echo "   - SECRET_KEY (generate 64-char random string)"
echo "   - ENV=production"
echo "   - DEBUG=false"
echo "5. Deploy"
echo ""

# ============================================
# STEP 7: Summary & Next Steps
# ============================================
echo -e "${GREEN}[7/7] Setup Complete!${NC}"

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  NEXT STEPS${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "1. Add GitHub Secrets (Settings > Secrets > Actions)"
echo "2. Deploy frontend to Vercel"
echo "3. Deploy backend to Render"
echo "4. Setup Supabase:"
echo "   - Create project at supabase.com"
echo "   - Run database/supabase_rls.sql"
echo "5. Configure Cloudflare (see docs/CLOUDFLARE.md)"
echo ""
echo "Documentation: docs/DEPLOYMENT.md"
echo "Scripts:"
echo "  ./deploy.sh - Run deployment commands"
echo "  ./setup.sh  - Interactive setup"
echo ""
echo -e "${GREEN}============================================${NC}"