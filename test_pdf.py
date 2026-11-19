
import pandas as pd

from validator import validate_records
from analyzer import analyze_data
from report_generator import generate_reports


def main():

    print("=" * 55)
    print("       DATAPULSE PDF REPORT TEST")
    print("=" * 55)

    try:

        print("\n[1] Loading dataset...")

        df = pd.read_csv("data/sample_records.csv")

        print("Dataset loaded:", len(df))

        print("\n[2] Validating dataset...")

        valid_df, invalid_df, issues = validate_records(df)

        print("Valid records:", len(valid_df))
        print("Invalid records:", len(invalid_df))

        print("\n[3] Analyzing data...")

        results = analyze_data(valid_df)

        print("Analysis completed!")

        print("\n[4] Generating PDF and other reports...")

        files = generate_reports(
            results,
            valid_df,
            invalid_df,
            issues
        )

        print("\nREPORT GENERATION SUCCESSFUL!")
        print("-" * 45)

        for name, path in files.items():

            print(f"{name.upper()}: {path}")

        pdf_path = files["pdf"]

        print("\nPDF EXISTS:", pdf_path.exists())

        if pdf_path.exists():
            print("PDF SIZE:", pdf_path.stat().st_size, "bytes")

        print("\nDATAPULSE REPORT TEST COMPLETED!")

    except Exception as error:

        print("ERROR:", error)
        raise


if __name__ == "__main__":
    main()
