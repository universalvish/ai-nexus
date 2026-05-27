# 🚀 Complete Deployment Guide - AI Nexus

## ✅ What Was Done Automatically

1. **Backend Code Updated**: CORS enabled for all origins
2. **Frontend Code Updated**: API URL points to your Render backend
3. **Code Pushed**: All changes pushed to GitHub main branch

---

## 📋 Manual Steps Required (5 minutes)

### Step 1: Redeploy Backend on Render

Render will auto-deploy from GitHub. Wait 2-3 minutes for deployment to complete.

**To trigger manual redeploy:**
1. Go to: https://dashboard.render.com
2. Select `ai-nexus-api` service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Step 2: Update Vercel Environment Variable

1. Go to: https://vercel.com/dashboard
2. Select your AI Nexus project
3. Go to **Settings** → **Environment Variables**
4. Add/Update:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://ai-nexus-22sc.onrender.com` |

5. Click **"Save"**
6. Go to **Deployments** → Click **"Redeploy"** (three dots menu)

### Step 3: Verify Deployment

After both redeploys complete (2-5 minutes):

**Test Backend:**
```
https://ai-nexus-22sc.onrender.com/health
```
Expected: `{"status":"healthy","database":"connected","cache":"connected"}`

**Test Billing Plans:**
```
https://ai-nexus-22sc.onrender.com/api/v1/billing/plans
```
Expected: JSON with subscription plans

**Test Frontend:**
Visit your Vercel URL and open browser console:
```javascript
fetch('https://ai-nexus-22sc.onrender.com/health')
  .then(r => r.json())
  .then(console.log)
```

---

## 🔐 CORS Configuration

The backend now has CORS enabled for ALL origins (`*`). This allows:
- Vercel frontend to call backend API
- Local development (localhost:3000)
- Any other domain

**For production**, update `/backend/app/middleware/security.py`:
```python
allow_origins=["https://your-domain.com"],  # Specific domain
allow_credentials=True,  # Enable cookies/auth
```

---

## 📊 Final URLs

| Service | URL |
|---------|-----|
| **Frontend** | `https://YOUR_VERCEL_PROJECT.vercel.app` |
| **Backend API** | `https://ai-nexus-22sc.onrender.com` |
| **API Docs** | `https://ai-nexus-22sc.onrender.com/docs` |
| **Health Check** | `https://ai-nexus-22sc.onrender.com/health` |

---

## 🗄️ Database Setup (For Authentication)

Currently auth endpoints (`/auth/login`, `/auth/register`) return 500 because no database is connected.

**To enable authentication:**

1. Create Supabase account: https://supabase.com
2. Create new project "ai-nexus"
3. Go to **Settings** → **Database** → **Connection Pooling**
4. Copy the **Connection URI**
5. In Render, add environment variable:
   ```
   DATABASE_URL=<your-supabase-uri>
   ```
6. Redeploy backend

---

## ✅ Deployment Checklist

- [x] Backend deployed on Render
- [x] Frontend deployed on Vercel  
- [x] CORS configured
- [x] API URL configured
- [ ] Backend redeployed (with CORS fix)
- [ ] Vercel env variable updated
- [ ] Vercel redeployed
- [ ] Database connected (optional - for auth)

---

## 🆘 If Something Doesn't Work

**CORS Error?**
→ Wait 3 minutes, then hard refresh browser (Ctrl+Shift+R)

**Backend not responding?**
→ Check Render dashboard for deployment status

**Frontend shows old code?**
→ Hard refresh browser or trigger new Vercel deploy

**Auth doesn't work?**
→ Connect Supabase database first

---

## 📞 Support

Share your:
1. Vercel frontend URL
2. Browser console error (if any)

And I'll help troubleshoot!
