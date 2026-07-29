from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "toronto_crime_sample.csv"


def load_data(file_path=None):
    """Load the Toronto crime dataset and return a pandas DataFrame."""

    path = Path(file_path) if file_path else DEFAULT_DATA_PATH

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {path}. "
            "Please add toronto_crime_sample.csv to the data folder."
        )

    df = pd.read_csv(path, low_memory=False)

    if df.empty:
        raise ValueError("The dataset was loaded but contains no records.")

    return df


def data_preview(df, rows=5):
    """Return the first rows of the dataset."""

    if df is None:
        raise ValueError("Cannot preview data because the DataFrame is None.")

    return df.head(rows)
