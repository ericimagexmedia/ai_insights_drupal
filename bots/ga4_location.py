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
    dimensions=[{"name": "country"}, {"name": "city"}],
    metrics=[{"name": "sessions"}],
    limit=100
)

response = client.run_report(request)

print("🌎 Relatório GA4: Sessões por país e cidade (últimos 30 dias)")
for row in response.rows:
    country = row.dimension_values[0].value
    city = row.dimension_values[1].value
    sessions = row.metric_values[0].value
    print(f"{country} - {city}: {sessions}")
