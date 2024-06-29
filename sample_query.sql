--MySQLの使い方
--mysql -u root -p
USE analytics_db;

--analytics_dbのanalytics_dataテーブルにアクセスデータ、postsテーブルに記事データが格納されている。

-- unifiedScreenClass(記事のタイトル) と、その記事の文字数、その記事の平均セッション時間の平均を取得するクエリ
LENGTH(p.text) AS textLength,
AVG(ad.averageSessionDuration) AS averageSessionDurationAverage
FROM analytics_data ad
JOIN posts p ON ad.unifiedScreenClass LIKE CONCAT('%', p.title, '%')
WHERE ad.date BETWEEN '2024-MM-DD' AND '2024-MM-DD'
GROUP BY ad.unifiedScreenClass, p.text;

--指定した期間で合計50PV以上の記事を取得するクエリ
SELECT ad.unifiedScreenClass,
SUM(ad.screenPageViews) AS totalPageViews,
p.title,
p.url
FROM analytics_data ad
JOIN posts p ON ad.unifiedScreenClass LIKE CONCAT('%', p.title, '%')
WHERE ad.date BETWEEN '2024-MM-DD' AND '2024-MM-DD'
GROUP BY ad.unifiedScreenClass, p.title, p.text, p.date, p.writer, p.designer
HAVING SUM(ad.screenPageViews) > 50;

-- 記事データをテーブルにインサートするクエリ
LOAD DATA LOCAL INFILE '/path/posts_rows.csv'
INTO TABLE posts
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, date, title, text, writer, designer, categorie, tags, url);

--アクセスデータをテーブルにインサートするクエリ
LOAD DATA LOCAL INFILE '/path/AnalyticsData - 2024-05-29.csv'
INTO TABLE analytics_data
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(date, unifiedScreenClass, screenPageViews, activeUsers, screenPageViewsPerUser, sessions, engagedSessions, sessionsPerUser, averageSessionDuration, screenPageViewsPerSession, bounceRate);
