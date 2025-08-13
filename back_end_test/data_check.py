import pandas as pd

def analyze_excel(file_path):
    # Luôn đọc tất cả các sheet
    sheets = pd.read_excel(file_path, sheet_name=None)

    for name, df in sheets.items():
        print(f"\n📄 Đang phân tích sheet: {name}")
        print("=" * 50)

        # Kiểu dữ liệu theo Pandas
        print("🔹 Kiểu dữ liệu theo Pandas:")
        print(df.dtypes)
        print("=" * 50)

        # Kiểu dữ liệu thực tế của từng cột
        print("🔹 Kiểu dữ liệu thực tế và cảnh báo:")
        for col in df.columns:
            values = df[col].dropna()
            unique_types = values.map(type).unique()
            type_names = [t.__name__ for t in unique_types]

            warning = ""
            # Cảnh báo 1: Cột toàn NaN
            if values.empty:
                warning = "⚠️ Toàn NaN (có thể bỏ cột)"
            # Cảnh báo 2: Nhiều kiểu dữ liệu trong 1 cột
            elif len(unique_types) > 1:
                warning = "⚠️ Lẫn nhiều kiểu dữ liệu"
            # Cảnh báo 3: Nếu là số nhưng đang là str
            elif all(t == str for t in unique_types) and col.lower().startswith(('tấn', 'khối', 'số lượng')):
                warning = "⚠️ Số liệu nhưng toàn chuỗi"

            print(f"{col}: {type_names} {warning}")

# ======= Chạy thử =======
file_path = "./data/data_clean.xlsx"  # Đường dẫn tới file của bạn
analyze_excel(file_path)
