import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path
from io import BytesIO
from html import escape

from validator import validate_records
from analyzer import analyze_data
from report_generator import generate_reports


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="DataPulse | Analytics Studio",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CUSTOM CSS - PREMIUM LIGHT THEME
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f6f8fc;
    color: #172033;
}

header[data-testid="stHeader"] {
    background: rgba(246,248,252,0.95);
}

[data-testid="stToolbar"] {
    right: 2rem;
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e8edf5;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

.block-container {
    max-width: 1500px;
    padding: 2rem 3rem 3rem 3rem;
}

h1, h2, h3 {
    color: #18243b !important;
    font-weight: 700 !important;
}

p {
    color: #64748b;
}

.brand {
    font-size: 28px;
    font-weight: 800;
    color: #5145cd;
    letter-spacing: -1px;
}

.brand-subtitle {
    font-size: 11px;
    color: #94a3b8;
    letter-spacing: 2px;
    margin-top: 3px;
}

.hero {
    background: linear-gradient(115deg, #5145cd, #7668e8);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 28px;
    color: white;
    box-shadow: 0 12px 30px rgba(81,69,205,0.15);
}

.hero h1 {
    color: white !important;
    font-size: 34px;
    margin: 8px 0;
}

.hero p {
    color: #e5e2ff;
    font-size: 15px;
    margin-bottom: 0;
}

.eyebrow {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #dcd8ff;
}

.metric-card {
    background: white;
    border: 1px solid #e8edf5;
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 4px 15px rgba(15,23,42,0.035);
}

.metric-label {
    color: #77839a;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #172033;
    font-size: 30px;
    font-weight: 800;
    margin-top: 10px;
}

.metric-note {
    color: #94a3b8;
    font-size: 11px;
    margin-top: 4px;
}

.panel {
    background: white;
    border: 1px solid #e8edf5;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 4px 15px rgba(15,23,42,0.025);
    margin-bottom: 18px;
}

.panel-title {
    color: #1e293b;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 5px;
}

.panel-description {
    color: #94a3b8;
    font-size: 12px;
}

.stButton > button {
    background: #5145cd;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 600;
    min-height: 42px;
}

.stButton > button:hover {
    background: #4035b0;
    color: white;
    border: none;
}


/* DATAPULSE - LIGHT LAVENDER DOWNLOAD BUTTONS */

.stDownloadButton > button {

    background: linear-gradient(
        110deg,
        #F3F0FF,
        #EAF0FF
    ) !important;

    color: #5145CD !important;

    border: 1px solid #DED8FF !important;

    border-radius: 12px !important;

    min-height: 49px !important;

    font-size: 15px !important;

    font-weight: 650 !important;

    box-shadow: 0 3px 10px rgba(81, 69, 205, 0.07);

    transition: all 0.3s ease !important;
}

.stDownloadButton > button p,
.stDownloadButton > button span,
.stDownloadButton > button div {

    color: #5145CD !important;

    -webkit-text-fill-color: #5145CD !important;

    font-weight: 650 !important;
}

.stDownloadButton > button:hover {

    background: linear-gradient(
        110deg,
        #E8E2FF,
        #DCE7FF
    ) !important;

    border-color: #BDB2FF !important;

    transform: translateY(-2px);

    box-shadow: 0 7px 16px rgba(81, 69, 205, 0.13);
}

.stDownloadButton > button:active {
    transform: scale(0.985);
}


[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e8edf5;
    padding: 15px;
    border-radius: 13px;
}

[data-testid="stMetricValue"] {
    color: #172033;
}

[data-testid="stFileUploader"] {
    background: #fafaff;
    border: 1px dashed #b9b1f6;
    border-radius: 14px;
    padding: 12px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #e8edf5;
    border-radius: 12px;
}

[data-testid="stExpander"] {
    background: white;
    border: 1px solid #e8edf5;
    border-radius: 12px;
}

div[data-testid="stRadio"] label {
    font-weight: 500;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    padding: 25px;
    border-top: 1px solid #e8edf5;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# CHART DESIGN
# =====================================================

COLORS = [
    "#5145cd",
    "#06b6d4",
    "#10b981",
    "#f59e0b",
    "#ec4899",
    "#8b5cf6"
]


def style_chart(fig, height=360):

    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter",
            color="#64748b",
            size=12
        ),
        margin=dict(l=15, r=15, t=50, b=20),
        title_font=dict(
            size=16,
            color="#1e293b"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#e8edf5"
    )

    fig.update_yaxes(
        gridcolor="#edf0f6",
        zeroline=False
    )

    return fig


# =====================================================
# DATA LOADER
# =====================================================

def load_dataset(uploaded_file):

    extension = Path(uploaded_file.name).suffix.lower()

    if extension == ".csv":

        df = pd.read_csv(
            BytesIO(uploaded_file.getvalue())
        )

    elif extension == ".json":

        content = json.loads(
            uploaded_file.getvalue().decode("utf-8")
        )

        if isinstance(content, dict) and "data" in content:
            content = content["data"]

        if isinstance(content, dict):
            df = pd.DataFrame(content)

        elif isinstance(content, list):
            df = pd.DataFrame(content)

        else:
            raise ValueError("Invalid JSON structure.")

    else:
        raise ValueError("Only CSV and JSON are supported.")

    if df.empty:
        raise ValueError("The dataset is empty.")

    if not df.columns.is_unique:
        raise ValueError("Duplicate column names detected.")

    return df


# =====================================================
# METRIC CARD
# =====================================================

def metric_card(label, value, note):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{escape(str(label))}</div>
            <div class="metric-value">{escape(str(value))}</div>
            <div class="metric-note">{escape(str(note))}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">◈ DataPulse</div>
        <div class="brand-subtitle">ANALYTICS STUDIO</div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("**WORKSPACE**")

    page = st.selectbox(
        "Navigate",
        [
            "Overview",
            "Data Explorer",
            "Analytics",
            "Data Quality",
            "Smart Insights",
            "Reports"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("**DATA SOURCE**")

    source = st.radio(
        "Choose your dataset",
        ["Sample Dataset", "Upload Dataset"]
    )

    uploaded_file = None

    if source == "Upload Dataset":

        uploaded_file = st.file_uploader(
            "Choose CSV or JSON",
            type=["csv", "json"]
        )

    else:

        st.success("Sample data ready")

    st.divider()

    st.caption("DataPulse Analytics Studio")
    st.caption("Version 3.0")


# =====================================================
# DATA PROCESSING
# =====================================================

try:

    if source == "Sample Dataset":

        df = pd.read_csv("data/sample_records.csv")

    elif uploaded_file is not None:

        df = load_dataset(uploaded_file)

    else:

        st.markdown(
            """
            <div class="hero">
                <div class="eyebrow">WELCOME TO DATAPULSE</div>
                <h1>Your data deserves better insights.</h1>
                <p>Upload a CSV or JSON dataset to explore,
                analyze and visualize your data.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info("Select Upload Dataset in the sidebar to begin.")
        st.stop()

    valid_df, invalid_df, issues = validate_records(df)

    if valid_df.empty:

        st.error("No valid records available.")
        st.stop()

    results = analyze_data(valid_df)

    overview = results["overview"]

except Exception as error:

    st.error(f"Dataset processing failed: {error}")
    st.stop()


# =====================================================
# DATA TYPES FOR VISUALIZATION
# =====================================================

numeric_columns = [
    col for col in valid_df.select_dtypes(include="number").columns
    if str(col).lower() not in ["id", "employee_id", "record_id"]
]

categorical_columns = [
    col for col in valid_df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns
    if valid_df[col].nunique() <= 30
]


# =====================================================
# MAIN HEADER
# =====================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">SMART DATA INTELLIGENCE PLATFORM</div>
        <h1>Discover the story behind your data.</h1>
        <p>Analyze records, monitor data quality and
        turn information into meaningful insights.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    f"CURRENT DATASET  /  {len(df)} RECORDS  /  {len(df.columns)} COLUMNS"
)


# =====================================================
# OVERVIEW
# =====================================================

if page == "Overview":

    st.subheader("Your dataset at a glance")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("TOTAL RECORDS", len(df), "Uploaded records")

    with c2:
        metric_card("VALID RECORDS", len(valid_df), "Passed validation")

    with c3:
        metric_card("INVALID RECORDS", len(invalid_df), "Require attention")

    with c4:
        metric_card("DATA COLUMNS", len(df.columns), "Available features")

    st.write("")

    left, right = st.columns([1.6, 1])

    with left:

        st.markdown(
            '<div class="panel-title">Dataset Preview</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            df.head(10),
            use_container_width=True,
            hide_index=True
        )

    with right:

        st.markdown(
            '<div class="panel-title">Data Quality Score</div>',
            unsafe_allow_html=True
        )

        score = len(valid_df) / len(df) * 100

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                number={"suffix": "%"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#5145cd"},
                    "bgcolor": "#edf0f8",
                    "steps": [
                        {"range": [0, 50], "color": "#fee2e2"},
                        {"range": [50, 80], "color": "#fef3c7"},
                        {"range": [80, 100], "color": "#dcfce7"}
                    ]
                }
            )
        )

        fig.update_layout(
            template="plotly_white",
            height=250,
            margin=dict(t=15, b=10, l=15, r=15)
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Dataset Health")

    a, b, c = st.columns(3)

    a.metric("Missing Values", overview["missing_values"])
    b.metric("Duplicate Records", overview["duplicate_records"])
    c.metric("Memory Usage", f"{overview['memory_usage_kb']} KB")


# =====================================================
# DATA EXPLORER
# =====================================================

elif page == "Data Explorer":

    st.subheader("Explore your records")

    search = st.text_input(
        "Search your dataset",
        placeholder="Enter a name, category or keyword..."
    )

    selected_columns = st.multiselect(
        "Select visible columns",
        list(df.columns),
        default=list(df.columns)
    )

    filtered_df = df.copy()

    if search:

        mask = filtered_df.astype(str).apply(
            lambda column: column.str.contains(
                search,
                case=False,
                na=False
            )
        ).any(axis=1)

        filtered_df = filtered_df[mask]

    st.metric("Matching Records", len(filtered_df))

    if selected_columns:

        st.dataframe(
            filtered_df[selected_columns],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Filtered Dataset",
            filtered_df[selected_columns].to_csv(index=False),
            file_name="filtered_dataset.csv",
            mime="text/csv"
        )

    else:

        st.warning("Select at least one column.")


# =====================================================
# ANALYTICS
# =====================================================

elif page == "Analytics":

    st.subheader("Explore your data visually")

    if numeric_columns:

        selected_numeric = st.selectbox(
            "Choose numerical field",
            numeric_columns
        )

        values = pd.to_numeric(
            valid_df[selected_numeric],
            errors="coerce"
        ).dropna()

        a, b, c, d = st.columns(4)

        a.metric("Average", round(values.mean(), 2))
        b.metric("Maximum", round(values.max(), 2))
        c.metric("Minimum", round(values.min(), 2))
        d.metric("Median", round(values.median(), 2))

        left, right = st.columns(2)

        with left:

            fig = px.histogram(
                values,
                nbins=12,
                title=f"{selected_numeric} Distribution",
                color_discrete_sequence=["#5145cd"]
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

        with right:

            fig = px.box(
                valid_df,
                y=selected_numeric,
                title=f"{selected_numeric} Box Plot",
                color_discrete_sequence=["#06b6d4"]
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

    else:

        st.info("No numerical columns found.")

    st.divider()

    if categorical_columns:

        selected_category = st.selectbox(
            "Choose category field",
            categorical_columns
        )

        category_counts = (
            valid_df[selected_category]
            .astype(str)
            .value_counts()
            .head(15)
            .rename_axis("Category")
            .reset_index(name="Count")
        )

        fig = px.bar(
            category_counts,
            x="Category",
            y="Count",
            color="Category",
            text="Count",
            title=f"{selected_category} Distribution",
            color_discrete_sequence=COLORS
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    else:

        st.info("No categorical columns available.")

    if len(numeric_columns) >= 2:

        st.subheader("Correlation Analysis")

        correlation = valid_df[numeric_columns].corr()

        fig = px.imshow(
            correlation,
            text_auto=".2f",
            color_continuous_scale="Purples",
            title="Numerical Feature Correlation"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )


# =====================================================
# DATA QUALITY
# =====================================================

elif page == "Data Quality":

    st.subheader("Data Quality Monitor")

    missing = df.isnull().sum()
    missing_total = int(missing.sum())
    duplicate_count = int(df.duplicated().sum())

    a, b, c = st.columns(3)

    a.metric("Total Records", len(df))
    b.metric("Missing Values", missing_total)
    c.metric("Duplicate Rows", duplicate_count)

    st.markdown("### Missing Value Analysis")

    if missing_total > 0:

        missing_df = (
            missing[missing > 0]
            .rename_axis("Column")
            .reset_index(name="Missing Count")
        )

        fig = px.bar(
            missing_df,
            x="Column",
            y="Missing Count",
            color_discrete_sequence=["#e87979"],
            title="Missing Values by Column"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    else:

        st.success("Excellent! No missing values were detected.")

    st.markdown("### Validation Results")

    if issues:

        st.warning(f"{len(issues)} validation issues detected.")

        st.dataframe(
            pd.DataFrame(issues),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("Your dataset passed all current validation checks.")

    with st.expander("View invalid records"):

        if invalid_df.empty:
            st.info("There are no invalid records.")
        else:
            st.dataframe(
                invalid_df,
                use_container_width=True
            )


# =====================================================
# SMART INSIGHTS
# =====================================================

elif page == "Smart Insights":

    st.subheader("Insights generated from your data")

    st.caption("Automatic observations based on statistical analysis.")

    if results["insights"]:

        for i, insight in enumerate(results["insights"], 1):

            st.markdown(
                f"""
                <div class="panel">
                    <div style="color:#5145cd;font-size:11px;
                    font-weight:700;letter-spacing:1px;">
                        INSIGHT {i:02d}
                    </div>
                    <div style="font-size:16px;color:#25324b;
                    margin-top:10px;">
                        {escape(str(insight))}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info("No insights are available.")



# =====================================================
# REPORT CENTER
# =====================================================

elif page == "Reports":

    st.subheader("DataPulse Report Center")

    st.write(
        "Generate and download professional reports "
        "for your current dataset."
    )

    st.info(
        "Generate reports containing dataset statistics, "
        "validation results and automatic insights."
    )

    
    # Custom Generate Reports Button Design
    
    st.markdown("""
    <style>

    /* Generate All Reports - Main Button */
    div.st-key-generate_reports_btn button {
        background: linear-gradient(90deg, #0F766E, #2563EB) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        height: 55px !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        opacity: 1 !important;
        box-shadow: 0 5px 15px rgba(37, 99, 235, 0.20);
        transition: all 0.3s ease;
    }

    /* Force white text inside Streamlit button */
    div.st-key-generate_reports_btn button p,
    div.st-key-generate_reports_btn button span,
    div.st-key-generate_reports_btn button div {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        opacity: 1 !important;
        font-weight: 700 !important;
    }

    /* Hover Effect */
    div.st-key-generate_reports_btn button:hover {
        background: linear-gradient(90deg, #115E59, #1D4ED8) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.30);
    }

    /* Active Effect */
    div.st-key-generate_reports_btn button:active {
        transform: scale(0.98);
    }

    </style>
    """, unsafe_allow_html=True)


    if st.button(
        "✦  Generate All Reports",
        type="primary",
        use_container_width=True,
        key="generate_reports_btn"
    ):


        try:

            files = generate_reports(
                results,
                valid_df,
                invalid_df,
                issues
            )

            st.session_state["report_files"] = {
                key: str(value)
                for key, value in files.items()
            }

            st.success("All reports generated successfully!")

        except Exception as error:

            st.error(f"Report generation failed: {error}")

    if "report_files" in st.session_state:

        labels = {
            "pdf": "Professional PDF Report",
            "text": "Text Analysis Report",
            "json": "JSON Analysis Report",
            "numerical": "Numerical Summary CSV",
            "category": "Category Summary CSV",
            "valid": "Valid Records CSV",
            "invalid": "Invalid Records CSV",
            "issues": "Validation Issues CSV"
        }

        mime_types = {
            "pdf": "application/pdf",
            "json": "application/json",
            "text": "text/plain",
            "numerical": "text/csv",
            "category": "text/csv",
            "valid": "text/csv",
            "invalid": "text/csv",
            "issues": "text/csv"
        }

        st.divider()

        st.markdown("### Available Downloads")

        # Professional PDF download
        if "pdf" in st.session_state["report_files"]:

            pdf_path = Path(
                st.session_state["report_files"]["pdf"]
            )

            if pdf_path.exists():

                st.markdown("#### Professional PDF Report")

                st.download_button(
                    label="Download DataPulse PDF Report",
                    data=pdf_path.read_bytes(),
                    file_name=pdf_path.name,
                    mime="application/pdf",
                    key="download_professional_pdf",
                    use_container_width=True
                )

        # Remaining report downloads
        st.markdown("#### Other Export Formats")

        for key, filepath in st.session_state[
            "report_files"
        ].items():

            if key == "pdf":
                continue

            path = Path(filepath)

            if path.exists():

                st.download_button(
                    label=f"Download {labels[key]}",
                    data=path.read_bytes(),
                    file_name=path.name,
                    mime=mime_types.get(
                        key,
                        "application/octet-stream"
                    ),
                    key=f"download_{key}",
                    use_container_width=True
                )

            else:

                st.warning(f"Report not found: {path.name}")




# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer">
        <b style="color:#5145cd;">DataPulse</b>
        · Analytics Studio
        <br><br>
        Built with Python · Pandas · Plotly · Streamlit
        <br>
        Turning raw data into meaningful insights.
    </div>
    """,
    unsafe_allow_html=True
)
