# src/data_generator_v2.py

import pandas as pd
import numpy as np
from datetime import timedelta
from faker import Faker
import random
from pathlib import Path

Faker.seed(42)
np.random.seed(42)
random.seed(42)

fake = Faker()

NEIGHBORHOODS = {
    "Manhattan": {"demand_mult": 1.8, "base_price": 200},
    "Brooklyn": {"demand_mult": 1.5, "base_price": 150},
    "Queens": {"demand_mult": 1.0, "base_price": 100},
    "San Francisco": {"demand_mult": 2.0, "base_price": 220},
    "Oakland": {"demand_mult": 1.2, "base_price": 120},
    "Austin": {"demand_mult": 1.6, "base_price": 140},
    "Denver": {"demand_mult": 1.3, "base_price": 130},
    "Seattle": {"demand_mult": 1.4, "base_price": 160},
}

ROOM_TYPES = ["Entire home/apt", "Private room", "Shared room"]
PROPERTY_TYPES = ["Apartment", "House", "Guesthouse", "Condo", "Loft", "Villa", "Studio"]


def generate_hosts(n_hosts=500):
    rows = []
    neighborhoods = list(NEIGHBORHOODS.keys())

    for i in range(n_hosts):
        rows.append({
            "host_id": f"HOST_{i+1:05d}",
            "host_name": fake.name(),
            "neighborhood": np.random.choice(neighborhoods),
            "host_since_days": np.random.randint(100, 2500),
            "response_rate": np.random.uniform(75, 100),
            "number_of_listings": np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1]),
            "avg_review_rating": np.random.uniform(4.2, 5.0),
            "review_count": np.random.randint(5, 200),
        })

    return pd.DataFrame(rows)


def generate_listings(hosts_df):
    rows = []

    for _, host in hosts_df.iterrows():
        for j in range(host["number_of_listings"]):
            room_type = np.random.choice(ROOM_TYPES, p=[0.5, 0.35, 0.15])
            neighborhood = host["neighborhood"]
            base_price = NEIGHBORHOODS[neighborhood]["base_price"]

            if room_type == "Entire home/apt":
                price = base_price * 1.5 * (0.9 + host["avg_review_rating"] / 10)
            elif room_type == "Private room":
                price = base_price * 0.75 * (0.9 + host["avg_review_rating"] / 10)
            else:
                price = base_price * 0.4 * (0.9 + host["avg_review_rating"] / 10)

            rows.append({
                "listing_id": f"LIST_{host['host_id']}_{j+1:02d}",
                "host_id": host["host_id"],
                "property_type": np.random.choice(PROPERTY_TYPES),
                "room_type": room_type,
                "neighborhood": neighborhood,
                "beds": 1 if room_type == "Shared room" else np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1]),
                "price_per_night": round(max(30, price), 2),
                "minimum_nights": np.random.choice([1, 2, 3, 7, 30], p=[0.4, 0.3, 0.15, 0.1, 0.05]),
                "availability_365": np.random.randint(100, 350),
            })

    return pd.DataFrame(rows)


def generate_guests(n_guests=5000):
    rows = []

    for i in range(n_guests):
        rows.append({
            "guest_id": f"GUEST_{i+1:05d}",
            "guest_name": fake.name(),
            "country": np.random.choice(["US", "US", "US", "CA", "UK", "AU"],
                                        p=[0.5, 0.2, 0.1, 0.1, 0.05, 0.05]),
            "verification": np.random.choice(["verified", "unverified"], p=[0.85, 0.15]),
            "total_bookings": np.random.randint(1, 15),
            "avg_rating_given": np.random.uniform(4.0, 5.0),
        })

    return pd.DataFrame(rows)


def generate_bookings(listings_df, guests_df, n_bookings=15000):
    start_date = pd.to_datetime("2023-01-01")
    end_date = pd.to_datetime("2023-12-31")

    rows = []

    for i in range(n_bookings):
        listing = listings_df.sample(1).iloc[0]
        guest = guests_df.sample(1).iloc[0]

        booking_date = start_date + timedelta(days=np.random.randint(0, 365))
        days_advance = int(max(1, np.random.exponential(14)))
        checkin_date = booking_date + timedelta(days=days_advance)

        if checkin_date > end_date:
            continue

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

        price = listing["price_per_night"] * seasonal_mult
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

        rows.append({
            "booking_id": f"BOOKING_{i+1:07d}",
            "listing_id": listing["listing_id"],
            "host_id": listing["host_id"],
            "guest_id": guest["guest_id"],
            "booking_date": booking_date,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "length_of_stay_nights": los,
            "base_price_per_night": round(price, 2),
            "total_base_price": round(price * los, 2),
            "room_type": listing["room_type"],
            "neighborhood": listing["neighborhood"],
            "is_cancelled": int(np.random.random() < cancel_prob),
            "days_until_checkin": days_to_checkin,
        })

    return pd.DataFrame(rows)


def generate_booking_fees(bookings_df):
    rows = []

    for _, booking in bookings_df.iterrows():
        base_price = booking["total_base_price"]

        cleaning_fee = 30
        host_fee = base_price * 0.03
        guest_fee = base_price * 0.142
        payment_fee = (base_price + guest_fee) * 0.02

        gbv = base_price + guest_fee + payment_fee + cleaning_fee
        if booking["is_cancelled"]:
            gbv *= 0.5

        net_payout = gbv - host_fee - payment_fee

        rows.append({
            "booking_id": booking["booking_id"],
            "gross_booking_value": round(gbv, 2),
            "base_price": base_price,
            "cleaning_fee_fixed": cleaning_fee,
            "host_platform_fee": round(host_fee, 2),
            "guest_service_fee": round(guest_fee, 2),
            "payment_processing_fee": round(payment_fee, 2),
            "net_payout_to_host": round(net_payout, 2),
        })

    return pd.DataFrame(rows)


def generate_host_costs(bookings_df):
    rows = []

    sorted_df = bookings_df.sort_values("total_base_price")
    loss_threshold = sorted_df.iloc[int(len(sorted_df) * 0.20)]["total_base_price"]
    breakeven_threshold = sorted_df.iloc[int(len(sorted_df) * 0.35)]["total_base_price"]

    for _, booking in bookings_df.iterrows():
        los = booking["length_of_stay_nights"]
        price = booking["base_price_per_night"]
        gbv = booking["total_base_price"]

        cleaning = price * los * 0.15
        supplies = price * los * 0.05
        maintenance = 12

        if gbv <= loss_threshold:
            mult = np.random.uniform(5.0, 12.0)
            cleaning *= mult
            supplies *= mult
            maintenance *= mult
        elif gbv <= breakeven_threshold:
            mult = np.random.uniform(2.5, 4.0)
            cleaning *= mult
            supplies *= mult
            maintenance *= mult

        total = cleaning + supplies + maintenance

        rows.append({
            "booking_id": booking["booking_id"],
            "cleaning_cost": round(cleaning, 2),
            "supplies_cost": round(supplies, 2),
            "maintenance_allocation": round(maintenance, 2),
            "total_host_costs": round(total, 2),
        })

    return pd.DataFrame(rows)


def main():
    hosts = generate_hosts()
    listings = generate_listings(hosts)
    guests = generate_guests()
    bookings = generate_bookings(listings, guests)
    fees = generate_booking_fees(bookings)
    costs = generate_host_costs(bookings)

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    hosts.to_csv(output_dir / "hosts.csv", index=False)
    listings.to_csv(output_dir / "listings.csv", index=False)
    guests.to_csv(output_dir / "guests.csv", index=False)
    bookings.to_csv(output_dir / "bookings.csv", index=False)
    fees.to_csv(output_dir / "booking_fees.csv", index=False)
    costs.to_csv(output_dir / "host_costs.csv", index=False)


if __name__ == "__main__":
    main()
