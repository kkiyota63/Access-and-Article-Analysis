# main.py

import mysql.connector
from mysql.connector import Error
import pandas as pd
from config import DB_CONFIG

def fetch_data():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT unifiedScreenClass, SUM(screenPageViews) AS totalPageViews
                FROM analytics_data
                WHERE date BETWEEN '2024-06-23' AND '2024-06-25'
                GROUP BY unifiedScreenClass
                HAVING totalPageViews > 50;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            df = pd.DataFrame(result)
            print(df)

    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    fetch_data()
