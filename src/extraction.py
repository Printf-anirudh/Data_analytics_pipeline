import pandas as pd
from pathlib import Path
def load_dataset(file_path):
    """
    Extract data from CSV or Excel files
    and return it as a Pandas DataFrame.
    """
    file_path = Path(file_path)
    # Identify file extension
    extension = file_path.suffix.lower()
# Validate supported formats
    if extension not in [".csv", ".xlsx"]:
      raise ValueError(
        f"Unsupported file format: {extension}"
    )
# Check whether file exists
    if not file_path.exists():
     raise FileNotFoundError(
        f"Dataset not found: {file_path}"
    )
    # Extract CSV
    if extension == ".csv":
        df = pd.read_csv(file_path)
    # Extract Excel
    elif extension == ".xlsx":
        df = pd.read_excel(file_path)
    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )
    print("\n========== DATA EXTRACTION ==========")
    print(f"File: {file_path.name}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print("Extraction successful!")
    print("=====================================\n")
    return df