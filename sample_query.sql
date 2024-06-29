-- unifiedScreenClass(記事のタイトル) と、その記事の文字数、その記事の平均セッション時間の平均を取得するクエリ
LENGTH(p.text) AS textLength,
AVG(ad.averageSessionDuration) AS averageSessionDurationAverage
FROM analytics_data ad
JOIN posts p ON ad.unifiedScreenClass LIKE CONCAT('%', p.title, '%')
WHERE ad.date BETWEEN '2024-05-29' AND '2024-06-28'
GROUP BY ad.unifiedScreenClass, p.text;


--指定した期間で合計50PV以上の記事を取得するクエリ
SELECT ad.unifiedScreenClass,
SUM(ad.screenPageViews) AS totalPageViews,
p.title,
p.url
FROM analytics_data ad
JOIN posts p ON ad.unifiedScreenClass LIKE CONCAT('%', p.title, '%')
WHERE ad.date BETWEEN '2024-05-29' AND '2024-06-28'
GROUP BY ad.unifiedScreenClass, p.title, p.text, p.date, p.writer, p.designer
HAVING SUM(ad.screenPageViews) > 50;