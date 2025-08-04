import pandas as pd

# Đọc dữ liệu tồn kho
df = pd.read_excel("./data/data_wms_ttc.xlsx", sheet_name="Data tồn kho")

PCS_PER_CASE = 12


df['TOTAL_ONHAND'] = df['ONHAND CASE'] * PCS_PER_CASE + df['ONHAND PCS']

# Tính tổng tồn kho theo tên hàng
products_onhand = df.groupby('TÊN HÀNG')['TOTAL_ONHAND'].sum().sort_values(ascending=False)

# In ra top 5 mặt hàng có tồn kho cao nhất
print("Top 5 mặt hàng tồn kho cao nhất (theo PCS):")
print(products_onhand.head())
