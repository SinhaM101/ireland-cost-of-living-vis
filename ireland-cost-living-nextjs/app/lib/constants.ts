export const MAIN_CATEGORIES = [
  "All-items HICP (COICOP 00)",
  "Food and non-alcoholic beverages (COICOP 01)",
  "Alcoholic beverages, tobacco and narcotics (COICOP 02)",
  "Clothing and footwear (COICOP 03)",
  "Housing, water, electricity, gas and other fuels (COICOP 04)",
  "Furnishings, household equipment and routine household maintenance (COICOP 05)",
  "Health (COICOP 06)",
  "Transport (COICOP 07)",
  "Communications (COICOP 08)",
  "Recreation and culture (COICOP 09)",
  "Education (COICOP 10)",
  "Restaurants and hotels (COICOP 11)",
  "Miscellaneous goods and services (COICOP 12)"
];

export const CATEGORY_SHORT_NAMES: Record<string, string> = {
  "All-items HICP (COICOP 00)": "All Items",
  "Food and non-alcoholic beverages (COICOP 01)": "Food & Beverages",
  "Alcoholic beverages, tobacco and narcotics (COICOP 02)": "Alcohol & Tobacco",
  "Clothing and footwear (COICOP 03)": "Clothing & Footwear",
  "Housing, water, electricity, gas and other fuels (COICOP 04)": "Housing & Utilities",
  "Furnishings, household equipment and routine household maintenance (COICOP 05)": "Furnishings",
  "Health (COICOP 06)": "Health",
  "Transport (COICOP 07)": "Transport",
  "Communications (COICOP 08)": "Communications",
  "Recreation and culture (COICOP 09)": "Recreation & Culture",
  "Education (COICOP 10)": "Education",
  "Restaurants and hotels (COICOP 11)": "Restaurants & Hotels",
  "Miscellaneous goods and services (COICOP 12)": "Miscellaneous"
};

export const CATEGORY_COLORS: Record<string, string> = {
  "All Items": "#929084",
  "Food & Beverages": "#E5323B",
  "Alcohol & Tobacco": "#A997DF",
  "Clothing & Footwear": "#BDD9BF",
  "Housing & Utilities": "#2E4052",
  "Furnishings": "#8B7355",
  "Health": "#FFC857",
  "Transport": "#5B8A72",
  "Communications": "#D4A5A5",
  "Recreation & Culture": "#7B68EE",
  "Education": "#FF8C42",
  "Restaurants & Hotels": "#6B5B95",
  "Miscellaneous": "#88B04B"
};

export const ESSENTIAL_CATEGORIES = [
  "Food and non-alcoholic beverages (COICOP 01)",
  "Housing, water, electricity, gas and other fuels (COICOP 04)",
  "Health (COICOP 06)",
  "Transport (COICOP 07)",
  "Education (COICOP 10)"
];

export const ECONOMIC_PERIODS = {
  'Pre-COVID (2015-2019)': [2015, 2019],
  'COVID (2020-2021)': [2020, 2021],
  'Inflation Surge (2022-2023)': [2022, 2023]
} as const;

export const DEMOGRAPHIC_PROFILES: Record<string, Record<string, number>> = {
  'Low Income Household': {
    'Food & Beverages': 0.20,
    'Housing & Utilities': 0.35,
    'Transport': 0.10,
    'Health': 0.05,
    'Education': 0.03,
    'Clothing & Footwear': 0.05,
    'Communications': 0.04,
    'Recreation & Culture': 0.05,
    'Restaurants & Hotels': 0.03,
    'Alcohol & Tobacco': 0.04,
    'Furnishings': 0.03,
    'Miscellaneous': 0.03
  },
  'Middle Income Household': {
    'Food & Beverages': 0.15,
    'Housing & Utilities': 0.25,
    'Transport': 0.15,
    'Health': 0.05,
    'Education': 0.05,
    'Clothing & Footwear': 0.06,
    'Communications': 0.03,
    'Recreation & Culture': 0.10,
    'Restaurants & Hotels': 0.08,
    'Alcohol & Tobacco': 0.03,
    'Furnishings': 0.03,
    'Miscellaneous': 0.02
  },
  'High Income Household': {
    'Food & Beverages': 0.10,
    'Housing & Utilities': 0.15,
    'Transport': 0.12,
    'Health': 0.06,
    'Education': 0.08,
    'Clothing & Footwear': 0.08,
    'Communications': 0.02,
    'Recreation & Culture': 0.15,
    'Restaurants & Hotels': 0.12,
    'Alcohol & Tobacco': 0.02,
    'Furnishings': 0.05,
    'Miscellaneous': 0.05
  },
  'Renters': {
    'Food & Beverages': 0.15,
    'Housing & Utilities': 0.40,
    'Transport': 0.10,
    'Health': 0.04,
    'Education': 0.04,
    'Clothing & Footwear': 0.05,
    'Communications': 0.03,
    'Recreation & Culture': 0.07,
    'Restaurants & Hotels': 0.05,
    'Alcohol & Tobacco': 0.03,
    'Furnishings': 0.02,
    'Miscellaneous': 0.02
  },
  'Homeowners': {
    'Food & Beverages': 0.14,
    'Housing & Utilities': 0.18,
    'Transport': 0.15,
    'Health': 0.06,
    'Education': 0.06,
    'Clothing & Footwear': 0.06,
    'Communications': 0.03,
    'Recreation & Culture': 0.12,
    'Restaurants & Hotels': 0.10,
    'Alcohol & Tobacco': 0.03,
    'Furnishings': 0.04,
    'Miscellaneous': 0.03
  },
  'Family with Children': {
    'Food & Beverages': 0.18,
    'Housing & Utilities': 0.22,
    'Transport': 0.14,
    'Health': 0.05,
    'Education': 0.12,
    'Clothing & Footwear': 0.08,
    'Communications': 0.03,
    'Recreation & Culture': 0.08,
    'Restaurants & Hotels': 0.04,
    'Alcohol & Tobacco': 0.01,
    'Furnishings': 0.03,
    'Miscellaneous': 0.02
  }
};
