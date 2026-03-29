'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { CATEGORY_COLORS } from '../lib/constants';

interface MonthlyDataPoint {
  date: string;
  [key: string]: string | number;
}

interface MonthlyTrendsChartProps {
  data: MonthlyDataPoint[];
  categories: string[];
}

export default function MonthlyTrendsChart({ data, categories }: MonthlyTrendsChartProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">2. How Do Price Increases Differ Over Time?</h2>
      
      <ResponsiveContainer width="100%" height={500}>
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tickFormatter={(date) => new Date(date).getFullYear().toString()}
          />
          <YAxis label={{ value: 'Price Index (Base 2015=100)', angle: -90, position: 'insideLeft' }} />
          <Tooltip 
            labelFormatter={(date) => new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'long' })}
            formatter={(value: number) => value.toFixed(1)}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          {categories.map((category) => (
            <Line
              key={category}
              type="monotone"
              dataKey={category}
              stroke={CATEGORY_COLORS[category] || '#666'}
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 6 }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
