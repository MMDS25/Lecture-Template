#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from textwrap import dedent

from common.config import get_paths, get_logger


def scaffold_exercise(lecture_name: str, exercise_name: str) -> Path:
    """
    Create a new exercise under lectures/<lecture_name>/exercises/<exercise_name>
    Structure:
      - notebooks/
      - <exercise_name>/
          - dataset.py, features.py, modeling/train.py
    """
    log = get_logger("new_exercise")
    paths = get_paths()
    lec_root = paths.lectures / lecture_name
    if not lec_root.exists():
        raise FileNotFoundError(f"Lecture '{lecture_name}' not found at {lec_root}")

    ex_root = lec_root / "exercises" / exercise_name
    code_root = ex_root / exercise_name
    (ex_root / "notebooks").mkdir(parents=True, exist_ok=True)
    (code_root / "modeling").mkdir(parents=True, exist_ok=True)

    # Minimal starter notebook
    (ex_root / "notebooks" / "1.0-starter.ipynb").write_text(
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

    # Code files
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

    log.info("Created exercise at %s", ex_root)
    return ex_root


def parse_args() -> tuple[str, str]:
    parser = argparse.ArgumentParser(description="Scaffold a new exercise inside a lecture")
    parser.add_argument("lecture", help="Lecture folder name, e.g., 03-neural-networks")
    parser.add_argument("name", help="Exercise folder name, e.g., uebung02")
    args = parser.parse_args()
    return args.lecture, args.name


if __name__ == "__main__":
    lecture, name = parse_args()
    scaffold_exercise(lecture, name)
