
from pathlib import Path

from src.extraction import load_dataset
from src.cleaning import clean_dataset
from src.transformation import transform_dataset
from src.analysis import analyze_dataset
from src.visualization import generate_charts
from src.reporting import generate_report


def run_pipeline(input_path, output_dir="data/output"):

    input_path = Path(input_path)
    output_dir = Path(output_dir)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n====================================")
    print("       DATA ANALYTICS PIPELINE")
    print("====================================")

    # STEP 1: Extraction
    df = load_dataset(input_path)

    # STEP 2: Cleaning
    cleaned_df, cleaning_report = clean_dataset(df)

    # STEP 3: Transformation
    transformed_df = transform_dataset(cleaned_df)

    # STEP 4: Analysis
    analysis_results = analyze_dataset(transformed_df)

    # STEP 5: Visualization
    charts_dir = output_dir / "charts"

    chart_paths = generate_charts(
        transformed_df,
        charts_dir
    )

    # STEP 6: Save processed dataset
    processed_path = output_dir / "processed_data.csv"

    transformed_df.to_csv(
        processed_path,
        index=False
    )

    # STEP 7: Generate report
    report_path = output_dir / "report.html"

    generate_report(
        analysis_results,
        chart_paths,
        report_path,
        cleaning_report
    )

    print("\n====================================")
    print("       PIPELINE COMPLETED")
    print("====================================")
    print(f"Processed data: {processed_path}")
    print(f"Charts: {charts_dir}")
    print(f"Report: {report_path}")

    return {
        "processed_data": processed_path,
        "charts": chart_paths,
        "report": report_path
    }


if __name__ == "__main__":

    input_dir = Path("data/input")

    # Find supported input files
    input_files = sorted(
        file for file in input_dir.iterdir()
        if file.is_file()
        and file.suffix.lower() in [".csv", ".xlsx"]
    ) if input_dir.exists() else []

    if not input_files:
        print("No CSV or Excel files found in data/input/")
    else:
        for input_file in input_files:
            print(f"\nProcessing: {input_file.name}")
            run_pipeline(input_file)
