
import pandas as pd


def validate_columns(df):
    """Check whether the dataset has valid column names and structure."""

    if df.empty:
        raise ValueError("The uploaded dataset is empty.")

    if len(df.columns) == 0:
        raise ValueError("No columns found.")

    if df.columns.duplicated().any():
        raise ValueError("Duplicate column names detected.")

    if any(str(col).strip() == "" for col in df.columns):
        raise ValueError("Empty column names detected.")

    return True


def is_missing(value):
    """Treat NaN, None, and empty or whitespace-only strings as missing."""

    if pd.isna(value):
        return True

    if isinstance(value, str) and value.strip() == "":
        return True

    return False


def validate_records(df):
    """
    Validate dataset records.

    Checks:
    - Missing values
    - Duplicate records
    - Duplicate IDs
    - Invalid numerical values
    - Negative or zero quantities
    - Invalid prices
    - Invalid age and marks
    - Invalid payment statuses

    Returns:
        valid_df, invalid_df, issues
    """

    validate_columns(df)

    # Reset index for consistent row numbering.
    df = df.reset_index(drop=True).copy()

    # Normalize column names for validation only.
    column_lookup = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    issues = []
    invalid_indexes = set()

    def add_issue(index, issue, details):
        """Record an issue and mark the corresponding row invalid."""

        issues.append({
            "row": index + 2,
            "issue": issue,
            "details": details
        })

        invalid_indexes.add(index)

    # --------------------------------------------------
    # 1. CHECK MISSING VALUES
    # --------------------------------------------------

    for index, row in df.iterrows():

        missing_columns = [
            column
            for column, value in row.items()
            if is_missing(value)
        ]

        if missing_columns:
            add_issue(
                index,
                "Missing values",
                ", ".join(str(col) for col in missing_columns)
            )

    # --------------------------------------------------
    # 2. CHECK DUPLICATE RECORDS
    # --------------------------------------------------

    duplicate_rows = df.duplicated(keep="first")

    for index in df[duplicate_rows].index:

        add_issue(
            index,
            "Duplicate record",
            "Entire record already exists"
        )

    # --------------------------------------------------
    # 3. CHECK DUPLICATE IDENTIFIERS
    # --------------------------------------------------

    identifier_columns = [
        column
        for normalized_name, column in column_lookup.items()
        if normalized_name == "id"
        or normalized_name.endswith("_id")
    ]

    for column in identifier_columns:

        seen_ids = set()

        for index, value in df[column].items():

            if is_missing(value):
                continue

            identifier = str(value).strip().casefold()

            if identifier in seen_ids:
                add_issue(
                    index,
                    "Duplicate ID",
                    f"Column: {column}, ID: {value}"
                )
            else:
                seen_ids.add(identifier)

    # --------------------------------------------------
    # 4. CHECK NUMERICAL VALUES
    # --------------------------------------------------

    numeric_columns = {
        "marks",
        "age",
        "quantity",
        "price",
        "unit_price",
        "salary"
    }

    for normalized_name, column in column_lookup.items():

        if normalized_name not in numeric_columns:
            continue

        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        for index, value in df[column].items():

            if is_missing(value):
                continue

            number = numeric_values.loc[index]

            if pd.isna(number):
                add_issue(
                    index,
                    "Invalid numerical value",
                    f"Column: {column}, Value: {value}"
                )
                continue

            # Quantity must be a positive whole number.
            if normalized_name == "quantity":

                if number <= 0:
                    add_issue(
                        index,
                        "Invalid quantity",
                        "Quantity must be greater than zero"
                    )

                elif number % 1 != 0:
                    add_issue(
                        index,
                        "Invalid quantity",
                        "Quantity must be a whole number"
                    )

            # Prices must be greater than zero.
            elif normalized_name in {"price", "unit_price"}:

                if number <= 0:
                    add_issue(
                        index,
                        "Invalid price",
                        f"{column} must be greater than zero"
                    )

            # Age must be positive.
            elif normalized_name == "age":

                if number <= 0:
                    add_issue(
                        index,
                        "Invalid age",
                        "Age must be greater than zero"
                    )

            # Marks must be between 0 and 100.
            elif normalized_name == "marks":

                if not 0 <= number <= 100:
                    add_issue(
                        index,
                        "Invalid marks",
                        "Marks must be between 0 and 100"
                    )

            # Salary cannot be negative.
            elif normalized_name == "salary":

                if number < 0:
                    add_issue(
                        index,
                        "Invalid salary",
                        "Salary cannot be negative"
                    )

    # --------------------------------------------------
    # 5. CHECK PAYMENT STATUS
    # --------------------------------------------------

    if "payment_status" in column_lookup:

        column = column_lookup["payment_status"]

        allowed_statuses = {
            "completed",
            "pending",
            "cancelled"
        }

        for index, value in df[column].items():

            if is_missing(value):
                continue

            status = str(value).strip().casefold()

            if status not in allowed_statuses:
                add_issue(
                    index,
                    "Invalid payment status",
                    f"Unexpected status: {value}"
                )

    # --------------------------------------------------
    # 6. SEPARATE VALID AND INVALID RECORDS
    # --------------------------------------------------

    valid_indexes = [
        index for index in range(len(df))
        if index not in invalid_indexes
    ]

    invalid_indexes_sorted = sorted(invalid_indexes)

    valid_df = df.loc[valid_indexes].copy()

    invalid_df = df.loc[invalid_indexes_sorted].copy()

    return valid_df, invalid_df, issues
