# Zillow Data Visualization Template

This repository is a simple starter template that shows how to build basic
data visualizations in Python using Zillow data. It includes a minimal
download snippet and a list of charts you can create from the dataset.

## Data Source

- Main Zillow research data portal:
  https://www.zillow.com/research/data/
- Direct CSV download link:
  https://files.zillowstatic.com/research/public_csvs/zhvi/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1770057731

## Charts to Build

- **Histogram**: Data + Position(x, freq) + Bar  
  Shows: distribution shape
- **Box Plot**: Data + Position(group, value) + Box  
  Shows: median, quartiles, outliers
- **Line Plot**: Data + Position(x, y) + Line  
  Shows: trends over time
- **Density Plot**: Data + Position(x, density) + Smooth  
  Shows: smooth distribution

## Quick Start: Download Zillow Data (Python)

The snippet below downloads the CSV into a local `data/` folder.
It uses only the Python standard library.

```python
from pathlib import Path
from urllib.request import urlretrieve

DATA_URL = (
    "https://files.zillowstatic.com/research/public_csvs/zhvi/"
    "Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1770057731"
)
DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = DATA_DIR / "zillow_zhvi_metro.csv"

urlretrieve(DATA_URL, OUTPUT_PATH)
print(f"Saved data to: {OUTPUT_PATH.resolve()}")
```

## Next Steps

1. Load the CSV into pandas.
2. Choose a metro or subset of columns for the visual you want.
3. Create the charts listed above with matplotlib or seaborn.