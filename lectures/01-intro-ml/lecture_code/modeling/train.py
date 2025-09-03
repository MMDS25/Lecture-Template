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
