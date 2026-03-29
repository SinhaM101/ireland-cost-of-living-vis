# 🚀 Deploy Ireland Cost of Living Dashboard to Render

## Quick Deploy (5 minutes)

### Step 1: Push to GitHub ✅ DONE
Your code is already pushed to: `https://github.com/SinhaM101/ireland-cost-of-living-vis`

### Step 2: Create Render Account
1. Go to **https://render.com**
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with GitHub (recommended) or email

### Step 3: Deploy Web Service
1. Once logged in, click **"New +"** → **"Web Service"**
2. Click **"Connect a repository"** → Select your GitHub account
3. Find and select: **`SinhaM101/ireland-cost-of-living-vis`**
4. Click **"Connect"**

### Step 4: Configure Deployment Settings

Fill in the following fields:

| Field | Value |
|-------|-------|
| **Name** | `ireland-cost-of-living` (or any name you prefer) |
| **Region** | Choose closest to you (e.g., `Frankfurt (EU Central)` or `Oregon (US West)`) |
| **Branch** | `main` |
| **Root Directory** | Leave blank |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements_dash.txt` |
| **Start Command** | `gunicorn app_dash:server` |
| **Instance Type** | `Free` (or paid if you need more resources) |

### Step 5: Environment Variables (Optional)
No environment variables needed for this app.

### Step 6: Deploy!
1. Click **"Create Web Service"** at the bottom
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements_dash.txt`
   - Start the app with Gunicorn
   - Assign you a public URL

### Step 7: Access Your Live Dashboard
- Deployment takes **3-5 minutes**
- Watch the build logs in real-time
- Once you see **"Your service is live 🎉"**, click the URL at the top
- Your dashboard will be at: `https://ireland-cost-of-living.onrender.com` (or similar)

---

## 📋 Deployment Checklist

✅ **Files Ready:**
- `app_dash.py` - Main application
- `assets/style.css` - Dark theme styling
- `requirements_dash.txt` - Python dependencies
- `Procfile` - Gunicorn configuration
- `data/` - CSV data files

✅ **Code Pushed to GitHub:** `ad138c4`

✅ **Ready to Deploy!**

---

## 🔧 Troubleshooting

### Build fails?
- Check build logs for missing dependencies
- Verify `requirements_dash.txt` is correct
- Ensure Python version is 3.9+

### App crashes on startup?
- Check logs for errors
- Verify `data/` folder exists with CSV files
- Ensure `app_dash.py` has `server = app.server`

### Slow loading?
- Free tier spins down after 15 min of inactivity
- First load after inactivity takes ~30 seconds
- Upgrade to paid tier for always-on service

---

## 🎯 What You'll Get

**Live URL:** `https://your-app-name.onrender.com`

**Features:**
- ✅ Interactive dark-themed dashboard
- ✅ Year range slider (2015-2024)
- ✅ Category filters with color-coded legend
- ✅ 5 interactive Plotly charts with fullscreen mode
- ✅ Responsive design
- ✅ No horizontal scrolling
- ✅ Key findings cards with insights

**Performance:**
- Free tier: 512MB RAM, shared CPU
- Automatic HTTPS
- Auto-deploy on git push
- Custom domain support (paid)

---

## 📱 Share Your Dashboard

Once deployed, share the URL with:
- Colleagues
- Stakeholders
- Portfolio viewers
- Social media

The dashboard is fully public and accessible to anyone with the link!

---

## 🔄 Update Your Dashboard

To update after deployment:

```bash
# Make changes to app_dash.py or assets/style.css
git add .
git commit -m "Update dashboard"
git push origin main
```

Render will **automatically redeploy** within 2-3 minutes!

---

## 💡 Next Steps

1. **Custom Domain:** Add your own domain in Render settings
2. **Analytics:** Add Google Analytics to track visitors
3. **Monitoring:** Set up Render health checks
4. **Scaling:** Upgrade to paid tier for better performance

---

**Need help?** Check the full deployment guide in `RENDER_DEPLOYMENT.md`
