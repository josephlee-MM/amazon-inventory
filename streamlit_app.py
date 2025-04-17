# streamlit_app.py
import streamlit as st
import pandas as pd
from logic.insights import generate_insights

st.title("📦 Amazon FBA Inventory Insights & Restock Planner")

uploaded_file = st.file_uploader("Upload FBA Inventory Report (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    restock_df, aged_df, no_sale_df, aging_summary, velocity_df = generate_insights(df)

    st.success("✅ File processed successfully!")

    st.subheader("📥 Restock Recommendations")
    st.dataframe(restock_df, use_container_width=True)
    st.download_button("Download Restock Plan", restock_df.to_csv(index=False), "restock_plan.csv")

    st.subheader("⚠️ Aged Inventory Alerts")
    st.dataframe(aged_df, use_container_width=True)
    st.download_button("Download Aged Inventory Report", aged_df.to_csv(index=False), "aged_inventory.csv")

    st.subheader("❌ No Sales (Last 90 Days)")
    st.dataframe(no_sale_df, use_container_width=True)
    st.download_button("Download No-Sales ASINs", no_sale_df.to_csv(index=False), "no_sales_asins.csv")
