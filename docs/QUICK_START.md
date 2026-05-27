# ============================================
# AI NEXUS - QUICK PUSH & DEPLOY GUIDE
# ============================================
# Run these commands ON YOUR LOCAL MACHINE
# ============================================

# ============================================
# STEP 1: Clone and Push to GitHub
# ============================================

# Option A: From this environment (if you have token access)
git clone https://github.com/universalvish/ai-nexus.git
cd ai-nexus
git remote add origin-local /workspace/project
git pull origin-local master --allow-unrelated-histories
git push -u origin master

# Option B: If you prefer to download/upload files
# Download all files from this workspace and upload to GitHub

# ============================================
# STEP 2: Add GitHub Secrets (GitHub Settings)
# ============================================

Go to: https://github.com/universalvish/ai-nexus/settings/secrets/actions

Add these NEW SECRETS:

```bash
# Vercel (Frontend Deployment)
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_vercel_org_id
VERCEL_PROJECT_ID=your_vercel_project_id

# Render (Backend Deployment)
RENDER_API_KEY=your_render_api_key
RENDER_SERVICE_ID=your_render_service_id

# Environment Variables
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api/v1
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
```

# ============================================
# STEP 3: Deploy Frontend to Vercel
# ============================================

1. Go to: https://vercel.com/new
2. Click "Import Project"
3. Select "GitHub" and choose `universalvish/ai-nexus`
4. Configure:
   - Framework: Next.js (auto-detected)
   - Root Directory: `./frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
5. Add Environment Variables in Vercel:
   - NEXT_PUBLIC_API_URL
   - NEXT_PUBLIC_SUPABASE_URL
   - NEXT_PUBLIC_SUPABASE_ANON_KEY
6. Click "Deploy"

# ============================================
# STEP 4: Deploy Backend to Render
# ============================================

1. Go to: https://dashboard.render.com/
2. Click "New +" > "Web Service"
3. Connect your GitHub repo
4. Configure:
   - Name: ai-nexus-api
   - Root Directory: `backend`
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app.main:app --bind 0.0.0.0:$PORT --workers 2`
5. Add Environment Variables:
   - ENVIRONMENT=production
   - DEBUG=false
   - DATABASE_URL=<your-supabase-connection-string>
   - SECRET_KEY=<generate-64-char-random-string>
   - CORS_ORIGINS=https://your-frontend.vercel.app
   - RATE_LIMIT_PER_MINUTE=60
6. Health Check: `/health`
7. Click "Create Web Service"

# ============================================
# STEP 5: Setup Supabase Database
# ============================================

1. Go to: https://supabase.com/dashboard
2. Create new project
3. Get connection string from Settings > Database
4. In SQL Editor, run `database/supabase_rls.sql`
5. Copy connection string to Render

# ============================================
# STEP 6: Configure Cloudflare
# ============================================

1. Go to: https://dash.cloudflare.com/
2. Add your domain
3. Update nameservers at your registrar
4. Configure:
   - SSL/TLS: Full (Strict)
   - Security > DDoS: Enabled
   - Security > WAF: Enabled
5. Add Page Rules (see docs/CLOUDFLARE.md)

# ============================================
# STEP 7: Update API URL
# ============================================

After Render deploys, get your backend URL:
- Go to Render Dashboard > ai-nexus-api
- Copy the URL (e.g., https://ai-nexus-api.onrender.com)

Update in Vercel:
- NEXT_PUBLIC_API_URL = https://ai-nexus-api.onrender.com/api/v1

# ============================================
# VERIFICATION CHECKLIST
# ============================================

After deployment:

□ Frontend loads at your Vercel URL
□ Backend health check: https://your-api.onrender.com/health
□ Database connection works
□ Rate limiting working (try >100 req/min)
□ Security headers visible (curl -I)
□ HTTPS enforced
□ RLS working (users only see own data)

# ============================================
# SUPPORT
# ============================================

Documentation:
- docs/DEPLOYMENT.md - Complete guide
- docs/SECURITY_CHECKLIST.md - Security verification
- docs/CLOUDFLARE.md - Cloudflare setup

All code is committed and ready. Just follow the steps above!