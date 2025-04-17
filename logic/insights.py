import pandas as pd

def generate_insights(df):
    df.columns = df.columns.str.lower().str.strip()

    # --- Restock Suggestions ---
    restock = df[(df['total days of supply (including units from open shipments)'] < 30) |
                 (df['available'] < df['fba-minimum-inventory-level'])].copy()
    restock['suggested_restock_qty'] = (df['fba-minimum-inventory-level'] - df['available']).clip(lower=0)

    restock_output = restock[[
        'sku', 'asin', 'product-name', 'available', 'fba-minimum-inventory-level',
        'total days of supply (including units from open shipments)',
        'units-shipped-t30', 'suggested_restock_qty'
    ]].rename(columns={
        'units-shipped-t30': '30d Units Sold',
        'total days of supply (including units from open shipments)': 'Days of Supply'
    })

    # --- Aged Inventory ---
    aged = df[(df['inventory-age-271-to-365-days'] > 10) |
              (df['inventory-age-365-plus-days'] > 10)].copy()

    aged_output = aged[[
        'sku', 'asin', 'product-name', 'available',
        'inventory-age-271-to-365-days', 'inventory-age-365-plus-days',
        'estimated-ais-365-plus-days', 'estimated-storage-cost-next-month'
    ]].rename(columns={
        'estimated-ais-365-plus-days': 'Est. Aged Fees',
        'estimated-storage-cost-next-month': 'Est. Storage Cost Next Month'
    })

    # --- No-Sale ASINs ---
    no_sales = df[(df['sales-shipped-last-90-days'] == 0) & (df['available'] > 0)].copy()

    no_sales_output = no_sales[[
        'sku', 'asin', 'product-name', 'available',
        'sales-shipped-last-30-days', 'sales-shipped-last-90-days'
    ]]

    return restock_output, aged_output, no_sales_output
