
import pandas as pd

from src.analysis import analyze_dataset


def create_sample_data():
    return pd.DataFrame({
        "student": ["A", "B", "C", "A"],
        "department": ["CSE", "ECE", "CSE", "CSE"],
        "marks": [85, 70, 95, 85],
        "attendance": [90, 80, 95, 90]
    })


def test_dataset_overview():
    result = analyze_dataset(create_sample_data())

    assert result["overview"]["total_rows"] == 4
    assert result["overview"]["total_columns"] == 4


def test_numeric_analysis():
    result = analyze_dataset(create_sample_data())

    assert "marks" in result["numeric_summary"]
    assert result["numeric_summary"]["marks"]["mean"] == 83.75


def test_categorical_analysis():
    result = analyze_dataset(create_sample_data())

    assert "department" in result["categorical_summary"]
    assert result["categorical_summary"]["department"]["unique_count"] == 2


def test_missing_value_analysis():
    df = pd.DataFrame({
        "name": ["A", "B", None],
        "marks": [80, None, 90]
    })

    result = analyze_dataset(df)

    assert result["missing_values"]["name"] == 1
    assert result["missing_values"]["marks"] == 1


def test_correlation_analysis():
    result = analyze_dataset(create_sample_data())

    assert "marks" in result["correlation"]
    assert "attendance" in result["correlation"]["marks"]
