from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, Filter, FilterExpression
from google.oauth2 import service_account

KEY_PATH = "ai-drupal-insights.json"
PROPERTY_ID = "510707085"

creds = service_account.Credentials.from_service_account_file(KEY_PATH)
client = BetaAnalyticsDataClient(credentials=creds)

request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    date_ranges=[{"start_date": "30daysAgo", "end_date": "today"}],
    dimensions=[
        {"name": "searchTerm"},
        {"name": "pagePath"},
    ],
    metrics=[{"name": "eventCount"}],
    dimension_filter=FilterExpression(
        filter=Filter(
            field_name="eventName",
            string_filter=Filter.StringFilter(value="view_search_results")
        )
    ),
    order_bys=[{"desc": True, "metric": {"metric_name": "eventCount"}}],
    limit=20
)

response = client.run_report(request)

print("\n🔍 Ranking de buscas (últimos 30 dias):")
for row in response.rows:
    term = row.dimension_values[0].value or "(sem termo)"
    path = row.dimension_values[1].value or "-"
    count = row.metric_values[0].value
    print(f"{count} buscas — termo '{term}' (página {path})")
