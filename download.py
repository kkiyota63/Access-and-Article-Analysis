import os
import pandas as pd
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2 import service_account

# スプレッドシートのIDとシート名を指定
SPREADSHEET_ID = '1o0zd3GPktEFiGzLo8pkA6Fh99gFNQt-sSsV4n682n5A'
RANGE_NAME = '2024-01-02'  # 例: 'Sheet1!A1:E10'

# サービスアカウントの認証情報ファイル
SERVICE_ACCOUNT_FILE = '/home/kkiyota/dev/gapv/kadaiinfo-analytics-b609c9eaf824.json'

# スコープを指定
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def main():
    # サービスアカウントの認証情報を使用してクライアントを作成
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Google Sheets APIサービスを構築
    service = build('sheets', 'v4', credentials=credentials)

    # スプレッドシートのデータを取得
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        # CSVファイルにデータを書き込む
        df = pd.DataFrame(values[1:], columns=values[0])  # ヘッダーを含むデータフレームを作成
        df.to_csv('output.csv', index=False)
        print('Data has been downloaded and saved to output.csv')

if __name__ == '__main__':
    main()