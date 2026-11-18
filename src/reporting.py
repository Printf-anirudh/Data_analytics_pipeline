
from pathlib import Path
from datetime import datetime
import html
import pandas as pd


def generate_report(analysis_results, chart_paths, output_path,
                   cleaning_report=None):
    """
    Generate an HTML report containing analysis results,
    cleaning information and visualizations.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert analysis results into HTML tables
    overview_html = pd.DataFrame(
        [analysis_results.get("overview", {})]
    ).to_html(index=False, border=0)

    numeric_html = pd.DataFrame(
        analysis_results.get("numeric_summary", {})
    ).to_html(border=0)

    categorical_html = pd.DataFrame(
        analysis_results.get("categorical_summary", {})
    ).to_html(border=0)

    missing_html = pd.DataFrame(
        list(analysis_results.get("missing_values", {}).items()),
        columns=["Column", "Missing Values"]
    ).to_html(index=False, border=0)

    correlation_html = pd.DataFrame(
        analysis_results.get("correlation", {})
    ).to_html(border=0)

    # Add generated charts
    charts_html = ""

    for chart_path in chart_paths:
        chart_path = Path(chart_path)

        if chart_path.exists():
            charts_html += f"""
            <div class="chart">
                <h3>{html.escape(chart_path.stem)}</h3>
                <img src="{html.escape(chart_path.relative_to(output_path.parent).as_posix())}"
                     alt="{html.escape(chart_path.stem)}">
            </div>
            """

    # Add cleaning summary if available
    cleaning_html = ""

    if cleaning_report:
        cleaning_html = (
            "<h2>Cleaning Summary</h2>"
            + pd.DataFrame(
                [cleaning_report]
            ).to_html(index=False, border=0)
        )

    # Build final HTML document
    report_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Data Analytics Report</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background: #f4f6f9;
                color: #222;
            }}

            h1, h2 {{
                color: #1f3c88;
            }}

            section {{
                background: white;
                padding: 20px;
                margin-bottom: 25px;
                border-radius: 8px;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
            }}

            th, td {{
                padding: 10px;
                border: 1px solid #ddd;
                text-align: left;
            }}

            th {{
                background: #e8edf7;
            }}

            img {{
                max-width: 100%;
                height: auto;
            }}

            .chart {{
                margin-bottom: 30px;
            }}
        </style>
    </head>

    <body>

        <h1>Data Analytics Report</h1>
        <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <section>
            <h2>Dataset Overview</h2>
            {overview_html}
        </section>

        {cleaning_html}

        <section>
            <h2>Numerical Analysis</h2>
            {numeric_html}
        </section>

        <section>
            <h2>Categorical Analysis</h2>
            {categorical_html}
        </section>

        <section>
            <h2>Missing Values</h2>
            {missing_html}
        </section>

        <section>
            <h2>Correlation Analysis</h2>
            {correlation_html}
        </section>

        <section>
            <h2>Visualizations</h2>
            {charts_html}
        </section>

    </body>
    </html>
    """

    output_path.write_text(
        report_content,
        encoding="utf-8"
    )

    print("\n========== REPORT GENERATION ==========")
    print(f"Report saved: {output_path}")
    print("Report generated successfully!")
    print("=======================================\n")

    return str(output_path)
