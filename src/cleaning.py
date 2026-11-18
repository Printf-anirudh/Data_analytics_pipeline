
import pandas as pd


def clean_dataset(df):
    """
    Clean a Pandas DataFrame by:
    1. Removing completely empty columns.
    2. Removing duplicate rows.
    3. Filling missing numerical values with median.
    4. Filling missing text values with 'Unknown'.

    Returns:
        cleaned_df: Cleaned DataFrame
        report: Cleaning operation summary
    """

    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a Pandas DataFrame")

    # Preserve original data
    cleaned_df = df.copy(deep=True)

    # Initialize cleaning report
    report = {
        "rows_before": len(cleaned_df),
        "columns_before": len(cleaned_df.columns),
        "duplicates_removed": 0,
        "empty_columns_removed": [],
        "missing_values_filled": {},
    }

    # STEP 1: Remove completely empty columns
    empty_columns = cleaned_df.columns[
        cleaned_df.isnull().all()
    ].tolist()

    cleaned_df = cleaned_df.drop(columns=empty_columns)

    report["empty_columns_removed"] = empty_columns

    # STEP 2: Remove duplicate rows
    duplicate_count = int(cleaned_df.duplicated().sum())

    cleaned_df = cleaned_df.drop_duplicates()

    report["duplicates_removed"] = duplicate_count

    # STEP 3: Handle missing values
    for column in cleaned_df.columns:

        missing_count = int(cleaned_df[column].isnull().sum())

        if missing_count == 0:
            continue

        # Handle numerical columns
        if pd.api.types.is_numeric_dtype(cleaned_df[column]):

            median_value = cleaned_df[column].median()

            cleaned_df[column] = (
                cleaned_df[column].fillna(median_value)
            )

            strategy = "Median"
            fill_value = median_value

        # Handle text columns
        elif (
            pd.api.types.is_object_dtype(cleaned_df[column])
            or pd.api.types.is_string_dtype(cleaned_df[column])
        ):

            cleaned_df[column] = (
                cleaned_df[column].fillna("Unknown")
            )

            strategy = "Unknown"
            fill_value = "Unknown"

        else:
            continue

        report["missing_values_filled"][column] = {
            "count": missing_count,
            "strategy": strategy,
            "value": fill_value
        }

    # STEP 4: Final statistics
    report["rows_after"] = len(cleaned_df)
    report["columns_after"] = len(cleaned_df.columns)

    report["missing_values_remaining"] = (
        cleaned_df.isnull().sum().to_dict()
    )

    print("\n========== DATA CLEANING ==========")
    print(f"Rows before: {report['rows_before']}")
    print(f"Rows after: {report['rows_after']}")
    print(f"Duplicates removed: {duplicate_count}")
    print(f"Empty columns removed: {empty_columns}")
    print(
        f"Missing values filled: "
        f"{report['missing_values_filled']}"
    )
    print("===================================\n")

    return cleaned_df, report
