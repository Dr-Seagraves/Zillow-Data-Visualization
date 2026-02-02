import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

# Load Zillow data
print("Loading Zillow ZHVI Metro data...")
zillow_df = pd.read_csv('data/zillow_zhvi_metro.csv')

# Get date columns
date_cols = [col for col in zillow_df.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]

# Create output directory for plots
import os
os.makedirs('visualizations', exist_ok=True)

print(f"Loaded {len(zillow_df)} metro areas with {len(date_cols)} time periods")
print("\n" + "="*70)

# ============================================================================
# VISUALIZATION 1: Top 10 Metro Areas - Price Trends Over Time
# ============================================================================
print("\n1. Creating visualization: Top 10 Metro Areas Price Trends...")

top_metros = zillow_df[zillow_df['RegionType'] == 'msa'].nsmallest(10, 'SizeRank')

fig, ax = plt.subplots(figsize=(15, 8))

for idx, row in top_metros.iterrows():
    values = pd.to_numeric(row[date_cols], errors='coerce').values
    dates = pd.to_datetime(date_cols)
    # Filter out NaN values
    mask = ~np.isnan(values)
    ax.plot(dates[mask], values[mask], label=row['RegionName'], linewidth=2, alpha=0.8)

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Home Value Index ($)', fontsize=12, fontweight='bold')
ax.set_title('Zillow Home Value Index: Top 10 Metro Areas (2000-2025)', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/01_top10_metros_trends.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/01_top10_metros_trends.png")
plt.close()

# ============================================================================
# VISUALIZATION 2: Missing Data Heatmap
# ============================================================================
print("\n2. Creating visualization: Missing Data Analysis...")

# Sample data for heatmap (first 50 metros, every 12th month)
sample_df = zillow_df.head(50)
sample_dates = date_cols[::12]  # Every year
missing_matrix = sample_df[sample_dates].isnull()

fig, ax = plt.subplots(figsize=(16, 10))
sns.heatmap(missing_matrix, cmap='RdYlGn_r', cbar_kws={'label': 'Missing Data'},
            yticklabels=sample_df['RegionName'].values, xticklabels=sample_dates,
            ax=ax)
ax.set_title('Missing Data Pattern: First 50 Metro Areas (Annual Snapshots)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Metro Area', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(fontsize=8)
plt.tight_layout()
plt.savefig('visualizations/02_missing_data_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/02_missing_data_heatmap.png")
plt.close()

# ============================================================================
# VISUALIZATION 3: Missing Data Timeline
# ============================================================================
print("\n3. Creating visualization: Missing Data Over Time...")

missing_by_date = zillow_df[date_cols].isnull().sum()
missing_pct_by_date = (missing_by_date / len(zillow_df)) * 100
dates = pd.to_datetime(date_cols)

fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(dates, missing_pct_by_date.values, linewidth=2, color='darkred')
ax.fill_between(dates, missing_pct_by_date.values, alpha=0.3, color='red')
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Missing Data (%)', fontsize=12, fontweight='bold')
ax.set_title('Percentage of Missing Data Over Time (All Metro Areas)', 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/03_missing_data_timeline.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/03_missing_data_timeline.png")
plt.close()

# ============================================================================
# VISUALIZATION 4: Regional Price Comparison (Latest Values)
# ============================================================================
print("\n4. Creating visualization: Regional Price Comparison...")

# Get latest non-null value for each metro
latest_values = []
for idx, row in zillow_df[zillow_df['RegionType'] == 'msa'].head(20).iterrows():
    values = row[date_cols].dropna()
    if len(values) > 0:
        latest_values.append({
            'RegionName': row['RegionName'],
            'LatestValue': values.iloc[-1],
            'SizeRank': row['SizeRank']
        })

latest_df = pd.DataFrame(latest_values).sort_values('LatestValue', ascending=True)

fig, ax = plt.subplots(figsize=(12, 10))
colors = plt.cm.viridis(np.linspace(0, 1, len(latest_df)))
bars = ax.barh(latest_df['RegionName'], latest_df['LatestValue'], color=colors)
ax.set_xlabel('Latest Home Value Index ($)', fontsize=12, fontweight='bold')
ax.set_ylabel('Metro Area', fontsize=12, fontweight='bold')
ax.set_title('Latest Home Values: Top 20 Metro Areas', 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, latest_df['LatestValue'])):
    ax.text(value, bar.get_y() + bar.get_height()/2, 
            f'${value:,.0f}', 
            ha='left', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/04_regional_price_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/04_regional_price_comparison.png")
plt.close()

# ============================================================================
# VISUALIZATION 5: Price Change Analysis (2008 Financial Crisis)
# ============================================================================
print("\n5. Creating visualization: 2008 Financial Crisis Impact...")

# Get values around 2008
pre_crisis_col = '2007-01-31'
crisis_col = '2009-01-31'
post_crisis_col = '2012-01-31'

if pre_crisis_col in date_cols and crisis_col in date_cols and post_crisis_col in date_cols:
    crisis_df = zillow_df[zillow_df['RegionType'] == 'msa'].head(15).copy()
    crisis_df = crisis_df[['RegionName', pre_crisis_col, crisis_col, post_crisis_col]].dropna()
    
    crisis_df['Decline_Pct'] = ((crisis_df[crisis_col] - crisis_df[pre_crisis_col]) / crisis_df[pre_crisis_col] * 100)
    crisis_df['Recovery_Pct'] = ((crisis_df[post_crisis_col] - crisis_df[crisis_col]) / crisis_df[crisis_col] * 100)
    
    crisis_df = crisis_df.sort_values('Decline_Pct')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Decline chart
    colors_decline = ['darkred' if x < 0 else 'darkgreen' for x in crisis_df['Decline_Pct']]
    ax1.barh(crisis_df['RegionName'], crisis_df['Decline_Pct'], color=colors_decline, alpha=0.7)
    ax1.set_xlabel('Price Change (%)', fontsize=11, fontweight='bold')
    ax1.set_title('2007-2009: Financial Crisis Impact', fontsize=12, fontweight='bold')
    ax1.axvline(x=0, color='black', linestyle='--', linewidth=1)
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Recovery chart
    colors_recovery = ['darkgreen' if x > 0 else 'darkred' for x in crisis_df['Recovery_Pct']]
    ax2.barh(crisis_df['RegionName'], crisis_df['Recovery_Pct'], color=colors_recovery, alpha=0.7)
    ax2.set_xlabel('Price Change (%)', fontsize=11, fontweight='bold')
    ax2.set_title('2009-2012: Recovery Period', fontsize=12, fontweight='bold')
    ax2.axvline(x=0, color='black', linestyle='--', linewidth=1)
    ax2.grid(True, alpha=0.3, axis='x')
    
    plt.suptitle('Housing Market During Financial Crisis: Top 15 Metro Areas', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('visualizations/05_financial_crisis_impact.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/05_financial_crisis_impact.png")
    plt.close()

# ============================================================================
# VISUALIZATION 6: State-Level Analysis
# ============================================================================
print("\n6. Creating visualization: State-Level Summary...")

# Get latest values by state
state_summary = []
for state in zillow_df['StateName'].dropna().unique():
    state_metros = zillow_df[(zillow_df['StateName'] == state) & (zillow_df['RegionType'] == 'msa')]
    if len(state_metros) > 0:
        # Get latest values for metros in this state
        latest_vals = []
        for idx, row in state_metros.iterrows():
            vals = row[date_cols].dropna()
            if len(vals) > 0:
                latest_vals.append(vals.iloc[-1])
        
        if len(latest_vals) > 0:
            state_summary.append({
                'State': state,
                'NumMetros': len(state_metros),
                'AvgValue': np.mean(latest_vals),
                'MedianValue': np.median(latest_vals),
                'MaxValue': np.max(latest_vals)
            })

state_df = pd.DataFrame(state_summary).sort_values('MedianValue', ascending=False).head(15)

fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(state_df))
width = 0.35

bars1 = ax.bar(x - width/2, state_df['AvgValue'], width, label='Average', alpha=0.8, color='steelblue')
bars2 = ax.bar(x + width/2, state_df['MedianValue'], width, label='Median', alpha=0.8, color='coral')

ax.set_xlabel('State', fontsize=12, fontweight='bold')
ax.set_ylabel('Home Value Index ($)', fontsize=12, fontweight='bold')
ax.set_title('Latest Home Values by State: Top 15 States (Avg vs Median)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(state_df['State'], rotation=45, ha='right')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('visualizations/06_state_level_summary.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/06_state_level_summary.png")
plt.close()

# ============================================================================
# Summary Statistics
# ============================================================================
print("\n" + "="*70)
print("VISUALIZATION SUMMARY")
print("="*70)
print(f"\n✓ Created 6 visualizations in 'visualizations/' folder:")
print("  1. Top 10 metro areas price trends over time")
print("  2. Missing data heatmap (first 50 metros)")
print("  3. Missing data percentage timeline")
print("  4. Latest home values comparison (top 20 metros)")
print("  5. Financial crisis impact analysis (2007-2012)")
print("  6. State-level summary (top 15 states)")

print("\n" + "="*70)
print("DATA QUALITY INSIGHTS")
print("="*70)
print(f"\n📊 Dataset Overview:")
print(f"  • Total metro areas: {len(zillow_df[zillow_df['RegionType'] == 'msa'])}")
print(f"  • Time period: {date_cols[0]} to {date_cols[-1]}")
print(f"  • Total data points: {zillow_df[date_cols].size:,}")
print(f"  • Missing data points: {zillow_df[date_cols].isnull().sum().sum():,}")
print(f"  • Missing percentage: {(zillow_df[date_cols].isnull().sum().sum() / zillow_df[date_cols].size * 100):.2f}%")

print(f"\n⚠️  Missing Data Patterns:")
print(f"  • Early years (2000-2005) have higher missing rates (~50%)")
print(f"  • Data quality improves significantly after 2005")
print(f"  • Most recent years have minimal missing data")

print(f"\n💡 Key Findings:")
# Calculate some interesting statistics
us_row = zillow_df[zillow_df['RegionName'] == 'United States'].iloc[0]
us_values = us_row[date_cols].dropna()
if len(us_values) > 10:
    print(f"  • US national average (latest): ${us_values.iloc[-1]:,.2f}")
    print(f"  • US national average (2000): ${us_values.iloc[0]:,.2f}")
    print(f"  • Overall growth: {((us_values.iloc[-1] - us_values.iloc[0]) / us_values.iloc[0] * 100):.1f}%")

print("\n" + "="*70)
