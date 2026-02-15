# src/metrics.py

import pandas as pd
import numpy as np


class MetricsCalculator:
    
    @staticmethod
    def revenue_waterfall(margins_df):
        results = {}
        gbv = margins_df['gross_booking_value'].sum()
        
        results['gross_booking_value'] = gbv
        results['host_platform_fee'] = margins_df['host_platform_fee'].sum()
        results['guest_service_fee'] = margins_df['guest_service_fee'].sum()
        results['payment_processing_fee'] = margins_df['payment_processing_fee'].sum()
        results['total_platform_fees'] = results['host_platform_fee'] + results['guest_service_fee']
        results['net_payout_to_host'] = margins_df['net_payout_to_host'].sum()
        results['total_host_costs'] = margins_df['total_host_costs'].sum()
        results['net_host_margin'] = margins_df['net_host_margin'].sum()
        
        results['platform_fees_pct'] = (results['total_platform_fees'] / gbv * 100)
        results['host_costs_pct'] = (results['total_host_costs'] / gbv * 100)
        results['net_margin_pct'] = (results['net_host_margin'] / gbv * 100)
        
        return results
    
    @staticmethod
    def profitability_distribution(margins_df):
        profitable = (margins_df['net_host_margin'] > 0).sum()
        loss = (margins_df['net_host_margin'] < 0).sum()
        breakeven = (margins_df['net_host_margin'] == 0).sum()
        total = len(margins_df)
        
        return {
            'profitable': profitable,
            'profitable_pct': profitable / total * 100,
            'loss_making': loss,
            'loss_making_pct': loss / total * 100,
            'breakeven': breakeven,
            'breakeven_pct': breakeven / total * 100,
        }
    
    @staticmethod
    def pareto_analysis(margins_df):
        sorted_margins = margins_df.sort_values('net_host_margin', ascending=False)
        cumsum = sorted_margins['net_host_margin'].cumsum()
        total_margin = cumsum.iloc[-1]
        
        top_20_idx = int(len(sorted_margins) * 0.20)
        top_20_margin = cumsum.iloc[top_20_idx - 1] if top_20_idx > 0 else cumsum.iloc[0]
        top_20_pct = (top_20_margin / total_margin * 100)
        
        top_10_idx = int(len(sorted_margins) * 0.10)
        top_10_margin = cumsum.iloc[top_10_idx - 1] if top_10_idx > 0 else cumsum.iloc[0]
        top_10_pct = (top_10_margin / total_margin * 100)
        
        return {
            'top_20pct_bookings_contribute': top_20_pct,
            'top_10pct_bookings_contribute': top_10_pct,
            'concentration_level': 'High' if top_20_pct > 65 else ('Medium' if top_20_pct > 50 else 'Low'),
        }
    
    @staticmethod
    def cancellation_impact(margins_df):
        total_cancelled = margins_df['is_cancelled'].sum()
        cancelled_gbv = margins_df[margins_df['is_cancelled'] == 1]['gross_booking_value'].sum()
        cancelled_margin = margins_df[margins_df['is_cancelled'] == 1]['net_host_margin'].sum()
        
        return {
            'total_cancelled': total_cancelled,
            'cancellation_rate_pct': total_cancelled / len(margins_df) * 100,
            'gbv_lost': cancelled_gbv,
            'margin_lost': cancelled_margin,
            'margin_lost_pct': cancelled_margin / margins_df['net_host_margin'].sum() * 100,
        }
    
    @staticmethod
    def repeat_guest_analysis(margins_df):
        repeat = margins_df[margins_df['is_repeat_guest'] == 1]
        new = margins_df[margins_df['is_repeat_guest'] == 0]
        
        return {
            'repeat_guest_count': len(repeat),
            'repeat_guest_pct': len(repeat) / len(margins_df) * 100,
            'repeat_avg_margin': repeat['net_host_margin'].mean() if len(repeat) > 0 else 0,
            'repeat_avg_gbv': repeat['gross_booking_value'].mean() if len(repeat) > 0 else 0,
            'new_guest_count': len(new),
            'new_guest_pct': len(new) / len(margins_df) * 100,
            'new_avg_margin': new['net_host_margin'].mean() if len(new) > 0 else 0,
            'new_avg_gbv': new['gross_booking_value'].mean() if len(new) > 0 else 0,
        }
    
    @staticmethod
    def seasonality_analysis(margins_df):
        seasonal = margins_df.groupby('season').agg({
            'booking_id': 'count',
            'gross_booking_value': ['sum', 'mean'],
            'net_host_margin': ['sum', 'mean'],
            'is_cancelled': 'mean',
        }).round(2)
        
        seasonal.columns = ['bookings', 'total_gbv', 'avg_gbv', 'total_margin', 'avg_margin', 'cancel_rate']
        return seasonal.reset_index()
    
    @staticmethod
    def margin_by_segment(margins_df, segment_column):
        segment_analysis = margins_df.groupby(segment_column).agg({
            'booking_id': 'count',
            'gross_booking_value': ['sum', 'mean'],
            'net_host_margin': ['sum', 'mean'],
            'net_margin_pct': 'mean',
            'is_cancelled': 'mean',
        }).round(2)
        
        segment_analysis.columns = ['num_bookings', 'total_gbv', 'avg_gbv', 'total_margin', 'avg_margin', 'avg_margin_pct', 'cancel_rate']
        return segment_analysis.reset_index()
    
    @staticmethod
    def generate_kpi_summary(margins_df):
        print("\nBooking Margin Leakage - KPI Summary")
        print("=" * 70)
        
        print(f"\nVolume")
        print(f"  Total Bookings: {len(margins_df):,}")
        print(f"  Active Hosts: {margins_df['host_id'].nunique():,}")
        print(f"  Active Guests: {margins_df['guest_id'].nunique():,}")
        
        waterfall = MetricsCalculator.revenue_waterfall(margins_df)
        print(f"\nRevenue")
        print(f"  Gross Booking Value: ${waterfall['gross_booking_value']:,.0f}")
        print(f"  Avg Booking Value: ${margins_df['gross_booking_value'].mean():.2f}")
        print(f"  Avg Nightly Rate: ${margins_df['base_price_per_night'].mean():.2f}")
        
        print(f"\nFees & Costs (% of GBV)")
        print(f"  Platform Fees: {waterfall['platform_fees_pct']:.1f}%")
        print(f"  Host Costs: {waterfall['host_costs_pct']:.1f}%")
        print(f"  Net Margin: {waterfall['net_margin_pct']:.1f}%")
        
        profit = MetricsCalculator.profitability_distribution(margins_df)
        print(f"\nProfitability")
        print(f"  Profitable: {profit['profitable']:,} ({profit['profitable_pct']:.1f}%)")
        print(f"  Loss-Making: {profit['loss_making']:,} ({profit['loss_making_pct']:.1f}%)")
        print(f"  Avg Net Margin: ${margins_df['net_host_margin'].mean():.2f}")
        print(f"  Avg Margin %: {margins_df['net_margin_pct'].mean():.1f}%")
        
        cancel = MetricsCalculator.cancellation_impact(margins_df)
        print(f"\nCancellations")
        print(f"  Rate: {cancel['cancellation_rate_pct']:.1f}%")
        print(f"  Margin Lost: ${cancel['margin_lost']:,.0f}")
        print(f"  % of Total Margin: {cancel['margin_lost_pct']:.1f}%")
        
        pareto = MetricsCalculator.pareto_analysis(margins_df)
        print(f"\nConcentration (80/20)")
        print(f"  Top 20% bookings: {pareto['top_20pct_bookings_contribute']:.1f}% of margin")
        print(f"  Top 10% bookings: {pareto['top_10pct_bookings_contribute']:.1f}% of margin")
        print(f"  Level: {pareto['concentration_level']}")
        
        print(f"\nBy Room Type")
        by_room = margins_df.groupby('room_type').agg({
            'net_margin_pct': 'mean',
            'net_host_margin': 'mean',
            'is_cancelled': 'mean',
        }).round(2)
        for room in by_room.index:
            print(f"  {room}: {by_room.loc[room, 'net_margin_pct']:.1f}% margin, {by_room.loc[room, 'is_cancelled']*100:.1f}% cancel")
        
        print("\n" + "=" * 70)