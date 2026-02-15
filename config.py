# Configuration settings for Booking Margin Leakage Analysis

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.absolute()
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
EXTERNAL_DATA_DIR = DATA_DIR / 'external'
REPORTS_DIR = PROJECT_ROOT / 'reports'
FIGURES_DIR = REPORTS_DIR / 'figures'
SQL_DIR = PROJECT_ROOT / 'sql'

# Ensure directories exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, EXTERNAL_DATA_DIR, FIGURES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Data generation parameters
SYNTHETIC_DATA_CONFIG = {
    'n_hosts': 500,
    'n_guests': 5000,
    'n_bookings': 15000,
    'date_range': ('2023-01-01', '2023-12-31'),
    'random_seed': 42,
}

# Room types and property types
ROOM_TYPES = ['Entire home/apt', 'Private room', 'Shared room']
PROPERTY_TYPES = [
    'Apartment', 'House', 'Guesthouse', 'Condo', 'Loft',
    'Villa', 'Studio', 'Townhouse', 'Boutique hotel'
]

# Neighborhoods (simulated cities)
NEIGHBORHOODS = {
    'Manhattan': {'demand_multiplier': 1.8, 'saturation': 0.8, 'tax_rate': 0.14},
    'Brooklyn': {'demand_multiplier': 1.5, 'saturation': 0.7, 'tax_rate': 0.14},
    'Queens': {'demand_multiplier': 1.0, 'saturation': 0.5, 'tax_rate': 0.14},
    'San Francisco': {'demand_multiplier': 2.0, 'saturation': 0.85, 'tax_rate': 0.085},
    'Oakland': {'demand_multiplier': 1.2, 'saturation': 0.6, 'tax_rate': 0.085},
    'Austin': {'demand_multiplier': 1.6, 'saturation': 0.75, 'tax_rate': 0.08},
    'Denver': {'demand_multiplier': 1.3, 'saturation': 0.65, 'tax_rate': 0.10},
    'Seattle': {'demand_multiplier': 1.4, 'saturation': 0.7, 'tax_rate': 0.10},
}

# Pricing and cost parameters
PRICING_BY_ROOM_TYPE = {
    'Entire home/apt': {'base_price': 150, 'std_dev': 80},
    'Private room': {'base_price': 75, 'std_dev': 40},
    'Shared room': {'base_price': 40, 'std_dev': 20},
}

# Cost structure (as % of nightly rate)
COST_STRUCTURE = {
    'cleaning_fee': 30,  # per booking, not per night
    'host_platform_fee_pct': 3.0,  # Airbnb takes 3%
    'guest_service_fee_pct': 14.2,  # Guest pays ~14.2%
    'payment_processing_pct': 2.0,  # Payment processor
}

HOST_COSTS = {
    'cleaning_cost_pct': 0.15,  # 15% of nightly rate per night
    'supplies_cost_pct': 0.05,  # 5% of nightly rate per night
    'maintenance_annual': 1200,  # annual fixed cost
}

# Cancellation rates by days before check-in
CANCELLATION_RATES = {
    'less_than_3_days': 0.15,
    '3_to_7_days': 0.10,
    '7_to_14_days': 0.07,
    '14_to_30_days': 0.05,
    'more_than_30_days': 0.03,
}

# Visualization settings
PLOT_STYLE = 'seaborn-v0_8-darkgrid'
FIGURE_DPI = 300
FIGURE_SIZE = (14, 8)

# Currency
CURRENCY = 'USD'