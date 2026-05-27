# Cloudflare Security Configuration

## DNS Setup

```
Type    Name    Content                         Proxy Status
A       @       76.76.21.21                     DNS Only (Vercel)
CNAME   www     cname.vercel.com                Proxied
CNAME   api     your-render-service.onrender.com Proxied
TXT     @       v=spf1 include:_spf.mailgun.org ~all
TXT     @       google-site-verification=xxx     DNS Only
```

## Page Rules

### Redirect HTTP to HTTPS
```
URL: http://yourdomain.com/*
Setting: Forwarding URL - 301 Redirect to https://yourdomain.com/$1
```

### Cache Static Assets
```
URL: *yourdomain.com/_next/static/*
Setting: Cache Level - Cache Everything
Edge Cache TTL: 1 month
```

### Security Headers
```
URL: *yourdomain.com/*
Setting: Custom Headers:
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## Firewall Rules

### Rule 1: Block Known Bad Actors
```
Expression: (cf.threat_score > 20) or (ip.geoip.country in {"CN" "RU" "KP"})
Action: Block
```

### Rule 2: Rate Limit API
```
Expression: http.request.uri.path contains "/api"
Action: Rate Limit - 100 requests per minute
```

### Rule 3: Challenge Bots
```
Expression: (cf.client.bot) or (not vercel)
Action: JS Challenge
```

### Rule 4: Allow Vercel IPs Only
```
Expression: not (ip.src in {103.21.244.0/22 103.22.200.0/22 103.31.4.0/22 104.16.0.0/13 104.24.0.0/14 108.162.192.0/18 131.0.72.0/22 141.101.64.0/18 162.158.0.0/15 172.64.0.0/13 173.245.48.0/20 188.114.96.0/20 190.93.240.0/20 197.234.240.0/22 198.41.128.0/17})
Action: Block
```

## DDoS Protection Settings

### Network Layer
```
- Automatic: On
- Sensitivity: Medium
- Action: Challenge
```

### Application Layer (L7)
```
- Request rate: 1000 requests/minute
- Burst: 100
- Mode: Challenge
```

## Workers Security Script

```javascript
// workers/security.js
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // Check for suspicious patterns
  const suspiciousPatterns = [
    /<script/i,
    /javascript:/i,
    /on\w+=/i,
    /expression\s*\(/i
  ]
  
  const url = new URL(request.url)
  const body = await request.text()
  
  // Check URL and body for suspicious content
  for (const pattern of suspiciousPatterns) {
    if (pattern.test(url.pathname) || pattern.test(body)) {
      return new Response('Blocked', { status: 403 })
    }
  }
  
  // Add security headers
  const response = await fetch(request)
  const newHeaders = new Headers(response.headers)
  
  newHeaders.set('X-Frame-Options', 'DENY')
  newHeaders.set('X-Content-Type-Options', 'nosniff')
  newHeaders.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  newHeaders.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
  
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders
  })
}
```

## SSL/TLS Settings

```
Encryption Mode: Full (Strict)
TLS 1.2: On
TLS 1.3: On
Automatic HTTPS Rewrites: On
Opportunratic Encryption: On
TLS Fingerprint: On (managed by Cloudflare)
```

## Caching Rules

### Tiered Cache
```
- Enabled: Yes
- Cache Key: Standard
- Origin Cache Control: On
```

### Purge Cache
```
- Purge Everything: When deploying new code
- Purge by tag: When content updates
- Purge by host: When API changes
```

## Monitoring

### Analytics
- Enable Logpush to Cloudflare Logs
- Send to: Datadog / Sumo Logic / Generic S3
- Fields: all

### Alerts
- Set up alerts for:
  - High error rate (>1%)
  - Slow response (>2s)
  - Traffic spikes (>2x normal)
  - Security events