
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


def generate_charts(df, output_dir):
    """
    Automatically generate charts based on column types.

    Generates:
    1. Histograms for numerical columns.
    2. Bar charts for categorical columns.
    3. Correlation heatmap for multiple numerical columns.

    Returns:
        List of generated chart file paths.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if df.empty:
        return []

    chart_paths = []

    def save_chart(fig, filename):
        path = output_dir / filename
        fig.savefig(path, bbox_inches="tight")
        plt.close(fig)
        chart_paths.append(str(path))

    # STEP 1: Numerical columns
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        values = df[column].dropna()

        if values.empty:
            continue

        fig, ax = plt.subplots(figsize=(8, 5))

        sns.histplot(
            values,
            kde=True,
            ax=ax
        )

        ax.set_title(f"Distribution of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")

        save_chart(
            fig,
            f"{column}_histogram.png"
        )

    # STEP 2: Categorical columns
    categorical_columns = df.select_dtypes(
        include=["object", "category", "string", "bool"]
    ).columns

    for column in categorical_columns:

        values = df[column].value_counts(
            dropna=True
        ).head(15)

        if values.empty:
            continue

        fig, ax = plt.subplots(figsize=(8, 5))

        sns.barplot(
            x=values.index.astype(str),
            y=values.values,
            ax=ax
        )

        ax.set_title(f"Distribution of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Count")

        ax.tick_params(
            axis="x",
            rotation=45
        )

        save_chart(
            fig,
            f"{column}_bar_chart.png"
        )

    # STEP 3: Correlation heatmap
    numeric_df = df.select_dtypes(include="number")

    if len(numeric_df.columns) >= 2:

        correlation = numeric_df.corr()

        fig, ax = plt.subplots(figsize=(8, 6))

        sns.heatmap(
            correlation,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
            ax=ax
        )

        ax.set_title("Correlation Heatmap")

        save_chart(
            fig,
            "correlation_heatmap.png"
        )

    print("\n========== VISUALIZATION ==========")
    print(f"Charts generated: {len(chart_paths)}")

    for path in chart_paths:
        print(path)

    print("===================================\n")

    return chart_paths
