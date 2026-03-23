# Data Requirements Checklist for CRO Audit

This checklist should be presented to the user at the start of every audit to gather all available data that will improve the quality and accuracy of the analysis.

## Required Data

### 1. Landing Page URL (REQUIRED)
- The live production URL of the landing page to be audited
- **Format**: Full URL including https://

### 2. Primary Conversion Goal (REQUIRED)
- What action should users take on this landing page?
- **Common examples**: 
  - Click through to Plans/Pricing page
  - Submit lead form
  - Start free trial
  - Make a purchase
  - Download a resource

## Highly Recommended Data (Dramatically Improves Audit Quality)

### 3. GA4 Landing Page Performance Report (CSV)
**What it contains**: Sessions, bounce rate, engagement time, broken down by traffic source

**How to export**:
- GA4 → Reports → Engagement → Pages and screens
- Customize report to add "Session source/medium" dimension
- Add metrics: Bounce rate, Average engagement time
- Filter to your landing page URL
- Export as CSV

**Why it matters**: Identifies which traffic sources have poor engagement, revealing source-specific issues

---

### 4. GA4 Funnel/Path Report (CSV or Screenshot)
**What it contains**: User flow from landing page → next step (e.g., Plans page), showing drop-off rates

**How to export**:
- GA4 → Explore → Funnel exploration
- Step 1: Landing page view
- Step 2: Next page in journey (e.g., Plans page)
- Optional: Add "Session source/medium" breakdown
- Export as CSV or take screenshot

**Why it matters**: Shows the click-through rate (primary conversion metric) and where users abandon the journey

---

### 5. Heatmap Data (CSV, Screenshot, or Session Recording Links)
**Tools**: Hotjar, Microsoft Clarity, Crazy Egg

**What to provide**:
- Heatmap screenshot (click map and scroll map)
- Session recording links (5-10 representative sessions)
- Or CSV export from Clarity/Hotjar if available

**Why it matters**: Reveals UX friction invisible in analytics (rage clicks, confusion, false affordances)

---

### 6. Device & Traffic Breakdown (CSV)
**What it contains**: % of traffic from Desktop vs. Mobile vs. Tablet

**How to export**:
- GA4 → Reports → Tech → Tech details
- Filter to your landing page
- Export as CSV

**Why it matters**: Determines audit priority (if 75% mobile, mobile experience is critical)

---

## Optional But Valuable Data

### 7. Ad Platform Landing Page Experience Scores
**Google Ads**:
- Campaigns → Select campaign → Landing pages tab
- Export showing "Landing page experience" score (Above average / Average / Below average)

**Meta Ads**:
- Ads Manager → Campaign level → Relevance diagnostics
- Screenshot or export showing Quality ranking, Engagement rate ranking

**Why it matters**: If flagged as "Below average," confirms specific technical/UX issues affecting ad performance

---

### 8. Top Exit Pages Report (CSV)
**What it contains**: Pages where users exit the site

**How to export**:
- GA4 → Reports → Engagement → Pages and screens
- Add "Exits" metric
- Filter to landing page
- Export as CSV

**Why it matters**: Confirms if users are leaving from landing page vs. clicking through

---

### 9. Ubersuggest SEO & Keyword Data (Optional)

**What to provide**:
- **Top Keywords for your LP (CSV)**: Ubersuggest → Enter LP URL → Top Pages → Export
- **Competitor Top Pages (CSV)**: Ubersuggest → Enter competitor domain → Top Pages → Export
- **Keyword Ideas for main topic (CSV)**: Ubersuggest → Keyword Ideas → Enter topic → Export

**Why it matters**:
- **Message Match**: Ensure your headline matches what users are searching for
- **Competitive Benchmarking**: Identify which competitor LPs are winning in search
- **A/B Test Ideas**: Use high-volume keywords in headline and CTA tests

---

### 10. Competitor & Reference Landing Page URLs (Optional)
**What to provide**:
- **Competitor LPs**: 3-5 URLs of direct competitors
- **Reference LPs**: 3-5 URLs of best-in-class pages, even from other industries

**Why it matters**: Benchmark your page against market standards, identify gaps and opportunities

---

## Data Collection Template for User

Present this checklist to the user at the start of the audit:

```
To provide the most accurate and actionable CRO audit, please provide the following:

**REQUIRED:**
✅ Landing page URL
✅ Primary conversion goal (e.g., "click through to Plans page")

**HIGHLY RECOMMENDED (if available):**
□ GA4 Landing Page Performance Report (CSV) - shows bounce rate by traffic source
□ GA4 Funnel Report (CSV/screenshot) - shows landing page → next step drop-off
□ Heatmap data from Clarity/Hotjar (screenshot or session recordings)
□ Device breakdown report (CSV) - desktop vs. mobile traffic %
□ Ubersuggest Top Keywords for your LP (CSV) - for message match analysis
□ Ubersuggest Competitor Top Pages (CSV) - for competitive benchmarking

**OPTIONAL (nice to have):**
□ Google Ads landing page experience scores (CSV/screenshot)
□ Meta Ads relevance diagnostics (screenshot)
□ Top exit pages report (CSV)
□ Competitor & Reference URLs (3-5 examples of each)

The more data you can provide, the more specific and actionable the recommendations will be. However, the audit can proceed with just the URL and conversion goal if other data is unavailable.
```
