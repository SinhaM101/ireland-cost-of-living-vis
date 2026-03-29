# Render Deployment Guide - Dash Application

## 🚀 Quick Deploy to Render

This guide will help you deploy the Ireland Cost of Living Dashboard to Render in ~10 minutes.

---

## 📋 Prerequisites

- GitHub account
- Render account (free at [render.com](https://render.com))
- Git repository with code pushed to GitHub

---

## 📁 Project Structure

```
ireland-cost-of-living-vis/
├── app_dash.py              # Main Dash application (server exposed)
├── assets/
│   └── style.css           # Dark theme CSS styling
├── data/                   # CSV data files
│   ├── Annual EU Index of Consumer Prices.csv
│   ├── Monthly EU Consumer Prices by Consumer Price .csv
│   ├── Annual consumption of persional income by item.csv
│   └── Annual estimates of household income.csv
├── requirements_dash.txt   # Python dependencies
├── Procfile               # Render deployment config
└── RENDER_DEPLOYMENT.md   # This file
```

---

## 🔧 Deployment Steps

### 1. Push Code to GitHub

Ensure all files are committed and pushed:

```bash
git add app_dash.py assets/ Procfile requirements_dash.txt data/
git commit -m "Add Dash app for Render deployment"
git push origin main
```

### 2. Create New Web Service on Render

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `SinhaM101/ireland-cost-of-living-vis`

### 3. Configure Web Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `ireland-cost-living-dashboard` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: Leave blank (or specify if in subdirectory)

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements_dash.txt`
- **Start Command**: `gunicorn app_dash:server`

**Instance Type:**
- Select **Free** tier (or paid for better performance)

### 4. Environment Variables (Optional)

If needed, add environment variables in the "Environment" section:
- No environment variables required for basic deployment

### 5. Deploy

1. Click **"Create Web Service"**
2. Render will:
   - Clone your repository
   - Install dependencies from `requirements_dash.txt`
   - Start the app using the Procfile command
   - Provide a public URL (e.g., `https://ireland-cost-living-dashboard.onrender.com`)

**Deployment typically takes 3-5 minutes.**

---

## 🌐 Access Your App

Once deployed, your dashboard will be available at:
```
https://your-app-name.onrender.com
```

---

## 📦 Files Explained

### `app_dash.py`
- Main Dash application
- **Critical**: Exposes `server = app.server` for Gunicorn
- Contains all dashboard sections and callbacks
- Configured for production deployment

### `assets/style.css`
- Dark theme styling
- Automatically loaded by Dash
- Responsive design with mobile support

### `requirements_dash.txt`
```
dash==2.14.2
plotly==5.18.0
pandas==2.0.3
numpy==1.24.3
gunicorn==21.2.0
```

### `Procfile`
```
web: gunicorn app_dash:server
```
- Tells Render how to start the application
- Uses Gunicorn WSGI server for production

---

## 🔄 Updating Your Deployment

To update your deployed app:

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update dashboard"
   git push origin main
   ```
3. Render will **automatically detect changes and redeploy**

---

## 🐛 Troubleshooting

### App Won't Start

**Check Render Logs:**
1. Go to your Render dashboard
2. Click on your web service
3. View "Logs" tab

**Common Issues:**
- **Missing dependencies**: Ensure all packages are in `requirements_dash.txt`
- **Data files not found**: Verify `data/` folder is committed to Git
- **Port issues**: Render automatically assigns ports; don't hardcode

### Data Files Not Loading

**Verify:**
- CSV files are in the `data/` directory
- `data/` folder is NOT in `.gitignore`
- File paths in `app_dash.py` are relative: `data/filename.csv`

### Slow Performance

**Free Tier Limitations:**
- Render free tier has resource limits
- App may sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds

**Solutions:**
- Upgrade to paid tier for always-on service
- Optimize data loading with caching
- Reduce dataset size if possible

---

## 🎨 Dashboard Features

The deployed dashboard includes:

### Section 1: Price Categories Analysis
- Horizontal bar chart showing which categories increased most
- Key findings cards with top 3 increases

### Section 2: Time Series Trends
- Multi-line interactive chart
- Monthly data from 2015-2024
- Category filtering via legend

### Section 3: Economic Periods
- Grouped bar chart by economic period
- Dropdown selector for specific periods
- Pre-COVID, COVID, and Inflation Surge analysis

### Section 4: Demographic Burden
- Weighted cost-of-living impact by household type
- Key findings for most/least affected groups

### Section 5: Spending Patterns
- Stacked area chart
- Household spending trends over time

### Summary Section
- Three-column key insights
- Highest increases, economic periods, demographic impact

---

## 🔒 Security Notes

- No sensitive data or API keys required
- All data is static CSV files
- No user authentication needed
- Safe for public deployment

---

## 💰 Cost

**Free Tier:**
- 750 hours/month (enough for one always-on service)
- Automatic sleep after 15 minutes of inactivity
- Perfect for portfolio/demo projects

**Paid Tier ($7/month):**
- Always-on service
- Better performance
- Custom domains
- More resources

---

## 📊 Monitoring

**Render Dashboard provides:**
- Real-time logs
- Deployment history
- Resource usage metrics
- Health checks

---

## 🆘 Support

**Render Documentation:**
- [Render Docs](https://render.com/docs)
- [Python Deployment Guide](https://render.com/docs/deploy-flask)

**Dash Documentation:**
- [Dash Docs](https://dash.plotly.com/)
- [Deployment Guide](https://dash.plotly.com/deployment)

**Project Issues:**
- Report bugs in your GitHub repository
- Check Render logs for deployment errors

---

## ✅ Deployment Checklist

Before deploying, ensure:

- [ ] All code committed and pushed to GitHub
- [ ] `requirements_dash.txt` includes all dependencies
- [ ] `Procfile` exists with correct command
- [ ] `data/` folder is committed (not in `.gitignore`)
- [ ] `app_dash.py` exposes `server = app.server`
- [ ] `assets/style.css` exists for styling
- [ ] Tested locally with `python app_dash.py`

---

## 🎯 Next Steps

1. **Test Locally First:**
   ```bash
   python app_dash.py
   # Visit http://localhost:8050
   ```

2. **Deploy to Render:**
   - Follow steps above
   - Wait for deployment to complete

3. **Share Your Dashboard:**
   - Get public URL from Render
   - Share with stakeholders
   - Add to portfolio/resume

---

## 📝 Notes

- **Data Sources**: CSO Ireland (HICP, Household Income, Consumption)
- **Base Year**: 2015 = 100
- **Methodology**: Weighted demographic basket approach
- **Last Updated**: 2024

---

**Your dashboard is now production-ready and deployable to Render! 🎉**
