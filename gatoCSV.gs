function writeDataFromGA4(startDate, endDate) {
  const spreadsheetId = '1o0zd3GPktEFiGzLo8pkA6Fh99gFNQt-sSsV4n682n5A'; // 取得したスプレッドシートIDをここに置き換えます
  const ss = SpreadsheetApp.openById(spreadsheetId);

  const metrics = [
    { name: 'screenPageViews' },
    { name: 'activeUsers' },
    { name: 'screenPageViewsPerUser' },
    { name: 'sessions' },
    { name: 'engagedSessions' },
    { name: 'sessionsPerUser' },
    { name: 'averageSessionDuration' },
    { name: 'screenPageViewsPerSession' },
    { name: 'bounceRate' }
  ];
  const dimensions = [{ name: 'unifiedScreenClass' }];

  const timezone = 'JST';

  const startDateObj = new Date(startDate);
  const endDateObj = new Date(endDate);

  const PROPERTY_ID = PropertiesService.getScriptProperties().getProperty('GA4_ID');

  if (!PROPERTY_ID) {
    Logger.log('プロパティIDが設定されていません。');
    return;
  }

  for (let date = startDateObj; date <= endDateObj; date.setDate(date.getDate() + 1)) {
    const formattedDate = Utilities.formatDate(date, timezone, 'yyyy-MM-dd');
    const dateRanges = [{ startDate: formattedDate, endDate: formattedDate }];

    const request = {
      dimensions: dimensions,
      metrics: metrics,
      dateRanges: dateRanges
    };

    try {
      const response = AnalyticsData.Properties.runReport(request, 'properties/' + PROPERTY_ID);

      if (!response.hasOwnProperty('dimensionHeaders') || !response.hasOwnProperty('metricHeaders') || !response.hasOwnProperty('rows')) {
        Logger.log(`データが取得できませんでした: ${formattedDate}`);
        continue;
      }

      const data = response.rows.map(row => {
        const dimensionValues = row.dimensionValues.map(dimension => dimension.value);
        const metricValues = row.metricValues.map(metric => metric.value);
        return [formattedDate].concat(dimensionValues, metricValues); // 日付を追加
      });

      const header = ['date'].concat(
        response.dimensionHeaders.map(header => header.name),
        response.metricHeaders.map(header => header.name)
      );
      data.unshift(header);

      let sheet = ss.getSheetByName(formattedDate);
      if (!sheet) {
        sheet = ss.insertSheet(formattedDate);
      }

      sheet.getRange(1, 1, data.length, data[0].length).setValues(data);

    } catch (error) {
      Logger.log(`error on ${formattedDate}: ${error}`);
    }
  }
}


writeDataFromGA4('2024-01-01', '2024-05-01');