#!/usr/bin/env python3
from __future__ import annotations
import argparse
import os
import re
from pathlib import Path
from textwrap import dedent

from common.config import get_paths, get_logger


def slug_to_pkg(name: str) -> str:
    # Replace non-alphanumeric with underscore, ensure doesn't start with digit
    pkg = re.sub(r"[^0-9a-zA-Z]+", "_", name).strip("_").lower()
    if re.match(r"^\d", pkg):
        pkg = f"lec_{pkg}"
    return pkg


def scaffold(lecture_name: str) -> Path:
    log = get_logger("new_lecture")
    paths = get_paths()
    lec_root = paths.lectures / lecture_name
    pkg_name = slug_to_pkg(lecture_name)

    # Directories
    subdirs = [
        lec_root / "data" / "raw",
        lec_root / "data" / "interim",
        lec_root / "data" / "processed",
        lec_root / "notebooks",
        lec_root / "models",
        lec_root / "reports" / "figures",
        lec_root / "exercises",
        lec_root / "lecture_code" / "modeling",
    ]
    for d in subdirs:
        d.mkdir(parents=True, exist_ok=True)

    # .gitkeep files for empty data dirs
    for d in [lec_root / "data" / "raw", lec_root / "data" / "interim", lec_root / "data" / "processed"]:
        (d / ".gitkeep").write_text("")

    # Notebook placeholder
    (lec_root / "notebooks" / "1.0-intro-overview.ipynb").write_text(
        dedent(
            """
            {
              "cells": [],
              "metadata": {},
              "nbformat": 4,
              "nbformat_minor": 5
            }
            """
        ).strip()
    )

    # Requirements placeholder (optional override)
    (lec_root / "requirements.txt").write_text("# Add lecture-specific dependencies here\n")

    # Lecture shared code (lecture_code)
    (lec_root / "lecture_code" / "__init__.py").write_text("\n")

    (lec_root / "lecture_code" / "dataset.py").write_text(
        dedent(
            f"""
            from __future__ import annotations
            from pathlib import Path
            import pandas as pd
            from common.dataio import read_csv

            def load_example(path: str | Path) -> pd.DataFrame:
                return read_csv(path)
            """
        ).lstrip()
    )

    (lec_root / "lecture_code" / "features.py").write_text(
        dedent(
            """
            from __future__ import annotations
            import pandas as pd

            def add_basic_features(df: pd.DataFrame) -> pd.DataFrame:
                # TODO: implement feature engineering
                return df.copy()
            """
        ).lstrip()
    )

    (lec_root / "lecture_code" / "modeling" / "train.py").write_text(
        dedent(
            """
            from __future__ import annotations
            from dataclasses import dataclass
            import pandas as pd
            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import mean_squared_error

            @dataclass
            class TrainConfig:
                test_size: float = 0.2
                random_state: int = 42

            def train(df: pd.DataFrame, target: str, config: TrainConfig = TrainConfig()):
                X = df.drop(columns=[target])
                y = df[target]
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=config.test_size, random_state=config.random_state
                )
                model = LinearRegression()
                model.fit(X_train, y_train)
                preds = model.predict(X_test)
                rmse = mean_squared_error(y_test, preds, squared=False)
                return model, rmse
            """
        ).lstrip()
    )

    # Exercises scaffold: create a starter exercise uebung01
    ex_name = "uebung01"
    ex_root = lec_root / "exercises" / ex_name
    code_root = ex_root / ex_name
    (ex_root / "notebooks").mkdir(parents=True, exist_ok=True)
    (code_root / "modeling").mkdir(parents=True, exist_ok=True)

    (ex_root / "notebooks" / "1.0-uebung01-starter.ipynb").write_text(
        dedent(
            """
            {
              "cells": [],
              "metadata": {},
              "nbformat": 4,
              "nbformat_minor": 5
            }
            """
        ).strip()
    )

    (code_root / "__init__.py").write_text("\n")
    (code_root / "dataset.py").write_text(
        dedent(
            """
            from __future__ import annotations
            from pathlib import Path
            import pandas as pd
            from common.dataio import read_csv

            def load_example(path: str | Path) -> pd.DataFrame:
                return read_csv(path)
            """
        ).lstrip()
    )
    (code_root / "features.py").write_text(
        dedent(
            """
            from __future__ import annotations
            import pandas as pd

            def add_basic_features(df: pd.DataFrame) -> pd.DataFrame:
                return df.copy()
            """
        ).lstrip()
    )
    (code_root / "modeling" / "train.py").write_text(
        dedent(
            """
            from __future__ import annotations
            from dataclasses import dataclass
            import pandas as pd
            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import mean_squared_error

            @dataclass
            class TrainConfig:
                test_size: float = 0.2
                random_state: int = 42

            def train(df: pd.DataFrame, target: str, config: TrainConfig = TrainConfig()):
                X = df.drop(columns=[target])
                y = df[target]
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=config.test_size, random_state=config.random_state
                )
                model = LinearRegression()
                model.fit(X_train, y_train)
                preds = model.predict(X_test)
                rmse = mean_squared_error(y_test, preds, squared=False)
                return model, rmse
            """
        ).lstrip()
    )

    # README for the lecture
    (lec_root / "README.md").write_text(
        dedent(
            f"""
            # {lecture_name}

            This lecture was scaffolded by scripts/new_lecture.py

            Structure:
            - data/{{raw, interim, processed}}
            - notebooks/
            - models/
            - reports/figures/
            - lecture_code/ (shared code for this lecture)
            - exercises/
                - uebung01/
                    - notebooks/
                    - uebung01/  # exercise-specific code package named like the exercise
            """
        ).lstrip()
    )

    log.info("Scaffolded lecture at %s", lec_root)
    return lec_root


def parse_args() -> str:
    parser = argparse.ArgumentParser(description="Scaffold a new lecture")
    parser.add_argument("name", help="Lecture folder name, e.g., 03-neural-networks")
    args = parser.parse_args()
    return args.name


if __name__ == "__main__":
    name = parse_args()
    scaffold(name)
