# Google Ads XML Export Schema Reference

## Common Report Fields

Google Ads XML exports typically include these key fields:

### Campaign-Level Metrics

- `campaign` / `campaign_name` - Campaign name
- `campaign_id` - Unique campaign identifier
- `campaign_type` - Type (Search, Display, Performance Max, Demand Gen, etc.)
- `campaign_status` - Status (Enabled, Paused, Removed)
- `budget` - Daily budget amount
- `bidding_strategy` - Bidding strategy type

### Performance Metrics

- `impressions` - Total impressions
- `clicks` - Total clicks
- `cost` / `spend` - Total spend (in micros or currency units)
- `conversions` - Total conversions
- `conversion_value` - Total conversion value
- `ctr` - Click-through rate (%)
- `avg_cpc` / `average_cpc` - Average cost per click
- `avg_cpm` / `average_cpm` - Average cost per thousand impressions
- `cost_per_conversion` / `cpa` - Cost per acquisition

### Calculated Metrics

- **ROAS** = conversion_value / cost
- **CTR** = (clicks / impressions) × 100
- **Conversion Rate** = (conversions / clicks) × 100

### Ad Group / Asset Group Fields

- `ad_group` / `ad_group_name` - Ad group name
- `ad_group_id` - Unique ad group identifier
- `ad_group_status` - Status
- `max_cpc` - Maximum CPC bid

### Keyword-Level Fields (Search campaigns)

- `keyword` / `keyword_text` - Keyword text
- `match_type` - Match type (Exact, Phrase, Broad)
- `quality_score` - Quality score (1-10)

### Device & Placement

- `device` - Device type (Mobile, Desktop, Tablet)
- `network` - Network (Search, Display, YouTube)
- `placement` - Specific placement URL (for Display)

## XML Structure Examples

### Standard Report Format

```xml
<report>
  <table>
    <row>
      <campaign>Campaign Name</campaign>
      <impressions>10000</impressions>
      <clicks>500</clicks>
      <cost>250000000</cost>
      <conversions>25</conversions>
      <conversion-value>5000</conversion-value>
    </row>
  </table>
</report>
```

### Alternative Format

```xml
<report-data>
  <row campaign="Campaign Name" impressions="10000" clicks="500" cost="250.00" conversions="25" conversion_value="5000.00"/>
</report-data>
```

## Notes

- Cost values may be in micros (divide by 1,000,000 for actual currency)
- Date fields typically in YYYY-MM-DD format
- Percentage fields may be decimals (0.05 = 5%) or whole numbers (5 = 5%)
