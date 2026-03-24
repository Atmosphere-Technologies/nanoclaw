# CRO Benchmarks & Performance Standards

This document provides general benchmarks for landing page conversion rates and technical performance. These are directional and can vary significantly by industry, traffic source, price point, and offer.

## Landing Page Conversion Rate Benchmarks (by Industry)

Use these as a starting point for analysis. The median is often more reliable than the average, as high-performing outliers can skew averages.

| Industry Vertical | Median Conversion Rate | Top 25% Conversion Rate |
|---|---|---|
| SaaS (Free Trial) | 3.0% | 5.5% |
| SaaS (Demo Request) | 2.5% | 4.8% |
| E-commerce | 2.8% | 5.2% |
| Lead Generation (B2B) | 2.1% | 4.5% |
| Lead Generation (B2C) | 4.0% | 8.1% |
| Finance & Insurance | 5.1% | 11.7% |
| Health & Medical | 3.4% | 7.2% |
| Legal | 2.7% | 6.4% |

*Source: Aggregated from various 2024-2025 industry reports from Unbounce, WordStream, and HubSpot.*

## Core Web Vitals (CWV) Performance Thresholds

These metrics, measured by Google PageSpeed Insights, are critical for user experience and SEO. The script `check_core_web_vitals.py` automates this check.

| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| **Largest Contentful Paint (LCP)** | ≤ 2.5 seconds | > 2.5s and ≤ 4.0s | > 4.0 seconds |
| **First Input Delay (FID)** | ≤ 100 milliseconds | > 100ms and ≤ 300ms | > 300 milliseconds |
| **Cumulative Layout Shift (CLS)** | ≤ 0.1 | > 0.1 and ≤ 0.25 | > 0.25 |

**Interpretation:**
- **LCP**: Measures loading performance. A poor score means the main content takes too long to appear.
- **FID**: Measures interactivity. A poor score means the page is slow to respond to user actions (clicks, taps).
- **CLS**: Measures visual stability. A poor score means elements on the page shift around unexpectedly during loading, leading to mis-clicks.

## Key Performance Indicator (KPI) Benchmarks

These benchmarks provide context for analytics data from GA4 and other tools.

| Metric | Poor | Average | Good | Excellent |
|---|---|---|---|---|
| **Bounce Rate** | > 60% | 45% - 60% | 30% - 45% | < 30% |
| **CTA Click-Through Rate (Hero)** | < 5% | 5% - 10% | 10% - 20% | > 20% |
| **Form Conversion Rate (Leads)** | < 10% | 10% - 20% | 20% - 30% | > 30% |
| **Avg. Session Duration** | < 60s | 1-2 min | 2-3 min | > 3 min |
| **Scroll Depth** | < 25% | 25% - 50% | 50% - 75% | > 75% |

*Note: These are general guidelines. B2B often has higher bounce rates and lower conversion rates than B2C. Traffic source also has a major impact (paid social often has higher bounce rates than organic search).*

---

## Mobile Usability Quick Checklist

Use this checklist when performing a manual mobile audit with browser developer tools.

- **Readable Font Size**: Base font size ≥ 16px.
- **Tap Target Size**: Buttons and links ≥ 48x48 CSS pixels.
- **No Horizontal Overflow**: Page fits within the viewport, no horizontal scrolling needed.
- **Accessible CTAs**: Primary call-to-action is visible without scrolling and easy to tap.
- **Non-Intrusive Pop-ups**: Interstitials don't block content access, especially on the first load.
