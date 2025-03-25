"""
Script to prepare the raw csv file 'customers_data.csv' and then saving the prepared data
to 'data/prepared'.
File: scripts/data_preparation/prepare_customers_data.py
"""

import pathlib
import sys
import pandas as pd

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now we can import local modules
from utils.logger import logger
from scripts.data_scrubber import DataScrubber

# Constants
DATA_DIR: pathlib.Path = PROJECT_ROOT.joinpath("data")
RAW_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("raw")
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("prepared")

def read_raw_data(file_name: str) -> pd.DataFrame:
    """Read raw data from CSV."""
    file_path: pathlib.Path = RAW_DATA_DIR.joinpath(file_name)
    return pd.read_csv(file_path)

def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    """Save cleaned data to CSV."""
    file_path: pathlib.Path = PREPARED_DATA_DIR.joinpath(file_name)
    df.to_csv(file_path, index=False)
    logger.info(f"Data saved to {file_path}")

def main() -> None:
    """Main function for processing customer data."""
    logger.info("Starting data preparation...")

    df = read_raw_data("customers_data.csv")
    scrubber = DataScrubber(df)

    scrubber.check_data_consistency_before_cleaning()
    # Process data

    # Clean column names
    df.columns = df.columns.str.strip()

    # Drop rows with missing values
    df.dropna(inplace=True)

    
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    
    # Drop rows with missing values in 'CustomerID' and 'Name'
    df = df.dropna(subset=['CustomerID', 'Name'])
    
    # Convert 'JoinDate' to datetime
    df["JoinDate"] = pd.to_datetime(df["JoinDate"])
    
    # Standardize 'PreferredContactMethod'
    df["PreferredContactMethod"] = df["PreferredContactMethod"].str.lower().str.strip()
    
    # Remove row with outliers in 'LoyaltyPoints'
    Q1 = df["LoyaltyPoints"].quantile(0.25)
    Q3 = df["LoyaltyPoints"].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1-1.5*IQR
    upper = Q3+1.5*IQR
    
    df = df[(df["LoyaltyPoints"] >= lower) & (df["LoyaltyPoints"] <= upper)]
    
    # Ensure correct entries in 'Region'
    df = df[df['Region'].isin(['North', 'South', 'East', 'West'])]

    # Correct possible typos in 'PreferredContactMethod'
    df["PreferredContactMethod"] = df["PreferredContactMethod"].replace("cll", "call")
    df["PreferredContactMethod"] = df["PreferredContactMethod"].replace("emal", "email")
    df["PreferredContactMethod"] = df["PreferredContactMethod"].replace("mai", "mail")
    df["PreferredContactMethod"] = df["PreferredContactMethod"].replace("emai", "email")
    df["PreferredContactMethod"] = df["PreferredContactMethod"].replace("cal", "call")
    df["PreferredContactMethod"] = df["PreferredContactMethod"].replace("textt", "text")
    
    # Ensure correct entries in 'PreferredContactMethod'
    df = df[df['PreferredContactMethod'].isin(['call', 'email', 'mail', 'text'])]

    scrubber.check_data_consistency_after_cleaning()

    # Save prepared data
    save_prepared_data(df, "customers_data_prepared.csv")

    logger.info("Data preparation complete.")

if __name__ == "__main__":
    main()