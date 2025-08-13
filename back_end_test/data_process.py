import pandas as pd

# ====== Cấu hình ======
input_file = "./data/data.xlsx"   # File Excel gốc
output_file = "./data/data_clean.xlsx"  # File Excel đã làm sạch
# ======================

# Hàm chuẩn hóa một sheet
def clean_sheet(df):
    # 1. Xoá cột toàn NaN
    df = df.dropna(axis=1, how='all')

    # 2. Chuẩn hóa cột ngày giờ
    datetime_cols = [
        "Dự kiến rời điểm lấy",
        "Dự kiến rời điểm giao",
        "Thời gian thực tế rời điểm lấy",
        "Thời gian thực tế rời điểm giao"
    ]
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # 3. Chuẩn hóa cột mã định danh về string
    id_cols = [
        "Mã chuyến", "Mã đơn hàng", "Mã điểm lấy", 
        "Mã điểm giao", "Mã nhóm hàng", "Mã hàng hóa"
    ]
    for col in id_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)

    # 4. Chuẩn hóa cột số liệu về numeric
    numeric_candidates = [
        col for col in df.columns
        if any(keyword in col.lower() for keyword in ["tấn", "khối", "số lượng"])
    ]
    for col in numeric_candidates:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

# Đọc toàn bộ sheet
all_sheets = pd.read_excel(input_file, sheet_name=None)

# Làm sạch toàn bộ sheet
cleaned_sheets = {name: clean_sheet(df) for name, df in all_sheets.items()}

# Xuất toàn bộ sheet ra file mới
with pd.ExcelWriter(output_file) as writer:
    for name, df in cleaned_sheets.items():
        df.to_excel(writer, sheet_name=name, index=False)

print(f"✅ Đã xuất file '{output_file}' với toàn bộ sheet đã chuẩn hóa.")
