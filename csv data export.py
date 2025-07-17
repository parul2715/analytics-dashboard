
import pandas as pd
import pyodbc

engine = create_engine(
    r"mssql+pyodbc://localhost\SQLEXPRESS/e_commerce?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# Define tables to export
tables = ["orders", "order_items", "products" , "order_item_refunds" , "website_pageviews" , "website_sessions"] 

# Export each table to CSV
for table in tables:
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, engine)
    output_path = f"C:/Users/parul/Documents/{table}.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Exported {table} to {output_path}")

engine.close()