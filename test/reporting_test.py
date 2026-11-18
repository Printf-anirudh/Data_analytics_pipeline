
from pathlib import Path

from src.reporting import generate_report


def test_generate_html_report(tmp_path):
    analysis_results = {
        "overview": {
            "total_rows": 10,
            "total_columns": 3
        },
        "numeric_summary": {
            "marks": {
                "mean": 80.0,
                "median": 82.0
            }
        },
        "categorical_summary": {},
        "missing_values": {
            "marks": 0
        },
        "correlation": {}
    }

    report_path = tmp_path / "report.html"

    result = generate_report(
        analysis_results,
        [],
        report_path
    )

    assert Path(result).exists()
    assert Path(result).suffix == ".html"


def test_report_contains_analysis_results(tmp_path):
    analysis_results = {
        "overview": {
            "total_rows": 10,
            "total_columns": 2
        },
        "numeric_summary": {
            "marks": {
                "mean": 85.0
            }
        },
        "categorical_summary": {},
        "missing_values": {},
        "correlation": {}
    }

    report_path = tmp_path / "report.html"

    generate_report(
        analysis_results,
        [],
        report_path
    )

    content = report_path.read_text(encoding="utf-8")

    assert "10" in content
    assert "marks" in content
    assert "85.0" in content


def test_report_includes_charts(tmp_path):
    chart_path = tmp_path / "marks_histogram.png"
    chart_path.write_bytes(b"sample image")

    analysis_results = {
        "overview": {},
        "numeric_summary": {},
        "categorical_summary": {},
        "missing_values": {},
        "correlation": {}
    }

    report_path = tmp_path / "report.html"

    generate_report(
        analysis_results,
        [str(chart_path)],
        report_path
    )

    content = report_path.read_text(encoding="utf-8")

    assert "marks_histogram.png" in content
    assert "<img" in content
