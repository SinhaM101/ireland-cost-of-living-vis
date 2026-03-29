'use client';

import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { CATEGORY_COLORS } from '../lib/constants';

interface PeriodData {
  category: string;
  period: string;
  annualChange: number;
  totalChange: number;
}

interface EconomicPeriodsChartProps {
  data: PeriodData[];
}

export default function EconomicPeriodsChart({ data }: EconomicPeriodsChartProps) {
  const [selectedPeriod, setSelectedPeriod] = useState<string>('All Periods');
  
  const periods = ['All Periods', 'Pre-COVID (2015-2019)', 'COVID (2020-2021)', 'Inflation Surge (2022-2023)'];
  
  const filteredData = selectedPeriod === 'All Periods' 
    ? data 
    : data.filter(d => d.period === selectedPeriod);

  const sortedData = [...filteredData].sort((a, b) => b.annualChange - a.annualChange);

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">3. Price Changes Across Economic Periods</h2>
      
      <p className="text-gray-600 mb-4">
        Analyzing how price changes evolved across three distinct economic periods:
        <strong> Pre-COVID (2015-2019)</strong> - Stable growth period,
        <strong> COVID (2020-2021)</strong> - Pandemic disruptions, supply chain issues,
        <strong> Inflation Surge (2022-2023)</strong> - Energy crisis, post-pandemic inflation
      </p>

      <div className="mb-4">
        <label className="block text-sm font-semibold mb-2">Select Economic Period</label>
        <select
          value={selectedPeriod}
          onChange={(e) => setSelectedPeriod(e.target.value)}
          className="border border-gray-300 rounded px-4 py-2"
        >
          {periods.map(period => (
            <option key={period} value={period}>{period}</option>
          ))}
        </select>
      </div>

      <ResponsiveContainer width="100%" height={450}>
        <BarChart data={sortedData} layout="vertical" margin={{ left: 150, right: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" label={{ value: 'Avg Annual Price Change (%)', position: 'insideBottom', offset: -5 }} />
          <YAxis type="category" dataKey="category" width={140} />
          <Tooltip 
            formatter={(value: number) => `${value.toFixed(1)}%`}
            labelFormatter={(label) => `Category: ${label}`}
          />
          <Bar dataKey="annualChange" radius={[0, 4, 4, 0]}>
            {sortedData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={CATEGORY_COLORS[entry.category] || '#666'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
