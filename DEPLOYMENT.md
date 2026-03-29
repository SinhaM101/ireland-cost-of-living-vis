# Streamlit Deployment Guide

This guide provides step-by-step instructions for deploying the Ireland Cost of Living Analysis dashboard to Streamlit Cloud.

## Prerequisites

- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- Git repository with your code pushed to GitHub

## Project Structure

```
ireland-cost-of-living-vis/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── data/                 # CSV data files
│   ├── Annual EU Index of Consumer Prices.csv
│   ├── Monthly EU Consumer Prices by Consumer Price .csv
│   ├── Annual consumption of persional income by item.csv
│   └── Annual estimates of household income.csv
└── README.md
```

## Deployment Steps

### 1. Push Code to GitHub

Ensure all your files are committed and pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Streamlit deployment"
git push origin main
```

### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Fill in the deployment settings:
   - **Repository**: `SinhaM101/ireland-cost-of-living-vis`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy!"**

### 3. Wait for Deployment

Streamlit Cloud will:
- Clone your repository
- Install dependencies from `requirements.txt`
- Start your app
- Provide you with a public URL (e.g., `https://your-app-name.streamlit.app`)

This typically takes 2-5 minutes.

### 4. Access Your App

Once deployed, you'll receive a URL like:
```
https://ireland-cost-of-living-vis.streamlit.app
```

## Configuration

The app uses the following configuration (`.streamlit/config.toml`):

```toml
[theme]
primaryColor="#E5323B"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
```

## Dependencies

The app requires the following Python packages (from `requirements.txt`):

```
pandas>=2.0.0
altair>=5.0.0
streamlit>=1.28.0
numpy>=1.24.0
```

## Testing Locally

Before deploying, test your app locally:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Updating Your Deployment

To update your deployed app:

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update app"
   git push origin main
   ```
3. Streamlit Cloud will automatically detect the changes and redeploy

## Troubleshooting

### App Won't Start

- Check the logs in Streamlit Cloud dashboard
- Verify all files are in the repository
- Ensure `requirements.txt` has correct package versions

### Data Files Not Found

- Verify the `data/` folder is committed to Git
- Check file paths in `app.py` are relative (e.g., `data/filename.csv`)
- Ensure CSV files are not in `.gitignore`

### Slow Performance

- Streamlit Cloud free tier has resource limits
- Consider caching data with `@st.cache_data`
- Optimize large datasets

## Managing Your App

From the Streamlit Cloud dashboard, you can:

- View app logs
- Restart the app
- Delete the app
- Change settings
- View analytics

## Custom Domain (Optional)

For a custom domain:
1. Upgrade to Streamlit Cloud paid plan
2. Configure DNS settings
3. Add custom domain in Streamlit Cloud settings

## Support

- Streamlit Documentation: [docs.streamlit.io](https://docs.streamlit.io)
- Streamlit Community: [discuss.streamlit.io](https://discuss.streamlit.io)
- GitHub Issues: Report bugs in your repository

## App Features

The deployed dashboard includes:

1. **Price Change Analysis** - Bar chart showing category price changes
2. **Monthly Trends** - Interactive line chart with hover highlighting
3. **Economic Periods** - Comparison across Pre-COVID, COVID, and Inflation Surge periods
4. **Demographic Burden** - Weighted cost-of-living impact by household type
5. **Spending Patterns** - Household consumption trends over time

All visualizations are interactive and respond to sidebar filters for year range and category selection.
