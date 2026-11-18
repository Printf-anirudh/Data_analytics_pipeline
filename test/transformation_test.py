import pandas as pd

from src.transformation import transform_dataset


def test_standardize_column_names():
    df = pd.DataFrame({
        "Product Name": ["Laptop"],
        "UnitPrice": [50000]
    })

    transformed_df = transform_dataset(df)

    assert "product_name" in transformed_df.columns
    assert "unit_price" in transformed_df.columns


def test_create_revenue_column():
    df = pd.DataFrame({
        "Quantity": [2, 5],
        "UnitPrice": [50000, 500]
    })

    transformed_df = transform_dataset(df)

    assert "revenue" in transformed_df.columns
    assert transformed_df["revenue"].tolist() == [100000, 2500]


def test_convert_date_column():
    df = pd.DataFrame({
        "Date": ["2026-01-15", "2026-02-20"]
    })

    transformed_df = transform_dataset(df)

    assert pd.api.types.is_datetime64_any_dtype(
        transformed_df["date"]
    )


def test_original_dataframe_is_preserved():
    df = pd.DataFrame({
        "Quantity": [2],
        "UnitPrice": [500]
    })

    original_df = df.copy(deep=True)

    transform_dataset(df)

    pd.testing.assert_frame_equal(df, original_df)
