from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
from google.oauth2 import service_account

KEY_PATH = "ai-drupal-insights.json"
PROPERTY_ID = "510707085"

creds = service_account.Credentials.from_service_account_file(KEY_PATH)
client = BetaAnalyticsDataClient(credentials=creds)

request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    date_ranges=[{"start_date": "30daysAgo", "end_date": "today"}],
    dimensions=[{"name": "pagePath"}, {"name": "pageTitle"}],
    metrics=[{"name": "screenPageViews"}],
    order_bys=[{"desc": True, "metric": {"metric_name": "screenPageViews"}}],
    limit=20
)

response = client.run_report(request)

print("\n📈 Top 20 páginas mais visualizadas:")
for row in response.rows:
    path = row.dimension_values[0].value
    title = row.dimension_values[1].value
    views = row.metric_values[0].value
    print(f"{views} views - {title} ({path})")