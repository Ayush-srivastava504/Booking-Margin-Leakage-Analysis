# src/data_loader.py

# data_loader.py

import pandas as pd
from pathlib import Path


class DataLoader:
    
    def __init__(self, data_dir='data/raw'):
        self.data_dir = Path(data_dir)
    
    def load_raw_data(self):
        datasets = {}
        files = ['hosts', 'listings', 'guests', 'bookings', 'booking_fees', 'host_costs']
        
        for file in files:
            path = self.data_dir / f'{file}.csv'
            if path.exists():
                datasets[file] = pd.read_csv(path)
                if file in ['bookings', 'booking_fees']:
                    date_cols = [c for c in datasets[file].columns if 'date' in c.lower()]
                    for col in date_cols:
                        datasets[file][col] = pd.to_datetime(datasets[file][col], errors='coerce')
            else:
                print(f"  File not found: {path}")
        
        return datasets
    
    def validate_datasets(self, datasets):
        print("\n DATA VALIDATION REPORT\n")
        
        for name, df in datasets.items():
            id_col = f'{name[:-1]}_id' if name[-1] == 's' else f'{name}_id'
            if id_col in df.columns:
                dups = df[id_col].duplicated().sum()
                if dups > 0:
                    print(f"  {name}: {dups} duplicate IDs found")
                else:
                    print(f"✓ {name}: No duplicates")
        
        if 'bookings' in datasets and 'hosts' in datasets:
            missing_hosts = ~datasets['bookings']['host_id'].isin(datasets['hosts']['host_id']).sum()
            if missing_hosts > 0:
                print(f"  {missing_hosts} bookings reference non-existent hosts")
            else:
                print(" Bookings: All host references valid")
        
        for name, df in datasets.items():
            nulls = df.isnull().sum()
            if nulls.sum() > 0:
                print(f"\n {name} has missing values:")
                print(nulls[nulls > 0])
            else:
                print(f" {name}: No missing values")
    
    def print_data_summary(self, datasets):
        print("\n DATA SUMMARY\n")
        
        for name, df in datasets.items():
            print(f"\n{name.upper()}")
            print(f"  Rows: {len(df):,}")
            print(f"  Columns: {len(df.columns)}")
            print(f"  Memory: {df.memory_usage(deep=True).sum() / 1024:.0f} KB")
            print(f"  Sample:")
            for i, row in df.head(2).iterrows():
                print(f"    {dict(row)}")