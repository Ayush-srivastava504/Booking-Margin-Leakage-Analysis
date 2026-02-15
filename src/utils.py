# src/utils.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path


def set_plot_style():
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (14, 8)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['axes.titlesize'] = 12


def format_currency(value):
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.1f}K"
    else:
        return f"${value:.2f}"


def format_percent(value):
    return f"{value:.1f}%"


def create_waterfall_chart(margins_df, output_path='reports/figures/waterfall.png'):
    gbv = margins_df['gross_booking_value'].sum()
    platform_fees = (margins_df['host_platform_fee'] + margins_df['guest_service_fee']).sum()
    payment_fees = margins_df['payment_processing_fee'].sum()
    host_costs = margins_df['total_host_costs'].sum()
    net_margin = margins_df['net_host_margin'].sum()
    
    categories = ['GBV', 'Platform\nFees', 'Payment\nFees', 'Host\nCosts', 'Net\nMargin']
    values = [gbv, -platform_fees, -payment_fees, -host_costs, net_margin]
    colors = ['green', 'red', 'red', 'orange', 'darkgreen']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(categories, np.abs(values), color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Amount ($)', fontsize=11)
    ax.set_title('Revenue Waterfall - Where Does the Money Go?', fontsize=13, fontweight='bold')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    ax.grid(axis='y', alpha=0.3)
    
    for i, (cat, val) in enumerate(zip(categories, values)):
        ax.text(i, np.abs(val) + gbv*0.02, f'${np.abs(val)/1e6:.1f}M', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def create_margin_by_room_type(margins_df, output_path='reports/figures/margin_by_room.png'):
    room_stats = margins_df.groupby('room_type').agg({
        'gross_booking_value': 'mean',
        'net_margin_pct': 'mean',
    }).round(2)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    room_stats['net_margin_pct'].plot(kind='bar', ax=ax1, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.7)
    ax1.set_ylabel('Avg Margin %', fontsize=11)
    ax1.set_title('Profitability by Room Type', fontsize=12, fontweight='bold')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
    ax1.grid(axis='y', alpha=0.3)
    
    room_stats['gross_booking_value'].plot(kind='bar', ax=ax2, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.7)
    ax2.set_ylabel('Avg Booking Value ($)', fontsize=11)
    ax2.set_title('Booking Value by Room Type', fontsize=12, fontweight='bold')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def create_neighborhood_heatmap(margins_df, output_path='reports/figures/neighborhood_heatmap.png'):
    neighborhood_stats = margins_df.groupby('neighborhood').agg({
        'booking_id': 'count',
        'net_margin_pct': 'mean',
    }).round(2).sort_values('net_margin_pct', ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.RdYlGn(neighborhood_stats['net_margin_pct'] / neighborhood_stats['net_margin_pct'].max())
    
    ax.barh(neighborhood_stats.index, neighborhood_stats['net_margin_pct'], color=colors)
    ax.set_xlabel('Avg Margin %', fontsize=11)
    ax.set_title('Profitability by Neighborhood', fontsize=12, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    for i, (idx, val) in enumerate(neighborhood_stats['net_margin_pct'].items()):
        ax.text(val + 1, i, f'{val:.1f}%', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def create_profitability_distribution(margins_df, output_path='reports/figures/profitability_dist.png'):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.hist(margins_df['net_margin_pct'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    ax1.axvline(margins_df['net_margin_pct'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: {margins_df['net_margin_pct'].mean():.1f}%")
    ax1.set_xlabel('Net Margin %', fontsize=11)
    ax1.set_ylabel('Frequency', fontsize=11)
    ax1.set_title('Distribution of Net Margins', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    profit_counts = margins_df['profitability_status'].value_counts()
    colors_pie = {'Profitable': '#2ecc71', 'Loss': '#e74c3c', 'Breakeven': '#f39c12'}
    ax2.pie(profit_counts.values, labels=profit_counts.index, autopct='%1.1f%%', 
            colors=[colors_pie.get(x, 'gray') for x in profit_counts.index], startangle=90)
    ax2.set_title('Profitable vs Loss-Making Bookings', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def create_cancellation_analysis(margins_df, output_path='reports/figures/cancellation.png'):
    cancel_by_window = margins_df.groupby('booking_window_category')['is_cancelled'].mean() * 100
    
    order = ['<3 days', '3-7 days', '7-14 days', '14-30 days', '30+ days']
    cancel_by_window = cancel_by_window.reindex([x for x in order if x in cancel_by_window.index])
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(cancel_by_window.index, cancel_by_window.values, color='indianred', alpha=0.7, edgecolor='black')
    ax.set_ylabel('Cancellation Rate (%)', fontsize=11)
    ax.set_xlabel('Booking Lead Time', fontsize=11)
    ax.set_title('Cancellation Rate by Booking Window', fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    for i, (cat, val) in enumerate(zip(cancel_by_window.index, cancel_by_window.values)):
        ax.text(i, val + 0.5, f'{val:.1f}%', ha='center', fontweight='bold')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def create_seasonality_chart(margins_df, output_path='reports/figures/seasonality.png'):
    monthly = margins_df.groupby('month').agg({
        'booking_id': 'count',
        'gross_booking_value': 'mean',
        'net_margin_pct': 'mean',
    }).round(2)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    ax1.plot(monthly.index, monthly['booking_id'], marker='o', linewidth=2, markersize=8, color='steelblue')
    ax1.fill_between(monthly.index, monthly['booking_id'], alpha=0.3, color='steelblue')
    ax1.set_ylabel('Number of Bookings', fontsize=11)
    ax1.set_title('Seasonality: Booking Volume', fontsize=12, fontweight='bold')
    ax1.grid(alpha=0.3)
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    ax2.plot(monthly.index, monthly['net_margin_pct'], marker='s', linewidth=2, markersize=8, color='darkgreen')
    ax2.fill_between(monthly.index, monthly['net_margin_pct'], alpha=0.3, color='green')
    ax2.set_ylabel('Avg Net Margin %', fontsize=11)
    ax2.set_xlabel('Month', fontsize=11)
    ax2.set_title('Seasonality: Profitability', fontsize=12, fontweight='bold')
    ax2.grid(alpha=0.3)
    ax2.set_xticks(range(1, 13))
    ax2.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def create_cost_breakdown_pie(margins_df, output_path='reports/figures/cost_breakdown.png'):
    avg_costs = {
        'Cleaning': margins_df['cleaning_cost'].mean(),
        'Supplies': margins_df['supplies_cost'].mean(),
        'Maintenance': margins_df['maintenance_allocation'].mean(),
        'Platform Fees': (margins_df['host_platform_fee'] + margins_df['guest_service_fee']).mean(),
        'Net Margin': margins_df['net_host_margin'].mean(),
    }
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#F7DC6F', '#2ECC71']
    ax.pie(avg_costs.values(), labels=avg_costs.keys(), autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title('Average Booking Breakdown (per $100 GBV)', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def print_summary_stats(margins_df):
    print("\nSummary Statistics")
    print("=" * 70)
    
    print(f"\nGross Booking Value:")
    print(f"  Total: ${margins_df['gross_booking_value'].sum():,.0f}")
    print(f"  Mean: ${margins_df['gross_booking_value'].mean():.2f}")
    print(f"  Median: ${margins_df['gross_booking_value'].median():.2f}")
    
    print(f"\nNet Host Margin:")
    print(f"  Total: ${margins_df['net_host_margin'].sum():,.0f}")
    print(f"  Mean: ${margins_df['net_host_margin'].mean():.2f}")
    print(f"  Median: ${margins_df['net_host_margin'].median():.2f}")
    
    print(f"\nMargin %:")
    print(f"  Mean: {margins_df['net_margin_pct'].mean():.1f}%")
    print(f"  Median: {margins_df['net_margin_pct'].median():.1f}%")
    print(f"  Min: {margins_df['net_margin_pct'].min():.1f}%")
    print(f"  Max: {margins_df['net_margin_pct'].max():.1f}%")
    
    print("\n" + "=" * 70)