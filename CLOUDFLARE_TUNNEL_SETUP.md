# Cloudflare Tunnel Setup Guide
## Expose Your Local RAG App to the Internet

This guide will help you expose your locally running RAG application to the internet using Cloudflare Tunnel (formerly Argo Tunnel). This is perfect for demonstrations and exhibitions.

---

## Prerequisites

1. **Cloudflare Account** (free account works)
   - Sign up at: https://dash.cloudflare.com/sign-up
   - You'll need to add a domain (or use a free subdomain)

2. **Your App Running Locally**
   - FastAPI on `http://localhost:8000`
   - Streamlit on `http://localhost:8501` (or your configured port)

---

## Step 1: Install Cloudflare Tunnel (cloudflared)

### For Windows (PowerShell as Administrator):

```powershell
# Download cloudflared
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile "$env:USERPROFILE\cloudflared.exe"

# Move to a permanent location (optional but recommended)
Move-Item "$env:USERPROFILE\cloudflared.exe" "C:\Program Files\cloudflared\cloudflared.exe"

# Add to PATH (optional - you can also use full path)
$env:Path += ";C:\Program Files\cloudflared"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::User)
```

### Alternative: Using Chocolatey (if installed):

```powershell
choco install cloudflared
```

### Verify Installation:

```powershell
cloudflared --version
```

---

## Step 2: Login to Cloudflare

```powershell
cloudflared tunnel login
```

This will:
1. Open your browser
2. Ask you to select your Cloudflare account
3. Authorize the tunnel
4. Save credentials to `C:\Users\<YourUsername>\.cloudflared\cert.pem`

---

## Step 3: Create a Tunnel

### Option A: Quick Tunnel (Easiest - No Domain Needed)

This creates a temporary tunnel that works immediately:

```powershell
# For Streamlit (port 8501)
cloudflared tunnel --url http://localhost:8501

# This will give you a URL like: https://random-words-1234.trycloudflare.com
```

**Note:** Quick tunnels are temporary and the URL changes each time you restart.

### Option B: Named Tunnel (Permanent - Requires Domain)

#### 3.1 Create the Tunnel:

```powershell
# Create a tunnel named "rag-app"
cloudflared tunnel create rag-app
```

This will output a Tunnel ID (save this for later).

#### 3.2 Configure the Tunnel:

Create a config file at: `C:\Users\<YourUsername>\.cloudflared\config.yml`

```yaml
tunnel: <YOUR_TUNNEL_ID>
credentials-file: C:\Users\<YourUsername>\.cloudflared\<TUNNEL_ID>.json

ingress:
  # Route Streamlit (main app)
  - hostname: rag-app.yourdomain.com
    service: http://localhost:8501
  
  # Route FastAPI (optional - for API access)
  - hostname: api-rag-app.yourdomain.com
    service: http://localhost:8000
  
  # Catch-all rule (must be last)
  - service: http_status:404
```

**Replace:**
- `<YOUR_TUNNEL_ID>` with the ID from step 3.1
- `<YourUsername>` with your Windows username
- `yourdomain.com` with your Cloudflare domain

#### 3.3 Create DNS Records:

In Cloudflare Dashboard:
1. Go to your domain → DNS → Records
2. Add CNAME record:
   - **Name:** `rag-app` (or `api-rag-app` for API)
   - **Target:** `<TUNNEL_ID>.cfargotunnel.com`
   - **Proxy status:** Proxied (orange cloud)

#### 3.4 Run the Tunnel:

```powershell
cloudflared tunnel run rag-app
```

---

## Step 4: Start Your Application

### Terminal 1: Start FastAPI

```powershell
cd C:\Users\rajiv_\OneDrive\Desktop\RAG-app\ingestion-phase
python start_api.py
```

Wait for: `INFO:     Uvicorn running on http://0.0.0.0:8000`

### Terminal 2: Start Streamlit

```powershell
cd C:\Users\rajiv_\OneDrive\Desktop\RAG-app\ingestion-phase
streamlit run app.py --server.port 8501
```

Wait for: `You can now view your Streamlit app in your browser.`

### Terminal 3: Start Cloudflare Tunnel

**For Quick Tunnel:**
```powershell
cloudflared tunnel --url http://localhost:8501
```

**For Named Tunnel:**
```powershell
cloudflared tunnel run rag-app
```

---

## Step 5: Access Your App

### Quick Tunnel:
- Copy the URL shown in Terminal 3 (e.g., `https://random-words-1234.trycloudflare.com`)
- Open in any browser, on any device

### Named Tunnel:
- Access at: `https://rag-app.yourdomain.com`
- API at: `https://api-rag-app.yourdomain.com` (if configured)

---

## Step 6: Configure Streamlit for External Access

Update your Streamlit config to work with Cloudflare:

### Create/Edit: `ingestion-phase/.streamlit/config.toml`

```toml
[server]
port = 8501
address = "0.0.0.0"  # Allow external connections
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

### Update FastAPI CORS (if needed):

The FastAPI app should already have CORS configured, but verify in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development/exhibition
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Step 7: Keep Tunnel Running (Optional - Background Service)

### Windows Service (Recommended for Exhibition):

1. **Create a service script** `start-tunnel.bat`:

```batch
@echo off
cd /d "C:\Program Files\cloudflared"
cloudflared tunnel run rag-app
```

2. **Run as Windows Service** (requires NSSM - Non-Sucking Service Manager):

```powershell
# Download NSSM
Invoke-WebRequest -Uri "https://nssm.cc/release/nssm-2.24.zip" -OutFile "$env:USERPROFILE\nssm.zip"
Expand-Archive "$env:USERPROFILE\nssm.zip" "$env:USERPROFILE\nssm" -Force

# Install as service
& "$env:USERPROFILE\nssm\win64\nssm.exe" install CloudflareTunnel "C:\Program Files\cloudflared\cloudflared.exe" "tunnel run rag-app"
& "$env:USERPROFILE\nssm\win64\nssm.exe" start CloudflareTunnel
```

### Alternative: Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: "When the computer starts"
4. Action: Start a program
5. Program: `C:\Program Files\cloudflared\cloudflared.exe`
6. Arguments: `tunnel run rag-app`
7. Run with highest privileges

---

## Troubleshooting

### Issue: "Connection refused"
- **Solution:** Make sure your app is running on the correct port
- Check: `netstat -an | findstr :8501` (for Streamlit)
- Check: `netstat -an | findstr :8000` (for FastAPI)

### Issue: "Tunnel not found"
- **Solution:** Make sure you're using the correct tunnel name/ID
- List tunnels: `cloudflared tunnel list`

### Issue: "Certificate error"
- **Solution:** Re-login: `cloudflared tunnel login`

### Issue: "DNS not resolving"
- **Solution:** 
  - Wait 1-2 minutes for DNS propagation
  - Check Cloudflare dashboard → DNS → Records
  - Ensure record is "Proxied" (orange cloud)

### Issue: App loads but API calls fail
- **Solution:** 
  - Check FastAPI is running
  - Update `FASTAPI_BASE_URL` in `app.py` to use the tunnel URL
  - Or use relative URLs if both are on same domain

---

## Security Notes

⚠️ **For Exhibition/Demo Only:**
- Quick tunnels are public - anyone with the URL can access
- Consider adding basic authentication for production
- Don't expose sensitive data without proper security

**For Production:**
- Use Cloudflare Access for authentication
- Enable WAF (Web Application Firewall)
- Use proper domain with SSL (automatic with Cloudflare)

---

## Quick Start Commands Summary

```powershell
# 1. Install cloudflared
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile "$env:USERPROFILE\cloudflared.exe"

# 2. Login
cloudflared tunnel login

# 3. Quick tunnel (easiest)
cloudflared tunnel --url http://localhost:8501

# 4. Access the URL shown in terminal
```

---

## Next Steps

1. ✅ Test locally first
2. ✅ Start FastAPI
3. ✅ Start Streamlit  
4. ✅ Start Cloudflare Tunnel
5. ✅ Test from another device
6. ✅ Share the URL for your exhibition!

---

## Support

- Cloudflare Docs: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- Cloudflare Community: https://community.cloudflare.com/
