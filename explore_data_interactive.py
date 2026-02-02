"""
Interactive Data Explorer for Zillow ZHVI Data
Run this script and follow prompts to explore specific metros or states
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
print("Loading Zillow ZHVI Metro data...")
zillow_df = pd.read_csv('data/zillow_zhvi_metro.csv')
date_cols = [col for col in zillow_df.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]

print("\n" + "="*70)
print("ZILLOW ZHVI DATA EXPLORER")
print("="*70)

def plot_metro_comparison(metro_names):
    """Plot comparison of selected metros"""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for metro_name in metro_names:
        metro_data = zillow_df[zillow_df['RegionName'].str.contains(metro_name, case=False, na=False)]
        
        if len(metro_data) > 0:
            row = metro_data.iloc[0]
            values = pd.to_numeric(row[date_cols], errors='coerce').values
            dates = pd.to_datetime(date_cols)
            mask = ~np.isnan(values)
            ax.plot(dates[mask], values[mask], label=row['RegionName'], linewidth=2, marker='o', markersize=3, alpha=0.7)
        else:
            print(f"  ⚠️  '{metro_name}' not found")
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Home Value Index ($)', fontsize=12, fontweight='bold')
    ax.set_title('Metro Area Comparison', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_state_metros(state_code):
    """Plot all metros in a state"""
    state_metros = zillow_df[(zillow_df['StateName'] == state_code) & (zillow_df['RegionType'] == 'msa')]
    
    if len(state_metros) == 0:
        print(f"  ⚠️  No metros found for state '{state_code}'")
        return
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    for idx, row in state_metros.iterrows():
        values = pd.to_numeric(row[date_cols], errors='coerce').values
        dates = pd.to_datetime(date_cols)
        mask = ~np.isnan(values)
        ax.plot(dates[mask], values[mask], label=row['RegionName'], linewidth=2, alpha=0.7)
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Home Value Index ($)', fontsize=12, fontweight='bold')
    ax.set_title(f'All Metro Areas in {state_code}', fontsize=14, fontweight='bold')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_metro_stats(metro_name):
    """Show detailed statistics for a metro"""
    metro_data = zillow_df[zillow_df['RegionName'].str.contains(metro_name, case=False, na=False)]
    
    if len(metro_data) == 0:
        print(f"  ⚠️  '{metro_name}' not found")
        return
    
    row = metro_data.iloc[0]
    values = pd.to_numeric(row[date_cols], errors='coerce').dropna()
    
    print(f"\n{'='*70}")
    print(f"STATISTICS FOR: {row['RegionName']}")
    print(f"{'='*70}")
    print(f"State: {row['StateName']}")
    print(f"Size Rank: {row['SizeRank']}")
    print(f"\nData Coverage:")
    print(f"  First available: {values.index[0]}")
    print(f"  Last available: {values.index[-1]}")
    print(f"  Total data points: {len(values)}")
    print(f"  Missing points: {len(date_cols) - len(values)}")
    
    print(f"\nHome Values:")
    print(f"  Current (latest): ${values.iloc[-1]:,.2f}")
    print(f"  First recorded: ${values.iloc[0]:,.2f}")
    print(f"  All-time high: ${values.max():,.2f} ({values.idxmax()})")
    print(f"  All-time low: ${values.min():,.2f} ({values.idxmin()})")
    
    print(f"\nGrowth Statistics:")
    total_growth = ((values.iloc[-1] - values.iloc[0]) / values.iloc[0] * 100)
    print(f"  Total growth: {total_growth:.1f}%")
    print(f"  Average annual growth: {total_growth / (len(values)/12):.1f}%")
    
    # Last 5 years
    if len(values) >= 60:
        recent_growth = ((values.iloc[-1] - values.iloc[-60]) / values.iloc[-60] * 100)
        print(f"  Last 5 years growth: {recent_growth:.1f}%")

# Main menu
while True:
    print("\n" + "="*70)
    print("MENU OPTIONS")
    print("="*70)
    print("1. Compare specific metro areas (e.g., 'New York', 'Los Angeles')")
    print("2. View all metros in a state (e.g., 'CA', 'NY', 'TX')")
    print("3. Show detailed statistics for a metro")
    print("4. List all available metros")
    print("5. List all states")
    print("6. Exit")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == '1':
        print("\nEnter metro names separated by commas")
        print("Examples: 'New York', 'Los Angeles, San Francisco', 'Chicago, Dallas, Houston'")
        metros = input("Metro names: ").strip().split(',')
        metros = [m.strip() for m in metros]
        print(f"\nPlotting comparison of: {', '.join(metros)}")
        plot_metro_comparison(metros)
    
    elif choice == '2':
        state = input("\nEnter state code (e.g., CA, NY, TX): ").strip().upper()
        print(f"\nPlotting all metros in {state}...")
        plot_state_metros(state)
    
    elif choice == '3':
        metro = input("\nEnter metro name (partial match OK): ").strip()
        show_metro_stats(metro)
    
    elif choice == '4':
        print("\nAVAILABLE METRO AREAS:")
        print("="*70)
        metros = zillow_df[zillow_df['RegionType'] == 'msa'][['SizeRank', 'RegionName', 'StateName']].sort_values('SizeRank')
        for idx, row in metros.head(50).iterrows():
            print(f"{row['SizeRank']:3d}. {row['RegionName']:<40s} ({row['StateName']})")
        print(f"\n... and {len(metros) - 50} more metros")
        print(f"Total: {len(metros)} metro areas")
    
    elif choice == '5':
        print("\nAVAILABLE STATES:")
        print("="*70)
        states = zillow_df['StateName'].dropna().unique()
        states.sort()
        for i, state in enumerate(states, 1):
            metro_count = len(zillow_df[(zillow_df['StateName'] == state) & (zillow_df['RegionType'] == 'msa')])
            print(f"{state:2s} ({metro_count:2d} metros)", end="    ")
            if i % 5 == 0:
                print()
        print()
    
    elif choice == '6':
        print("\nThank you for using the Zillow Data Explorer!")
        break
    
    else:
        print("\n⚠️  Invalid choice. Please enter 1-6.")
