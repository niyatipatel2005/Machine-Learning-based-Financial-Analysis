# 📊 ML Financial Analysis

A web-based platform that provides fundamental analysis of companies using historical financial data, key ratios, and visualizations.

---

## 🔧 Features

- Extracts and calculates key metrics like:
  - ROE (Return on Equity)
  - Sales & Profit growth (3Y, 5Y, 10Y)
- Displays pros and cons from MySQL database
- Clean UI with HTML + CSS
- Metrics fetched from JSON files (per company)
- Built using Python Flask

---

## 📁 Project Structure

```bash
ML_Financial_Analysis/
│
├── app/ # Flask routes and templates
    ├── static/
    ├── templates/
├── assets/ # CSS, images, etc.
├── metrics/ # Generated metric JSON files
├── raw_data/ # Raw company JSON input files
├── scripts/ # Python script for metrics extraction
├── insights/ # Visual outputs 
├── output/ # Optional export/output directory
├── .venv/ # Python virtual environment
├── main.py # Entry point for the app
├── app.py # (optional) if used to launch
└── README.md # You are here

```

## 🚀 Setup Instructions

### 1. Clone the repo:

```bash
git clone https://github.com/niyatipatel2005/Machine-Learning-based-Financial-Analysis.git
cd Machine-Learning-based-Financial-Analysis

```

### 2. Create and activate virtual environment (Windows):

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install required packages:

```bash
pip install -r requirements.txt
```

### 4. Generate metrics:

```bash
python scripts/extract_metrics.py
```

### 5. Run the Flask app:

```bash
python app.py
```

## Authors

* Niyati Patel  -  https://github.com/niyatipatel2005


## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

