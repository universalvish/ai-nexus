# 🚀 AI Nexus Deployment Guide

## ✅ Code Successfully Pushed

Repository: **https://github.com/universalvish/ai-nexus** (Private)

---

## 📋 Pre-Deployment Checklist

### Step 1: Add CI/CD Workflow (2 minutes)

**Option A: Add Workflow Scope to Token (Recommended)**
1. Go to: https://github.com/settings/tokens/YOUR_TOKEN_ID
2. Under "Repository access", click **"Configure"** next to ai-nexus
3. Check ✅ **Workflow** 
4. Click **Update token**

**Option B: Add Workflow via GitHub UI**
1. Go to: https://github.com/universalvish/ai-nexus/actions
2. Click **"New workflow"**
3. Copy contents from `.github/workflows/ci-cd.yml` in local repo
4. Commit the workflow

---

### Step 2: Create Vercel Account & Deploy Frontend (5 minutes)

1. **Sign up**: https://vercel.com/signup (free tier)
2. **Import Project**:
   - Click "Add New" → "Project"
   - Select "GitHub" and authorize
   - Choose `ai-nexus` repository
   - Framework: Next.js (auto-detected)
3. **Environment Variables** (in Vercel project settings):
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api/v1
   NEXTAUTH_URL=https://your-frontend.vercel.app
   NEXTAUTH_SECRET=<generate random string>
   DATABASE_URL=postgresql://user:pass@host:5432/db
   ```
4. **Deploy**: Click "Deploy"

5. **Get Production URL** (e.g., `ai-nexus-frontend.vercel.app`)

---

### Step 3: Create Supabase Database (5 minutes)

1. **Sign up**: https://supabase.com (free tier)
2. **Create Project**: Name it "ai-nexus"
3. **Get Connection String**: Settings → Connection Pooling → URI
4. **Run Migrations**:
   ```bash
   # In Supabase SQL Editor, run contents of:
   # database/supabase_rls.sql
   # database/prisma/schema.prisma (after prisma format)
   ```

---

### Step 4: Create Render Account & Deploy Backend (5 minutes)

1. **Sign up**: https://render.com (free tier)
2. **Create Web Service**:
   - Connect GitHub repo
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. **Environment Variables**:
   ```
   DATABASE_URL=postgresql://user:pass@host:5432/db
   SECRET_KEY=<generate random string>
   ALLOWED_ORIGINS=https://ai-nexus-frontend.vercel.app
   CORS_ORIGINS=https://ai-nexus-frontend.vercel.app
   ```
4. **Deploy**: Click "Create Web Service"

5. **Get Backend URL** (e.g., `ai-nexus-backend.onrender.com`)

---

### Step 5: Update Environment Variables

1. **In Vercel**, update:
   ```
   NEXT_PUBLIC_API_URL=https://ai-nexus-backend.onrender.com/api/v1
   ```

2. **In Render**, update:
   ```
   ALLOWED_ORIGINS=https://ai-nexus-frontend.vercel.app
   CORS_ORIGINS=https://ai-nexus-frontend.vercel.app
   FRONTEND_URL=https://ai-nexus-frontend.vercel.app
   ```

---

## 🔐 Security Configuration

### Cloudflare (Recommended)
1. Sign up: https://dash.cloudflare.com
2. Add your domain or use Cloudflare Pages
3. Enable:
   - DDoS Protection
   - WAF rules
   - SSL/TLS (Full strict)

---

## 📊 Monitoring Setup

### Health Check Endpoint
```
GET https://your-backend.onrender.com/api/v1/health
```

### Vercel Analytics
- Enable in Vercel dashboard (free tier available)

### Render Monitoring
- Built-in logs and metrics
- Set up uptime checks

---

## 🎯 Expected Result

| Component | URL |
|-----------|-----|
| Frontend | `ai-nexus-frontend.vercel.app` |
| Backend API | `ai-nexus-backend.onrender.com/api/v1` |
| API Docs | `ai-nexus-backend.onrender.com/docs` |
| Health | `ai-nexus-backend.onrender.com/api/v1/health` |

---

## ❓ Troubleshooting

**CORS Errors?**
→ Ensure `ALLOWED_ORIGINS` matches your Vercel URL exactly

**Database Connection Failed?**
→ Check Supabase connection string format

**Build Failed?**
→ Check Vercel/Render build logs for specific errors

---

## 📞 Support

- Next.js docs: https://nextjs.org/docs
- FastAPI docs: https://fastapi.tiangolo.com
- Supabase docs: https://supabase.com/docs
- Render docs: https://render.com/docs
