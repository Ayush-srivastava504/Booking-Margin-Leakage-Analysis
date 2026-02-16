# Booking Margin Leakage Analysis

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Data Pipeline](https://img.shields.io/badge/Pipeline-Staging%20%E2%86%92%20Intermediate%20%E2%86%92%20Marts-brightgreen)](#data-architecture)

A comprehensive data analytics platform for identifying and quantifying booking margin leakage in Airbnb-style marketplaces. Includes synthetic data generation, ETL pipeline, and interactive Power BI dashboard.

---

##  Executive Summary

This project analyzes **15,000 synthetic bookings** across **500 hosts** and **8 neighborhoods** to identify where profitability is lost. The analysis reveals:

- **34.9%** average profit margin per booking
- **78.7%** of bookings are profitable
- **21.3%** of bookings operate at a loss
- **$2.1M** margin lost to cancellations annually
- **Top 20% of hosts** generate **70%+ of margins**

**Business Impact**: A 10% price increase could add **$918K annual margin**. Reducing cancellations by 20% could recover **$420K**.

---

## Quick Start 

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/booking-margin-leakage.git
cd booking-margin-leakage-analysis
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Database
```bash
cp .env.example .env
# Edit .env with your MySQL credentials:
# DB_HOST=localhost
# DB_USER=main
# DB_PASSWORD=your_password
# DB_NAME=booking_analysis
```

### 4. Generate Data
```bash
python -m src.data_generator
# Creates 6 CSV files in data/raw/
```

### 5. Load & Transform
```bash
python load_raw_data.py      # Load CSVs to MySQL
python run_sql.py             # Run transformation pipeline
```

### 6. Open Dashboard
```
Open: Booking_Margin_Dashboard.pbix in Power BI Desktop
```

---

## Dashboard Overview

**5 Interactive Pages** analyzing booking profitability:

| Page | Focus | Key Metrics |
|------|-------|------------|
| **Executive Summary** | High-level overview | Revenue, margin %, bookings, hosts |
| **Revenue Analysis** | Money flow breakdown | GBV waterfall, fee structure, margins |
| **Profitability** | Segment performance | Room type, neighborhood, status distribution |
| **Trends & Patterns** | Temporal insights | Seasonality, cancellations, top hosts |
| **Deep Dive** | Risk analysis | Worst performers, scenarios, what-ifs |

---

## Project Structure

```
booking-margin-leakage-analysis/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── .env.example                       # Config template
│
├── docs/                              # Documentation
│   ├── BUSINESS_PROBLEM.md           # Why this analysis matters
│   ├── KPIS.md                       # KPI definitions
│   ├── BUSINESS_DECISIONS.md         # How to use insights
│   └── SYNTHETIC_DATA_GUIDE.md       # Data generation details
│
├── src/                               # Source code
│   ├── __init__.py
│   ├── config.py                     # Configuration
│   ├── data_generator.py             # Synthetic data generation
│   └───db.py                              # Database utilities
│     └──  load_raw_data.py                   # Load CSVs to MySQL
│     └──  run_sql.py                         # Run SQL pipeline
│
├── sql/                               # SQL transformations
│   ├── staging/                      # Raw data cleaning
│   │   ├── stg_bookings.sql
│   │   ├── stg_booking_fees.sql
│   │   └── stg_host_costs.sql
│   ├── intermediate/                 # Business logic
│   │   └── int_booking_margins.sql
│   └── marts/                        # Analytics tables (15 KPI tables)
│       ├── kpi_revenue_overview.sql
│       ├── kpi_profitability_distribution.sql
│       └── ... (13 more)
│
│
├── data/                              # Data directory
│   ├── raw/                          # CSV files (generated)
│   ├── processed/                    # Intermediate data
│   └── external/                     # Reference data
│
├──PowerBI
└── Booking_Margin_Dashboard.pbix      # Power BI dashboard
```

---

## Workflows

### Generate Fresh Data
```bash
python -m src.data_generator
# Output: 6 CSV files with ~15K bookings
```

### Reload Booking Data (Keep Static Data)
```bash
make reload
# OR manually:
python load_raw_data.py
python run_sql.py
```

### Refresh Power BI
```
Power BI → Home → Refresh (Ctrl + Shift + R)
```

### Full Pipeline
```bash
make drop-dependent    # Drop dependent tables
make load-data         # Load new CSVs
make run-sql           # Run transformations
# Then refresh Power BI manually
```

---

## Key Metrics (KPIs)

### Revenue Metrics
- **Total GBV**: $13.74M gross booking value
- **Platform Fees**: $2.05M (14.9% of GBV)
- **Net to Hosts**: $11.10M after platform fees
- **Net Margin**: $9.18M after all costs

### Profitability Metrics
- **Profitable Bookings**: 78.7% (11,384 bookings)
- **Loss-Making**: 21.3% (3,073 bookings)
- **Avg Margin %**: 34.9% per booking
- **Avg Margin $**: $636 per booking

### Operational Metrics
- **Active Hosts**: 500
- **Total Bookings**: 14,457
- **Cancellation Rate**: 8.5%
- **Avg Booking Value**: $950

### Geographic Metrics
- **8 Neighborhoods** analyzed
- **San Francisco**: Highest prices (~60% margin)
- **Shared rooms**: Lowest profitability (~15% margin)
- **Entire homes**: Best margins (~52%)

---

##  Business Insights

### Major Finding: Shared Rooms Underperform
- **Shared rooms in Queens**: -66.6% margin (major loss)
- **Entire homes in Manhattan**: +52.4% margin (strong)
- **Recommendation**: Redesign shared room pricing or discontinue

### Seasonality Impact
- **Peak season** (Jun-Aug, Dec): +50% margins
- **Low season** (Jan-Feb, Nov): -20% margins
- **Opportunity**: Dynamic pricing strategy

### Cancellation Cost
- **1,231 cancelled bookings** annually
- **$2.1M margin loss** to cancellations
- **<3 days before**: 15% cancel rate (highest risk)
- **Recommendation**: Stricter cancellation policies or incentives

### Concentration Risk
- **Top 20% of hosts** generate **70%+ of margin**
- **Bottom 50% of hosts** generate only **10% of margin**
- **Recommendation**: Focus retention on high-value hosts

---

## Business Scenarios

### Scenario 1: 10% Price Increase
```
Impact: +$918K additional margin annually
Risk: May reduce bookings 5-10%
Recommendation: Test in low-elasticity segments first
```

### Scenario 2: Reduce Cancellations by 20%
```
Impact: +$420K recovered margin
Timeline: 6-month initiative
Channels: Better host communication, stricter policies
```

### Scenario 3: Focus on High-Margin Segments
```
Target: Entire homes in premium neighborhoods
Current: 45% of bookings, 70% of margin
Goal: Increase to 55% of bookings
Impact: +$500K-750K additional margin
```

---

##  Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Data Generation** | Python 3.8+ | faker, pandas, numpy |
| **ETL Pipeline** | SQL | MySQL 8.0+ |
| **Data Warehouse** | MySQL | InnoDB |
| **Transformation** | SQLAlchemy | 2.0+ |
| **Analytics** | Power BI Desktop | Latest |
| **Version Control** | Git | GitHub |

### Dependencies
```
pandas==2.0.3
sqlalchemy==2.0.20
pymysql==1.1.0
python-dotenv==1.0.0
faker==18.0.0
numpy==1.24.0
```

---

##  Documentation

- **[Business Problem](docs/BUSINESS_PROBLEM.md)** - Why this analysis matters
- **[KPIs](docs/KPIS.md)** - What we measure and why
- **[Business Decisions](docs/BUSINESS_DECISIONS.md)** - How to act on insights
- **[Synthetic Data](docs/SYNTHETIC_DATA_GUIDE.md)** - Data generation details

---

##  Data Architecture

### Pipeline Layers (Medallion Architecture)

```
Raw Data (CSVs)
    ↓
[STAGING LAYER] - Clean & standardize
    ├── stg_bookings
    ├── stg_booking_fees
    └── stg_host_costs
    ↓
[INTERMEDIATE LAYER] - Business logic
    └── int_booking_margins (all metrics calculated)
    ↓
[MARTS LAYER] - Analytics tables
    ├── kpi_revenue_overview
    ├── kpi_profitability_distribution
    ├── kpi_room_type_performance
    └── ... (12 more KPI tables)
    ↓
Power BI Dashboard
```

### Data Flow
```
hosts.csv ─┐
listings.csv ─┼─→ bookings.csv ─→ [Staging] ─→ [Intermediate] ─→ [Marts] ─→ Power BI
guests.csv ─┤
             └─→ booking_fees.csv ──┘
                 host_costs.csv ─────┘
```

---

##  Data Statistics

### Generated Datasets
| Dataset | Rows | Columns | Size |
|---------|------|---------|------|
| hosts | 500 | 8 | 50KB |
| listings | 758 | 9 | 100KB |
| guests | 5,000 | 6 | 400KB |
| bookings | 14,457 | 14 | 2.5MB |
| booking_fees | 14,457 | 8 | 1.5MB |
| host_costs | 14,457 | 4 | 800KB |

### KPI Tables
| Table | Purpose | Rows |
|-------|---------|------|
| kpi_revenue_overview | Summary metrics | 1 |
| kpi_revenue_waterfall | Fee breakdown | 5 |
| kpi_profitability_distribution | Status distribution | 2 |
| kpi_room_type_performance | Room analysis | 3 |
| kpi_neighborhood_performance | Geographic analysis | 8 |
| ... | 10 more tables | varies |

---

##  Troubleshooting

### MySQL Connection Failed
```bash
# Check MySQL is running
sudo systemctl status mysql

# Verify credentials in .env
cat .env

# Test connection
mysql -h localhost -u main -p
```

### CSV Files Not Found
```bash
# Generate data first
python -m src.data_generator

# Verify files exist
ls -la data/raw/
```

### Power BI Showing Old Data
```
1. In Power BI: Home → Refresh (Ctrl + Shift + R)
2. Wait for "Ready" status
3. Check data in MySQL: SELECT COUNT(*) FROM kpi_*
```

### SQL Pipeline Failed
```bash
# Check SQL file syntax
mysql -u main -p booking_analysis < sql/staging/stg_bookings.sql

# View specific errors
# Edit SQL file and retry
```

---

##  Development

### Running Tests
```bash
# (Add pytest tests in future)
pytest tests/
```

### Code Style
```bash
# Format code
black src/
# Lint code
flake8 src/
```

### Contributing
1. Fork the repository
2. Create a branch: `git checkout -b feature/improvement`
3. Commit: `git commit -am 'Add improvement'`
4. Push: `git push origin feature/improvement`
5. Submit pull request

---

##  Support

For questions or issues:
1. Check [docs/BUSINESS_DECISIONS.md](docs/BUSINESS_DECISIONS.md) for common questions
2. Review [docs/KPIS.md](docs/KPIS.md) for metric definitions
3. Open an issue on GitHub
4. Contact: your-email@company.com

---

##  License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

##  Acknowledgments

- Data generation inspired by Airbnb's marketplace model
- Dashboard design follows modern BI best practices
- SQL pipeline uses medallion architecture (staging → intermediate → marts)

---

