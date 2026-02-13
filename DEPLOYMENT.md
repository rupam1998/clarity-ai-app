# 🚀 Deployment Guide: Clarity AI

This guide covers deploying both the **n8n backend** (to Render) and the **Streamlit frontend** (to Streamlit Cloud).

---

## Part 1: Deploy n8n to Render

### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended) or email
3. Verify your email

### Step 2: Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Select **"Deploy an existing image from a registry"**
3. Enter image URL: `n8nio/n8n:latest`
4. Click **"Next"**

### Step 3: Configure Service

**Basic Settings:**
- **Name:** `clarity-n8n` (or your preferred name)
- **Region:** Choose closest to your users
- **Instance Type:** `Starter` ($7/mo) or `Free` (spins down after 15min)

**Environment Variables:**
```
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your_secure_password_here
N8N_HOST=clarity-n8n.onrender.com
N8N_PROTOCOL=https
N8N_PORT=5678
WEBHOOK_URL=https://clarity-n8n.onrender.com
GENERIC_TIMEZONE=America/New_York
```

### Step 4: Add Persistent Disk (Important!)

1. Scroll to **"Disks"** section
2. Click **"Add Disk"**
3. **Name:** `n8n-data`
4. **Mount Path:** `/home/node/.n8n`
5. **Size:** 1 GB (minimum)

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Once deployed, you'll get a URL like: `https://clarity-n8n.onrender.com`

### Step 6: Access n8n

1. Go to your n8n URL: `https://clarity-n8n.onrender.com`
2. Login with your configured username/password
3. You should see the n8n editor

### Step 7: Import Workflow

1. In n8n, click the **hamburger menu** (☰) → **"Import from File"**
2. Upload `n8n/workflow_webhook.json` from this project
3. The workflow should appear in your editor

### Step 8: Configure Credentials

**Kaggle API (for Live Demo mode):**
1. Go to [kaggle.com/account](https://www.kaggle.com/account)
2. Scroll to "API" → "Create New Token"
3. Download `kaggle.json`
4. In n8n: Settings → Credentials → Add Credential → HTTP Basic Auth
5. Name: `Kaggle API`
6. Username: your Kaggle username
7. Password: your Kaggle API key

**OpenAI API (for AI Insights):**
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create new API key
3. In n8n: Settings → Credentials → Add Credential → Header Auth
4. Name: `OpenAI API`
5. Name: `Authorization`
6. Value: `Bearer sk-your-api-key-here`

### Step 9: Activate Workflow

1. Open the imported workflow
2. Click the **"Active"** toggle in the top right
3. The workflow is now live!

### Step 10: Get Webhook URL

1. Click on the **"Webhook Trigger"** node
2. Copy the **"Production URL"**
3. It should look like: `https://clarity-n8n.onrender.com/webhook/clarity-analyze`
4. **Save this URL** - you'll need it for Streamlit

---

## Part 2: Deploy Streamlit to Streamlit Cloud

### Step 1: Prepare GitHub Repository

1. Create a new GitHub repository: `clarity-ai-app`
2. Push all files from this project:

```bash
git init
git add .
git commit -m "Initial commit: Clarity AI MVP"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/clarity-ai-app.git
git push -u origin main
```

### Step 2: Create Streamlit Cloud Account

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Authorize Streamlit to access your repositories

### Step 3: Deploy App

1. Click **"New app"**
2. Select your repository: `clarity-ai-app`
3. Branch: `main`
4. Main file path: `app.py`
5. Click **"Advanced settings"**

### Step 4: Add Secrets

In the **"Secrets"** section, add:

```toml
N8N_WEBHOOK_URL = "https://clarity-n8n.onrender.com/webhook/clarity-analyze"
```

Replace with your actual n8n webhook URL from Part 1, Step 10.

### Step 5: Deploy

1. Click **"Deploy!"**
2. Wait for deployment (2-5 minutes)
3. Your app will be live at: `https://your-app-name.streamlit.app`

---

## 🧪 Testing the Deployment

### Test 1: Quick Demo Mode

1. Go to your Streamlit app URL
2. Click **"Try Demo"** tab
3. Click **"⚡ Run Quick Demo"**
4. Wait 15-30 seconds
5. You should see results in the **"Results"** tab

### Test 2: Live Demo Mode

1. Go to **"Try Demo"** tab
2. Click **"🌐 Run Live Demo"**
3. Wait 45-60 seconds
4. Check that Kaggle data is being processed

### Test 3: Upload Mode

1. Go to **"Upload Data"** tab
2. Upload a sample CSV file with columns: keyword, spend, clicks, conversions
3. Click **"🚀 Analyze My Data"**
4. Verify results appear

### Test 4: PDF Download

1. After running an analysis
2. Go to **"Results"** tab
3. Click **"📥 Download PDF Report"**
4. Verify the PDF opens correctly

---

## 🔧 Troubleshooting

### n8n Issues

**"Webhook not responding"**
- Check if the workflow is activated (toggle should be ON)
- Verify the webhook URL is correct
- Check Render logs for errors

**"Kaggle API error"**
- Verify Kaggle credentials are correct
- Check if the Kaggle dataset URLs are accessible
- Review n8n execution logs

**"OpenAI error"**
- Verify API key is valid
- Check if you have API credits
- Try reducing max_tokens in the OpenAI node

### Streamlit Issues

**"N8N_WEBHOOK_URL not configured"**
- Add the secret in Streamlit Cloud settings
- Redeploy the app after adding secrets

**"Analysis timed out"**
- Render free tier may spin down - first request wakes it up
- Try again after 30 seconds
- Consider upgrading to Render Starter plan

**"PDF generation error"**
- Check if reportlab is in requirements.txt
- Clear Streamlit cache and redeploy

---

## 📊 Monitoring

### Render Dashboard
- View logs: Render Dashboard → Your Service → Logs
- Check metrics: CPU, Memory, Bandwidth
- Set up alerts for downtime

### Streamlit Cloud
- View app analytics in Streamlit Cloud dashboard
- Check viewer count and session duration
- Monitor for errors in the logs

---

## 💰 Cost Estimates

| Service | Plan | Cost |
|---------|------|------|
| Render (n8n) | Free | $0 (spins down) |
| Render (n8n) | Starter | $7/month (always on) |
| Streamlit Cloud | Community | $0 (public apps) |
| OpenAI API | Pay-as-you-go | ~$0.01-0.05 per analysis |
| Kaggle API | Free | $0 |

**Estimated Monthly Cost:** $0-7/month (depending on Render plan)

---

## 🔄 Updating the App

### Update Streamlit App
1. Make changes locally
2. Push to GitHub
3. Streamlit Cloud auto-deploys on push

### Update n8n Workflow
1. Export updated workflow from n8n
2. Or edit directly in n8n editor
3. Changes take effect immediately

---

## 🆘 Support

If you encounter issues:

1. Check this troubleshooting guide
2. Review Render/Streamlit logs
3. Open an issue on GitHub
4. Contact: [LinkedIn - Rupam Patra](https://linkedin.com/in/rupam-patra)

---

*Last updated: February 2026*
