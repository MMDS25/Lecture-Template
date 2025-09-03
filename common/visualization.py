from __future__ import annotations
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def hist(df, column: str, title: str | None = None):
    ax = sns.histplot(df[column], kde=True)
    ax.set_title(title or f"Distribution of {column}")
    return ax


def scatter(df, x: str, y: str, hue: str | None = None, title: str | None = None):
    ax = sns.scatterplot(data=df, x=x, y=y, hue=hue)
    ax.set_title(title or f"{y} vs {x}")
    return ax
