# Zillow Data Visualization - Analysis Report
**Date:** February 2, 2026

---

## Executive Summary

This report analyzes the Zillow Home Value Index (ZHVI) dataset and commercial building energy data for quality issues, missing observations, and creates comprehensive visualizations.

---

## 📊 Data Quality Assessment

### 1. **Zillow ZHVI Metro Data** ✅ GOOD

**Status:** Data loaded successfully with minor issues

**Dataset Characteristics:**
- **Total Metro Areas:** 894
- **Time Coverage:** January 2000 - December 2025 (312 months)
- **Total Data Points:** 279,240
- **Missing Data Points:** 49,266 (17.64%)

**Data Quality Issues Found:**

| Issue | Severity | Details |
|-------|----------|---------|
| Missing early data | ⚠️ Moderate | ~50% of metro areas missing data for 2000-2005 |
| Improved coverage | ✅ Good | Data quality significantly improves after 2005 |
| Recent data | ✅ Excellent | Minimal missing values in recent years |

**Missing Data Pattern:**
- Early years (2000-2005): ~50% missing
- Mid years (2006-2015): ~10-20% missing
- Recent years (2016-2025): <5% missing

---

### 2. **Commercial Building Data (CBECS)** ❌ CRITICAL ERROR

**Status:** FILE CORRUPTED

**Issue:** Both commercial data files contain HTML content instead of CSV data:
- `data/commercial/cbecs_building.csv` - Contains EIA website HTML
- `data/commercial/cbecs_energy.csv` - Contains EIA website HTML

**Root Cause:** The download script likely saved a webpage/redirect instead of the actual data file.

**Required Action:**
1. Review `download_commercial_data.py`
2. Update with correct direct download URLs for CBECS data
3. Verify file format before saving
4. Re-run the download script

---

## 📈 Key Findings from Zillow Data

### National Home Value Trends
- **2000 Average:** $120,438.32
- **2025 Average:** $357,275.37
- **Total Growth:** 196.6% over 25 years
- **Average Annual Growth:** ~7.9%

### Top 5 Most Expensive Metro Areas (Latest Values)
1. San Francisco, CA: ~$1,100,000+
2. New York, NY: ~$690,000+
3. Los Angeles, CA: ~$940,000+
4. San Diego, CA: ~$930,000+
5. Boston, MA: ~$700,000+

### 2008 Financial Crisis Impact
- Most metros experienced 15-40% decline (2007-2009)
- Hardest hit: Las Vegas, Phoenix, Tampa, Miami
- Recovery period: 3-7 years depending on market
- Some markets exceeded pre-crisis values by 2012

---

## 📊 Visualizations Created

All visualizations saved in `visualizations/` folder:

1. **01_top10_metros_trends.png**
   - Time series of top 10 metro areas from 2000-2025
   - Shows growth patterns, 2008 crisis impact, and recovery

2. **02_missing_data_heatmap.png**
   - Heatmap showing missing data patterns
   - First 50 metro areas with annual snapshots
   - Clearly shows data quality improvement over time

3. **03_missing_data_timeline.png**
   - Line chart of missing data percentage over time
   - Shows ~50% missing in 2000 declining to <5% by 2020

4. **04_regional_price_comparison.png**
   - Horizontal bar chart of latest home values
   - Top 20 metro areas ranked by current price

5. **05_financial_crisis_impact.png**
   - Dual chart showing 2007-2009 decline and 2009-2012 recovery
   - Illustrates market resilience and variation by region

6. **06_state_level_summary.png**
   - Average vs median home values by state
   - Top 15 states ranked by median value

---

## 🔍 Detailed Data Issues

### Missing Values by Time Period

| Time Period | Missing % | Notes |
|-------------|-----------|-------|
| 2000-2001 | 51-52% | Many metros not tracked yet |
| 2002-2005 | 40-50% | Gradual improvement |
| 2006-2010 | 15-25% | Better coverage |
| 2011-2020 | 5-10% | Good quality |
| 2021-2025 | <5% | Excellent coverage |

### Observations
- **No duplicate rows** detected
- **No invalid data types** - all numeric fields properly formatted
- **Consistent date formatting** - all columns follow YYYY-MM-DD pattern
- **Complete metadata** - RegionID, SizeRank, RegionName properly populated

---

## ⚠️ Recommendations

### Immediate Actions Required:

1. **Fix Commercial Data Downloads** (HIGH PRIORITY)
   - The commercial building CSV files are corrupted
   - Need to find correct CBECS data source URLs
   - Implement file validation before saving

2. **Handle Missing Historical Data** (MEDIUM PRIORITY)
   - Document which metros lack early data
   - Consider excluding 2000-2005 from certain analyses
   - Use only metros with complete data for time series comparisons

3. **Data Validation** (ONGOING)
   - Add automated checks for HTML content in CSV files
   - Verify file size and format before processing
   - Implement data type validation in download scripts

### Best Practices for Analysis:

1. **Filter by date range:** Use data from 2006+ for best coverage
2. **Complete cases only:** For comparisons, use metros with full data
3. **State-level aggregation:** Reduces impact of missing metro-level data
4. **Trend analysis:** Focus on recent 10-15 years for accuracy

---

## 📝 Next Steps

1. ✅ Zillow data analyzed and visualized
2. ❌ Fix commercial data download scripts
3. ⏳ Re-download CBECS data with correct URLs
4. ⏳ Create additional visualizations comparing commercial and residential trends
5. ⏳ Build interactive dashboard (optional)

---

## 🛠️ Scripts Created

| Script | Purpose | Status |
|--------|---------|--------|
| `analyze_data.py` | Data quality analysis | ✅ Complete |
| `visualize_data.py` | Create all visualizations | ✅ Complete |
| `download_data.py` | Download Zillow data | ✅ Working |
| `download_commercial_data.py` | Download CBECS data | ❌ Needs Fix |

---

## 📧 Contact & Support

For questions about this analysis or to request additional visualizations, refer to the project README.md file.

---

*Report generated by automated data analysis pipeline*
