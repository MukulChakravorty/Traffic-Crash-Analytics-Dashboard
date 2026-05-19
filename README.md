# Traffic Crash Analytics Dashboard

An interactive data analytics dashboard developed using **SQL, Python, Streamlit, Pandas, and Matplotlib** to analyze real-world traffic crash data and generate actionable road safety insights.

The project focuses on identifying crash trends, high-risk zones, injury-prone conditions, peak crash periods, and major contributory crash causes through advanced SQL analysis and interactive visualizations.

---

# Project Features

- Crash Type Analysis
- Injury Percentage Analysis
- Peak Crash Hour Detection
- Night-Time Crash Cause Analysis
- Daylight vs Darkness Injury Comparison
- Traffic Control Device Analysis
- Crash Hotspot Detection
- High-Risk Time Bucket Analysis
- Year-over-Year Crash Growth Analysis
- Hotspot Zone Clustering using Latitude & Longitude
- Advanced SQL Window Functions (`ROW_NUMBER()`, `LAG()`)

---

# Technologies Used

- Python
- SQL
- Streamlit
- Pandas
- Matplotlib
- SQLite

---

# SQL Concepts Used

- `GROUP BY`
- `HAVING`
- `CASE WHEN`
- `CTE (WITH Clause)`
- `ROW_NUMBER()`
- `LAG()`
- Aggregate Functions
- Ranking & Window Functions

---

# Dashboard Insights

The dashboard helps identify:

- High-risk crash locations
- Injury-prone road conditions
- Frequent crash causes
- Peak accident hours
- Traffic behavior patterns
- Yearly crash growth trends

These insights support traffic monitoring, road safety planning, and transportation analysis.

---

# Project Structure

```bash
Traffic-Crash-Analytics-Dashboard/
│
├── app.py
├── traffic_crash.db
├── requirements.txt
├── README.md
└── screenshots/
```

---

# Installation & Setup

Clone the repository:

```bash
git clone https://github.com/MukulChakravorty/Traffic-Crash-Analytics-Dashboard.git
```

Navigate to the project directory:

```bash
cd Traffic-Crash-Analytics-Dashboard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
streamlit run app.py
```

---

# Future Improvements

- Interactive map visualizations
- Machine learning crash prediction
- Real-time traffic analysis
- Power BI integration

---

# Author

**Mukul Chakravorty**

Data Analytics & Machine Learning Enthusiast
