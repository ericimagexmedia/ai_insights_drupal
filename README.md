# Ai Insights for Drupal (MVP)
**AI Insights for Drupal** is a lightweight analytics module for Drupal that brings content performance insights directly into the node edit experience.

Instead of relying on external dashboards like Google Analytics, this module helps content editors understand how their content performs **while they are editing it** — using clear signals, simple metrics, and actionable feedback.

This MVP focuses on answering two essential questions:

- Does this page retain users?
- Does this page encourage users to continue navigating?

## Scope (MVP 1 + MVP 1.5)

This first version is intentionally focused and pragmatic.

All insights are displayed at the node level, inside:

```shell
/node/{nid}/edit
```

There are no global dashboards or complex reports — only contextual insights where editors need them most.

---

## Core Idea

AI Insights for Drupal is not a full analytics replacement.

It is a content intelligence layer inside Drupal, designed to:

- Translate analytics into simple signals
- Reduce cognitive load for editors
- Highlight what needs attention
- Support better content decisions

---

## Data Source

The module integrates with:

- Google Analytics 4

Data is retrieved via the GA4 Data API and mapped to Drupal nodes using page paths.

---

## MVP Features
### 1. Per-node insights inside the editor

Each content node displays its own performance signals directly in the edit form.

Editors do not need to leave Drupal or open external tools.

---

### 2. Retention detection (MVP 1)

Measures whether users are actually consuming the content.

Based on:
- Average engagement time
- Engagement rate
  
Optional (MVP 1.5):
- Scroll depth (25%, 50%, 75%, 100%)

Example insights:
- “Users spend significant time on this page — strong content retention.”
- “Low engagement suggests users are not consuming the content.”

---

### 3. Progression detection (MVP 1)

Measures whether users continue navigating after visiting the page.

Based on:
- Exit rate
- Presence of a next page in the session

  
Optional (MVP 1.5):
- Internal link clicks
- CTA clicks


Example insights:
- “Users continue navigating after this page.”
- “High drop-off — users tend to leave after this content.”

---

### 4. Simple performance classification

Each page is classified using lightweight heuristics:

- High performance
- Needs improvement
- Low performance

This classification is based on a combination of retention and progression signals.

---

### 5. Clear, editor-friendly messaging

Insights are presented in natural language, such as:
- “This page retains users but does not drive further navigation.”
- “Users leave this page quickly — consider improving structure or relevance.”

---

#Why This Matters?

Google Analytics is powerful, but not editor-friendly.

AI Insights for Drupal solves this by:

- Bringing insights into the CMS
- Removing the need for external dashboards
- Making analytics understandable and actionable

---

Future Direction

This MVP lays the foundation for:

- Engagement scoring
- Content ranking
- Predictive analytics
- Machine learning models

But only after validating real usage and value.

---

**Summary**

AI Insights for Drupal (MVP) is a focused, practical tool that helps answer:

- Are users engaging with this content?
- Are users continuing their journey?

By surfacing these answers directly inside Drupal, it empowers editors to improve content with confidence — without needing to interpret complex analytics platforms.
