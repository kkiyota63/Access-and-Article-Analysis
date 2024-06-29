# 必要なモジュールをインポート
import mysql.connector  # MySQLデータベースに接続するためのモジュール
from mysql.connector import Error  # MySQLエラーを処理するためのモジュール
import pandas as pd  # データをDataFrameで処理するためのモジュール
from config import DB_CONFIG  # 別ファイルのデータベース設定をインポート

# データベースからデータを取得する関数
def fetch_data():
    try:
        # DB_CONFIGの設定を使ってデータベースに接続
        connection = mysql.connector.connect(**DB_CONFIG)
        
        # 接続が成功したか確認
        if connection.is_connected():
            # データベース操作のためのカーソルを作成
            cursor = connection.cursor(dictionary=True)
            # データを選択および集計するSQLクエリ
            query = """
                SELECT unifiedScreenClass, SUM(screenPageViews) AS totalPageViews
                FROM analytics_data
                WHERE date BETWEEN '2024-06-23' AND '2024-06-25'
                GROUP BY unifiedScreenClass
                HAVING totalPageViews > 50;
            """
            # SQLクエリを実行
            cursor.execute(query)
            # 実行したクエリからすべての結果を取得
            result = cursor.fetchall()

            # 結果をpandas DataFrameに変換して表示
            df = pd.DataFrame(result)
            print(df)

    # データベース操作中に発生するエラーを処理
    except Error as e:
        print(f"Error: {e}")
    
    # 操作が完了した後にデータベース接続を閉じることを保証
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()  # カーソルを閉じる
            connection.close()  # 接続を閉じる

# スクリプトのメインエントリーポイント
if __name__ == "__main__":
    fetch_data()  # データを取得する関数を呼び出す
