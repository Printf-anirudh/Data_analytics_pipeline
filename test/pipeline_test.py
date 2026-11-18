
import pandas as pd

from main import run_pipeline


def test_complete_pipeline(tmp_path):
    # Create sample input dataset
    input_file = tmp_path / "students.csv"

    df = pd.DataFrame({
        "Student Name": ["A", "B", "C", "A"],
        "Department": ["CSE", "ECE", "CSE", "CSE"],
        "Marks": [85, 70, 95, 85],
        "Attendance": [90, 80, 95, 90]
    })

    df.to_csv(input_file, index=False)

    output_dir = tmp_path / "output"

    # Execute complete pipeline
    results = run_pipeline(input_file, output_dir)

    # Verify generated files
    assert results["processed_data"].exists()
    assert results["report"].exists()
    assert results["processed_data"].suffix == ".csv"

    # Verify charts were generated
    assert len(results["charts"]) > 0
