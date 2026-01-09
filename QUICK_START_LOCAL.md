# Quick Start: Run Locally with Cloudflare Tunnel

## Fast Setup (5 minutes)

### Step 1: Install Cloudflare Tunnel

Open PowerShell as Administrator and run:

```powershell
# Download cloudflared
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile "$env:USERPROFILE\cloudflared.exe"

# Move to Program Files
New-Item -ItemType Directory -Force -Path "C:\Program Files\cloudflared" | Out-Null
Move-Item "$env:USERPROFILE\cloudflared.exe" "C:\Program Files\cloudflared\cloudflared.exe" -Force

# Add to PATH
$env:Path += ";C:\Program Files\cloudflared"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::User)
```

### Step 2: Login to Cloudflare

```powershell
cloudflared tunnel login
```

This opens your browser - select your Cloudflare account and authorize.

### Step 3: Start Your App

**Terminal 1 - FastAPI:**
```powershell
cd C:\Users\rajiv_\OneDrive\Desktop\RAG-app\ingestion-phase
python start_api.py
```

**Terminal 2 - Streamlit:**
```powershell
cd C:\Users\rajiv_\OneDrive\Desktop\RAG-app\ingestion-phase
streamlit run app.py --server.port 8501
```

**Terminal 3 - Cloudflare Tunnel:**
```powershell
cloudflared tunnel --url http://localhost:8501
```

Or use the batch file:
```powershell
.\start_cloudflare_tunnel.bat
```

### Step 4: Access Your App

Copy the URL from Terminal 3 (e.g., `https://random-words-1234.trycloudflare.com`)

Open it in any browser on any device!

---

## Troubleshooting

### "cloudflared not found"
- Make sure you added it to PATH
- Or use full path: `C:\Program Files\cloudflared\cloudflared.exe tunnel --url http://localhost:8501`

### "Connection refused"
- Make sure Streamlit is running on port 8501
- Check: `netstat -an | findstr :8501`

### "App loads but API doesn't work"
- Make sure FastAPI is running on port 8000
- The app should automatically connect to `http://localhost:8000` for FastAPI

---

## For Exhibition

1. ✅ Start FastAPI (Terminal 1)
2. ✅ Start Streamlit (Terminal 2)  
3. ✅ Start Tunnel (Terminal 3)
4. ✅ Share the tunnel URL
5. ✅ Access from any device!

**Note:** Quick tunnel URLs change each time. For a permanent URL, see `CLOUDFLARE_TUNNEL_SETUP.md` for named tunnel setup.
