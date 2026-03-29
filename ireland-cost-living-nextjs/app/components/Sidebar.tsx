'use client';

import { CATEGORY_SHORT_NAMES, CATEGORY_COLORS } from '../lib/constants';

interface SidebarProps {
  yearRange: [number, number];
  setYearRange: (range: [number, number]) => void;
  selectedCategories: string[];
  setSelectedCategories: (categories: string[]) => void;
}

export default function Sidebar({
  yearRange,
  setYearRange,
  selectedCategories,
  setSelectedCategories
}: SidebarProps) {
  const allCategories = Object.values(CATEGORY_SHORT_NAMES).filter(c => c !== "All Items");

  const toggleCategory = (category: string) => {
    if (selectedCategories.includes(category)) {
      setSelectedCategories(selectedCategories.filter(c => c !== category));
    } else {
      setSelectedCategories([...selectedCategories, category]);
    }
  };

  return (
    <div className="w-80 bg-gray-50 p-6 border-r border-gray-200 overflow-y-auto">
      <h2 className="text-xl font-bold mb-6">Filters & Controls</h2>
      
      <div className="mb-8">
        <label className="block text-sm font-semibold mb-3">Select Year Range</label>
        <div className="space-y-2">
          <input
            type="range"
            min={2015}
            max={2024}
            value={yearRange[0]}
            onChange={(e) => setYearRange([parseInt(e.target.value), yearRange[1]])}
            className="w-full"
          />
          <input
            type="range"
            min={2015}
            max={2024}
            value={yearRange[1]}
            onChange={(e) => setYearRange([yearRange[0], parseInt(e.target.value)])}
            className="w-full"
          />
          <div className="flex justify-between text-sm text-gray-600">
            <span>{yearRange[0]}</span>
            <span>{yearRange[1]}</span>
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-sm font-semibold mb-3">Select Categories to Compare</h3>
        <div className="space-y-2">
          {allCategories.map((category) => (
            <div key={category} className="flex items-center gap-2">
              <div
                className="w-5 h-5 rounded"
                style={{ backgroundColor: CATEGORY_COLORS[category] }}
              />
              <label className="flex items-center gap-2 cursor-pointer flex-1">
                <input
                  type="checkbox"
                  checked={selectedCategories.includes(category)}
                  onChange={() => toggleCategory(category)}
                  className="cursor-pointer"
                />
                <span className="text-sm">{category}</span>
              </label>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
