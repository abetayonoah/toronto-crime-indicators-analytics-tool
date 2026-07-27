import pandas as pd

from src.data_loader import (
    load_data,
    data_preview
)


def test_load_data():

    df = load_data(
        "data/Toronto_Crime_Indicators.csv"
    )

    assert df is not None
    assert isinstance(df, pd.DataFrame)


def test_data_preview():

    df = load_data(
        "data/Toronto_Crime_Indicators.csv"
    )

    preview = data_preview(df)

    assert preview is not None
    assert len(preview) <= 5
    assert isinstance(preview, pd.DataFrame)