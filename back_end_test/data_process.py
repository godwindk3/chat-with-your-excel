import pandas as pd
import numpy as np

def clean_excel(file_path, sheet_name=None, output_path="cleaned_data.xlsx"):
    """
    Đọc và làm sạch dữ liệu từ file Excel.
    - Đồng nhất kiểu dữ liệu
    - Chuẩn hóa ngày giờ
    - Xử lý NaN
    - Xóa khoảng trắng thừa
    """

    # Đọc Excel
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # 1. Xóa khoảng trắng ở tên cột
    df.columns = df.columns.str.strip()

    # 2. Chuẩn hóa từng cột
    for col in df.columns:
        # Nếu toàn bộ là số hoặc NaN -> chuyển sang float
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Nếu có giá trị datetime hoặc dạng chuỗi ngày giờ -> convert sang datetime
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], errors="coerce")
        else:
            # Nếu là object thì thử ép kiểu
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                if df[col].notna().any():
                    continue
            except:
                pass

            # Nếu không phải datetime thì convert toàn bộ sang string để tránh mixed types
            df[col] = df[col].astype(str).replace("nan", np.nan).str.strip()

    # 3. Xử lý NaN
    df = df.fillna("")

    # 4. Xuất ra file mới
    df.to_excel(output_path, index=False)
    print(f"✅ Dữ liệu đã được làm sạch và lưu tại: {output_path}")

    return df

if __name__ == "__main__":
    cleaned_df = clean_excel(
        file_path="data.xlsx",
        sheet_name=None,  # hoặc tên sheet, vd: "Sheet1"
        output_path="cleaned_data.xlsx"
    )
