from pathlib import Path
from urllib.request import urlretrieve

# US Census Bureau - Commercial Building Characteristics Survey (CBECS)
# This is the most comprehensive publicly available commercial real estate data

DATA_URLS = {
    "cbecs_building": "https://www.eia.gov/consumption/commercial/data/2018/csv/b1.csv",
    "cbecs_energy": "https://www.eia.gov/consumption/commercial/data/2018/csv/c1.csv",
}

DATA_DIR = Path("data/commercial")
DATA_DIR.mkdir(parents=True, exist_ok=True)

for name, url in DATA_URLS.items():
    output_path = DATA_DIR / f"{name}.csv"
    try:
        urlretrieve(url, output_path)
        print(f"✓ Downloaded: {output_path.resolve()}")
    except Exception as e:
        print(f"✗ Failed to download {name}: {e}")

print("\nCommercial Real Estate Data Sources:")
print("- CBECS Building Data: Building characteristics and counts")
print("- CBECS Energy Data: Energy consumption by building type")
print("\nNote: For comprehensive commercial property data (prices, transactions),")
print("you typically need paid subscriptions to CoStar or similar services.")
