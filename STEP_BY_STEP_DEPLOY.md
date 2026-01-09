# 🎯 Step-by-Step Deployment Guide

Follow these steps exactly to deploy your application for the exhibition.

---

## 📋 BEFORE YOU START

**Required:**
- ✅ GitHub repository with all code pushed
- ✅ Groq API key (get from https://console.groq.com/keys)
- ✅ MongoDB connection string (already in your code)

**Time needed:** 20-30 minutes

---

## 🚀 STEP 1: Push Deployment Files to GitHub

1. Open terminal/command prompt
2. Navigate to your project:
   ```bash
   cd C:\Users\rajiv_\OneDrive\Desktop\RAG-app
   ```
3. Add all new files:
   ```bash
   git add .
   ```
4. Commit:
   ```bash
   git commit -m "Add deployment configuration for Railway"
   ```
5. Push to GitHub:
   ```bash
   git push origin main
   ```

**✅ Check:** Go to GitHub and verify all files are there.

---

## 🚀 STEP 2: Create Railway Account

1. Go to **https://railway.app**
2. Click **"Start a New Project"** or **"Login"**
3. Choose **"Login with GitHub"**
4. Authorize Railway to access your GitHub account

**✅ Check:** You should see the Railway dashboard.

---

## 🚀 STEP 3: Create New Project

1. In Railway dashboard, click **"New Project"** (big button)
2. Select **"Deploy from GitHub repo"**
3. You'll see a list of your repositories
4. Find and click **"clinical-summary-rag-v2"**
5. Railway will start deploying automatically

**⏳ Wait:** Railway will detect your Dockerfile and start building (this takes 5-10 minutes).

---

## 🚀 STEP 4: Configure the Service

1. Once the service appears, **click on it**
2. Go to the **"Settings"** tab (left sidebar)
3. Railway should automatically detect the Dockerfile in the root directory
4. Verify these settings:
   - **Build Command**: Should auto-detect Docker build
   - **Start Command**: Should be `/app/start_services.sh` (from railway.json)
5. **No need to set Root Directory** - the root Dockerfile handles this

**✅ Check:** Settings are correct (Railway auto-detects Docker).

---

## 🚀 STEP 5: Add Environment Variables

1. In your service, go to **"Variables"** tab (left sidebar)
2. Click **"New Variable"** for each of these:

   **Variable 1:**
   - Name: `GROQ_API_KEY`
   - Value: `your_actual_groq_api_key_here` (paste your real key)
   - Click **"Add"**

   **Variable 2:**
   - Name: `FASTAPI_URL`
   - Value: `http://localhost:8000`
   - Click **"Add"**

   **Variable 3:**
   - Name: `FASTAPI_PORT`
   - Value: `8000`
   - Click **"Add"**

   **Variable 4:**
   - Name: `PYTHONUNBUFFERED`
   - Value: `1`
   - Click **"Add"**

   **Variable 5 (Optional - if you want to override MongoDB):**
   - Name: `MONGO_URI`
   - Value: `your_mongodb_connection_string`
   - Click **"Add"**

**✅ Check:** All 4-5 variables are listed in the Variables tab.

---

## 🚀 STEP 6: Wait for Deployment

1. Go to **"Deployments"** tab (left sidebar)
2. You'll see the build progress
3. **First build takes 10-15 minutes** (downloading models)
4. Watch the logs - you'll see:
   - Installing dependencies
   - Downloading models (this is the slow part)
   - Starting services

**⏳ Be Patient:** The first deployment is slow because it downloads:
- Python packages
- Bio ClinicalBERT model (~400MB)
- Other dependencies

**✅ Check:** Build status shows "Active" or "Deployed"

---

## 🚀 STEP 7: Get Your Public URL

1. Go to **"Settings"** tab
2. Scroll to **"Networking"** section
3. You'll see **"Public Domain"** - this is your app URL!
4. It looks like: `https://your-app-name.up.railway.app`
5. **Copy this URL** - you'll need it!

**✅ Check:** You have a public URL.

---

## 🚀 STEP 8: Test Your Application

1. Open the public URL in your browser
2. Wait for the app to load (30-60 seconds on first load)
3. Test these features:
   - ✅ App loads without errors
   - ✅ Search for a patient
   - ✅ Ask AI assistant a question
   - ✅ Generate a discharge summary
   - ✅ Download PDF

**✅ Check:** All features work correctly.

---

## 🎉 SUCCESS!

Your application is now live and ready for the exhibition!

**Your public URL:** `https://your-app-name.up.railway.app`

---

## 🚨 TROUBLESHOOTING

### Problem: Build Failed
**Solution:**
- Check the **Logs** tab for errors
- Verify all files are in GitHub
- Make sure Dockerfile is in `ingestion-phase/` folder

### Problem: App Won't Start
**Solution:**
- Check **Logs** tab for error messages
- Verify all environment variables are set
- Check that GROQ_API_KEY is correct

### Problem: Models Not Loading
**Solution:**
- First deployment takes 10-15 minutes for models
- Check logs - you should see "Downloading model..."
- Wait patiently - this is normal!

### Problem: FastAPI Not Connecting
**Solution:**
- Verify `FASTAPI_URL` is set to `http://localhost:8000`
- Check logs to see if FastAPI started
- Both services should be running

### Problem: Timeout or Slow
**Solution:**
- Free tier has resource limits
- First load is always slow (model loading)
- Subsequent loads are faster
- Consider upgrading to paid plan for better performance

---

## 📞 BACKUP PLAN

If Railway doesn't work, use **ngrok** for local deployment:

1. Install ngrok: https://ngrok.com/download
2. Run your app locally:
   ```bash
   cd ingestion-phase
   python start_api.py  # Terminal 1
   streamlit run app.py  # Terminal 2
   ```
3. In a new terminal:
   ```bash
   ngrok http 8501
   ```
4. Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)
5. Share this URL for exhibition

---

## ✅ FINAL CHECKLIST

Before exhibition:
- [ ] Application is deployed and accessible
- [ ] All features tested and working
- [ ] Public URL saved and ready to share
- [ ] Backup plan ready (ngrok) just in case
- [ ] Tested on different devices/browsers

---

**You're all set! Good luck with your exhibition! 🚀**
