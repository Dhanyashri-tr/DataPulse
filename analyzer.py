
import pandas as pd


# ==========================================================
# 1. DATASET OVERVIEW
# ==========================================================

def get_dataset_overview(df):

    """Generate general information about the dataset."""

    return {
        "total_records": len(df),
        "total_columns": len(df.columns),
        "column_names": list(df.columns),
        "duplicate_records": int(df.duplicated().sum()),
        "missing_values": int(df.isnull().sum().sum()),
        "memory_usage_kb": round(
            df.memory_usage(deep=True).sum() / 1024, 2
        )
    }


# ==========================================================
# 2. IDENTIFIER DETECTION
# ==========================================================

def is_identifier_column(column):

    """Identify columns that represent record identifiers."""

    name = str(column).strip().lower()

    identifier_names = {
        "id",
        "identifier",
        "index",
        "serial",
        "serial_number",
        "record_id",
        "employee_id",
        "student_id",
        "customer_id",
        "order_id",
        "product_id"
    }

    return (
        name in identifier_names
        or name.endswith("_id")
        or name.endswith("_identifier")
    )


# ==========================================================
# 3. NUMERICAL ANALYSIS
# ==========================================================

def analyze_numerical_data(df):

    """Calculate statistics for meaningful numerical columns."""

    numerical_summary = {}

    for column in df.select_dtypes(include="number").columns:

        # Ignore identifier columns
        if is_identifier_column(column):
            continue

        values = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        if values.empty:
            continue

        numerical_summary[column] = {
            "count": int(values.count()),
            "sum": round(float(values.sum()), 2),
            "average": round(float(values.mean()), 2),
            "median": round(float(values.median()), 2),
            "minimum": round(float(values.min()), 2),
            "maximum": round(float(values.max()), 2),
            "standard_deviation": round(
                float(values.std()), 2
            ) if len(values) > 1 else 0.0
        }

    return numerical_summary


# ==========================================================
# 4. CATEGORICAL COLUMN DETECTION
# ==========================================================

def is_meaningful_category(series):

    """
    Keep useful categorical columns.
    Exclude high-cardinality fields such as individual names.
    """

    non_missing = series.dropna()

    if non_missing.empty:
        return False

    unique_count = non_missing.nunique()

    unique_ratio = unique_count / len(non_missing)

    # Avoid columns with too many distinct values
    if unique_count > 30:
        return False

    # Exclude columns where nearly every value is unique
    if unique_ratio > 0.5:
        return False

    return True


# ==========================================================
# 5. CATEGORICAL ANALYSIS
# ==========================================================

def analyze_categorical_data(df):

    """Calculate frequency and percentage of categories."""

    categorical_summary = {}

    columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    for column in columns:

        series = df[column].dropna()

        if not is_meaningful_category(series):
            continue

        counts = series.astype(str).value_counts()

        total = len(series)

        categorical_summary[column] = {}

        for category, count in counts.items():

            categorical_summary[column][category] = {
                "count": int(count),
                "percentage": round(
                    (count / total) * 100, 2
                )
            }

    return categorical_summary


# ==========================================================
# 6. AUTOMATIC INSIGHTS
# ==========================================================

def generate_insights(
    numerical_summary,
    categorical_summary
):

    """Generate useful observations from analyzed data."""

    insights = []

    # Numerical insights
    for column, stats in numerical_summary.items():

        insights.append(
            f"{column}: Average is {stats['average']}, "
            f"minimum is {stats['minimum']}, "
            f"maximum is {stats['maximum']}."
        )

    # Categorical insights
    for column, categories in categorical_summary.items():

        if not categories:
            continue

        most_common = max(
            categories.items(),
            key=lambda item: item[1]["count"]
        )

        category, details = most_common

        insights.append(
            f"{column}: Most common category is "
            f"{category} with {details['count']} records."
        )

    return insights


# ==========================================================
# 7. MAIN ANALYSIS FUNCTION
# ==========================================================

def analyze_data(df):

    """Run the complete dataset analysis pipeline."""

    if df is None or df.empty:
        raise ValueError("Cannot analyze an empty dataset.")

    overview = get_dataset_overview(df)

    numerical_summary = analyze_numerical_data(df)

    categorical_summary = analyze_categorical_data(df)

    insights = generate_insights(
        numerical_summary,
        categorical_summary
    )

    return {
        "overview": overview,
        "numerical_summary": numerical_summary,
        "categorical_summary": categorical_summary,
        "insights": insights
    }
