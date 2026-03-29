'use client';

import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import PriceChangeChart from './components/PriceChangeChart';
import MonthlyTrendsChart from './components/MonthlyTrendsChart';
import EconomicPeriodsChart from './components/EconomicPeriodsChart';
import DemographicBurdenChart from './components/DemographicBurdenChart';
import { loadAnnualCPI, loadMonthlyCPI, CPIData, MonthlyCPIData } from './lib/dataLoader';
import { MAIN_CATEGORIES, CATEGORY_SHORT_NAMES, ESSENTIAL_CATEGORIES, ECONOMIC_PERIODS, DEMOGRAPHIC_PROFILES } from './lib/constants';

export default function Home() {
  const [yearRange, setYearRange] = useState<[number, number]>([2015, 2024]);
  const [selectedCategories, setSelectedCategories] = useState<string[]>(
    Object.values(CATEGORY_SHORT_NAMES).filter(c => c !== "All Items")
  );
  
  const [annualData, setAnnualData] = useState<CPIData[]>([]);
  const [monthlyData, setMonthlyData] = useState<MonthlyCPIData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [annual, monthly] = await Promise.all([
          loadAnnualCPI(),
          loadMonthlyCPI()
        ]);
        setAnnualData(annual);
        setMonthlyData(monthly);
        setLoading(false);
      } catch (error) {
        console.error('Error loading data:', error);
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const reverseShortNames = Object.fromEntries(
    Object.entries(CATEGORY_SHORT_NAMES).map(([k, v]) => [v, k])
  );
  const selectedFullCategories = selectedCategories.map(c => reverseShortNames[c]);

  const filteredAnnual = annualData.filter(
    d => d.Statistic === 'Harmonised Index of Consumer Prices' &&
         MAIN_CATEGORIES.includes(d.Category) &&
         d.Year >= yearRange[0] &&
         d.Year <= yearRange[1]
  );

  const priceChangeData = MAIN_CATEGORIES
    .filter(cat => cat !== "All-items HICP (COICOP 00)")
    .map(cat => {
      const baseData = filteredAnnual.find(d => d.Category === cat && d.Year === yearRange[0]);
      const latestData = filteredAnnual.find(d => d.Category === cat && d.Year === yearRange[1]);
      
      if (baseData && latestData && baseData.Value > 0) {
        const change = ((latestData.Value - baseData.Value) / baseData.Value) * 100;
        return {
          category: CATEGORY_SHORT_NAMES[cat],
          change,
          baseValue: baseData.Value,
          latestValue: latestData.Value
        };
      }
      return null;
    })
    .filter((d): d is NonNullable<typeof d> => d !== null)
    .filter(d => selectedCategories.includes(d.category));

  const filteredMonthly = monthlyData.filter(
    d => d.Statistic === 'EU HICP' &&
         selectedFullCategories.includes(d.Category) &&
         d.Year >= yearRange[0] &&
         d.Year <= yearRange[1]
  );

  const monthlyTrendsData: any[] = [];
  const dateMap = new Map<string, any>();

  filteredMonthly.forEach(d => {
    const dateKey = d.Date.toISOString();
    if (!dateMap.has(dateKey)) {
      dateMap.set(dateKey, { date: dateKey });
    }
    const shortName = CATEGORY_SHORT_NAMES[d.Category];
    dateMap.get(dateKey)[shortName] = d.Value;
  });

  dateMap.forEach(value => monthlyTrendsData.push(value));
  monthlyTrendsData.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  const periodData: any[] = [];
  Object.entries(ECONOMIC_PERIODS).forEach(([periodName, [startYear, endYear]]) => {
    MAIN_CATEGORIES.forEach(cat => {
      if (cat === "All-items HICP (COICOP 00)") return;
      
      const startData = annualData.find(d => 
        d.Statistic === 'Harmonised Index of Consumer Prices' &&
        d.Category === cat &&
        d.Year === startYear
      );
      const endData = annualData.find(d => 
        d.Statistic === 'Harmonised Index of Consumer Prices' &&
        d.Category === cat &&
        d.Year === endYear
      );
      
      if (startData && endData && startData.Value > 0) {
        const totalChange = ((endData.Value - startData.Value) / startData.Value) * 100;
        const years = endYear - startYear + 1;
        const annualChange = totalChange / years;
        
        const shortName = CATEGORY_SHORT_NAMES[cat];
        if (selectedCategories.includes(shortName)) {
          periodData.push({
            category: shortName,
            period: periodName,
            annualChange,
            totalChange
          });
        }
      }
    });
  });

  const categoryChanges: Record<string, number> = {};
  MAIN_CATEGORIES.forEach(cat => {
    if (cat === "All-items HICP (COICOP 00)") return;
    const startData = filteredAnnual.find(d => d.Category === cat && d.Year === yearRange[0]);
    const endData = filteredAnnual.find(d => d.Category === cat && d.Year === yearRange[1]);
    if (startData && endData && startData.Value > 0) {
      const change = ((endData.Value - startData.Value) / startData.Value) * 100;
      categoryChanges[CATEGORY_SHORT_NAMES[cat]] = change;
    }
  });

  const burdenData = Object.entries(DEMOGRAPHIC_PROFILES).map(([groupName, weights]) => {
    let weightedChange = 0;
    Object.entries(weights).forEach(([category, weight]) => {
      if (categoryChanges[category]) {
        weightedChange += weight * categoryChanges[category];
      }
    });
    return {
      group: groupName,
      burden: weightedChange
    };
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Loading data...</div>
      </div>
    );
  }

  return (
    <div className="flex h-screen">
      <Sidebar
        yearRange={yearRange}
        setYearRange={setYearRange}
        selectedCategories={selectedCategories}
        setSelectedCategories={setSelectedCategories}
      />
      
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-7xl mx-auto p-8">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2">Ireland Cost of Living Analysis (2015-2024)</h1>
            <p className="text-gray-600">
              This interactive dashboard explores how the cost of living has changed in Ireland since 2015,
              examining which price categories have increased the most, how changes evolved across economic periods
              (pre-COVID, COVID, inflation surge), and which demographic groups face the greatest burden.
            </p>
          </div>

          <div className="space-y-8">
            <PriceChangeChart data={priceChangeData} yearRange={yearRange} />
            
            <div className="border-t pt-8">
              <MonthlyTrendsChart data={monthlyTrendsData} categories={selectedCategories} />
            </div>
            
            <div className="border-t pt-8">
              <EconomicPeriodsChart data={periodData} />
            </div>
            
            <div className="border-t pt-8">
              <DemographicBurdenChart data={burdenData} />
            </div>

            <div className="border-t pt-8">
              <div className="bg-gray-50 p-6 rounded-lg">
                <h2 className="text-2xl font-bold mb-4">Key Insights & Summary</h2>
                <div className="grid grid-cols-3 gap-6">
                  <div>
                    <h3 className="font-semibold mb-2">Highest Price Increases</h3>
                    <ul className="space-y-1 text-sm">
                      {priceChangeData.slice(0, 3).map(item => (
                        <li key={item.category}>
                          <strong>{item.category}:</strong> +{item.change.toFixed(1)}%
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h3 className="font-semibold mb-2">Economic Periods</h3>
                    <p className="text-sm">
                      Worst period: <strong>Inflation Surge (2022-2023)</strong>
                    </p>
                  </div>
                  <div>
                    <h3 className="font-semibold mb-2">Demographic Impact</h3>
                    <p className="text-sm">
                      Most affected: <strong>{burdenData[0]?.group}</strong>
                      <br />
                      Burden: <strong>+{burdenData[0]?.burden.toFixed(1)}%</strong>
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="border-t pt-8 pb-8">
              <div className="text-sm text-gray-600">
                <p className="mb-2">
                  <strong>Data Sources:</strong> Central Statistics Office (CSO) Ireland - Harmonised Index of Consumer Prices (HICP),
                  Household Income Statistics, Personal Consumption Expenditure
                </p>
                <p>
                  <strong>Methodology:</strong> Price indices are based on 2015=100. Economic periods defined as Pre-COVID (2015-2019),
                  COVID (2020-2021), Inflation Surge (2022-2023). Demographic burden calculated
                  using weighted spending profiles based on CSO Household Budget Survey patterns.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
