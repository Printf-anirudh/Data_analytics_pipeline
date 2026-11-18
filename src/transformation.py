
import pandas as pd
import re


def transform_dataset(df):
    """
    Transform a DataFrame by:
    1. Standardizing column names.
    2. Creating a revenue column.
    3. Converting date columns into datetime format.

    Returns:
        Transformed DataFrame
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a Pandas DataFrame")

    # Preserve original data
    transformed_df = df.copy(deep=True)

    # STEP 1: Standardize column names
    def standardize_name(column):
        name = str(column).strip()
        name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
        name = re.sub(r"[^a-zA-Z0-9]+", "_", name)
        return name.strip("_").lower()

    transformed_df.columns = [
        standardize_name(column)
        for column in transformed_df.columns
    ]

    # STEP 2: Create revenue column
    if {"quantity", "unit_price"}.issubset(
        transformed_df.columns
    ):
        transformed_df["revenue"] = (
            transformed_df["quantity"]
            * transformed_df["unit_price"]
        )

    # STEP 3: Convert date columns
    date_columns = [
        column for column in transformed_df.columns
        if column == "date" or column.endswith("_date")
    ]

    for column in date_columns:
        transformed_df[column] = pd.to_datetime(
            transformed_df[column],
            errors="coerce"
        )

    print("\n========== DATA TRANSFORMATION ==========")
    print(f"Columns: {list(transformed_df.columns)}")

    if "revenue" in transformed_df.columns:
        print("Revenue column created successfully!")

    print("Transformation successful!")
    print("=========================================\n")

    return transformed_df
