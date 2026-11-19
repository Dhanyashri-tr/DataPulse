
import pandas as pd
import traceback

from validator import validate_records
from analyzer import analyze_data


def main():

    print("=" * 60)
    print("COMMON RECORDS ANALYZER - DEBUG MODE")
    print("=" * 60)

    try:
        print("\n[1] Loading dataset...")

        df = pd.read_csv("data/sample_records.csv")

        print("Dataset loaded successfully!")

        print("\n[2] Testing validation module...")

        valid_df, invalid_df, issues = validate_records(df)

        print("Validation successful!")
        print("Valid records:", len(valid_df))
        print("Invalid records:", len(invalid_df))

        print("\n[3] Testing analysis module...")

        results = analyze_data(valid_df)

        print("Analysis successful!")

        print("\n[4] Dataset overview:")
        print(results["overview"])

        print("\n[5] Numerical summary:")
        print(results["numerical_summary"])

        print("\n[6] Categorical summary:")
        print(results["categorical_summary"])

        print("\n[7] Automatic insights:")

        for insight in results["insights"]:
            print("-", insight)

        print("\nALL TESTS COMPLETED SUCCESSFULLY!")

    except Exception:
        print("\nFULL ERROR TRACEBACK:")
        traceback.print_exc()


if __name__ == "__main__":
    main()
