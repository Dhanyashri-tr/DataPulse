# DataPulse – Smart Data Intelligence Platform

DataPulse is a Python-based data analytics application that simplifies dataset analysis through automated data validation, statistical analysis, interactive visualizations, and professional report generation.

It allows users to upload CSV and JSON datasets, identify data quality issues, explore records, generate insights, and export analysis reports in multiple formats.

## Features

- **CSV & JSON Upload:** Import datasets in CSV and JSON formats.
- **Data Explorer:** View, inspect, and explore uploaded records.
- **Data Validation:** Detect missing values, duplicate records, invalid numerical values, and other data quality issues.
- **Statistical Analysis:** Generate numerical and categorical summaries.
- **Interactive Visualizations:** Explore data using interactive Plotly charts, including histograms and box plots.
- **Automatic Insights:** Generate useful observations from dataset analysis.
- **Report Generation:** Export analysis results in PDF, TXT, JSON, and CSV formats.
- **User-Friendly Interface:** Simple and interactive dashboard built with Streamlit.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Data processing and analysis |
| Matplotlib | Data visualization |
| Plotly | Interactive charts |
| ReportLab | PDF report generation |
| JSON | Structured data handling |
| VS Code | Development environment |

## Project Structure

```text
DataPulse/
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   ├── e_commerce_sales.csv
│   ├── sample_records.csv
│   └── sample_records.json
│
├── .gitignore
├── README.md
├── analyzer.py
├── app.py
├── report_generator.py
├── requirements.txt
├── validator.py
│
├── test_analyzer.py
├── test_pdf.py
├── test_report_generator.py
└── test_validator.py
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Dhanyashri-tr/DataPulse.git
```

### 2. Navigate to the Project Directory

```bash
cd DataPulse
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser.

## Usage

1. Launch the DataPulse application.
2. Upload a CSV or JSON dataset.
3. Explore the uploaded records using the Data Explorer.
4. Run data quality validation to identify errors and inconsistencies.
5. View numerical and categorical analysis.
6. Explore interactive visualizations and automatically generated insights.
7. Generate and download reports in supported formats.

## Testing

The project includes test scripts for its core functionality:

- `test_analyzer.py` – Tests data analysis functionality.
- `test_validator.py` – Tests data validation.
- `test_pdf.py` – Tests PDF report generation.
- `test_report_generator.py` – Tests report generation.

Run individual tests using:

```bash
python test_analyzer.py
python test_validator.py
python test_pdf.py
python test_report_generator.py
```

## Supported Report Formats

| Format | Description |
|---|---|
| PDF | Professional analysis report |
| TXT | Text-based summary |
| JSON | Structured analysis results |
| CSV | Downloadable analysis and validation data |

## Future Enhancements

- Advanced data visualization.
- Support for additional file formats.
- More configurable validation rules.
- Enhanced analytical insights.
- Cloud deployment.

## Author

**T R Dhanyashri**

GitHub: [Dhanyashri-tr](https://github.com/Dhanyashri-tr)

## License

This project is open-source. A formal license can be added to define permissions for reuse and distribution.