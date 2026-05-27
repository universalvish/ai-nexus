# 🚀 Vercel Deployment (Project ID: prj_YyK5EosdNQt05TmBqqsOOzqalAEm)

## Option 1: Manual Deploy (Recommended)

### Step 1: Add Vercel Token to GitHub Secrets

1. Go to: https://github.com/universalvish/ai-nexus/settings/secrets/actions
2. Click **New repository secret**
3. Add:
   - Name: `VERCEL_TOKEN`
   - Secret: Your Vercel API token from https://vercel.com/account/tokens

### Step 2: Trigger Deploy via GitHub Actions

1. Go to: https://github.com/universalvish/ai-nexus/actions
2. Click **"Deploy Frontend to Vercel"**
3. Click **"Run workflow"**
4. Enter:
   - Vercel Token: Your token
   - Vercel Project ID: `prj_YyK5EosdNQt05TmBqqsOOzqalAEm`
5. Click **Run workflow**

---

## Option 2: Direct Vercel Manual Deploy

1. Go to https://vercel.com/dashboard
2. Find your AI Nexus project
3. Click **Deployments** tab
4. Click **Create New Deployment**
5. Select `universalvish/ai-nexus` repo
6. Set root directory: `frontend`
7. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = `https://ai-nexus-22sc.onrender.com`
8. Click **Deploy**

---

## Option 3: Vercel CLI (If logged in)

```bash
cd frontend
vercel --prod --yes --project-id=prj_YyK5EosdNQt05TmBqqsOOzqalAEm
```

---

## Quick Fix (Vercel Dashboard)

If you're already logged into Vercel:

1. https://vercel.com/universalvish/ai-nexus/settings/environment-variables
2. Add: `NEXT_PUBLIC_API_URL` = `https://ai-nexus-22sc.onrender.com`
3. Go to Deployments
4. Click **Redeploy** (three dots menu)

---

## Frontend Already Deployed?

Check: https://vercel.com/universalvish/ai-nexus

If deployed, just update environment variable and redeploy!
