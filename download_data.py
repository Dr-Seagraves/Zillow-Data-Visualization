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
