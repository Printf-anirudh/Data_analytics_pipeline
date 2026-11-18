
import pandas as pd
import pytest

from src.cleaning import clean_dataset


def test_remove_duplicates():
    df = pd.DataFrame({
        "Product": ["Laptop", "Mouse", "Laptop"],
        "Price": [50000, 500, 50000]
    })

    cleaned_df, report = clean_dataset(df)

    assert len(cleaned_df) == 2
    assert report["duplicates_removed"] == 1


def test_fill_missing_numeric_values():
    df = pd.DataFrame({
        "Price": [100, None, 300]
    })

    cleaned_df, report = clean_dataset(df)

    assert cleaned_df["Price"].isnull().sum() == 0
    assert cleaned_df.loc[1, "Price"] == 200


def test_fill_missing_text_values():
    df = pd.DataFrame({
        "Product": ["Laptop", None, "Mouse"]
    })

    cleaned_df, report = clean_dataset(df)

    assert cleaned_df["Product"].isnull().sum() == 0
    assert cleaned_df.loc[1, "Product"] == "Unknown"


def test_remove_empty_columns():
    df = pd.DataFrame({
        "Product": ["Laptop", "Mouse"],
        "EmptyColumn": [None, None]
    })

    cleaned_df, report = clean_dataset(df)

    assert "EmptyColumn" not in cleaned_df.columns
    assert "EmptyColumn" in report["empty_columns_removed"]


def test_original_dataframe_is_preserved():
    df = pd.DataFrame({
        "Price": [100, None, 300]
    })

    original_df = df.copy(deep=True)

    cleaned_df, report = clean_dataset(df)

    pd.testing.assert_frame_equal(df, original_df)
