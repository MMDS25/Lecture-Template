# DS Lectures Template

This repository provides a multi-lecture Data Science lectures template. Each lecture is a mini-project with a consistent structure and shared infrastructure in `common/`.

Structure:

- lectures/
  - 01-intro-ml/
    - data/{raw,interim,processed}
    - notebooks/
    - models/
    - reports/figures/
    - lecture_code/               # shared code for the lecture
    - exercises/
      - uebung01/
        - notebooks/
        - uebung01/               # exercise-specific code package named like the exercise
- common/ (shared utilities: config, utils, dataio, visualization)
- scripts/ (helper scripts, e.g., new_lecture.py, new_exercise.py)
- docs/ (documentation scaffolding)
- Makefile (common commands)
- pyproject.toml (global dependencies)

Quick start:

- Ensure Python 3.9+ is installed.
- Install base deps: `pip install -e .` or with Poetry/uv if you prefer.
- Create a new lecture:

  make new-lecture NAME=03-neural-networks

- Create a new exercise under a lecture:

  make new-exercise LECTURE=03-neural-networks NAME=uebung02

This will scaffold `lectures/03-neural-networks` with the standard layout and `exercises/uebung02` inside it. If a `requirements.txt` exists in the lecture folder, you can install them via:

  make install-lecture-reqs NAME=03-neural-networks

Conventions:

- Shared code goes into `common/` to avoid duplication.
- Data flow: `data/raw -> data/interim -> data/processed`.
- Each lecture may define additional dependencies in its own `requirements.txt`.
