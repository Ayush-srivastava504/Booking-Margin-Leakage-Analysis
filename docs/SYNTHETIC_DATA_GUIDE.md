# Synthetic Data Generator – Quality Validation Guide

## Overview

This guide validates the realism and analytical readiness of generated synthetic data. The goal is to ensure hosts, guests, and bookings reflect believable marketplace behavior and support meaningful margin analysis.

---

## Dataset Scope

* **Hosts:** 500
* **Guests:** 5,000
* **Bookings:** 15,000

The generated data should resemble a functioning short-term rental marketplace with realistic distributions, risk patterns, and profitability structure.

---

## Host Quality Standards

Hosts should reflect a balanced performance portfolio:

* Experience mix: new (10%), established (25%), veteran (65%)
* Ratings distribution: majority between 4.3–5.0
* Response rates: predominantly above 85%
* Listings: mix of single and multi-property hosts

Expected outcome:

* 70%+ hosts rated good or better
* 80%+ responsive communication
* Small underperforming segment to simulate real risk

---

## Guest Quality Standards

Guests should represent a healthy customer base:

* 85% verified accounts
* Mix of repeat and first-time users
* Majority rated 4.0+

Expected outcome:

* 75% repeat or returning users
* 90% good or excellent guest ratings
* 10–15% risk segment

---

## Booking Portfolio Standards

Bookings must follow realistic behavioral and financial patterns:

* 75–80% profitable
* 6–10% cancellation rate overall
* Higher cancellation rate for last-minute bookings
* Balanced segment mix:

  * Entire homes (~50%)
  * Private rooms (~35%)
  * Shared rooms (~15%)

Lead-time distribution:

* 45% advance bookings (14+ days)
* 35% medium (3–14 days)
* 20% last-minute (<3 days)

---

## Pre-Generation Checklist

Before running:

```bash
python -m pip list | grep -E "pandas|sqlalchemy|faker"
mysql -u main -p -e "SELECT 'Database ready';"
ls data/
```

Confirm:

* Required packages installed
* Database connection active
* Folder structure exists
* Config matches expected counts (500 hosts, 15,000 bookings)

---

## Post-Generation Audit

After running:

```bash
python -m src.data_generator
```

Validate:

### 1. Row Counts

* Hosts ≈ 500
* Bookings ≈ 15,000
* Fees match bookings

### 2. Data Integrity

* No missing values
* Valid date ranges (Jan–Dec 2023)
* Reasonable average nightly price
* Cancellation rate 6–10%

### 3. Profitability

* 75–80% bookings profitable
* Realistic average margin
* Negative margin segment present but controlled

---

## Acceptance Criteria

Data qualifies if:

* Correct record counts
* Zero null critical fields
* Realistic cancellation patterns
* Balanced profitability distribution
* Ratings within 3.5–5.0 range
* Financial outputs align with expected business model

If all checks pass, the dataset is ready for MySQL loading and downstream analytics.

---

## Generation Workflow

```
Run generator
   ↓
Validate counts and distributions
   ↓
Audit profitability and cancellations
   ↓
Approve for production analytics
```

If metrics fall outside expected ranges, regenerate with a new seed.

---

This ensures the synthetic dataset is not random noise but a structured, analysis-ready marketplace simulation.
