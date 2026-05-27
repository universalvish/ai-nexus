# Frontend Configuration Guide

## Current API Configuration

**File:** `frontend/lib/api.ts`
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
```

---

## Required Vercel Environment Variables

Go to: **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**

Add these variables:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://ai-nexus-22sc.onrender.com` |

### Optional but Recommended:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_SITE_URL` | `https://your-project.vercel.app` |

---

## Required Render CORS Configuration

Go to: **Render Dashboard** → `ai-nexus-api` → **Environment**

Update `ALLOWED_ORIGINS` to include your Vercel frontend URL:

```
ALLOWED_ORIGINS=https://your-project.vercel.app,http://localhost:3000
```

### ⚠️ IMPORTANT:
- Replace `your-project.vercel.app` with your **actual Vercel project URL**
- Do NOT include trailing slash
- Must be `https://` (not `http://`)

---

## After Making Changes

1. **Redeploy Vercel**: Trigger a new deployment in Vercel dashboard
2. **Redeploy Render**: Save environment variables (auto-triggers redeploy)

---

## Testing the Connection

### Test from Browser Console:

```javascript
// Open browser dev tools and run:
fetch('https://ai-nexus-22sc.onrender.com/health')
  .then(r => r.json())
  .then(console.log)
```

Expected:
```json
{"status":"healthy","database":"connected","cache":"connected"}
```

### CORS Test:

```javascript
fetch('https://ai-nexus-22sc.onrender.com/api/v1/auth/login', {
  method: 'OPTIONS',
  headers: {
    'Origin': 'https://your-project.vercel.app'
  }
}).then(r => {
  console.log('CORS Headers:', {
    'access-control-allow-origin': r.headers.get('access-control-allow-origin'),
    'access-control-allow-methods': r.headers.get('access-control-allow-methods')
  });
})
```

Expected:
- `access-control-allow-origin` should match your Vercel URL
