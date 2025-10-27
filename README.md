# Ai Insights for Drupal
AI Insights for Drupal is a modular analytics and intelligence toolkit designed for higher-education websites built on Drupal. It combines data from Google Analytics 4 and Drupal entities to generate natural-language insights, detect outdated content, and predict future engagement using machine learning.

## Overview

This project introduces a new layer of intelligence to Drupal by connecting content data and analytics with AI-driven narratives and predictions.
The goal is to help universities and organizations understand how their content performs, which topics attract engagement, and where to improve.

### Core Features

- GA4 connection and basic analytics dashboard.
- Top-performing pages and time-on-page metrics.
- Basic "content freshness" report (identify outdated pages).
- Short AI-generated summary (using Drupal AI).
- Optional lightweight engagement scoring (rule-based or static model).

### Premium (SaaS Integration)

- Advanced predictive analytics (content engagement forecast).
- Semantic duplication and outdated content detection (via NLP).
- Full AI-generated narrative reports with recommendations.
- Automated scheduling and weekly reports.
- Access to the external AI Insights API (Python microservice).

### Data Flow

- Drupal requests metrics from GA4 (freemium) or from the Python service (premium). (TBD)
- Python aggregates, analyzes, and predicts engagement patterns.
- Drupal AI uses LLMs to generate natural-language insights.
- Results are displayed in the AI Insights Dashboard inside Drupal Admin.
