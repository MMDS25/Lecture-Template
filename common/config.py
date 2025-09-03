from __future__ import annotations
import logging
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Paths:
    project_root: Path
    lectures: Path
    common: Path
    docs: Path

    def for_lecture(self, name: str) -> dict[str, Path]:
        lec = self.lectures / name
        return {
            "root": lec,
            "data": lec / "data",
            "raw": lec / "data" / "raw",
            "interim": lec / "data" / "interim",
            "processed": lec / "data" / "processed",
            "notebooks": lec / "notebooks",
            "models": lec / "models",
            "reports": lec / "reports",
        }


def get_paths(start: str | os.PathLike | None = None) -> Paths:
    """Discover project paths starting from a directory (defaults to CWD)."""
    root = Path(start or Path.cwd()).resolve()
    # Walk upwards to find a pyproject.toml as project root
    for parent in [root, *root.parents]:
        if (parent / "pyproject.toml").exists():
            root = parent
            break
    return Paths(
        project_root=root,
        lectures=root / "lectures",
        common=root / "common",
        docs=root / "docs",
    )


def get_logger(name: str = "ds-lectures", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
