# Synthetic Data Generator - Step-by-Step Guide

##  Overview

This guide explains how to generate realistic Airbnb-like booking data with all fees, costs, and cancellations built in.

---

##  How It Works

The data generator creates **interconnected datasets** that simulate a real marketplace:

1. **500 Hosts** → Create properties in 8 neighborhoods
2. **2,000+ Listings** → Multiple properties per host
3. **5,000+ Guests** → Across different countries/verification types
4. **15,000 Bookings** → Throughout 2023 with seasonality
5. **Fees** → Platform charges, payment processing
6. **Costs** → Cleaning, supplies, maintenance per booking

All data is **realistic** but **synthetic** (generated, not real):
- Names from Faker library
- Prices follow distributions (not random)
- Bookings cluster around seasons (summer, holidays)
- Cancellations follow real patterns (higher for last-minute)

---

##  Quick Start (2 Minutes)

### Option A: Run from Command Line
```bash
cd booking-margin-leakage-analysis/
python -m src.data_generator
```

Output:
```
Generating hosts...
Generating listings...
Generating guests...
Generating bookings...
Generating booking fees...
Generating host costs...
✓ Saved all datasets to data/raw/
```

### Option B: Run in Python
```python
from src.data_generator import AirbnbDataGenerator

generator = AirbnbDataGenerator()
datasets = generator.generate_all()
generator.save_all(datasets)

print(f" Generated {len(datasets['bookings'])} bookings")
```

---

##  Generated Files

After running, you'll have 6 CSV files in `data/raw/`:

### 1. `hosts.csv` (500 rows)
```
host_id,host_name,neighborhood,host_since_days,response_rate,number_of_listings,verification_status,avg_review_rating,review_count
HOST_00001,John Smith,Manhattan,1200,95.5,2,verified,4.8,45
HOST_00002,Sarah Johnson,Brooklyn,800,92.3,1,verified,4.7,28
...
```

**Key fields**:
- `host_id`: Unique identifier
- `neighborhood`: Where they're located (Manhattan, San Francisco, etc.)
- `response_rate`: % of messages answered (80-100%)
- `avg_review_rating`: Guest ratings (3.5-5.0)

### 2. `listings.csv` (2,000+ rows)
```
listing_id,host_id,listing_name,property_type,room_type,neighborhood,beds,price_per_night,minimum_nights,availability_365
LIST_HOST_00001_01,HOST_00001,Apartment in Manhattan,Apartment,Entire home/apt,Manhattan,2,245.50,1,280
LIST_HOST_00001_02,HOST_00001,Loft in Manhattan,Loft,Private room,Manhattan,1,98.25,2,260
...
```

**Key fields**:
- `room_type`: Entire home/apt, Private room, or Shared room
- `price_per_night`: Base nightly rate (seasonally adjusted)
- `availability_365`: Days available per year

### 3. `guests.csv` (5,000+ rows)
```
guest_id,guest_name,country,verification_status,reviews_count,avg_rating_as_guest,is_superhost
GUEST_00001,Michael Brown,US,verified,5,4.9,0
GUEST_00002,Emma Davis,CA,verified,12,4.8,1
...
```

### 4. `bookings.csv` (15,000 rows)
```
booking_id,listing_id,host_id,guest_id,booking_date,checkin_date,checkout_date,length_of_stay_nights,base_price_per_night,total_base_price,room_type,neighborhood,is_cancelled,cancellation_date,days_until_checkin
BOOKING_0000001,LIST_HOST_00001_01,HOST_00001,GUEST_00123,2023-01-15,2023-01-20,2023-01-23,3,245.50,736.50,Entire home/apt,Manhattan,0,,5
BOOKING_0000002,LIST_HOST_00002_01,HOST_00002,GUEST_00456,2023-01-16,2023-02-01,2023-02-08,7,145.25,1016.75,Private room,Brooklyn,1,2023-01-25,16
...
```

**Key fields**:
- `booking_date`: When guest booked
- `checkin_date`: When they check in
- `is_cancelled`: 1 if cancelled, 0 if completed
- `days_until_checkin`: Advance booking (affects cancellation rate)
- `length_of_stay_nights`: Number of nights
- `base_price_per_night`: Actual price (includes seasonal variation)

### 5. `booking_fees.csv` (15,000 rows)
```
booking_id,gross_booking_value,base_price,cleaning_fee_fixed,host_platform_fee,guest_service_fee,payment_processing_fee,net_payout_to_host
BOOKING_0000001,852.80,736.50,30.00,22.10,104.50,29.70,800.70
BOOKING_0000002,1181.42,1016.75,30.00,30.50,144.38,43.29,1107.12
...
```

**How it's calculated**:
- `gross_booking_value` = base_price + cleaning_fee + guest_service_fee + payment_processing_fee
- `host_platform_fee` = base_price × 3%
- `guest_service_fee` = base_price × 14.2%
- `payment_processing_fee` = (base_price + guest_service_fee) × 2%
- `net_payout_to_host` = gross_booking_value - host_platform_fee - payment_processing_fee
- If cancelled: `gross_booking_value` × 50% (refund penalty)

### 6. `host_costs.csv` (15,000 rows)
```
booking_id,cleaning_cost,supplies_cost,maintenance_allocation,total_host_costs
BOOKING_0000001,110.53,36.84,12.00,159.37
BOOKING_0000002,152.45,50.82,12.00,215.27
...
```

**How it's calculated**:
- `cleaning_cost` = base_price_per_night × length_of_stay × 15%
- `supplies_cost` = base_price_per_night × length_of_stay × 5%
- `maintenance_allocation` = annual_maintenance ($1,200) / bookings_per_year (100)

---

##  Configuration Parameters

Edit `config.py` to customize data generation:

```python
SYNTHETIC_DATA_CONFIG = {
    'n_hosts': 500,              # Number of hosts
    'n_guests': 5000,            # Number of guests
    'n_bookings': 15000,         # Number of bookings
    'date_range': ('2023-01-01', '2023-12-31'),  # Year
    'random_seed': 42,           # For reproducibility
}
```

**Neighborhoods** (change multipliers):
```python
NEIGHBORHOODS = {
    'Manhattan': {'demand_multiplier': 1.8, 'saturation': 0.8, 'tax_rate': 0.14},
    # demand_multiplier: Price multiplier (1.0 = base price)
    # saturation: Market competition level (0-1)
    # tax_rate: Local tax rate
    ...
}
```

**Cost Structure** (customize fees):
```python
COST_STRUCTURE = {
    'cleaning_fee': 30,           # Fixed per booking ($)
    'host_platform_fee_pct': 3.0, # Airbnb commission (%)
    'guest_service_fee_pct': 14.2,# Guest-side fee (%)
    'payment_processing_pct': 2.0,# Payment processor (%)
}
```

**Host Costs** (customize expense rates):
```python
HOST_COSTS = {
    'cleaning_cost_pct': 0.15,    # 15% of nightly rate
    'supplies_cost_pct': 0.05,    # 5% of nightly rate
    'maintenance_annual': 1200,   # Annual maintenance
}
```

---

##  What's Realistic About This Data?

### Realistic Elements

1. **Pricing by Location**
   - Manhattan: ~1.8x base price
   - Budget areas: ~1.0x base price
   - Driven by demand multiplier

2. **Pricing by Room Type**
   - Entire home: $150/night avg
   - Private room: $75/night avg
   - Shared room: $40/night avg

3. **Seasonality**
   - Peak: June-August, December (1.3x multiplier)
   - Shoulder: March-May, September-October (1.1x)
   - Low: January, February, November (0.8x)

4. **Booking Patterns**
   - Lead time: Average ~14 days in advance
   - Length of stay: 1-7 nights most common
   - Some 28+ night bookings (monthly rentals)

5. **Cancellations**
   - <3 days before: 15% cancel rate
   - 3-7 days: 10%
   - 7-14 days: 7%
   - 14-30 days: 5%
   - 30+ days: 3%

6. **Host Quality**
   - High ratings (4.5-5.0 range) → higher prices
   - Low ratings (3.5-4.0 range) → discount
   - Good response rate (80-100%) → more bookings

7. **Fee Structure**
   - Matches Airbnb's actual fees
   - Platform: 3% (host side)
   - Guest service: 14.2% (guest side)
   - Payment: 2%

###  Simplified Elements

- Tax treatment is basic
- Dynamic pricing not simulated
- No reviews/ratings in bookings
- Maintenance cost is averaged
- No host/guest disputes
- No service issues/refunds

---

##  Expected Data Statistics

After generation, check these ranges:

### Booking Statistics
- **Total bookings**: 15,000
- **Cancellation rate**: ~7% overall
- **Avg booking value**: $800-900
- **Avg length of stay**: 3-4 nights
- **Avg booking advance**: 14-21 days

### Profitability Statistics
- **Avg net margin**: $400-450 per booking
- **Avg margin %**: 50-60% of GBV
- **Profitable bookings**: 95%+
- **Loss-making**: <5%

### Geographic Statistics
- **Highest prices**: San Francisco, Manhattan
- **Highest margins**: Mid-tier neighborhoods
- **Most bookings**: Well-saturated areas

---

##  Troubleshooting

### Issue: "Module not found"
```bash
# Make sure you're in the project directory
cd booking-margin-leakage-analysis/
python -m src.data_generator
```

### Issue: "No such file or directory: data/raw/"
```bash
# Create directories first
mkdir -p data/{raw,processed,external}
python -m src.data_generator
```

### Issue: Data looks wrong
```bash
# Reset random seed in config.py
SYNTHETIC_DATA_CONFIG = {
    'random_seed': 42,  # Change to different number
}
```

### Issue: Out of memory with large datasets
```python
# Reduce in config.py
SYNTHETIC_DATA_CONFIG = {
    'n_bookings': 5000,  # Instead of 15000
}
```

---

##  Next Steps

1. **Generate data**: `python -m src.data_generator`
2. **Verify files**: Check `data/raw/` folder
3. **Inspect data**: Open CSVs in Excel or:
   ```python
   import pandas as pd
   df = pd.read_csv('data/raw/bookings.csv')
   print(df.head())
   print(df.describe())
   ```
4. **Continue to EDA**: Follow `STEP_BY_STEP_EDA.md`

---

## 📝 Data Dictionary

| File | Rows | Purpose |
|------|------|---------|
| hosts.csv | 500 | Host profiles |
| listings.csv | 2,000+ | Property listings |
| guests.csv | 5,000+ | Guest profiles |
| bookings.csv | 15,000 | Booking transactions |
| booking_fees.csv | 15,000 | Fee breakdowns |
| host_costs.csv | 15,000 | Cost allocations |

---

**Generated**: February 2026
**Format**: CSV (Excel compatible)
**Total Size**: ~10-15MB