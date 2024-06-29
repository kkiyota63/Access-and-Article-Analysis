# fetch.py
import mysql.connector  # MySQLデータベースに接続するためのモジュール
from mysql.connector import Error  # MySQLエラーを処理するためのモジュール
import pandas as pd  # データをDataFrameで処理するためのモジュール
from config import DB_CONFIG  # 別ファイルのデータベース設定をインポート

# 任意のクエリを実行してデータを取得する関数
def fetch_data(query):
    try:
        # DB_CONFIGの設定を使ってデータベースに接続
        connection = mysql.connector.connect(**DB_CONFIG)
        
        # 接続が成功したか確認
        if connection.is_connected():
            # データベース操作のためのカーソルを作成
            cursor = connection.cursor(dictionary=True)
            # クエリを実行
            cursor.execute(query)
            # 実行したクエリからすべての結果を取得
            result = cursor.fetchall()

            # 結果をpandas DataFrameに変換して返す
            df = pd.DataFrame(result)
            return df

    # データベース操作中に発生するエラーを処理
    except Error as e:
        print(f"Error: {e}")
        return None
    
    # 操作が完了した後にデータベース接続を閉じることを保証
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()  # カーソルを閉じる
            connection.close()  # 接続を閉じる
