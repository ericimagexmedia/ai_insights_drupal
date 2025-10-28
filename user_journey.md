# AI Insights for Drupal — User Journey (Work in progress)

This document describes how a university user or web team interacts with the **AI Insights for Drupal** ecosystem — from installation to insight generation.

---

## 1️⃣ Installation and Initial Setup

1. **Install the AI Insights for Drupal module**  
   The user (site administrator) installs the module through Composer or directly from the Drupal admin.

2. **Connect Google Analytics 4 (GA4)**  
   In the module’s configuration screen (`/admin/config/ai-insights/settings`), the admin provides:
   - The GA4 **Property ID**
   - A **Service Account JSON key** or OAuth token
   - The reporting frequency (manual or scheduled)

3. **Choose a plan mode**  
   - **Freemium:** Only the Drupal module and GA4 API are used.  
   - **Premium:** The module is linked to an external **AI Insights API** (Python service) via an API key.

---

## 2️⃣ Data Collection (Freemium)

1. The Drupal module authenticates and requests GA4 data directly using the **Google Analytics Data API**.  
   Typical metrics collected:
   - Page views
   - Average engagement time
   - Bounce rate
   - Device and geography data

2. The module processes this data locally (via PHP) and displays:
   - A basic **Analytics Dashboard** within Drupal Admin  
   - A **“Top Performing Pages”** table  
   - A simple **“Content Freshness”** report (detects outdated pages)

3. Using the **Drupal AI module**, the system generates a short narrative:
   > “Your Program pages saw a 14% increase this week, with strong engagement on the Psychology section.”

💡 No external services are used beyond GA4 and the LLM provider chosen by the admin (e.g. OpenAI, Gemini, or Anthropic).

---

## 3️⃣ Data Enrichment (Premium)

When the user activates the **Premium API key**, a deeper process begins.

1. The Drupal module now sends both GA4 metrics **and Drupal metadata** (nodes, authors, taxonomies, publish dates) to the **Python API** via a secure JSON payload.

   Example payload:
   ```json
   {
     "property_id": "123456",
     "metrics": ["screenPageViews", "engagementRate"],
     "content": [
       {"nid": 42, "type": "program", "title": "Nursing B.S.", "tags": ["Health", "Science"], "published": "2024-09-01"},
       {"nid": 57, "type": "faculty", "title": "Dr. Elena Vega", "tags": ["Research", "Psychology"]}
     ]
   }

2. The Python Layer (FastAPI):

    - Cleans and merges data from multiple sources.
    - Aggregates metrics by content type and taxonomy.
    - Runs pre-trained models to detect:
        - Anomalies (drops or spikes)
        - Engagement trends
        - Content clusters by topic or behavior
3. The Machine Learning Layer (inside the same service or as a submodule):
    - Uses scikit-learn for regression and clustering.
    - Uses Prophet for trend forecasting.
    - Optionally applies spaCy for semantic similarity (detects redundant content).
4. The API returns a structured JSON report:
    ```json
        {
            "summary": {
                "trend": "upward",
                "forecast": "+12% expected engagement next week"
            },
            "top_performers": ["Nursing B.S.", "Psychology M.A."],
            "low_performers": ["History Department"],
            "recommendations": [
                "Update the History Department page (low engagement)",
                "Add internal links between Nursing and Psychology content"
            ]
        }

## 4️⃣ Narrative Generation and Visualization

1. The JSON is received by the Drupal module.
2. The data is passed to the Drupal AI module, which converts it into a readable narrative:

    > “Overall engagement grew by 12% compared to last week, led by the Nursing and Psychology programs. The History section underperformed, suggesting a content review.”
3. The result is displayed in the AI Insights Dashboard:
    - Summary paragraph
    - Key metrics and charts
    - Recommendations list
4. Users can export or schedule summaries (Premium feature):
     - Weekly Report: automatically generated and emailed to site admins.
     - PDF/CSV Export: for institutional reporting or leadership meetings.

## 5️⃣ Continuous Use

- Freemium users can trigger manual refreshes (“Run Analysis”) to see updated summaries.
- Premium users have automatic analysis via Drupal’s cron or a Python scheduler (FastAPI background tasks).
- Over time, the ML models improve with more data, offering:

    - Better forecasts
    - Smarter recommendations
    - Adaptive narrative prompts

## 6️⃣ Long-Term Vision

- Extend analysis to Webform submissions (e.g., admission interest, event registrations).
- Build benchmarking features (compare departments or institutions).
- Provide a training data feedback loop to improve models based on real usage.
- Continue refining narrative templates to match academic tone and accessibility standards.