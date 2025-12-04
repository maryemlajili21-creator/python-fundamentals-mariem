from __future__ import annotations

import pandas as pd
import requests  # type: ignore[import-untyped]


def download_html(row: pd.Series) -> str:
    try:
        response = requests.get(row["url"], timeout=10)
        return response.text
    except Exception:
        return ""
