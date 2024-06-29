import mysql.connector  # MySQLデータベースに接続するためのモジュール
from mysql.connector import Error  # MySQLエラーを処理するためのモジュール
import pandas as pd  # データをDataFrameで処理するためのモジュール
import matplotlib.pyplot as plt  # データの可視化のためのモジュール
import streamlit as st  # Streamlitをインポート

from config import DB_CONFIG  # 別ファイルのデータベース設定をインポート

# Streamlitアプリのタイトル
st.title('Correlation between Text Length and Average Session Duration')

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
                SELECT ad.unifiedScreenClass,
                       LENGTH(p.text) AS textLength,
                       AVG(ad.averageSessionDuration) AS averageSessionDurationAverage
                FROM analytics_data ad
                JOIN posts p ON ad.unifiedScreenClass LIKE CONCAT('%', p.title, '%')
                WHERE ad.date BETWEEN '2024-05-29' AND '2024-06-28'
                GROUP BY ad.unifiedScreenClass, p.text;
            """
            # SQLクエリを実行
            cursor.execute(query)
            # 実行したクエリからすべての結果を取得
            result = cursor.fetchall()

            # 結果をpandas DataFrameに変換して返す
            df = pd.DataFrame(result)
            return df

    # データベース操作中に発生するエラーを処理
    except Error as e:
        st.error(f"Error: {e}")
        return None
    
    # 操作が完了した後にデータベース接続を閉じることを保証
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()  # カーソルを閉じる
            connection.close()  # 接続を閉じる

# データを取得
df = fetch_data()

if df is not None:
    # DataFrameの内容を表示
    st.write(df)

    # textLengthとaverageSessionDurationAverageを散布図で可視化
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['textLength'], df['averageSessionDurationAverage'], color='blue')
    ax.set_xlabel('Text Length')
    ax.set_ylabel('Average Session Duration')
    ax.set_title('Correlation between Text Length and Average Session Duration')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

    # 相関係数を計算して表示
    correlation = df[['textLength', 'averageSessionDurationAverage']].corr()
    st.write("Correlation Matrix:")
    st.write(correlation)
