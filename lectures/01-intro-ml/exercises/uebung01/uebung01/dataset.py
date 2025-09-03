from __future__ import annotations
from pathlib import Path
import pandas as pd
from common.dataio import read_csv

def load_example(path: str | Path) -> pd.DataFrame:
    return read_csv(path)
