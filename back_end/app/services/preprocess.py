from __future__ import annotations

import re
from typing import Iterable, Optional

import numpy as np
import pandas as pd


NA_STRINGS = {"", "na", "n/a", "nan", "null", "none", "-", "--"}


def _is_numeric_like(value: str) -> bool:
    if value is None:
        return False
    s = str(value).strip()
    if s.lower() in NA_STRINGS:
        return True
    # remove thousand separators and spaces
    s = s.replace(",", "").replace(" ", "")
    return bool(re.fullmatch(r"[-+]?\d*(?:\.\d+)?", s)) and s not in {"", "+", "-"}


def _to_numeric_series(series: pd.Series) -> pd.Series:
    # remove thousand separators and spaces, normalize decimal points
    cleaned = series.astype(str).str.strip()
    cleaned = cleaned.str.replace(",", "", regex=False).str.replace(" ", "", regex=False)
    numeric = pd.to_numeric(cleaned, errors="coerce")
    return numeric


def _maybe_convert_to_numeric(series: pd.Series) -> pd.Series:
    if series.dtype.kind in {"i", "u", "f"}:
        return series
    if series.dtype == "boolean":
        return series
    s_obj = series.astype("object")
    sample = s_obj.dropna().astype(str)
    if sample.empty:
        return series
    numeric_like_ratio = sample.apply(_is_numeric_like).mean()
    if numeric_like_ratio >= 0.6:
        converted = _to_numeric_series(s_obj)
        return converted
    return series


def _maybe_convert_to_boolean(series: pd.Series) -> pd.Series:
    if series.dtype == "boolean":
        return series
    s = series.astype("object").copy()
    truthy = {"true", "yes", "y", "1"}
    falsy = {"false", "no", "n", "0"}

    def classify(v):
        if pd.isna(v):
            return np.nan
        sv = str(v).strip().lower()
        if sv in truthy:
            return True
        if sv in falsy:
            return False
        return None

    classified = s.map(classify)
    # proportion of values that look like booleans among non-null original values
    denom = s.dropna().shape[0]
    bool_like_count = classified.dropna().shape[0]
    bool_ratio = (bool_like_count / denom) if denom > 0 else 0.0

    if bool_ratio >= 0.8:
        # Coerce unknowns to NA, then cast to pandas BooleanDtype safely
        def map_to_bool_or_na(v):
            if pd.isna(v):
                return np.nan
            sv = str(v).strip().lower()
            if sv in truthy:
                return True
            if sv in falsy:
                return False
            return np.nan

        mapped = s.map(map_to_bool_or_na)
        try:
            return mapped.astype("boolean")
        except Exception:
            # If casting still fails, fall back to original series
            return series

    return series


def _maybe_convert_to_datetime(series: pd.Series) -> pd.Series:
    if pd.api.types.is_datetime64_any_dtype(series):
        return series
    # Heuristics: attempt to parse; accept if sufficient non-null after conversion
    s = series.astype("object")
    try:
        parsed = pd.to_datetime(s, errors="coerce", dayfirst=True)
        if parsed.notna().mean() >= 0.6:  # at least 60% parsable
            return parsed
    except Exception:
        pass
    return series


def _normalize_na(series: pd.Series) -> pd.Series:
    if series.dtype.kind in {"i", "u", "f", "b", "M"}:  # numeric, boolean, datetime
        return series
    s = series.astype("object")
    return s.apply(lambda v: np.nan if (isinstance(v, str) and v.strip().lower() in NA_STRINGS) else v)


def _strip_whitespace(series: pd.Series) -> pd.Series:
    if series.dtype.kind in {"O", "S", "U"} or pd.api.types.is_string_dtype(series):
        return series.astype("object").apply(lambda v: v.strip() if isinstance(v, str) else v)
    return series


def infer_and_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Work on a copy to avoid mutating caller's df
    cleaned = df.copy()

    # Normalize column names' surrounding whitespace but preserve original names otherwise
    cleaned.columns = [c.strip() if isinstance(c, str) else c for c in cleaned.columns]

    for col in cleaned.columns:
        s = cleaned[col]
        s = _strip_whitespace(s)
        s = _normalize_na(s)
        # Try boolean first (yes/no, 1/0)
        s = _maybe_convert_to_boolean(s)
        # Then numeric
        s = _maybe_convert_to_numeric(s)
        # Then datetime
        s = _maybe_convert_to_datetime(s)
        # Finally, let pandas suggest best dtypes
        cleaned[col] = s

    # Let pandas do a final pass of dtype conversion
    try:
        cleaned = cleaned.convert_dtypes()
    except Exception:
        pass

    return cleaned


def read_and_preprocess_sheet(file_path: str, sheet_name: str) -> pd.DataFrame:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return infer_and_clean_dataframe(df)


