# DataPulse – Smart Data Intelligence Platform

A Python-based data analysis application that transforms raw datasets into meaningful insights through automated data validation, statistical analysis, interactive visualizations and professional report generation.

## About the Project

DataPulse is an interactive analytics platform developed using Python and Streamlit. It allows users to upload CSV and JSON datasets, validate records, identify data quality issues, explore statistical summaries and generate downloadable reports.

The application is designed to simplify data analysis through an intuitive dashboard without requiring users to write SQL queries or Python scripts.

## Key Features

### 1. Dataset Management
- Upload CSV and JSON files.
- Load and preview datasets.
- Explore records through an interactive interface.

### 2. Data Validation
- Detect missing values.
- Identify duplicate records and IDs.
- Detect invalid numerical values.
- Validate quantities and prices.
- Identify invalid payment statuses.
- Separate valid and invalid records.
- Generate detailed validation issue reports.

### 3. Data Analytics
- Calculate average, minimum, maximum and median.
- Analyze numerical columns.
- Generate categorical frequency distributions.
- Calculate category percentages.
- Generate automatic analytical insights.

### 4. Interactive Visualizations
- Numerical distribution histograms.
- Box plot visualizations.
- Statistical summary cards.
- Interactive data exploration.

### 5. Professional Report Generation

Generate and download eight report formats:

| Report | Format |
|---|---|
| Analysis Report | TXT |
| Analysis Report | JSON |
| Professional Report | PDF |
| Numerical Summary | CSV |
| Category Summary | CSV |
| Valid Records | CSV |
| Invalid Records | CSV |
| Validation Issues | CSV |

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application framework |
| Pandas | Data processing and analysis |
| Plotly | Interactive visualizations |
| ReportLab | PDF report generation |
| JSON | Structured data handling |
| VS Code | Development environment |

## Project Structure

```text
record_analyzer/
│
├── app.py
├── validator.py
├── analyzer.py
├── report_generator.py
│
├── data/
│   ├── sample_records.csv
│   └── ecommerce_sales.csv
│
├── reports/
│   └── Generated reports
│
├── tests/
│
├── test_validator.py
├── test_analyzer.py
├── test_report_generator.py
├── test_pdf.py
│
├── requirements.txt
└── README.md
```

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Alternatively, download the project ZIP and extract it.

### Step 2: Open the Project

Open the project folder in Visual Studio Code.

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## How to Use DataPulse

1. Launch the application.
2. Select a sample dataset or upload your own CSV/JSON file.
3. Explore the uploaded dataset.
4. Navigate to the Data Quality section to inspect validation issues.
5. Open Analytics to explore statistical summaries and visualizations.
6. Visit Reports to generate and download analysis reports.

## Testing

DataPulse was tested using both clean and intentionally flawed datasets.

### Functional Testing Results

| Test Case | Result |
|---|---|
| Application Launch | Passed |
| CSV Upload | Passed |
| JSON Upload | Passed |
| Data Validation | Passed |
| Analytics | Passed |
| Data Explorer | Passed |
| Report Generation | Passed |

### Validation Testing

A deliberately flawed e-commerce dataset was used to test:

- Missing customer information.
- Duplicate and invalid records.
- Negative and zero quantities.
- Negative prices.
- Invalid numerical values.
- Invalid payment statuses.

The validation system successfully identified the tested issues.

## Future Enhancements

Potential improvements include:

- Advanced anomaly detection.
- Additional statistical analysis.
- Customizable report templates.
- Database integration.
- Cloud deployment.
- Machine learning-based data quality predictions.

## Author

**T R Dhanyashri**

Developed as a Python application project to demonstrate data processing, validation, analytics, visualization and automated reporting.

## License

This project is available for educational and learning purposes. Add a suitable open-source license if you intend to distribute it publicly.
