
import pandas as pd

from src.visualization import generate_charts


def test_generate_numerical_chart(tmp_path):
    df = pd.DataFrame({
        "marks": [70, 80, 90, 85, 60]
    })

    charts = generate_charts(df, tmp_path)

    assert len(charts) >= 1
    assert all(path.endswith(".png") for path in charts)


def test_generate_categorical_chart(tmp_path):
    df = pd.DataFrame({
        "department": ["CSE", "ECE", "CSE", "ISE"]
    })

    charts = generate_charts(df, tmp_path)

    assert len(charts) >= 1
    assert all(path.endswith(".png") for path in charts)


def test_generate_multiple_charts(tmp_path):
    df = pd.DataFrame({
        "department": ["CSE", "ECE", "CSE", "ISE"],
        "marks": [80, 70, 90, 85],
        "attendance": [90, 80, 95, 85]
    })

    charts = generate_charts(df, tmp_path)

    assert len(charts) >= 3


def test_empty_dataframe(tmp_path):
    df = pd.DataFrame()

    charts = generate_charts(df, tmp_path)

    assert charts == []
