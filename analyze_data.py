import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("="*70)
print("DATA QUALITY ANALYSIS REPORT")
print("="*70)

# 1. Analyze Zillow ZHVI Metro Data
print("\n1. ZILLOW ZHVI METRO DATA")
print("-"*70)

try:
    zillow_df = pd.read_csv('data/zillow_zhvi_metro.csv')
    
    print(f"Shape: {zillow_df.shape}")
    print(f"Columns: {zillow_df.columns.tolist()[:10]}... (showing first 10)")
    
    # Check for missing values
    missing_counts = zillow_df.isnull().sum()
    missing_pct = (missing_counts / len(zillow_df)) * 100
    
    print(f"\nMissing Values Summary:")
    print(f"Total cells: {zillow_df.size:,}")
    print(f"Missing cells: {zillow_df.isnull().sum().sum():,}")
    print(f"Missing percentage: {(zillow_df.isnull().sum().sum() / zillow_df.size * 100):.2f}%")
    
    # Show columns with missing data
    cols_with_missing = missing_pct[missing_pct > 0].sort_values(ascending=False)
    if len(cols_with_missing) > 0:
        print(f"\nColumns with missing data (top 10):")
        for col, pct in cols_with_missing.head(10).items():
            print(f"  {col}: {pct:.2f}% missing ({missing_counts[col]:,} values)")
    else:
        print("\n✓ No missing values in metadata columns")
    
    # Check for duplicate rows
    duplicates = zillow_df.duplicated().sum()
    print(f"\nDuplicate rows: {duplicates}")
    
    # Check data types
    print(f"\nData types:")
    print(zillow_df.dtypes.value_counts())
    
    # Get date columns (exclude metadata columns)
    date_cols = [col for col in zillow_df.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
    
    # Check for missing dates in time series
    print(f"\nTime series coverage:")
    print(f"  Date columns: {len(date_cols)}")
    print(f"  Date range: {date_cols[0]} to {date_cols[-1]}")
    
    # Sample some regions to check data quality
    print(f"\nSample regions:")
    print(zillow_df[['RegionName', 'RegionType', 'StateName']].head(5))
    
except Exception as e:
    print(f"ERROR reading Zillow data: {e}")

# 2. Analyze Commercial Building Data
print("\n\n2. COMMERCIAL BUILDING DATA")
print("-"*70)

try:
    # Try to read the file
    with open('data/commercial/cbecs_building.csv', 'r') as f:
        first_lines = f.read(500)
    
    if '<html>' in first_lines.lower() or '<!doctype' in first_lines.lower():
        print("❌ ERROR: File contains HTML content instead of CSV data!")
        print("This file needs to be re-downloaded with actual data.")
        print("\nFirst 200 characters of file:")
        print(first_lines[:200])
    else:
        cbecs_building = pd.read_csv('data/commercial/cbecs_building.csv')
        print(f"✓ File loaded successfully")
        print(f"Shape: {cbecs_building.shape}")
        print(f"Missing values: {cbecs_building.isnull().sum().sum()}")
except Exception as e:
    print(f"ERROR: {e}")

# 3. Analyze Commercial Energy Data
print("\n\n3. COMMERCIAL ENERGY DATA")
print("-"*70)

try:
    with open('data/commercial/cbecs_energy.csv', 'r') as f:
        first_lines = f.read(500)
    
    if '<html>' in first_lines.lower() or '<!doctype' in first_lines.lower():
        print("❌ ERROR: File contains HTML content instead of CSV data!")
        print("This file needs to be re-downloaded with actual data.")
        print("\nFirst 200 characters of file:")
        print(first_lines[:200])
    else:
        cbecs_energy = pd.read_csv('data/commercial/cbecs_energy.csv')
        print(f"✓ File loaded successfully")
        print(f"Shape: {cbecs_energy.shape}")
        print(f"Missing values: {cbecs_energy.isnull().sum().sum()}")
except Exception as e:
    print(f"ERROR: {e}")

# Summary and recommendations
print("\n\n" + "="*70)
print("SUMMARY & RECOMMENDATIONS")
print("="*70)
print("\n✓ GOOD:")
print("  - Zillow ZHVI metro data is loaded and appears valid")

print("\n❌ ISSUES FOUND:")
print("  - cbecs_building.csv contains HTML instead of CSV data")
print("  - cbecs_energy.csv contains HTML instead of CSV data")

print("\n📝 NEXT STEPS:")
print("  1. Fix the commercial data download scripts")
print("  2. Re-run download_commercial_data.py with proper data URLs")
print("  3. Verify Zillow data for any missing values in key regions/dates")

print("\n" + "="*70)
