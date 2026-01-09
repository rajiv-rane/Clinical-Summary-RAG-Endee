# 🚀 Deployment Guide - Clinical Summary RAG Application

This guide will help you deploy your application on **Railway.app** (recommended) or **Render.com** for your project exhibition.

## 📋 Prerequisites

1. **GitHub Account** - Your code should be pushed to GitHub
2. **Groq API Key** - Get one from https://console.groq.com/keys
3. **MongoDB Connection String** - Already configured in your code
4. **Railway Account** - Sign up at https://railway.app (free tier available)

---

## 🎯 Option 1: Railway.app Deployment (Recommended)

Railway.app is the best option because:
- ✅ Free tier with $5 credit monthly
- ✅ No timeout limits
- ✅ Easy deployment from GitHub
- ✅ Automatic HTTPS
- ✅ Environment variable management

### Step 1: Prepare Your Repository

1. Make sure all files are committed and pushed to GitHub:
   ```bash
   git add .
   git commit -m "Add deployment files"
   git push origin main
   ```

### Step 2: Sign Up for Railway

1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (recommended for easy integration)

### Step 3: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `clinical-summary-rag-v2`
4. Select the repository and click **"Deploy Now"**

### Step 4: Configure Deployment

1. Railway will detect the Dockerfile automatically
2. Click on your service
3. Go to **"Settings"** tab
4. Set the **Root Directory** to: `ingestion-phase`
5. Set the **Start Command** to: `/app/start_services.sh`

### Step 5: Configure Environment Variables

1. In your Railway project, go to **"Variables"** tab
2. Add the following environment variables:

   ```
   GROQ_API_KEY=your_groq_api_key_here
   MONGO_URI=your_mongodb_connection_string
   FASTAPI_URL=http://0.0.0.0:$PORT
   PORT=8000
   STREAMLIT_PORT=8501
   PYTHONUNBUFFERED=1
   TRANSFORMERS_CACHE=/app/.cache/transformers
   HF_HOME=/app/.cache/huggingface
   ```

   **Important Notes:**
   - Replace `your_groq_api_key_here` with your actual Groq API key
   - The `PORT` variable is automatically set by Railway
   - `FASTAPI_URL` should point to the internal FastAPI service

### Step 6: Deploy

1. Railway will automatically start building and deploying
2. Wait for the build to complete (5-10 minutes for first build)
3. Once deployed, Railway will provide you with a public URL

### Step 7: Access Your Application

1. Railway provides a public URL like: `https://your-app-name.up.railway.app`
2. The Streamlit app will be accessible at this URL
3. FastAPI will be running internally on port 8000

### Step 8: Custom Domain (Optional)

1. Go to **"Settings"** → **"Domains"**
2. Click **"Generate Domain"** or add your custom domain
3. Railway automatically provides HTTPS

---

## 🎯 Option 2: Render.com Deployment

Render.com is also a good alternative with a free tier.

### Step 1: Sign Up

1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select `clinical-summary-rag-v2`
4. Set **Root Directory** to `ingestion-phase`

### Step 3: Configure Service

- **Name**: `clinical-rag-app`
- **Environment**: `Docker`
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: `ingestion-phase`

### Step 4: Environment Variables

Add the same environment variables as Railway:
```
GROQ_API_KEY=your_groq_api_key_here
MONGO_URI=your_mongodb_connection_string
FASTAPI_URL=http://0.0.0.0:10000
PORT=10000
STREAMLIT_PORT=8501
PYTHONUNBUFFERED=1
```

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will build and deploy automatically
3. Wait for deployment (10-15 minutes first time)

---

## 🔧 Troubleshooting

### Issue: Build Fails

**Solution:**
- Check that all files are committed to GitHub
- Verify Dockerfile is in `ingestion-phase/` directory
- Check build logs for specific errors

### Issue: Application Times Out

**Solution:**
- Railway/Render free tier may have resource limits
- Consider upgrading to paid plan for production
- Check that models are loading correctly

### Issue: FastAPI Not Connecting

**Solution:**
- Verify `FASTAPI_URL` environment variable is set correctly
- Check that FastAPI is running on the correct port
- Review logs to see if FastAPI started successfully

### Issue: Models Not Loading

**Solution:**
- First deployment downloads models (can take 10-15 minutes)
- Check disk space allocation
- Verify `TRANSFORMERS_CACHE` and `HF_HOME` are set

### Issue: MongoDB Connection Failed

**Solution:**
- Verify `MONGO_URI` environment variable is correct
- Check MongoDB Atlas allows connections from Railway/Render IPs
- In MongoDB Atlas, go to Network Access and allow all IPs (0.0.0.0/0) for testing

---

## 📊 Monitoring Your Deployment

### Railway

1. Go to your project dashboard
2. Click on your service
3. View **"Logs"** tab for real-time logs
4. Check **"Metrics"** for resource usage

### Render

1. Go to your service dashboard
2. Click **"Logs"** to view application logs
3. Check **"Metrics"** for performance data

---

## 🎨 Customization for Exhibition

### Update App Title

Edit `ingestion-phase/config.py`:
```python
APP_TITLE = "Your Custom Title"
```

### Add Custom Branding

Modify the header in `ingestion-phase/app.py` around line 2080.

---

## 🚨 Important Notes for Exhibition

1. **First Load Time**: First deployment takes 10-15 minutes due to model downloads
2. **Cold Starts**: Free tier services may have cold starts (30-60 seconds)
3. **Resource Limits**: Free tier has limited CPU/RAM - consider paid plan for better performance
4. **Backup Plan**: Have a local version running as backup
5. **Test Beforehand**: Deploy at least 24 hours before exhibition to test everything

---

## 📞 Quick Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Railway/Render account created
- [ ] Project created and connected to GitHub
- [ ] Environment variables configured
- [ ] Build successful
- [ ] Application accessible via public URL
- [ ] Tested patient search functionality
- [ ] Tested AI assistant
- [ ] Tested summary generation
- [ ] Tested PDF download

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Public URL for your application
- ✅ Automatic HTTPS
- ✅ No timeout limits
- ✅ Persistent storage for vector database
- ✅ Professional deployment ready for exhibition

**Good luck with your exhibition! 🚀**
