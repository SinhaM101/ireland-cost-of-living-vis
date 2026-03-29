# Ireland Cost of Living Visualization - Next.js Version

This is a Next.js conversion of the Streamlit dashboard, designed for deployment on Vercel.

## Features

- Interactive dashboard with sidebar filters
- Year range selection (2015-2024)
- Category filtering with color-coded checkboxes
- 4 main visualizations:
  1. Price Change by Category (Bar Chart)
  2. Monthly Price Trends (Line Chart)
  3. Economic Periods Analysis (Grouped Bar Chart)
  4. Demographic Burden Analysis (Bar Chart)

## Tech Stack

- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **PapaParse** - CSV parsing

## Local Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Deploy to Vercel

### Option 1: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Option 2: GitHub Integration

1. Push this folder to a GitHub repository
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Vercel will auto-detect Next.js and deploy

## Project Structure

```
ireland-cost-living-nextjs/
├── app/
│   ├── components/          # React components
│   │   ├── Sidebar.tsx
│   │   ├── PriceChangeChart.tsx
│   │   ├── MonthlyTrendsChart.tsx
│   │   ├── EconomicPeriodsChart.tsx
│   │   └── DemographicBurdenChart.tsx
│   ├── lib/                 # Utilities
│   │   ├── constants.ts
│   │   └── dataLoader.ts
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx             # Main dashboard page
├── public/
│   └── data/                # CSV data files
├── package.json
├── tsconfig.json
└── vercel.json
```

## Data Sources

All data sourced from the Central Statistics Office (CSO) Ireland:
- Harmonised Index of Consumer Prices (HICP)
- Household Income Statistics
- Personal Consumption Expenditure
