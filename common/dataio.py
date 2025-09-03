from __future__ import annotations
from pathlib import Path
from typing import Optional

import pandas as pd


def read_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """Read a CSV file with sane defaults."""
    return pd.read_csv(path, encoding=kwargs.pop("encoding", "utf-8"), **kwargs)


def write_csv(df: pd.DataFrame, path: str | Path, index: bool = False, **kwargs) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index, encoding=kwargs.pop("encoding", "utf-8"), **kwargs)
