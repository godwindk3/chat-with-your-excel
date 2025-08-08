import pandas as pd

# # Đọc dữ liệu tồn kho
# df = pd.read_excel("./data/data_wms_ttc.xlsx", sheet_name="Data tồn kho")

# PCS_PER_CASE = 12


# df['TOTAL_ONHAND'] = df['ONHAND CASE'] * PCS_PER_CASE + df['ONHAND PCS']

# # Tính tổng tồn kho theo tên hàng
# products_onhand = df.groupby('TÊN HÀNG')['TOTAL_ONHAND'].sum().sort_values(ascending=False)

# # In ra top 5 mặt hàng có tồn kho cao nhất
# print("Top 5 mặt hàng tồn kho cao nhất (theo PCS):")
# print(products_onhand.head())

# Đường dẫn tới file Excel
file_path = "./data/data.xlsx"

# Mở file Excel
excel_file = pd.ExcelFile(file_path)

df = pd.read_excel(file_path, sheet_name="Đơn hàng vận chuyển")

# colulm_description = pd.read_excel("./data/data.xlsx", sheet_name="Mô tả trường thông tin")

# Chuyển cột thời gian thực tế rời điểm lấy sang datetime
df["Thời gian thực tế rời điểm lấy"] = pd.to_datetime(df["Thời gian thực tế rời điểm lấy"], errors="coerce")

# Lọc các chuyến trong tháng 6 (ví dụ 2025)
df_june = df[df["Thời gian thực tế rời điểm lấy"].dt.month == 6]

# Tính tổng số lượng thực xuất trong tháng 6
total_quantity_june = df_june["Số lượng thực xuất"].sum()

print(f"Tổng số lượng hàng xuất bán trong tháng 6: {total_quantity_june}")