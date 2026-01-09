# ⚡ Quick Deployment Steps for Exhibition

## 🎯 Railway.app (Fastest - Recommended)

### Step 1: Push Code to GitHub
```bash
cd ingestion-phase
git add .
git commit -m "Add deployment configuration"
git push origin main
```

### Step 2: Deploy on Railway

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **Click**: "New Project" → "Deploy from GitHub repo"
4. **Select**: Your repository `clinical-summary-rag-v2`
5. **Wait**: Railway will detect Dockerfile automatically

### Step 3: Configure Service

1. Click on your service
2. Go to **Settings** tab
3. Set **Root Directory**: `ingestion-phase`
4. Set **Start Command**: `/app/start_services.sh`

### Step 4: Add Environment Variables

Go to **Variables** tab and add:

```
GROQ_API_KEY=your_actual_groq_api_key
MONGO_URI=your_mongodb_connection_string
FASTAPI_URL=http://localhost:8000
FASTAPI_PORT=8000
PYTHONUNBUFFERED=1
```

### Step 5: Deploy & Get URL

1. Railway will build automatically (5-10 minutes first time)
2. Once deployed, get your public URL from the dashboard
3. Your app will be live at: `https://your-app-name.up.railway.app`

---

## ✅ Testing Checklist

After deployment, test:
- [ ] App loads without errors
- [ ] Patient search works
- [ ] AI assistant responds
- [ ] Summary generation works
- [ ] PDF download works

---

## 🚨 If Something Goes Wrong

1. **Check Logs**: Railway dashboard → Your service → Logs tab
2. **Verify Environment Variables**: All required vars are set
3. **Check Build**: Make sure Dockerfile build succeeded
4. **Test Locally First**: Run `docker build` and `docker run` locally

---

## 📞 Backup Plan

If deployment fails, you can:
1. Run locally with `streamlit run app.py` and `python start_api.py`
2. Use ngrok to create a public tunnel: `ngrok http 8501`
3. Share the ngrok URL for exhibition

---

**Time Estimate**: 15-20 minutes for deployment
**First Build**: 10-15 minutes (model downloads)
**Subsequent Updates**: 3-5 minutes

Good luck! 🚀
