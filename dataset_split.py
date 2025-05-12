from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

NUM_CLIENTS = 5
DATASET_PATH = Path(__file__).parent / "dataset" / "pima-indians-diabetes-database"
assert DATASET_PATH.exists()

SPLIT_PATH = DATASET_PATH / "split_dataset"
SPLIT_PATH.mkdir(parents=True, exist_ok=True)

column_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'y']
df_diabetes = pd.read_csv(DATASET_PATH / "diabetes.csv", header=0, names=column_names)

# Shuffle the dataset
df_diabetes = df_diabetes.sample(frac=1, random_state=42).reset_index(drop=True)

# Calculate rows per client
total_rows = len(df_diabetes)
rows_per_client = total_rows // NUM_CLIENTS

# Split data for each client
for client_id in range(NUM_CLIENTS):
    # Create client directories
    client_path = SPLIT_PATH / f"client_{client_id}"
    mock_path = client_path / "mock"
    private_path = client_path / "private"
    readme_path = client_path / "README.md"

    for path in [mock_path, private_path]:
        path.mkdir(parents=True, exist_ok=True)

    # Get client's portion of data
    start_idx = client_id * rows_per_client
    end_idx = start_idx + rows_per_client if client_id < NUM_CLIENTS - 1 else total_rows
    client_data = df_diabetes.iloc[start_idx:end_idx].copy()

    # Split into train and test for private data
    private_train, private_test = train_test_split(client_data, test_size=0.2, random_state=42)

    # Create smaller mock datasets (10 rows each)
    mock_train = private_train.sample(n=10, random_state=42)
    mock_test = private_test.sample(n=10, random_state=42)

    # Save the datasets
    private_train.to_csv(private_path / "train.csv", index=False)
    private_test.to_csv(private_path / "test.csv", index=False)
    mock_train.to_csv(mock_path / "train.csv", index=False)
    mock_test.to_csv(mock_path / "test.csv", index=False)

    # Create README.md file
    readme_content = f"""
# Pima Indians Diabetes Dataset Split

This directory contains a dataset split for [Pima Indians Diabetes Database](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database).

## Mock Data
The mock data is a smaller dataset (10 rows) that is used to test the model components.

## Private Data
The private data is the remaining data that is used to train the model.
"""

    with open(readme_path, "w") as f:
        f.write(readme_content)

print("Dataset splitting completed successfully!")