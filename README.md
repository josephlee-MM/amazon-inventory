# 📦 Amazon FBA Inventory Insights App

This Streamlit app lets you upload your Amazon FBA Inventory Report (CSV format) and instantly generates:

- ✅ Restock Recommendations (based on supply coverage and thresholds)
- ⚠️ Aged Inventory Alerts (to avoid long-term storage fees)
- ❌ No-Sale ASINs Report (flag stale inventory)

## 🚀 How to Use

1. Export your FBA Inventory Report from Seller Central
2. Upload the CSV file to this app
3. Review insights and download:
   - Restock plan
   - Aged inventory report
   - No-sales ASINs

## 📂 File Structure

```
📁 logic/
    └── insights.py        # Generates all inventory insights
📄 streamlit_app.py         # Main app UI
📄 requirements.txt         # Install dependencies
📄 README.md                # This file
```

## 🛠 Installation

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
