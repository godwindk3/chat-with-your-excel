import pandas as pd

# Read excel file

file_path = "./data/data.xlsx"

excel_file = pd.ExcelFile(file_path)

sheet_names = excel_file.sheet_names

df = pd.read_excel(file_path, sheet_name="Các câu hỏi liên quan")
# print(df.to_string(index=False))

## Question 1 : Top 5 nhà vận tải có số chuyến vận chuyển xuất bán nhiều nhất?
# Sheet (Đơn hàng vận chuyển)
df_1 = pd.read_excel(file_path, sheet_name="Đơn hàng vận chuyển")
top5 = (
    df_1['Tên nhà vận tải']
    .value_counts()      # Đếm số chuyến theo từng nhà vận tải
    .head(5)             # Lấy top 5
)
# print("--------------------------------")
# print("Câu 1: Top 5 nhà vận tải có số chuyến xuất bán nhiều nhất (Sheet Đơn hàng vận chuyển):")
# print(top5)

# Sheet (Đơn hàng vận chuyển nội bộ)

df_2 = pd.read_excel(file_path, sheet_name="Đơn hàng vận chuyển nội bộ")
top5 = (
    df_2['Tên nhà vận tải']
    .value_counts()     
    .head(5)             
)
# print("--------------------------------")
# print("Câu 1: Top 5 nhà vận tải có số chuyến xuất bán nhiều nhất (Sheet Đơn hàng vận chuyển nội bộ):")
# print(top5)

## Question 2: Số lượng hàng vận chuyển xuất bán trong tháng 6 là bao nhiêu? 
# (Sheet Đơn hàng vận chuyển)
print("--------------------------------")
df_1["Thời gian thực tế rời điểm lấy"] = pd.to_datetime(df_1["Thời gian thực tế rời điểm lấy"], errors="coerce")

# Lọc các chuyến trong tháng 6 (ví dụ 2025)
df_june = df_1[df_1["Thời gian thực tế rời điểm lấy"].dt.month == 6]

# Tính tổng số lượng thực xuất trong tháng 6
total_quantity_june = df_june["Số lượng thực xuất"].sum()

# print(f"Tổng số lượng hàng xuất bán trong tháng 6: {total_quantity_june}")
# (Sheet Đơn hàng vận chuyển nội bộ)
print("--------------------------------")
df_2["Thời gian thực tế rời điểm lấy"] = pd.to_datetime(df_2["Thời gian thực tế rời điểm lấy"], errors="coerce")

# Lọc các chuyến trong tháng 6 (ví dụ 2025)
df_june = df_2[df_2["Thời gian thực tế rời điểm lấy"].dt.month == 6]

# Tính tổng số lượng thực xuất trong tháng 6
total_quantity_june = df_june["Số lượng thực xuất"].sum()

# print(f"Tổng số lượng hàng xuất bán trong tháng 6: {total_quantity_june}")

## Question 3: Mặt hàng nào có lượng xuất bán cao nhất?
# (Sheet Đơn hàng vận chuyển)
total_by_product = df_1.groupby("Tên hàng hóa")["Số lượng thực xuất"].sum()

# Tìm mặt hàng có lượng xuất bán cao nhất
max_product = total_by_product.idxmax()
max_quantity = total_by_product.max()

print(f"Mặt hàng có lượng xuất bán cao nhất: {max_product} ({max_quantity})")
# (Sheet Đơn hàng vận chuyển nội bộ)
total_by_product = df_2.groupby("Tên hàng hóa")["Số lượng thực xuất"].sum()

# Tìm mặt hàng có lượng xuất bán cao nhất
max_product = total_by_product.idxmax()
max_quantity = total_by_product.max()

print(f"Mặt hàng có lượng xuất bán cao nhất: {max_product} ({max_quantity})")

## Question 4: Các kho xuất hàng bán chủ yếu trong tháng 6 là các kho nào?
# (Sheet Đơn hàng vận chuyển)
df_1['Thời gian thực tế rời điểm lấy'] = pd.to_datetime(df_1['Thời gian thực tế rời điểm lấy'], errors='coerce')

# Lọc tháng 6
df_june = df_1[df_1['Thời gian thực tế rời điểm lấy'].dt.month == 6]

# Nhóm theo Tên điểm lấy và tính tổng số lượng thực xuất
top_warehouses = (
    df_june.groupby("Tên điểm lấy")["Số lượng thực xuất"]
    .sum()
    .sort_values(ascending=False)
)

print("Các kho xuất hàng nhiều nhất trong tháng 6:")
print(top_warehouses)
# (Sheet Đơn hàng vận chuyển nội bộ)
df_2['Thời gian thực tế rời điểm lấy'] = pd.to_datetime(df_2['Thời gian thực tế rời điểm lấy'], errors='coerce')

# Lọc tháng 6
df_june = df_2[df_2['Thời gian thực tế rời điểm lấy'].dt.month == 6]

# Nhóm theo Tên điểm lấy và tính tổng số lượng thực xuất
top_warehouses = (
    df_june.groupby("Tên điểm lấy")["Số lượng thực xuất"]
    .sum()
    .sort_values(ascending=False)
)

print("Các kho xuất hàng nhiều nhất trong tháng 6:")
print(top_warehouses)