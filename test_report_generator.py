
import pandas as pd

from validator import validate_records
from analyzer import analyze_data
from report_generator import generate_reports


def main():

    print("=" * 60)
    print("       COMMON RECORDS ANALYZER")
    print("              REPORT GENERATOR")
    print("=" * 60)

    try:

        # Load dataset
        print("\n[1] Loading dataset...")

        df = pd.read_csv("data/sample_records.csv")

        print("Dataset loaded:", len(df), "records")

        # Validate dataset
        print("\n[2] Validating records...")

        valid_df, invalid_df, issues = validate_records(df)

        print("Valid records:", len(valid_df))
        print("Invalid records:", len(invalid_df))

        # Analyze dataset
        print("\n[3] Analyzing dataset...")

        results = analyze_data(valid_df)

        print("Analysis completed!")

        # Generate reports
        print("\n[4] Generating reports...")

        files = generate_reports(
            results,
            valid_df,
            invalid_df,
            issues
        )

        print("\nREPORTS GENERATED SUCCESSFULLY!")
        print("-" * 50)

        for report_type, filepath in files.items():

            print(f"{report_type.upper()}: {filepath}")

        print("\nAll reports saved in the reports folder.")

    except FileNotFoundError:
        print("Error: Dataset file not found.")

    except pd.errors.EmptyDataError:
        print("Error: Dataset is empty.")

    except PermissionError:
        print("Error: Permission denied while saving reports.")

    except Exception as error:
        print("Unexpected error:", error)
        raise


if __name__ == "__main__":
    main()
