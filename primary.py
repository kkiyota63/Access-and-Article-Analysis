import pandas as pd
#主キーの重複を確認する

# CSVファイルのパス
file_path = '/home/kkiyota/data/AnalyticsData - 2024-05-18.csv'

# CSVファイルを読み込む
df = pd.read_csv(file_path)

# 重複を確認するための主キーとなるカラムを指定
primary_key_columns = ['date', 'unifiedScreenClass']

# 重複する行を確認
duplicate_rows = df[df.duplicated(subset=primary_key_columns, keep=False)]

# 重複する行を表示
print(duplicate_rows)
