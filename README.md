# Diabetes Prediction with `syft_flwr`

Diabetes prediction using [syft_flwr](https://github.com/OpenMined/syft-flwr)

Dataset: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database/


## Data Scientist

```bash
uv venv
source .venv/bin/activate
cd fl-diabetes-prediction
uv sync --active
```

Run the `ds.ipynb`


## Data Owner
```bash
uv venv
source .venv/bin/activate
uv pip install jupyter
```
Run the `do.ipynb`