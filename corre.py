import matplotlib.pyplot as plt  # データの可視化のためのモジュール
import pandas as pd
from fetch import fetch_data  # fetch_data関数をインポート
import re  # 正規表現モジュール

# データベースクエリ
query = """
    SELECT ad.unifiedScreenClass,
    LENGTH(p.text),
    AVG(ad.averageSessionDuration)
    FROM analytics_data ad
    JOIN posts p ON ad.unifiedScreenClass LIKE CONCAT('%', p.title, '%')
    WHERE ad.date BETWEEN '2024-01-01' AND '2024-05-31'
    GROUP BY ad.unifiedScreenClass, p.text;
"""

# クエリからカラム名を抽出する関数
def extract_column_names(query):
    pattern = re.compile(r'SELECT (.+?) FROM', re.IGNORECASE | re.DOTALL)
    match = pattern.search(query)
    if match:
        columns = match.group(1).split(',')
        columns = [col.split(' AS ')[-1].strip() if ' AS ' in col else col.split('.')[-1].strip() for col in columns]
        return columns
    return []

# 外れ値を削除する関数
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# データを取得
df = fetch_data(query)

# クエリからカラム名を抽出
columns = extract_column_names(query)
x_label = columns[1]  # LENGTH(p.text)
y_label = columns[2]  # AVG(ad.averageSessionDuration)

if df is not None:
    # DataFrameの内容を表示
    print("Original DataFrame:")
    print(df)

    # カラム名を変える
    df.columns = columns

    # 数値型に変換
    df[x_label] = pd.to_numeric(df[x_label], errors='coerce')
    df[y_label] = pd.to_numeric(df[y_label], errors='coerce')

    # 外れ値を削除
    df = remove_outliers(df, x_label)
    df = remove_outliers(df, y_label)

    # 外れ値削除後のDataFrameを表示
    print("DataFrame after removing outliers:")
    print(df)

    # 散布図を作成
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df[x_label], df[y_label], color='blue')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(f'Correlation between {x_label} and {y_label}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('scatter_plot.png')  # 画像ファイルとして保存
    print("Scatter plot saved as scatter_plot.png")

    # 相関係数を計算して表示
    correlation = df[[x_label, y_label]].corr()
    print("Correlation Matrix:")
    print(correlation)
