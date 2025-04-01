# smart-store-miller

This repository is for multiple modules of BI and Analytics where we will create a basic business intelligence project over the course of a few weeks.

## How to Install and Run the Project

### How to Install

First you must clone the project to your local machine.

1. Copy the URL of the GitHub Repository you would like
2. Open Powershell and run the following commands

```shell
cd \
cd Projects
git clone https://github.com/**account**/**repo-name**
cd **repo-name**
code . 
```

If .gitignore and/or requirements.txt aren't created, create them.

After creating these files we can now Git add-commit-push using the following code in the terminal

```shell
git add . 
git commit -m "YOUR MESSAGE HERE"
git push -u origin main
```

Once pushed, we now create our virtual environment by running the command:

```shell
py -m venv .venv
```

Now we will activate the virtual environment using this command:

```shell
.venv\Scripts\activate
```

Once the virtual environment has been activated, we can install our dependencies from requirements.txt.

Before installing, it's best to update key packages first.

```shell
py -m pip install --upgrade pip setuptools wheel
py -m pip install -r requirements.txt
```

Lastly, we will select our VS Code Interpreter

1. Press Ctrl+Shift+P
2. Search for "Python: Select Interpreter"
3. Choose the Interpreter for the local .venv 

Now your project is ready and the real fun can begin

Don't forget to regularly Git add-commit-push to keep everything up to date

### How to Run

```shell
py scripts\data_prep.py
py test_data_scrubber.py
py prepare_customers_data.py
py prepare_products_data.py
py prepare_sales_data.py
```

## Data Cleaning Process

### 1. Initial Data Inspection and Profiling

- df.info(): Check data types and identify missing values.
- df.describe(): Get summary statistics for numerical columns.
- df.head() and df.sample(): Inspect the structure and sample of the data.

### 2. Handle Missing Data

- Identify missing values: df.isnull().sum()
- Drop missing values: df.dropna()
- Fill missing values: df.fillna(value)

### 3. Remove Duplicates

- Identify duplicates: df.duplicated()
- Drop duplicates: df.drop_duplicates()

### 4. Filter or Handle Outliers

- Identify outliers: df.describe() and box plot visualization.
- Filter outliers: df[df['column'] < upper_bound]

### 5. Data Type Conversion and Standardization

- Convert data types: df.astype()
- Parse dates: pd.to_datetime(df['column'])

### 6. Standardize and Format Data

- Apply string formatting: df['column'].str.lower() and df['column'].str.strip()
- Rename columns: df.rename(columns={'old_name': 'new_name'})

### 7. Column Management

- Drop unnecessary columns: df.drop(columns=['column'])
- Reorder columns: df = df[['col1', 'col2', ...]]

### 8. Data Integration and Aggregation

- Merge data: pd.merge(df1, df2, on='key_column')
- Aggregate data: df.groupby().agg()

### 9. Final Quality Checks

- Check data consistency, completeness, and final structure.

## Data Warehouse

### Schema

**customers table**

| Column Name              | Data Type | Description                                 |
|--------------------------|-----------|---------------------------------------------|
| customer_id              | INTEGER   | Primary Key                                 |
| name                     | TEXT      | Name of the customer                        |
| region                   | TEXT      | Where the customer lives                    |
| join_date                | DATE      | When the customer joined                    |
| loyalty_points           | INTEGER   | How many loyalty points the customer has    |
| preferred_contact_method | TEXT      | How the customer would like to be contacted |

**products table**

| Column Name              | Data Type | Description                         |
|--------------------------|-----------|-------------------------------------|
| product_id               | INTEGER   | Primary Key                         |
| product_name             | TEXT      | Name of the product                 |
| category                 | TEXT      | Category of the product             |
| unit_price               | REAL      | Price of the product                |
| current_discount_percent | INTEGER   | Discount on the product             |
| subcategory              | TEXT      | Subcategory of the product          |

**sales table**

| Column Name     | Data Type | Description                               |
|-----------------|-----------|-------------------------------------------|
| transaction_id  | INTEGER   | Primary Key                               |
| sale_date       | TEXT      | Date of the sale                          |
| customer_id     | INTEGER   | The customer's ID                         |
| product_id      | INTEGER   | The product's ID                          |
| store_id        | INTEGER   | The store's ID                            |
| campaign_id     | INTEGER   | The campaign's ID                         |
| sale_amount     | REAL      | Total amount of the sale                  |
| bonus_points    | INTEGER   | How many bonus points the sale generated  |
| payment_type    | TEXT      | How the customer paid                     |