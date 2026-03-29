# Deploy to Vercel - Step by Step Guide

## Prerequisites
- GitHub account
- Vercel account (free tier available at [vercel.com](https://vercel.com))

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Create a new GitHub repository**
   ```bash
   cd ireland-cost-living-nextjs
   git init
   git add .
   git commit -m "Initial commit - Next.js Ireland Cost of Living Dashboard"
   ```

2. **Push to GitHub**
   ```bash
   # Create a new repository on GitHub first, then:
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy on Vercel**
   - Go to [vercel.com](https://vercel.com) and sign in
   - Click "Add New Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js settings
   - Click "Deploy"
   - Your app will be live in ~2 minutes!

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   cd ireland-cost-living-nextjs
   vercel
   ```

3. **Follow the prompts**
   - Link to existing project or create new
   - Confirm settings
   - Deploy!

## Your Dashboard Features

✅ **Same layout as Streamlit version**
- Sidebar with filters (year range + category selection)
- Color-coded category checkboxes
- 4 main visualizations matching your original design

✅ **Interactive Charts**
- Price Change by Category (horizontal bar chart)
- Monthly Price Trends (multi-line chart)
- Economic Periods Analysis (grouped bar chart)
- Demographic Burden Analysis (bar chart with metrics)

✅ **Production Ready**
- Built with Next.js 15 + TypeScript
- Optimized for Vercel deployment
- Fast loading with static generation
- Responsive design with Tailwind CSS

## Post-Deployment

After deployment, Vercel will give you:
- **Production URL**: `https://your-app.vercel.app`
- **Automatic deployments**: Every push to `main` branch auto-deploys
- **Preview deployments**: Pull requests get preview URLs
- **Analytics**: Built-in performance monitoring

## Troubleshooting

If you encounter issues:
1. Check build logs in Vercel dashboard
2. Ensure all data files are in `public/data/` folder
3. Verify Node.js version (should be 18+)

## Custom Domain (Optional)

To add a custom domain:
1. Go to your project in Vercel dashboard
2. Click "Settings" → "Domains"
3. Add your domain and follow DNS instructions
