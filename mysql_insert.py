import mysql.connector
import pandas as pd
import os
from mysql.connector import Error
from datetime import datetime, timedelta
from config import DB_CONFIG

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def insert_data_from_csv(directory, start_date, end_date):
    connection = None  # 初期化
    try:
        # データベース接続の設定
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            # 指定された期間内の日付に一致するファイルを探す
            for single_date in daterange(start_date, end_date):
                date_str = single_date.strftime("%Y-%m-%d")
                for file in os.listdir(directory):
                    if file.endswith(f"{date_str}.csv"):
                        file_path = os.path.join(directory, file)
                        # CSVファイルを読み込む
                        df = pd.read_csv(file_path)
                        # 各行をデータベースに挿入
                        for _, row in df.iterrows():
                            insert_query = """INSERT IGNORE INTO analytics_data (date, unifiedScreenClass, screenPageViews, activeUsers, screenPageViewsPerUser, sessions, engagedSessions, sessionsPerUser, averageSessionDuration, screenPageViewsPerSession, bounceRate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                            cursor.execute(insert_query, (
                                row['date'], 
                                row['unifiedScreenClass'], 
                                row['screenPageViews'], 
                                row['activeUsers'], 
                                row['screenPageViewsPerUser'], 
                                row['sessions'], 
                                row['engagedSessions'], 
                                row['sessionsPerUser'], 
                                row['averageSessionDuration'], 
                                row['screenPageViewsPerSession'], 
                                row['bounceRate']
                            ))
                        connection.commit()
                        print(f"Data from '{file}' inserted successfully into posts.")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
# 使用例
directory_path = '/home/kkiyota/data'
start_date = datetime.strptime('2024-05-18', '%Y-%m-%d')
end_date = datetime.strptime('2024-05-28', '%Y-%m-%d')
insert_data_from_csv(directory_path, start_date, end_date)
