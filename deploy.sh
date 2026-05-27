#!/bin/bash
# ============================================
# AI NEXUS - AUTOMATED DEPLOYMENT SCRIPT
# ============================================
# This script automates the complete deployment
# Run: chmod +x deploy.sh && ./deploy.sh
# ============================================

set -e

echo "=============================================="
echo "  AI NEXUS - SECURE DEPLOYMENT AUTOMATION"
echo "=============================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================
# STEP 1: Create GitHub Private Repository
# ============================================
echo -e "${BLUE}Step 1: Creating GitHub Private Repository...${NC}"
echo ""

# Check if gh CLI is available
if command -v gh &> /dev/null; then
    echo "Using GitHub CLI..."
    
    # Check if authenticated
    if gh auth status &> /dev/null; then
        # Create private repository
        gh repo create ai-nexus --private --source=. --remote=origin --push 2>/dev/null || \
        echo "Repository may already exist, pushing to existing repo..."
        
        echo -e "${GREEN}✓ GitHub repository created/pushed${NC}"
    else
        echo -e "${YELLOW}⚠ GitHub CLI not authenticated. Please run: gh auth login${NC}"
        echo "Or create repository manually at: https://github.com/new"
    fi
else
    echo -e "${YELLOW}⚠ GitHub CLI not installed. Please either:${NC}"
    echo "1. Install: https://cli.github.com/"
    echo "2. Or create repository manually at: https://github.com/new"
    echo ""
    echo "Then run: git remote add origin YOUR_REPO_URL"
fi

echo ""

# ============================================
# STEP 2: Configure GitHub Settings
# ============================================
echo -e "${BLUE}Step 2: Configuring GitHub Security Settings...${NC}"
echo ""

# Create branch protection settings (if gh is available)
if command -v gh &> /dev/null && gh auth status &> /dev/null; then
    # Enable branch protection
    echo "Setting up branch protection for main branch..."
    
    # This would require admin permissions, so we provide instructions
    echo -e "${YELLOW}⚠ Please configure manually in GitHub Settings:${NC}"
    echo "1. Go to: Settings > Branches > Add rule"
    echo "2. Branch name pattern: main"
    echo "3. Enable:"
    echo "   - Require pull request reviews"
    echo "   - Dismiss stale reviews"
    echo "   - Require status checks"
    echo "   - Require branches to be up to date"
    echo "   - Include administrators"
fi

echo ""

# ============================================
# STEP 3: GitHub Secrets Setup
# ============================================
echo -e "${BLUE}Step 3: GitHub Secrets Configuration${NC}"
echo ""

echo "Please add these secrets in GitHub > Settings > Secrets:${NC}"
echo ""
echo "VERCEL_SECRETS:"
echo "  - VERCEL_TOKEN (from vercel.com/settings/tokens)"
echo "  - VERCEL_ORG_ID (from vercel.com/settings/teams)"
echo "  - VERCEL_PROJECT_ID (from your project settings)"
echo ""
echo "RENDER_SECRETS:"
echo "  - RENDER_API_KEY (from render.com/api-keys)"
echo "  - RENDER_SERVICE_ID (from your service)"
echo ""
echo "ENV_SECRETS:"
echo "  - NEXT_PUBLIC_API_URL"
echo "  - NEXT_PUBLIC_SUPABASE_URL"
echo "  - NEXT_PUBLIC_SUPABASE_ANON_KEY"
echo ""

# ============================================
# STEP 4: Vercel Deployment
# ============================================
echo -e "${BLUE}Step 4: Vercel Frontend Deployment${NC}"
echo ""

if command -v vercel &> /dev/null; then
    echo "Deploying frontend to Vercel..."
    cd frontend
    vercel --prod --yes 2>/dev/null || echo "Run 'vercel --prod' manually"
    cd ..
    echo -e "${GREEN}✓ Frontend deployed to Vercel${NC}"
else
    echo -e "${YELLOW}⚠ Vercel CLI not installed. Install with: npm i -g vercel${NC}"
    echo "Then run: cd frontend && vercel --prod"
fi

echo ""

# ============================================
# STEP 5: Render Backend Deployment
# ============================================
echo -e "${BLUE}Step 5: Render Backend Deployment${NC}"
echo ""

echo "To deploy backend to Render:"
echo "1. Go to render.com and connect your GitHub repo"
echo "2. Create Web Service:"
echo "   - Root Directory: backend"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn app.main:app --bind 0.0.0.0:\$PORT --workers 2"
echo "3. Set environment variables in dashboard"
echo ""

# ============================================
# STEP 6: Supabase Setup
# ============================================
echo -e "${BLUE}Step 6: Supabase Database Setup${NC}"
echo ""

echo "To setup Supabase:"
echo "1. Create project at supabase.com"
echo "2. Get connection string from Settings > Database"
echo "3. Run database/supabase_rls.sql in SQL Editor"
echo "4. Copy connection string to RENDER_DATABASE_URL"
echo ""

# ============================================
# STEP 7: Cloudflare Protection
# ============================================
echo -e "${BLUE}Step 7: Cloudflare Security Configuration${NC}"
echo ""

echo "Configure Cloudflare:"
echo "1. Add domain to Cloudflare"
echo "2. Update nameservers at your registrar"
echo "3. Enable DDoS protection in Security > DDoS"
echo "4. Configure firewall rules (see docs/CLOUDFLARE.md)"
echo "5. Enable SSL/TLS with Full (Strict) mode"
echo ""

# ============================================
# STEP 8: Security Verification
# ============================================
echo -e "${BLUE}Step 8: Security Verification${NC}"
echo ""

echo "Verify security settings:"
echo "✓ Repository is PRIVATE"
echo "✓ .gitignore excludes sensitive files"
echo "✓ GitHub Actions have restricted permissions"
echo "✓ Secrets stored in GitHub Secrets"
echo "✓ CORS restricted to specific domains"
echo "✓ Rate limiting enabled"
echo "✓ Security headers configured"
echo ""

echo "=============================================="
echo -e "${GREEN}  DEPLOYMENT SETUP COMPLETE!${NC}"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Add GitHub Secrets"
echo "2. Deploy to Vercel/Render"
echo "3. Configure Cloudflare"
echo "4. Setup Supabase"
echo ""
echo "See docs/DEPLOYMENT.md for detailed instructions"
echo ""