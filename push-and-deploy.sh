#!/bin/bash
# ============================================
# AI NEXUS - COMPLETE PUSH & DEPLOY SCRIPT
# ============================================
# Run this script to push code to GitHub
# ============================================

set -e

echo "=============================================="
echo "  AI NEXUS - PUSH & DEPLOY SCRIPT"
echo "=============================================="
echo ""

REPO_URL="https://github.com/universalvish/ai-nexus.git"

# Step 1: Configure git
echo "[1/5] Configuring Git..."
git config user.email "ai-nexus[bot]@users.noreply.github.com"
git config user.name "AI Nexus Bot"
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/universalvish/ai-nexus.git"
echo "✓ Git configured"
echo ""

# Step 2: Ensure .gitignore is correct
echo "[2/5] Verifying .gitignore..."
if ! grep -q "\.env" .gitignore; then
    echo ".env" >> .gitignore
fi
echo "✓ .gitignore verified"
echo ""

# Step 3: Stage all files
echo "[3/5] Staging files..."
git add -A
echo "✓ Files staged"
echo ""

# Step 4: Commit
echo "[4/5] Committing..."
git commit -m "AI Nexus v1.0 - Enterprise AI SaaS Platform

Features:
- Futuristic Next.js frontend with dark theme
- FastAPI backend with 40+ endpoints
- AI agent configuration (LangChain, CrewAI, AutoGen ready)
- Supabase database with RLS
- Docker production configuration
- CI/CD with security scanning
- Cloudflare protection settings
- Production security middleware

Security:
- Secret scanning in CI/CD
- Row-Level Security in database
- Security headers (CSP, HSTS, XSS)
- Rate limiting
- Prompt injection protection
- HTTPS enforcement" 2>/dev/null || echo "Nothing to commit"
echo ""

# Step 5: Push
echo "[5/5] Pushing to GitHub..."
echo "⚠ If prompted for credentials, use GitHub Token"
echo "   Create token at: https://github.com/settings/tokens"
echo ""

if command -v gh &> /dev/null; then
    gh auth refresh --hostname github.com 2>/dev/null || true
fi

git push -u origin master
echo ""

echo "=============================================="
echo "  ✓ Code pushed to GitHub!"
echo "=============================================="
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. Configure GitHub Secrets:"
echo "   Settings > Secrets > Actions > New secret"
echo ""
echo "2. Add these secrets:"
echo "   - VERCEL_TOKEN, VERCEL_ORG_ID, VERCEL_PROJECT_ID"
echo "   - RENDER_API_KEY, RENDER_SERVICE_ID"
echo "   - NEXT_PUBLIC_API_URL, NEXT_PUBLIC_SUPABASE_URL, etc."
echo ""
echo "3. Deploy Frontend to Vercel:"
echo "   - Import: https://vercel.com/new"
echo "   - Root: frontend"
echo ""
echo "4. Deploy Backend to Render:"
echo "   - Connect GitHub repo"
echo "   - Root: backend"
echo "   - Build: pip install -r requirements.txt"
echo "   - Start: gunicorn app.main:app --bind 0.0.0.0:\$PORT --workers 2"
echo ""
echo "5. Setup Supabase:"
echo "   - Create project at supabase.com"
echo "   - Run database/supabase_rls.sql"
echo ""
echo "See docs/DEPLOYMENT.md for full instructions"
echo ""