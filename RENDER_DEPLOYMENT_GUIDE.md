# 🚀 Render Backend Deployment Guide

## Step 1: Create Render Account

1. Go to https://render.com
2. Click **"Get Started"** → Sign up with **GitHub**
3. Authorize Render to access your GitHub repositories

---

## Step 2: Create Web Service

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub account if not already connected
3. Find and select the **`ai-nexus`** repository
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `ai-nexus-api` |
| **Region** | Oregon (or closest to you) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3.11` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

5. Select **Free** plan (or paid for production)

6. Click **"Create Web Service"**

---

## Step 3: Add Environment Variables

In the Render dashboard, go to **Environment** tab and add these variables:

### Required Variables

```env
# App Settings
APP_NAME=AI Nexus
DEBUG=false
SECRET_KEY=<generate-random-64-char-string>

# Database (Get from Supabase)
DATABASE_URL=postgresql+asyncpg://postgres.xxx:password@aws-0-region.pooler.supabase.com:6543/postgres

# CORS - REPLACE WITH YOUR VERCEL FRONTEND URL
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000

# Security
BCRYPT_ROUNDS=12
RATE_LIMIT_PER_MINUTE=60
```

### Generate SECRET_KEY
```bash
openssl rand -base64 64
```

### Optional Variables (for AI features)

```env
# AI Services
OPENAI_API_KEY=sk-... (if using OpenAI)
HUGGING_FACE_API_KEY=hf_... (if using HuggingFace)

# Redis (for caching - optional on free tier)
REDIS_URL=redis://localhost:6379/0

# Email (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Stripe (for billing)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## Step 4: Health Check

Once deployed, your backend URL will be:
```
https://ai-nexus-api.onrender.com
```

Test health endpoint:
```
https://ai-nexus-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected"
}
```

---

## Step 5: Connect Frontend to Backend

### Update Vercel Environment Variables

In your Vercel project settings, update:

```env
NEXT_PUBLIC_API_URL=https://ai-nexus-api.onrender.com
```

### If using NextAuth, also add:

```env
NEXTAUTH_URL=https://your-frontend.vercel.app
NEXTAUTH_SECRET=<same-secret-as-backend>
```

---

## Step 6: API Documentation

Once deployed, access the API docs:
```
https://ai-nexus-api.onrender.com/docs
```

Swagger UI will show all available endpoints.

---

## 🔧 Troubleshooting

### CORS Errors
If you see CORS errors:
1. Check `ALLOWED_ORIGINS` includes your exact Vercel URL (no trailing slash)
2. Make sure URL is `https://` not `http://`
3. Redeploy backend after updating environment variables

### Database Connection Failed
1. Verify `DATABASE_URL` from Supabase is correct
2. Check Supabase project is not paused
3. Ensure IP allowlist includes Render's IPs (or use connection pooler)

### Build Failed
Check Render build logs. Common issues:
- Missing dependencies → Check `requirements.txt`
- Python version mismatch → Set to Python 3.11
- Import errors → Check all imports are correct

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger UI |
| `/api/v1/auth/*` | POST | Authentication |
| `/api/v1/chat/*` | POST | AI Chat |
| `/api/v1/agents/*` | POST | AI Agents |
| `/api/v1/billing/*` | GET | Subscription info |

---

## 🔐 Security Notes

- All secrets are stored in Render environment variables
- CORS is configured to only allow your frontend domain
- Rate limiting is enabled (60 req/min)
- Security headers are automatically added
- No sensitive data in code or logs
