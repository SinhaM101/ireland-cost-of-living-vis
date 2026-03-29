import Papa from 'papaparse';

export interface CPIData {
  Statistic: string;
  Year: number;
  Category: string;
  Unit: string;
  Value: number;
}

export interface MonthlyCPIData {
  Statistic: string;
  Month: string;
  Category: string;
  Unit: string;
  Value: number;
  Date: Date;
  Year: number;
  MonthNum: number;
}

export interface ConsumptionData {
  Statistic: string;
  Year: number;
  Item: string;
  Unit: string;
  Value: number;
}

async function loadCSV<T>(path: string, transform: (row: any) => T): Promise<T[]> {
  const response = await fetch(path);
  const csvText = await response.text();
  
  return new Promise((resolve, reject) => {
    Papa.parse(csvText, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        const data = results.data.map(transform).filter(item => item !== null);
        resolve(data as T[]);
      },
      error: (error: any) => reject(error)
    });
  });
}

export async function loadAnnualCPI(): Promise<CPIData[]> {
  return loadCSV('/data/Annual EU Index of Consumer Prices.csv', (row) => {
    const year = parseInt(row.Year);
    const value = parseFloat(row.VALUE);
    
    if (isNaN(year) || isNaN(value)) return null as any;
    
    return {
      Statistic: row.Statistic,
      Year: year,
      Category: row['COICOP Classification of Individual Consumption by Purpose'],
      Unit: row.UNIT,
      Value: value
    };
  });
}

export async function loadMonthlyCPI(): Promise<MonthlyCPIData[]> {
  return loadCSV('/data/Monthly EU Consumer Prices by Consumer Price .csv', (row) => {
    const value = parseFloat(row.VALUE);
    if (isNaN(value)) return null as any;
    
    const monthStr = row.Month;
    const [yearStr, monthName] = monthStr.split(' ');
    const year = parseInt(yearStr);
    
    const monthMap: Record<string, number> = {
      'January': 0, 'February': 1, 'March': 2, 'April': 3,
      'May': 4, 'June': 5, 'July': 6, 'August': 7,
      'September': 8, 'October': 9, 'November': 10, 'December': 11
    };
    
    const monthNum = monthMap[monthName];
    const date = new Date(year, monthNum, 1);
    
    return {
      Statistic: row.Statistic,
      Month: monthStr,
      Category: row['COICOP Classification of Individual Consumption by Purpose'],
      Unit: row.UNIT,
      Value: value,
      Date: date,
      Year: year,
      MonthNum: monthNum + 1
    };
  });
}

export async function loadConsumption(): Promise<ConsumptionData[]> {
  return loadCSV('/data/Annual consumption of persional income by item.csv', (row) => {
    const year = parseInt(row.Year);
    const value = parseFloat(row.VALUE);
    
    if (isNaN(year) || isNaN(value)) return null as any;
    
    return {
      Statistic: row.Statistic,
      Year: year,
      Item: row.Item,
      Unit: row.UNIT,
      Value: value
    };
  });
}
