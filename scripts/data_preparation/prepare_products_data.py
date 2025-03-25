"""
Script to prepare the raw csv file 'products_data.csv' and then saving the prepared data
to 'data/prepared'.
File: scripts/data_preparation/prepare_products_data.py
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
    """Main function for processing product data."""
    logger.info("Starting data preparation...")

    df = read_raw_data("products_data.csv")
    scrubber = DataScrubber(df)

    # Process data

    scrubber.check_data_consistency_before_cleaning()

    # Clean column names
    df.columns = df.columns.str.strip()

    # Drop rows with missing values
    df.dropna(inplace=True)
    
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    
    # Drop rows with missing values in 'ProductID' and 'ProductName'
    df = df.dropna(subset=['ProductID', 'ProductName'])
    
    
    # Standardize 'Subcategory'
    df["Subcategory"] = df["Subcategory"].str.lower().str.strip()
    
    # Remove row with outliers in 'CurrentDiscountPercent'
    Q1 = df["CurrentDiscountPercent"].quantile(0.25)
    Q3 = df["CurrentDiscountPercent"].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1-1.5*IQR
    upper = Q3+1.5*IQR
    
    df = df[(df["CurrentDiscountPercent"] >= lower) & (df["CurrentDiscountPercent"] <= upper)]
    
    # Ensure correct entries in 'Category'
    df = df[df['Category'].isin(['Electronics', 'Clothing', 'Sports'])]

    # Correct possible typos in 'Subcategory'
    df["Subcategory"] = df["Subcategory"].replace("computrs", "computers")
    df["Subcategory"] = df["Subcategory"].replace("miscellaneus", "miscellaneous")
    df["Subcategory"] = df["Subcategory"].replace("miscelaneous", "miscellaneous")
    df["Subcategory"] = df["Subcategory"].replace("accessorie", "accessories")
    df["Subcategory"] = df["Subcategory"].replace("ball", "balls")
    df["Subcategory"] = df["Subcategory"].replace("top", "tops")
    df["Subcategory"] = df["Subcategory"].replace("headwea", "headwear")
    df["Subcategory"] = df["Subcategory"].replace("ecurity", "security")
    df["Subcategory"] = df["Subcategory"].replace("safety", "security")
    
    # Ensure correct entries in 'Subcategory'
    df = df[df['Subcategory'].isin(['tops', 'computers', 'accessories', 'miscellaneous',
                                     'security', 'balls', 'headwear'])]
    
    scrubber.check_data_consistency_after_cleaning()

    # Save prepared data
    save_prepared_data(df, "products_data_prepared.csv")

    logger.info("Data preparation complete.")

if __name__ == "__main__":
    main()