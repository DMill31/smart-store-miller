import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import sys

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from utils.logger import logger  # noqa: E402

# Constants
DW_DIR: pathlib.Path = pathlib.Path("data").joinpath("dw")
DB_PATH: pathlib.Path = DW_DIR.joinpath("smart_sales.db")
RESULTS_OUTPUT_DIR: pathlib.Path = pathlib.Path("screenshots")

# Create output directory for results if it doesn't exist
RESULTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    '''Load sales data from SQLite database and return as a DataFrame.'''
    logger.info("Loading sales data from SQLite database...")
    
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    
    # SQL query to get sales by customer
    query = '''
        SELECT c.region, SUM(s.sale_amount) AS total_spent
        FROM sale s
        JOIN customer c ON s.customer_id = c.customer_id
        GROUP BY c.region
    '''
    
    # Execute query and load data into DataFrame
    df = pd.read_sql_query(query, conn)
    
    # Close the database connection
    conn.close()
    logger.info("Sales data loaded successfully.")

    return df


def visualize_data(df: pd.DataFrame) -> None:
    '''Create a pie chart for sales by customer and save it.'''
    plt.figure(figsize=(8, 8))
    plt.pie(df['total_spent'], labels=df['region'], autopct='%1.1f%%', startangle=90)
    plt.title('Sales by Region')
    plt.axis('equal') 
    
    
    # Save the visualization
    output_path = RESULTS_OUTPUT_DIR.joinpath("sales_by_region.png")
    plt.savefig(output_path)
    logger.info(f"Pie chart saved to {output_path}.")
    plt.show()

# Main function to load data and create the pie chart
def main():
    # Load data
    customer_data = load_data()
    
    # Visualize the results of the data
    visualize_data(customer_data)

# Run the main function
if __name__ == "__main__":
    main()