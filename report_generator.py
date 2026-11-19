
import json
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    PageBreak
)


# ==========================================================
# 1. REPORT DIRECTORY
# ==========================================================

def create_report_directory(output_dir="reports"):
    """Create the report directory if it does not exist."""

    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)

    return folder


# ==========================================================
# 2. TEXT REPORT
# ==========================================================

def export_text_report(results, validation_summary, filepath):

    """Generate a readable TXT report."""

    overview = results["overview"]

    with open(filepath, "w", encoding="utf-8") as file:

        file.write("=" * 65 + "\n")
        file.write("                 DATAPULSE\n")
        file.write("          SMART DATA INTELLIGENCE\n")
        file.write("=" * 65 + "\n\n")

        file.write("DATA ANALYSIS REPORT\n")
        file.write(
            f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n\n"
        )

        file.write("1. DATASET OVERVIEW\n")
        file.write("-" * 45 + "\n")

        for key, value in overview.items():
            file.write(f"{key}: {value}\n")

        file.write("\n2. VALIDATION SUMMARY\n")
        file.write("-" * 45 + "\n")

        for key, value in validation_summary.items():
            file.write(f"{key}: {value}\n")

        file.write("\n3. NUMERICAL ANALYSIS\n")
        file.write("-" * 45 + "\n")

        for column, stats in results["numerical_summary"].items():

            file.write(f"\nColumn: {column}\n")

            for metric, value in stats.items():
                file.write(f"{metric}: {value}\n")

        file.write("\n4. CATEGORY ANALYSIS\n")
        file.write("-" * 45 + "\n")

        for column, categories in results["categorical_summary"].items():

            file.write(f"\nColumn: {column}\n")

            for category, details in categories.items():

                file.write(
                    f"{category}: {details['count']} records "
                    f"({details['percentage']}%)\n"
                )

        file.write("\n5. AUTOMATIC INSIGHTS\n")
        file.write("-" * 45 + "\n")

        for number, insight in enumerate(
            results["insights"], start=1
        ):
            file.write(f"{number}. {insight}\n")

        file.write("\n" + "=" * 65 + "\n")
        file.write("             END OF REPORT\n")
        file.write("=" * 65 + "\n")


# ==========================================================
# 3. JSON REPORT
# ==========================================================

def export_json_report(results, validation_summary, issues, filepath):

    """Export analysis results as JSON."""

    report_data = {
        "application": "DataPulse",
        "report_type": "Data Analysis Report",
        "generated_at": datetime.now().isoformat(),
        "dataset_overview": results["overview"],
        "validation_summary": validation_summary,
        "numerical_analysis": results["numerical_summary"],
        "categorical_analysis": results["categorical_summary"],
        "automatic_insights": results["insights"],
        "validation_issues": issues
    }

    with open(filepath, "w", encoding="utf-8") as file:

        json.dump(
            report_data,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================================
# 4. NUMERICAL CSV
# ==========================================================

def export_numerical_summary(results, filepath):

    """Export numerical statistics as CSV."""

    rows = []

    for column, stats in results["numerical_summary"].items():

        row = {"column": column}
        row.update(stats)

        rows.append(row)

    pd.DataFrame(rows).to_csv(filepath, index=False)


# ==========================================================
# 5. CATEGORY CSV
# ==========================================================

def export_category_summary(results, filepath):

    """Export category statistics as CSV."""

    rows = []

    for column, categories in results["categorical_summary"].items():

        for category, details in categories.items():

            rows.append({
                "column": column,
                "category": category,
                "count": details["count"],
                "percentage": details["percentage"]
            })

    pd.DataFrame(
        rows,
        columns=["column", "category", "count", "percentage"]
    ).to_csv(filepath, index=False)


# ==========================================================
# 6. VALIDATION ISSUES CSV
# ==========================================================

def export_validation_issues(issues, filepath):

    """Export validation issues as CSV."""

    pd.DataFrame(
        issues,
        columns=["row", "issue", "details"]
    ).to_csv(filepath, index=False)


# ==========================================================
# 7. PDF DESIGN HELPERS
# ==========================================================

PURPLE = colors.HexColor("#5145CD")
DARK = colors.HexColor("#18243B")
LIGHT_PURPLE = colors.HexColor("#F1F0FF")
LIGHT_GREY = colors.HexColor("#F5F7FB")
MID_GREY = colors.HexColor("#64748B")
GREEN = colors.HexColor("#15803D")
RED = colors.HexColor("#BE123C")


def make_pdf_styles():

    """Create reusable PDF text styles."""

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="Brand",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=30,
        textColor=PURPLE,
        alignment=TA_LEFT,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=25,
        textColor=DARK,
        spaceBefore=10,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=PURPLE,
        spaceBefore=15,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="BodyCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=14,
        textColor=DARK,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        name="SmallCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=MID_GREY
    ))

    styles.add(ParagraphStyle(
        name="TableHeaderCustom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white
    ))

    styles.add(ParagraphStyle(
        name="TableCellCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=DARK,
        wordWrap="CJK"
    ))

    return styles


def make_pdf_table(headers, rows, widths=None):

    """Create a consistently styled printable table."""

    styles = make_pdf_styles()

    header = [
        Paragraph(escape(str(item)), styles["TableHeaderCustom"])
        for item in headers
    ]

    body = []

    for row in rows:

        body.append([
            Paragraph(
                escape(str(value)),
                styles["TableCellCustom"]
            )
            for value in row
        ])

    data = [header] + body

    if not body:
        data.append([
            Paragraph("No records available.", styles["TableCellCustom"])
        ] + [
            Paragraph("", styles["TableCellCustom"])
            for _ in headers[1:]
        ])

    table = Table(
        data,
        colWidths=widths,
        repeatRows=1,
        hAlign="LEFT"
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            LIGHT_GREY
        ]),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#E2E8F0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
    ]))

    return table


# ==========================================================
# 8. PDF HEADER AND FOOTER
# ==========================================================

def draw_pdf_header_footer(canvas, document):

    """Draw branded header and page footer."""

    canvas.saveState()

    page_width, page_height = A4

    # Header logo badge
    canvas.setFillColor(PURPLE)
    canvas.roundRect(
        17 * mm,
        page_height - 22 * mm,
        9 * mm,
        9 * mm,
        2 * mm,
        fill=1,
        stroke=0
    )

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(
        21.5 * mm,
        page_height - 19 * mm,
        "D"
    )

    canvas.setFillColor(PURPLE)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawString(
        29 * mm,
        page_height - 17 * mm,
        "DataPulse"
    )

    canvas.setFillColor(MID_GREY)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(
        29 * mm,
        page_height - 21 * mm,
        "SMART DATA INTELLIGENCE"
    )

    canvas.setStrokeColor(colors.HexColor("#E2E8F0"))
    canvas.line(
        17 * mm,
        page_height - 27 * mm,
        page_width - 17 * mm,
        page_height - 27 * mm
    )

    # Footer
    canvas.setStrokeColor(colors.HexColor("#E2E8F0"))
    canvas.line(
        17 * mm,
        16 * mm,
        page_width - 17 * mm,
        16 * mm
    )

    canvas.setFillColor(MID_GREY)
    canvas.setFont("Helvetica", 8)

    canvas.drawString(
        17 * mm,
        10 * mm,
        "DataPulse | Smart Data Intelligence Platform"
    )

    canvas.drawRightString(
        page_width - 17 * mm,
        10 * mm,
        f"Page {document.page}"
    )

    canvas.restoreState()


# ==========================================================
# 9. PROFESSIONAL PDF REPORT
# ==========================================================

def export_pdf_report(
    results,
    validation_summary,
    issues,
    filepath
):

    """Generate a branded, printable A4 PDF report."""

    styles = make_pdf_styles()

    document = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=17 * mm,
        leftMargin=17 * mm,
        topMargin=35 * mm,
        bottomMargin=23 * mm,
        title="DataPulse Data Analysis Report",
        author="DataPulse Analytics Studio"
    )

    story = []

    overview = results["overview"]

    # Cover heading
    story.append(Paragraph(
        "DATA ANALYSIS REPORT",
        styles["ReportTitle"]
    ))

    story.append(Paragraph(
        "A comprehensive summary of dataset quality, "
        "statistics and analytical insights.",
        styles["BodyCustom"]
    ))

    story.append(Spacer(1, 5 * mm))

    # Report metadata
    metadata = [
        ["Report Generated", datetime.now().strftime("%d %B %Y, %I:%M %p")],
        ["Total Records", validation_summary["original_records"]],
        ["Valid Records", validation_summary["valid_records"]],
        ["Invalid Records", validation_summary["invalid_records"]],
        ["Total Columns", overview["total_columns"]]
    ]

    story.append(make_pdf_table(
        ["REPORT INFORMATION", "VALUE"],
        metadata,
        [65 * mm, 105 * mm]
    ))

    # Executive summary
    story.append(Paragraph(
        "1. Executive Summary",
        styles["SectionTitle"]
    ))

    summary_text = (
        f"The dataset contains {validation_summary['original_records']} "
        f"records across {overview['total_columns']} columns. "
        f"{validation_summary['valid_records']} records passed "
        f"the current validation checks, while "
        f"{validation_summary['invalid_records']} records "
        f"were identified as invalid."
    )

    story.append(Paragraph(
        summary_text,
        styles["BodyCustom"]
    ))

    # Dataset overview
    story.append(Paragraph(
        "2. Dataset Overview",
        styles["SectionTitle"]
    ))

    overview_rows = [
        ["Total Records", overview["total_records"]],
        ["Total Columns", overview["total_columns"]],
        ["Missing Values", overview["missing_values"]],
        ["Duplicate Records", overview["duplicate_records"]],
        ["Memory Usage", f"{overview['memory_usage_kb']} KB"],
        ["Columns", ", ".join(map(str, overview["column_names"]))]
    ]

    story.append(make_pdf_table(
        ["METRIC", "RESULT"],
        overview_rows,
        [65 * mm, 105 * mm]
    ))

    # Validation summary
    story.append(Paragraph(
        "3. Data Validation Summary",
        styles["SectionTitle"]
    ))

    validation_rows = [
        [key.replace("_", " ").title(), value]
        for key, value in validation_summary.items()
    ]

    story.append(make_pdf_table(
        ["VALIDATION METRIC", "RESULT"],
        validation_rows,
        [105 * mm, 65 * mm]
    ))

    # Numerical analysis
    story.append(Paragraph(
        "4. Numerical Analysis",
        styles["SectionTitle"]
    ))

    numerical_rows = []

    for column, stats in results["numerical_summary"].items():

        numerical_rows.append([
            column,
            stats["count"],
            stats["average"],
            stats["minimum"],
            stats["maximum"],
            stats["median"]
        ])

    story.append(make_pdf_table(
        ["COLUMN", "COUNT", "AVERAGE", "MIN", "MAX", "MEDIAN"],
        numerical_rows,
        [34 * mm, 23 * mm, 31 * mm, 24 * mm, 24 * mm, 34 * mm]
    ))

    # Category analysis
    story.append(Paragraph(
        "5. Category Analysis",
        styles["SectionTitle"]
    ))

    category_rows = []

    for column, categories in results["categorical_summary"].items():

        for category, details in categories.items():

            category_rows.append([
                column,
                category,
                details["count"],
                f"{details['percentage']}%"
            ])

    story.append(make_pdf_table(
        ["COLUMN", "CATEGORY", "COUNT", "PERCENTAGE"],
        category_rows,
        [42 * mm, 55 * mm, 28 * mm, 45 * mm]
    ))

    # Automatic insights
    story.append(Paragraph(
        "6. Automatic Insights",
        styles["SectionTitle"]
    ))

    if results["insights"]:

        for number, insight in enumerate(
            results["insights"], start=1
        ):

            story.append(Paragraph(
                f"<b>{number}.</b> {escape(str(insight))}",
                styles["BodyCustom"]
            ))

    else:

        story.append(Paragraph(
            "No automatic insights were generated.",
            styles["BodyCustom"]
        ))

    # Validation issues
    story.append(Paragraph(
        "7. Validation Issues",
        styles["SectionTitle"]
    ))

    issue_rows = [
        [item["row"], item["issue"], item["details"]]
        for item in issues
    ]

    story.append(make_pdf_table(
        ["ROW", "ISSUE", "DETAILS"],
        issue_rows,
        [25 * mm, 55 * mm, 90 * mm]
    ))

    # Closing note
    story.append(Spacer(1, 10 * mm))

    story.append(HRFlowable(
        width="100%",
        thickness=0.8,
        color=colors.HexColor("#DDE3EF")
    ))

    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph(
        "Report generated automatically by DataPulse Analytics Studio. "
        "Please verify the source dataset and validation rules before "
        "using these results for important decisions.",
        styles["SmallCustom"]
    ))

    document.build(
        story,
        onFirstPage=draw_pdf_header_footer,
        onLaterPages=draw_pdf_header_footer
    )


# ==========================================================
# 11. COMPLETE REPORT GENERATOR
# ==========================================================

def generate_reports(
    results,
    valid_df,
    invalid_df,
    issues,
    output_dir="reports"
):
    """Generate all eight reports using complete dataset metrics."""

    folder = create_report_directory(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ------------------------------------------------------
    # 1. RECONSTRUCT THE ORIGINAL DATASET
    # ------------------------------------------------------

    full_df = pd.concat(
        [valid_df, invalid_df],
        ignore_index=True
    )

    # ------------------------------------------------------
    # 2. CALCULATE ACCURATE DATA QUALITY METRICS
    # ------------------------------------------------------

    missing_values = int(full_df.isna().sum().sum())

    # Count blank and whitespace-only strings as missing.
    blank_values = int(
        full_df.apply(
            lambda column: column.map(
                lambda value: (
                    isinstance(value, str)
                    and value.strip() == ""
                )
            ).sum()
        ).sum()
    )

    missing_values += blank_values

    duplicate_records = int(
        full_df.duplicated(keep="first").sum()
    )

    memory_usage = round(
        full_df.memory_usage(deep=True).sum() / 1024,
        2
    )

    # ------------------------------------------------------
    # 3. UPDATE DATASET OVERVIEW
    # ------------------------------------------------------

    report_results = dict(results)

    report_results["overview"] = {
        "total_records": len(full_df),
        "total_columns": len(full_df.columns),
        "missing_values": missing_values,
        "duplicate_records": duplicate_records,
        "memory_usage_kb": memory_usage,
        "column_names": full_df.columns.tolist()
    }

    # ------------------------------------------------------
    # 4. VALIDATION SUMMARY
    # ------------------------------------------------------

    validation_summary = {
        "original_records": len(full_df),
        "valid_records": len(valid_df),
        "invalid_records": len(invalid_df),
        "total_validation_issues": len(issues)
    }

    # ------------------------------------------------------
    # 5. CREATE FILE PATHS
    # ------------------------------------------------------

    files = {
        "text": folder / f"Analysis_Report_{timestamp}.txt",
        "json": folder / f"Analysis_Report_{timestamp}.json",
        "pdf": folder / f"DataPulse_Report_{timestamp}.pdf",
        "numerical": folder / f"Numerical_Summary_{timestamp}.csv",
        "category": folder / f"Category_Summary_{timestamp}.csv",
        "valid": folder / f"Valid_Records_{timestamp}.csv",
        "invalid": folder / f"Invalid_Records_{timestamp}.csv",
        "issues": folder / f"Validation_Issues_{timestamp}.csv"
    }

    # ------------------------------------------------------
    # 6. GENERATE ALL EIGHT REPORTS
    # ------------------------------------------------------

    export_text_report(
        report_results,
        validation_summary,
        files["text"]
    )

    export_json_report(
        report_results,
        validation_summary,
        issues,
        files["json"]
    )

    export_pdf_report(
        report_results,
        validation_summary,
        issues,
        files["pdf"]
    )

    export_numerical_summary(
        report_results,
        files["numerical"]
    )

    export_category_summary(
        report_results,
        files["category"]
    )

    valid_df.to_csv(files["valid"], index=False)

    invalid_df.to_csv(files["invalid"], index=False)

    export_validation_issues(
        issues,
        files["issues"]
    )

    return files
