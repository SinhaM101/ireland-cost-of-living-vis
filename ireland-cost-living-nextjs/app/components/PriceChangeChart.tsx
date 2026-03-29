'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { CATEGORY_COLORS } from '../lib/constants';

interface PriceChangeData {
  category: string;
  change: number;
  baseValue: number;
  latestValue: number;
}

interface PriceChangeChartProps {
  data: PriceChangeData[];
  yearRange: [number, number];
}

export default function PriceChangeChart({ data, yearRange }: PriceChangeChartProps) {
  const sortedData = [...data].sort((a, b) => b.change - a.change);

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">1. Which Price Categories Have Increased the Most?</h2>
      
      <div className="grid grid-cols-3 gap-4">
        <div className="col-span-2">
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={sortedData} layout="vertical" margin={{ left: 150, right: 20 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" label={{ value: `Price Change (%) from ${yearRange[0]} to ${yearRange[1]}`, position: 'insideBottom', offset: -5 }} />
              <YAxis type="category" dataKey="category" width={140} />
              <Tooltip 
                formatter={(value: number) => `${value.toFixed(1)}%`}
                labelFormatter={(label) => `Category: ${label}`}
              />
              <Bar dataKey="change" radius={[0, 4, 4, 0]}>
                {sortedData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={CATEGORY_COLORS[entry.category] || '#666'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Key Findings</h3>
          {sortedData.slice(0, 3).map((item) => (
            <div key={item.category} className="border rounded p-3">
              <div className="text-sm font-medium text-gray-600">{item.category}</div>
              <div className="text-2xl font-bold text-green-600">+{item.change.toFixed(1)}%</div>
              <div className="text-xs text-gray-500">Index: {item.latestValue.toFixed(1)}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
