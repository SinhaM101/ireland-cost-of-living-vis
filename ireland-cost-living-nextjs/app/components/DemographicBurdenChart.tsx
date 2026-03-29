'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface BurdenData {
  group: string;
  burden: number;
}

interface DemographicBurdenChartProps {
  data: BurdenData[];
}

export default function DemographicBurdenChart({ data }: DemographicBurdenChartProps) {
  const sortedData = [...data].sort((a, b) => b.burden - a.burden);
  const mostAffected = sortedData[0];
  const leastAffected = sortedData[sortedData.length - 1];
  const gap = mostAffected.burden - leastAffected.burden;

  const getColor = (value: number) => {
    const maxBurden = Math.max(...data.map(d => d.burden));
    const intensity = value / maxBurden;
    return `rgba(220, 38, 38, ${0.3 + intensity * 0.7})`;
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">4. Cost-of-Living Burden by Demographic Group</h2>
      
      <p className="text-gray-600 mb-4">
        Different demographic groups experience cost-of-living changes differently based on their spending patterns.
        This analysis calculates a <strong>weighted cost-of-living index</strong> for each group based on typical spending allocations.
      </p>

      <div className="grid grid-cols-3 gap-4">
        <div className="col-span-2">
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={sortedData} layout="vertical" margin={{ left: 150, right: 20 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" label={{ value: 'Weighted Cost-of-Living Increase (%)', position: 'insideBottom', offset: -5 }} />
              <YAxis type="category" dataKey="group" width={140} />
              <Tooltip formatter={(value: number) => `${value.toFixed(1)}%`} />
              <Bar dataKey="burden" radius={[0, 4, 4, 0]}>
                {sortedData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getColor(entry.burden)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Key Findings</h3>
          <div className="border rounded p-3">
            <div className="text-sm font-medium text-gray-600">Most Affected</div>
            <div className="text-xl font-bold">{mostAffected.group}</div>
            <div className="text-lg text-red-600">+{mostAffected.burden.toFixed(1)}%</div>
          </div>
          <div className="border rounded p-3">
            <div className="text-sm font-medium text-gray-600">Least Affected</div>
            <div className="text-xl font-bold">{leastAffected.group}</div>
            <div className="text-lg text-green-600">+{leastAffected.burden.toFixed(1)}%</div>
          </div>
          <div className="border rounded p-3">
            <div className="text-sm font-medium text-gray-600">Burden Gap</div>
            <div className="text-lg font-bold">{gap.toFixed(1)} percentage points</div>
          </div>
        </div>
      </div>
    </div>
  );
}
