# AAA(Access-and-Article-Analysis)
Python,MySQL,GoogleAppScriptを利用して、記事データとアクセスデータを統合し分析

### 概要
STUDIOで投稿した記事のテキストデータをスクレイピングで取得します。記事のアクセスデータはGoogleAnalyticsで取得します。

それらのデータベースをMySQLデータベースに格納し、Pythonで分析します。

・fetch.pyでMySQLからデータを取得し、それぞれのPythonファイルで任意の分析を行う。

・sample_query.sqlによく使うクエリの置き場。

・mysql_insert.pyは日付指定を行なって複数ファイルを一括してデータベースに保存する。

・gatoCSV.pyはGoogleアナリティクスからデータを取得し、スプレッドシートに取得する

・config.pyはgitignoreしてて、MySQLのログイン情報を置く。

TODO

・スプレッドシートからローカルにcsvを自動でダウンロードするスクリプト(Python?)
・インサートを自動化

