import pandas as pd

# Load data
fba_df = pd.read_csv('fba_inventory.csv')
shopify_df = pd.read_csv('shopify_inventory.csv')

# Normalize columns
fba_df['SKU'] = fba_df['SKU'].str.strip().str.upper() # Remove trailing space and uppercase SKU values
shopify_df['SKU'] = shopify_df['SKU'].str.strip().str.upper()

# Merge datasets on SKU - If SKU exists in FBA and not Shopify then it will appear in the merged dataset and vice versa
merged_df = pd.merge(shopify_df, fba_df, on='SKU', how='outer', suffixes=('_shopify', '_fba'))

# Flag issues
merged_df['Status'] = 'Match'
merged_df.loc[merged_df['Shopify_Quantity'] != merged_df['FBA_Quantity'], 'Status'] = 'Mismatch'
merged_df.loc[merged_df['FBA_Quantity'].isna(), 'Status'] = 'Missing in FBA'
merged_df.loc[merged_df['Shopify_Quantity'].isna(), 'Status'] = 'Missing in Shopify'

# Output audit report
merged_df.to_csv('audit_report.csv', index=False)