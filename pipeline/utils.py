from datetime import datetime
from typing import Union  # Add this import for type hinting compatibility


def normalize_space(s: str) -> Union[str, None]:
    """Trim whitespace and collapse multiple spaces."""
    if not s:
        return None
    return " ".join(s.strip().split())


def parse_date(date_str: str) -> Union[str, None]:
    """Parse MM/DD/YY or MM/DD/YYYY to 'YYYY-MM-DD HH:MM:SS'."""
    if not date_str:
        return None
    for fmt in ("%m/%d/%Y", "%m/%d/%y"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    return None


def sql_val(val) -> str:
    """Format a Python value for SQL INSERT (quoting strings, NULL otherwise)."""
    if val is None or val == "":
        return "NULL"
    if isinstance(val, str):
        escape = val.replace("'", "''")
        return f"'{escape}'"
    return str(val)
