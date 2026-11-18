
import pandas as pd


def analyze_dataset(df):
    """
    Perform generic automated analysis on a DataFrame.

    Includes:
    1. Dataset overview
    2. Numerical statistics
    3. Categorical statistics
    4. Missing value analysis
    5. Correlation analysis
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a Pandas DataFrame")

    # STEP 1: Dataset overview
    overview = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "column_names": list(df.columns),
        "duplicate_rows": int(df.duplicated().sum())
    }

    # STEP 2: Numerical analysis
    numeric_df = df.select_dtypes(include="number")

    numeric_summary = {}

    for column in numeric_df.columns:
        numeric_summary[column] = {
            "mean": float(numeric_df[column].mean())
                if not numeric_df[column].empty else None,
            "median": float(numeric_df[column].median())
                if not numeric_df[column].empty else None,
            "minimum": float(numeric_df[column].min())
                if not numeric_df[column].empty else None,
            "maximum": float(numeric_df[column].max())
                if not numeric_df[column].empty else None,
            "std": float(numeric_df[column].std())
                if not numeric_df[column].empty else None
        }

    # STEP 3: Categorical analysis
    categorical_df = df.select_dtypes(
        include=["object", "category", "string", "bool"]
    )

    categorical_summary = {}

    for column in categorical_df.columns:
        value_counts = categorical_df[column].value_counts(
            dropna=True
        )

        categorical_summary[column] = {
            "unique_count": int(categorical_df[column].nunique()),
            "most_frequent": (
                value_counts.index[0]
                if not value_counts.empty else None
            ),
            "frequency": (
                int(value_counts.iloc[0])
                if not value_counts.empty else 0
            )
        }

    # STEP 4: Missing value analysis
    missing_values = {
        column: int(count)
        for column, count in df.isnull().sum().items()
    }

    # STEP 5: Correlation analysis
    correlation = {}

    if len(numeric_df.columns) >= 2:
        correlation = numeric_df.corr().to_dict()

    # STEP 6: Combine results
    results = {
        "overview": overview,
        "numeric_summary": numeric_summary,
        "categorical_summary": categorical_summary,
        "missing_values": missing_values,
        "correlation": correlation
    }

    # Display analysis summary
    print("\n========== DATA ANALYSIS ==========")
    print("Dataset overview:", overview)

    print("\nNumerical summary:")
    print(pd.DataFrame(numeric_summary))

    print("\nCategorical summary:")
    print(categorical_summary)

    print("\nMissing values:")
    print(missing_values)

    print("\nCorrelation:")
    print(pd.DataFrame(correlation))

    print("===================================\n")

    return results
