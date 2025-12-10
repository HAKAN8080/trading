import pandas as pd
from typing import List, Tuple

def format_number(value: float, decimals: int = 0, suffix: str = "") -> str:
    if pd.isna(value):
        return "-"
    if decimals == 0:
        formatted = f"{int(value):,}".replace(",", ".")
    else:
        formatted = f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{formatted}{suffix}"

def format_currency(value: float, currency: str = "TL") -> str:
    return format_number(value, decimals=0, suffix=f" {currency}")

def format_percentage(value: float, decimals: int = 1, show_sign: bool = True) -> str:
    if pd.isna(value):
        return "-"
    sign = "+" if value > 0 and show_sign else ""
    return f"{sign}{value:.{decimals}f}%"

def cover_grubu_belirle(cover: float) -> str:
    if pd.isna(cover):
        return "N/A"
    if cover < 5:
        return "0-5"
    elif cover < 9:
        return "5-9"
    elif cover < 12:
        return "9-12"
    elif cover < 15:
        return "12-15"
    elif cover < 20:
        return "15-20"
    elif cover < 25:
        return "20-25"
    elif cover < 30:
        return "25-30"
    else:
        return "30+"

def cover_emoji(cover: float) -> str:
    if pd.isna(cover):
        return "❓"
    if cover < 8:
        return "⚠️"
    elif cover <= 12:
        return "✅"
    elif cover <= 20:
        return "🟡"
    elif cover <= 30:
        return "🟠"
    else:
        return "🔴"

def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> Tuple[bool, List[str]]:
    missing = [col for col in required_columns if col not in df.columns]
    return len(missing) == 0, missing

def safe_divide(numerator: float, denominator: float, default: float = 0) -> float:
    try:
        if denominator == 0 or pd.isna(denominator) or pd.isna(numerator):
            return default
        return numerator / denominator
    except:
        return default

def calculate_cover(stok_tl: float, haftalik_smm: float) -> float:
    return safe_divide(stok_tl, haftalik_smm, default=999)

def calculate_margin(asf: float, smm: float, kdv: float = 0.20) -> float:
    asf_kdv_haric = asf / (1 + kdv)
    return ((asf_kdv_haric - smm) / asf_kdv_haric) * 100 if asf_kdv_haric > 0 else -100