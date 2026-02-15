# src/feature_engineering.py

# feature_engineering.py

import pandas as pd
from pathlib import Path


class MarginFeatureEngineer:
    
    def create_booking_margins(self, bookings, fees, costs, listings, hosts):
        combined = bookings.merge(fees, on='booking_id', how='left')
        combined = combined.merge(costs, on='booking_id', how='left')
        combined = combined.merge(listings[['listing_id', 'property_type']], on='listing_id', how='left')
        combined = combined.merge(hosts[['host_id', 'response_rate', 'avg_review_rating']], on='host_id', how='left')
        
        combined['net_host_margin'] = combined['net_payout_to_host'] - combined['total_host_costs']
        combined['net_margin_pct'] = (combined['net_host_margin'] / combined['gross_booking_value'] * 100).round(2)
        
        combined['profitability_status'] = combined['net_host_margin'].apply(
            lambda x: 'Profitable' if x > 0 else ('Breakeven' if x == 0 else 'Loss')
        )
        
        def get_booking_window(days):
            if days < 3:
                return '<3 days'
            elif days < 7:
                return '3-7 days'
            elif days < 14:
                return '7-14 days'
            elif days < 30:
                return '14-30 days'
            return '30+ days'
        
        combined['booking_window_category'] = combined['days_until_checkin'].apply(get_booking_window)
        
        combined['booking_date'] = pd.to_datetime(combined['booking_date'])
        combined['checkin_date'] = pd.to_datetime(combined['checkin_date'])
        combined['month'] = combined['checkin_date'].dt.month
        combined['year'] = combined['checkin_date'].dt.year
        
        def get_season(month):
            if month in [6, 7, 8, 12]:
                return 'Peak'
            elif month in [3, 4, 5, 9, 10]:
                return 'Shoulder'
            return 'Low'
        
        combined['season'] = combined['month'].apply(get_season)
        
        combined['platform_fees_pct'] = (
            (combined['host_platform_fee'] + combined['guest_service_fee']) / 
            combined['gross_booking_value'] * 100
        ).round(2)
        
        combined['host_costs_pct'] = (
            combined['total_host_costs'] / combined['gross_booking_value'] * 100
        ).round(2)
        
        combined['cleaning_cost_pct'] = (
            combined['cleaning_cost'] / combined['gross_booking_value'] * 100
        ).round(2)
        
        combined['is_repeat_guest'] = 0
        
        return combined
    
    def create_host_aggregates(self, margins, hosts_df):
        host_aggs = margins.groupby('host_id').agg({
            'booking_id': 'count',
            'gross_booking_value': ['sum', 'mean'],
            'net_host_margin': ['sum', 'mean'],
            'net_margin_pct': 'mean',
            'is_cancelled': 'mean',
            'response_rate': 'first',
            'avg_review_rating': 'first',
        }).round(2)
        
        host_aggs.columns = ['total_bookings', 'total_gbv', 'avg_gbv', 
                             'total_margin', 'avg_margin', 'avg_margin_pct',
                             'cancellation_rate', 'response_rate', 'avg_rating']
        
        host_aggs = host_aggs.reset_index()
        host_aggs = host_aggs.sort_values('total_margin', ascending=False)
        host_aggs['cumsum_margin'] = host_aggs['total_margin'].cumsum()
        total_margin = host_aggs['total_margin'].sum()
        host_aggs['cumsum_pct'] = (host_aggs['cumsum_margin'] / total_margin * 100).round(2)
        host_aggs['pareto_classification'] = host_aggs['cumsum_pct'].apply(
            lambda x: 'Top 20%' if x <= 20 else 'Tail 80%'
        )
        
        return host_aggs
    
    def create_neighborhood_aggregates(self, margins):
        neighborhood_aggs = margins.groupby('neighborhood').agg({
            'booking_id': 'count',
            'host_id': 'nunique',
            'listing_id': 'nunique',
            'gross_booking_value': ['sum', 'mean'],
            'net_host_margin': ['sum', 'mean'],
            'net_margin_pct': 'mean',
            'is_cancelled': 'mean',
            'base_price_per_night': 'mean',
        }).round(2)
        
        neighborhood_aggs.columns = ['total_bookings', 'num_hosts', 'num_listings',
                                     'total_gbv', 'avg_gbv', 'total_margin', 
                                     'avg_margin', 'avg_margin_pct', 'cancellation_rate',
                                     'avg_nightly_rate']
        
        neighborhood_aggs = neighborhood_aggs.reset_index()
        neighborhood_aggs['market_saturation'] = (
            neighborhood_aggs['num_listings'] / neighborhood_aggs['num_hosts']
        ).round(2)
        
        profitable_bookings = margins[margins['profitability_status'] == 'Profitable'].groupby('neighborhood').size()
        neighborhood_aggs['pct_profitable'] = (
            neighborhood_aggs['neighborhood'].map(profitable_bookings) / 
            neighborhood_aggs['total_bookings'] * 100
        ).round(1)
        
        return neighborhood_aggs
    
    def create_room_type_analysis(self, margins):
        room_analysis = margins.groupby('room_type').agg({
            'booking_id': 'count',
            'host_id': 'nunique',
            'listing_id': 'nunique',
            'gross_booking_value': ['sum', 'mean'],
            'net_host_margin': ['sum', 'mean'],
            'net_margin_pct': 'mean',
            'is_cancelled': 'mean',
            'base_price_per_night': 'mean',
            'cleaning_cost': 'mean',
            'supplies_cost': 'mean',
            'total_host_costs': 'mean',
        }).round(2)
        
        room_analysis.columns = ['total_bookings', 'num_hosts', 'num_listings',
                                 'total_gbv', 'avg_gbv', 'total_margin', 'avg_margin_per_booking',
                                 'avg_margin_pct', 'cancellation_rate', 'avg_nightly_rate',
                                 'avg_cleaning', 'avg_supplies', 'avg_total_costs']
        
        return room_analysis.reset_index()
    
    def save_enriched_datasets(self, margins, host_aggs, neighborhood_aggs, room_analysis):
        output_dir = Path('data/processed')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        margins.to_csv(output_dir / 'booking_margins.csv', index=False)
        host_aggs.to_csv(output_dir / 'host_profitability.csv', index=False)
        neighborhood_aggs.to_csv(output_dir / 'neighborhood_analysis.csv', index=False)
        room_analysis.to_csv(output_dir / 'room_type_analysis.csv', index=False)
        
        print(f"\n✓ Saved processed datasets to {output_dir}/")