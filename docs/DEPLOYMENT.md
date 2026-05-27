# AI NEXUS - SECURE DEPLOYMENT GUIDE

## Security Overview

This deployment follows enterprise security best practices:
- **Private Repository**: Code never exposed publicly
- **Environment Variables**: All secrets stored securely
- **HTTPS Everywhere**: SSL/TLS enforced
- **Cloudflare Protection**: DDoS, WAF, rate limiting
- **Supabase RLS**: Database access controlled at row level
- **Vercel + Render**: Production-ready hosting

## Architecture

```
GitHub Private Repo
        ↓
Frontend → Vercel (Global CDN, DDoS protection)
Backend → Render (API server)
Database → Supabase (PostgreSQL + Auth + RLS)
Protection → Cloudflare (WAF, SSL, CDN)
```

## Security Checklist

- [ ] Repository set to PRIVATE
- [ ] Forking disabled
- [ ] Branch protection enabled
- [ ] All secrets in GitHub Secrets
- [ ] CORS restricted to specific domains
- [ ] Rate limiting configured
- [ ] Security headers enabled
- [ ] RLS enabled in Supabase
- [ ] Cloudflare DDoS protection on
- [ ] HTTPS enforced everywhere
- [ ] Admin routes protected via API
- [ ] Monitoring enabled
- [ ] Backups configured

---

## Step 1: Create Private GitHub Repository

1. Create new repository at github.com (set to **PRIVATE**)
2. Disable forking in repository settings
3. Add branch protection rules for main

```bash
cd /workspace/project
git init
git add .
git commit -m "Initial commit - AI Nexus v1.0.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-nexus.git
git push -u origin main
```

## Step 2: Setup GitHub Secrets

Add these in Settings > Secrets and variables > Actions:

### Vercel Secrets
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

### Render Secrets
- `RENDER_API_KEY`
- `RENDER_SERVICE_ID`

### Environment Secrets
- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

## Step 3: Deploy Backend to Render

1. Connect repo to render.com
2. Create Web Service:
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app.main:app --bind 0.0.0.0:$PORT --workers 2`
3. Set environment variables (from .env.example)

## Step 4: Deploy Frontend to Vercel

1. Import repo in vercel.com
2. Set root directory to `frontend`
3. Add environment variables
4. Deploy

## Step 5: Configure Cloudflare

1. Add domain to Cloudflare
2. Update nameservers
3. Enable DDoS protection
4. Configure firewall rules
5. Enable security headers

## Step 6: Setup Supabase RLS

Run `database/supabase_rls.sql` in Supabase SQL Editor.

---

## Production Commands

```bash
# Local development (Docker)
docker-compose -f docker/docker-compose.production.yml up -d

# Build frontend
cd frontend && npm run build

# Run backend
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000
```
