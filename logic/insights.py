# logic/insights.py
import pandas as pd

def generate_insights(df):
    df.columns = df.columns.str.lower().str.strip()

    # Alias support for older/simplified column names
    rename_map = {
        'inv-age-0-to-90-days': 'inventory-age-0-to-90-days',
        'inv-age-91-to-180-days': 'inventory-age-91-to-180-days',
        'inv-age-181-to-270-days': 'inventory-age-181-to-270-days',
        'inv-age-271-to-365-days': 'inventory-age-271-to-365-days',
        'inv-age-365-plus-days': 'inventory-age-365-plus-days',
        'units-shipped-t30': 'units-shipped-t30',
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # --- Restock Suggestions ---
    restock = df.copy()
    if 'total days of supply (including units from open shipments)' in df.columns and 'fba-minimum-inventory-level' in df.columns:
        restock = restock[(df['total days of supply (including units from open shipments)'] < 30) |
                          (df['available'] < df['fba-minimum-inventory-level'])]
        restock['suggested_restock_qty'] = (df['fba-minimum-inventory-level'] - df['available']).clip(lower=0)
    else:
        restock['suggested_restock_qty'] = 0

    restock_output = restock[[
        'sku', 'asin', 'product-name', 'available',
        'fba-minimum-inventory-level' if 'fba-minimum-inventory-level' in df.columns else 'available',
        'total days of supply (including units from open shipments)' if 'total days of supply (including units from open shipments)' in df.columns else 'available',
        'units-shipped-t30' if 'units-shipped-t30' in df.columns else 'available',
        'suggested_restock_qty'
    ]].rename(columns={
        'units-shipped-t30': '30d Units Sold',
        'total days of supply (including units from open shipments)': 'Days of Supply'
    })

    # --- Aged Inventory ---
    aged_output = pd.DataFrame()
    if 'inventory-age-271-to-365-days' in df.columns and 'inventory-age-365-plus-days' in df.columns:
        aged = df[(df['inventory-age-271-to-365-days'] > 10) |
                  (df['inventory-age-365-plus-days'] > 10)].copy()
        aged_output = aged[[
            'sku', 'asin', 'product-name', 'available',
            'inventory-age-271-to-365-days', 'inventory-age-365-plus-days',
            'estimated-ais-365-plus-days' if 'estimated-ais-365-plus-days' in df.columns else 'available',
            'estimated-storage-cost-next-month' if 'estimated-storage-cost-next-month' in df.columns else 'available'
        ]].rename(columns={
            'estimated-ais-365-plus-days': 'Est. Aged Fees',
            'estimated-storage-cost-next-month': 'Est. Storage Cost Next Month'
        })

    # --- No-Sale ASINs ---
    no_sales_output = pd.DataFrame()
    if 'sales-shipped-last-90-days' in df.columns:
        no_sales = df[(df['sales-shipped-last-90-days'] == 0) & (df['available'] > 0)].copy()
        no_sales_output = no_sales[[
            'sku', 'asin', 'product-name', 'available',
            'sales-shipped-last-30-days' if 'sales-shipped-last-30-days' in df.columns else 'available',
            'sales-shipped-last-90-days'
        ]]

    # --- Aging Chart Data ---
    aging_cols = [
        'inventory-age-0-to-90-days', 'inventory-age-91-to-180-days',
        'inventory-age-181-to-270-days', 'inventory-age-271-to-365-days',
        'inventory-age-365-plus-days'
    ]
    available_aging = [col for col in aging_cols if col in df.columns]
    aging_summary = pd.DataFrame()
    if available_aging:
        aging_summary = df[['sku'] + available_aging].copy()
        aging_summary.columns = ['SKU'] + [c.split('-')[-3] + '-' + c.split('-')[-2] + 'd' if 'to' in c else '365+d' for c in available_aging]

    # --- Sales Velocity vs Supply ---
    velocity_df = restock_output[['sku', '30d Units Sold', 'Days of Supply']].copy() if 'Days of Supply' in restock_output.columns else pd.DataFrame()
    if not velocity_df.empty:
        velocity_df.columns = ['SKU', '30d Units Sold', 'Days of Supply']

    return restock_output, aged_output, no_sales_output, aging_summary, velocity_df
