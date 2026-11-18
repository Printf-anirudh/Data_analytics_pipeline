
import pandas as pd
import pytest

from src.extraction import load_dataset


def test_load_csv(tmp_path):
    # Arrange: create a sample CSV file
    file_path = tmp_path / "sales.csv"

    data = {
        "Product": ["Laptop", "Mouse"],
        "Price": [50000, 500]
    }

    pd.DataFrame(data).to_csv(file_path, index=False)

    # Act: extract the dataset
    df = load_dataset(file_path)

    # Assert: verify the extracted data
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert "Product" in df.columns


def test_load_excel(tmp_path):
    file_path = tmp_path / "sales.xlsx"

    data = {
        "Product": ["Laptop", "Mouse"],
        "Price": [50000, 500]
    }

    pd.DataFrame(data).to_excel(file_path, index=False)

    df = load_dataset(file_path)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_dataset("nonexistent.csv")


def test_unsupported_file():
    with pytest.raises(ValueError):
        load_dataset("sales.txt")
