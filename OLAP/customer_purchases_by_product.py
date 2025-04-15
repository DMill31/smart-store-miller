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
OLAP_OUTPUT_DIR: pathlib.Path = pathlib.Path("data").joinpath("olap_cubing_outputs")
CUBED_FILE: pathlib.Path = OLAP_OUTPUT_DIR.joinpath("multidimensional_olap_cube.csv")
RESULTS_OUTPUT_DIR: pathlib.Path = pathlib.Path("screenshots")

# Create output directory for results if it doesn't exist
RESULTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_olap_cube(file_path: pathlib.Path) -> pd.DataFrame:
    """Load the precomputed OLAP cube data."""
    try:
        cube_df = pd.read_csv(file_path)
        logger.info(f"OLAP cube data successfully loaded from {file_path}.")
        return cube_df
    except Exception as e:
        logger.error(f"Error loading OLAP cube data: {e}")
        raise


def visualize_customer_sales_by_product(cube_df: pd.DataFrame) -> None:
    """Visualize total sales by customer, broken down by product."""
    try:
        # Pivot the data to organize sales by CustomerID and ProductID
        sales_pivot = cube_df.pivot_table(
            index="customer_id",
            columns="product_id",
            values="sale_amount_sum",
            aggfunc="sum",
            fill_value=0
        )

        # Plot the stacked bar chart
        sales_pivot.plot(
            kind="bar",
            stacked=True,
            figsize=(12, 8),
            colormap="tab10"
        )

        plt.title("Total Sales by Customer on Each Product", fontsize=16)
        plt.xlabel("Customer", fontsize=12)
        plt.ylabel("Total Sales (USD)", fontsize=12)
        plt.xticks(rotation=45)
        plt.legend(title="Product ID", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()

        # Save the visualization
        output_path = RESULTS_OUTPUT_DIR.joinpath("customer_sales_by_product.png")
        plt.savefig(output_path)
        logger.info(f"Stacked bar chart saved to {output_path}.")
        plt.show()
    except Exception as e:
        logger.error(f"Error visualizing sales by day and product: {e}")
        raise


def main():
    """Main function for analyzing and visualizing customer sales by product."""
    logger.info("Starting CUSTOMER_SALES_BY_PRODUCT analysis...")

    # Load the OLAP cube
    cube_df = load_olap_cube(CUBED_FILE)

    # Visualize the results
    visualize_customer_sales_by_product(cube_df)
    logger.info("Analysis and visualization completed successfully.")


if __name__ == "__main__":
    main()
