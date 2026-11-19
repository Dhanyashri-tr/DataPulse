
import pandas as pd
from validator import validate_records


def main():

    print("=" * 50)
    print("       DATA VALIDATION TEST")
    print("=" * 50)

    # Sample dataset containing intentional errors
    data = {
        "id": [1, 2, 3, 3, 5, 6],
        "name": [
            "Akhil",
            "Rahul",
            "Ananya",
            "Priya",
            None,
            "Kiran"
        ],
        "category": [
            "Science",
            "Commerce",
            "Science",
            "Arts",
            "Commerce",
            "Science"
        ],
        "marks": [
            85,
            76,
            92,
            88,
            67,
            "hello"
        ]
    }

    df = pd.DataFrame(data)

    try:

        valid_df, invalid_df, issues = validate_records(df)

        print("\nORIGINAL RECORDS:", len(df))
        print("VALID RECORDS:", len(valid_df))
        print("INVALID RECORDS:", len(invalid_df))

        print("\nVALIDATION ISSUES")
        print("-" * 40)

        if issues:
            for issue in issues:
                print(
                    f"Row {issue['row']} | "
                    f"{issue['issue']} | "
                    f"{issue['details']}"
                )
        else:
            print("No validation issues found!")

        print("\nVALID RECORDS:")
        print(valid_df.to_string(index=False))

        print("\nINVALID RECORDS:")
        print(invalid_df.to_string(index=False))

        print("\nVALIDATION TEST COMPLETED!")

    except ValueError as error:
        print("Validation Error:", error)

    except Exception as error:
        print("Unexpected Error:", error)


if __name__ == "__main__":
    main()
