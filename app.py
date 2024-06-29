import mysql.connector
from mysql.connector import Error
import pandas as pd
import streamlit as st
from config import DB_CONFIG

def fetch_data():
    try:
        # MySQLデータベースに接続
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT ad.unifiedScreenClass,
		        LENGTH(p.text) AS textLength,
		        AVG(ad.averageSessionDuration) AS averageSessionDurationAverage
		        FROM analytics_data ad
		        JOIN posts p ON ad.unifiedScreenClass LIKE CONCAT('%', p.title, '%')
		        WHERE ad.date BETWEEN '2024-05-29' AND '2024-06-28'
		        GROUP BY ad.unifiedScreenClass, p.text;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # データを表示
            df = pd.DataFrame(result)
            return df

    except Error as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    st.title("Analytics Data Viewer")
    
    # データの取得
    data = fetch_data()
    
    if not data.empty:
        st.write("取得したデータ：")
        st.dataframe(data)
    else:
        st.write("データが見つかりませんでした。")

if __name__ == "__main__":
    main()
