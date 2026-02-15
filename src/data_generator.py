# data_generator.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
from pathlib import Path

Faker.seed(42)
np.random.seed(42)
random.seed(42)

fake = Faker()

NEIGHBORHOODS = {
    'Manhattan': {'demand_mult': 1.8, 'base_price': 200},
    'Brooklyn': {'demand_mult': 1.5, 'base_price': 150},
    'Queens': {'demand_mult': 1.0, 'base_price': 100},
    'San Francisco': {'demand_mult': 2.0, 'base_price': 220},
    'Oakland': {'demand_mult': 1.2, 'base_price': 120},
    'Austin': {'demand_mult': 1.6, 'base_price': 140},
    'Denver': {'demand_mult': 1.3, 'base_price': 130},
    'Seattle': {'demand_mult': 1.4, 'base_price': 160},
}

ROOM_TYPES = ['Entire home/apt', 'Private room', 'Shared room']
PROPERTY_TYPES = ['Apartment', 'House', 'Guesthouse', 'Condo', 'Loft', 'Villa', 'Studio']


def generate_hosts(n_hosts=500):
    data = []
    for i in range(n_hosts):
        data.append({
            'host_id': f'HOST_{i+1:05d}',
            'host_name': fake.name(),
            'neighborhood': np.random.choice(list(NEIGHBORHOODS.keys())),
            'host_since_days': np.random.randint(100, 2500),
            'response_rate': np.random.uniform(75, 100),
            'number_of_listings': np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1]),
            'avg_review_rating': np.random.uniform(4.2, 5.0),
            'review_count': np.random.randint(5, 200),
        })
    return pd.DataFrame(data)


def generate_listings(hosts_df):
    data = []
    for _, host in hosts_df.iterrows():
        for j in range(host['number_of_listings']):
            room_type = np.random.choice(ROOM_TYPES, p=[0.5, 0.35, 0.15])
            neighborhood = host['neighborhood']
            base = NEIGHBORHOODS[neighborhood]['base_price']
            
            # price varies by room type and host quality
            if room_type == 'Entire home/apt':
                price = base * 1.5 * (0.9 + host['avg_review_rating']/10)
            elif room_type == 'Private room':
                price = base * 0.75 * (0.9 + host['avg_review_rating']/10)
            else:
                price = base * 0.4 * (0.9 + host['avg_review_rating']/10)
            
            data.append({
                'listing_id': f"LIST_{host['host_id']}_{j+1:02d}",
                'host_id': host['host_id'],
                'property_type': np.random.choice(PROPERTY_TYPES),
                'room_type': room_type,
                'neighborhood': neighborhood,
                'beds': 1 if room_type == 'Shared room' else np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1]),
                'price_per_night': round(max(30, price), 2),
                'minimum_nights': np.random.choice([1, 2, 3, 7, 30], p=[0.4, 0.3, 0.15, 0.1, 0.05]),
                'availability_365': np.random.randint(100, 350),
            })
    return pd.DataFrame(data)


def generate_guests(n_guests=5000):
    data = []
    for i in range(n_guests):
        data.append({
            'guest_id': f'GUEST_{i+1:05d}',
            'guest_name': fake.name(),
            'country': np.random.choice(['US', 'US', 'US', 'CA', 'UK', 'AU'], p=[0.5, 0.2, 0.1, 0.1, 0.05, 0.05]),
            'verification': np.random.choice(['verified', 'unverified'], p=[0.85, 0.15]),
            'total_bookings': np.random.randint(1, 15),
            'avg_rating_given': np.random.uniform(4.0, 5.0),
        })
    return pd.DataFrame(data)


def generate_bookings(listings_df, guests_df, n_bookings=15000):
    date_start = pd.to_datetime('2023-01-01')
    date_end = pd.to_datetime('2023-12-31')
    
    data = []
    for i in range(n_bookings):
        listing = listings_df.sample(1).iloc[0]
        guest = guests_df.sample(1).iloc[0]
        
        days_offset = np.random.randint(0, 365)
        booking_date = date_start + timedelta(days=days_offset)
        
        days_advance = np.random.exponential(14)
        checkin_date = booking_date + timedelta(days=max(1, int(days_advance)))
        
        if checkin_date > date_end:
            continue
        
        # length of stay - mostly short trips
        los = int(np.random.choice([1, 2, 3, 4, 5, 7, 14], 
                           p=[0.25, 0.25, 0.2, 0.1, 0.1, 0.07, 0.03]))
        checkout_date = checkin_date + timedelta(days=los)
        
        month = checkin_date.month
        if month in [6, 7, 8, 12]:
            seasonal_mult = 1.4
        elif month in [3, 4, 5, 9, 10]:
            seasonal_mult = 1.1
        else:
            seasonal_mult = 0.85
        
        actual_price = listing['price_per_night'] * seasonal_mult
        
        # cancel rates higher for last-minute bookings
        days_to_checkin = (checkin_date - booking_date).days
        if days_to_checkin < 3:
            cancel_prob = 0.15
        elif days_to_checkin < 7:
            cancel_prob = 0.10
        elif days_to_checkin < 14:
            cancel_prob = 0.07
        elif days_to_checkin < 30:
            cancel_prob = 0.05
        else:
            cancel_prob = 0.03
        
        is_cancelled = np.random.random() < cancel_prob
        
        data.append({
            'booking_id': f'BOOKING_{i+1:07d}',
            'listing_id': listing['listing_id'],
            'host_id': listing['host_id'],
            'guest_id': guest['guest_id'],
            'booking_date': booking_date,
            'checkin_date': checkin_date,
            'checkout_date': checkout_date,
            'length_of_stay_nights': los,
            'base_price_per_night': round(actual_price, 2),
            'total_base_price': round(actual_price * los, 2),
            'room_type': listing['room_type'],
            'neighborhood': listing['neighborhood'],
            'is_cancelled': 1 if is_cancelled else 0,
            'days_until_checkin': days_to_checkin,
        })
    
    return pd.DataFrame(data)


def generate_booking_fees(bookings_df):
    data = []
    for _, booking in bookings_df.iterrows():
        base_price = booking['total_base_price']
        
        cleaning_fee = 30
        host_platform_fee = base_price * 0.03
        guest_service_fee = base_price * 0.142
        payment_fee = (base_price + guest_service_fee) * 0.02
        
        gbv = base_price + guest_service_fee + payment_fee + cleaning_fee
        
        if booking['is_cancelled']:
            gbv = gbv * 0.5
        
        net_payout = gbv - host_platform_fee - payment_fee
        
        data.append({
            'booking_id': booking['booking_id'],
            'gross_booking_value': round(gbv, 2),
            'base_price': base_price,
            'cleaning_fee_fixed': cleaning_fee,
            'host_platform_fee': round(host_platform_fee, 2),
            'guest_service_fee': round(guest_service_fee, 2),
            'payment_processing_fee': round(payment_fee, 2),
            'net_payout_to_host': round(net_payout, 2),
        })
    
    return pd.DataFrame(data)


def generate_host_costs(bookings_df):
    data = []
    for _, booking in bookings_df.iterrows():
        los = booking['length_of_stay_nights']
        price = booking['base_price_per_night']
        
        cleaning_cost = price * los * 0.15
        supplies_cost = price * los * 0.05
        maintenance_cost = 12
        
        total_costs = cleaning_cost + supplies_cost + maintenance_cost
        
        data.append({
            'booking_id': booking['booking_id'],
            'cleaning_cost': round(cleaning_cost, 2),
            'supplies_cost': round(supplies_cost, 2),
            'maintenance_allocation': round(maintenance_cost, 2),
            'total_host_costs': round(total_costs, 2),
        })
    
    return pd.DataFrame(data)


def main():
    print("Generating synthetic data...")
    
    print("  → Generating 500 hosts...")
    hosts = generate_hosts(500)
    
    print("  → Generating ~2000 listings...")
    listings = generate_listings(hosts)
    
    print("  → Generating 5000 guests...")
    guests = generate_guests(5000)
    
    print("  → Generating 15000 bookings...")
    bookings = generate_bookings(listings, guests, 15000)
    
    print("  → Generating booking fees...")
    fees = generate_booking_fees(bookings)
    
    print("  → Generating host costs...")
    costs = generate_host_costs(bookings)
    
    output_dir = Path('data/raw')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nSaving to data/raw/...")
    hosts.to_csv(output_dir / 'hosts.csv', index=False)
    listings.to_csv(output_dir / 'listings.csv', index=False)
    guests.to_csv(output_dir / 'guests.csv', index=False)
    bookings.to_csv(output_dir / 'bookings.csv', index=False)
    fees.to_csv(output_dir / 'booking_fees.csv', index=False)
    costs.to_csv(output_dir / 'host_costs.csv', index=False)
    
    print("\n✓ Data generation complete!")
    print(f"\nDatasets created:")
    print(f"  hosts.csv          ({len(hosts):,} hosts)")
    print(f"  listings.csv       ({len(listings):,} listings)")
    print(f"  guests.csv         ({len(guests):,} guests)")
    print(f"  bookings.csv       ({len(bookings):,} bookings)")
    print(f"  booking_fees.csv   ({len(fees):,} records)")
    print(f"  host_costs.csv     ({len(costs):,} records)")
    
    print("\nQuick Stats:")
    print(f"  Total GBV: ${fees['gross_booking_value'].sum():,.0f}")
    print(f"  Avg booking value: ${fees['gross_booking_value'].mean():.2f}")
    print(f"  Cancellation rate: {bookings['is_cancelled'].mean()*100:.1f}%")
    print(f"  Avg net margin: ${(fees['net_payout_to_host'].sum() - costs['total_host_costs'].sum()) / len(bookings):.2f}")


if __name__ == '__main__':
    main()