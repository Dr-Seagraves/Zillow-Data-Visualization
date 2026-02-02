import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("Loading Zillow ZHVI Metro data...")
zillow_df = pd.read_csv('data/zillow_zhvi_metro.csv')

# Get date columns
date_cols = [col for col in zillow_df.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]

# Create output directory
import os
os.makedirs('charts', exist_ok=True)

print("\nGenerating 4 chart types...")
print("="*70)

# ============================================================================
# 1. HISTOGRAM - Distribution Shape
# ============================================================================
print("\n1. Creating HISTOGRAM - Distribution of Latest Home Values...")

# Get latest non-null values for all metro areas
latest_values = []
for idx, row in zillow_df[zillow_df['RegionType'] == 'msa'].iterrows():
    values = pd.to_numeric(row[date_cols], errors='coerce').dropna()
    if len(values) > 0:
        latest_values.append(values.iloc[-1])

latest_values = np.array(latest_values)

fig, ax = plt.subplots(figsize=(12, 7))

# Create histogram with custom bins
n, bins, patches = ax.hist(latest_values, bins=30, edgecolor='black', alpha=0.7, color='steelblue')

# Add a vertical line for the mean
mean_val = np.mean(latest_values)
median_val = np.median(latest_values)
ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: ${mean_val:,.0f}')
ax.axvline(median_val, color='orange', linestyle='--', linewidth=2, label=f'Median: ${median_val:,.0f}')

ax.set_xlabel('Home Value Index ($)', fontsize=12, fontweight='bold')
ax.set_ylabel('Frequency (Number of Metro Areas)', fontsize=12, fontweight='bold')
ax.set_title('Histogram: Distribution of Latest Home Values Across Metro Areas', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

# Add statistics text box
stats_text = f'n = {len(latest_values)}\nStd Dev = ${np.std(latest_values):,.0f}'
ax.text(0.98, 0.97, stats_text, transform=ax.transAxes, 
        fontsize=10, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('charts/histogram_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Saved: charts/histogram_distribution.png")
plt.close()

# ============================================================================
# 2. BOX PLOT - Median, Quartiles, Outliers
# ============================================================================
print("\n2. Creating BOX PLOT - Home Values by Top States...")

# Get top 10 states by number of metros
state_counts = zillow_df[zillow_df['RegionType'] == 'msa']['StateName'].value_counts().head(10)
top_states = state_counts.index.tolist()

# Collect data for box plot
box_data = []
box_labels = []

for state in top_states:
    state_metros = zillow_df[(zillow_df['StateName'] == state) & (zillow_df['RegionType'] == 'msa')]
    state_values = []
    
    for idx, row in state_metros.iterrows():
        values = pd.to_numeric(row[date_cols], errors='coerce').dropna()
        if len(values) > 0:
            state_values.append(values.iloc[-1])
    
    if len(state_values) > 0:
        box_data.append(state_values)
        box_labels.append(f'{state}\n(n={len(state_values)})')

fig, ax = plt.subplots(figsize=(14, 8))

# Create box plot
bp = ax.boxplot(box_data, labels=box_labels, patch_artist=True,
                showmeans=True, meanline=True,
                medianprops=dict(color='red', linewidth=2),
                meanprops=dict(color='blue', linewidth=2, linestyle='--'),
                whiskerprops=dict(linewidth=1.5),
                capprops=dict(linewidth=1.5),
                flierprops=dict(marker='o', markerfacecolor='red', markersize=5, alpha=0.5))

# Color the boxes
colors = plt.cm.Set3(np.linspace(0, 1, len(box_data)))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_xlabel('State', fontsize=12, fontweight='bold')
ax.set_ylabel('Home Value Index ($)', fontsize=12, fontweight='bold')
ax.set_title('Box Plot: Home Value Distribution by State (Median, Quartiles, Outliers)', 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='y')

# Add legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='red', linewidth=2, label='Median'),
    Line2D([0], [0], color='blue', linewidth=2, linestyle='--', label='Mean'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Outliers')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('charts/boxplot_by_state.png', dpi=300, bbox_inches='tight')
print("✓ Saved: charts/boxplot_by_state.png")
plt.close()

# ============================================================================
# 3. LINE PLOT - Trends Over Time
# ============================================================================
print("\n3. Creating LINE PLOT - Trends Over Time for Major Metros...")

# Select top 5 largest metros
top_metros = zillow_df[zillow_df['RegionType'] == 'msa'].nsmallest(5, 'SizeRank')

fig, ax = plt.subplots(figsize=(14, 7))

dates = pd.to_datetime(date_cols)

for idx, row in top_metros.iterrows():
    values = pd.to_numeric(row[date_cols], errors='coerce').values
    mask = ~np.isnan(values)
    ax.plot(dates[mask], values[mask], label=row['RegionName'], linewidth=2.5, marker='o', 
            markersize=2, alpha=0.8)

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Home Value Index ($)', fontsize=12, fontweight='bold')
ax.set_title('Line Plot: Home Value Trends Over Time (Top 5 Metro Areas)', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.3)

# Highlight the 2008 financial crisis
ax.axvspan(pd.Timestamp('2007-12-01'), pd.Timestamp('2009-06-01'), 
           alpha=0.2, color='red', label='Financial Crisis')

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('charts/lineplot_trends.png', dpi=300, bbox_inches='tight')
print("✓ Saved: charts/lineplot_trends.png")
plt.close()

# ============================================================================
# 4. DENSITY PLOT - Smooth Distribution
# ============================================================================
print("\n4. Creating DENSITY PLOT - Smooth Distribution of Home Values...")

fig, ax = plt.subplots(figsize=(12, 7))

# Get latest values again
latest_values_clean = latest_values[~np.isnan(latest_values)]

# Create density plot using seaborn
sns.kdeplot(data=latest_values_clean, ax=ax, fill=True, alpha=0.5, 
            linewidth=2, color='steelblue', label='Density')

# Overlay with histogram for reference
ax.hist(latest_values_clean, bins=30, density=True, alpha=0.3, 
        color='gray', edgecolor='black', label='Histogram (normalized)')

# Add vertical lines for statistics
mean_val = np.mean(latest_values_clean)
median_val = np.median(latest_values_clean)
mode_idx = np.argmax(stats.gaussian_kde(latest_values_clean)(latest_values_clean))
mode_val = latest_values_clean[mode_idx]

ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: ${mean_val:,.0f}')
ax.axvline(median_val, color='orange', linestyle='--', linewidth=2, label=f'Median: ${median_val:,.0f}')

ax.set_xlabel('Home Value Index ($)', fontsize=12, fontweight='bold')
ax.set_ylabel('Density', fontsize=12, fontweight='bold')
ax.set_title('Density Plot: Smooth Distribution of Latest Home Values', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=10, loc='upper right')
ax.grid(True, alpha=0.3, axis='y')

# Add statistics box
stats_text = (f'Sample Size: {len(latest_values_clean)}\n'
              f'Mean: ${mean_val:,.0f}\n'
              f'Median: ${median_val:,.0f}\n'
              f'Std Dev: ${np.std(latest_values_clean):,.0f}\n'
              f'Skewness: {stats.skew(latest_values_clean):.2f}')

ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
        fontsize=9, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('charts/densityplot_smooth.png', dpi=300, bbox_inches='tight')
print("✓ Saved: charts/densityplot_smooth.png")
plt.close()

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*70)
print("CHART GENERATION COMPLETE")
print("="*70)
print("\n✓ All 4 charts created successfully in 'charts/' folder:")
print("\n1. histogram_distribution.png")
print("   - Shows: Distribution shape of home values")
print("   - Data + Position(x=value, y=frequency) + Bar")
print(f"   - Sample: {len(latest_values)} metro areas")

print("\n2. boxplot_by_state.png")
print("   - Shows: Median, quartiles, and outliers by state")
print("   - Data + Position(group=state, value=home_value) + Box")
print(f"   - Groups: Top {len(box_labels)} states")

print("\n3. lineplot_trends.png")
print("   - Shows: Trends over time for major metros")
print("   - Data + Position(x=date, y=value) + Line")
print("   - Series: Top 5 metro areas (2000-2025)")

print("\n4. densityplot_smooth.png")
print("   - Shows: Smooth distribution of home values")
print("   - Data + Position(x=value, y=density) + Smooth curve")
print(f"   - Distribution: {len(latest_values_clean)} observations")

print("\n" + "="*70)
print("📊 Charts ready for analysis and presentation!")
print("="*70)
