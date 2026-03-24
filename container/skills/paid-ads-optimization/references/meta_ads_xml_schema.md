# Meta Ads XML Export Schema Reference

## Common Report Fields

Meta Ads XML exports typically include these key fields:

### Campaign-Level Metrics

- `campaign_name` / `campaign` - Campaign name
- `campaign_id` - Unique campaign identifier
- `objective` - Campaign objective (CONVERSIONS, TRAFFIC, AWARENESS, etc.)
- `buying_type` - Buying type (AUCTION, RESERVED)
- `status` - Campaign status (ACTIVE, PAUSED, ARCHIVED)
- `daily_budget` / `lifetime_budget` - Budget settings

### Ad Set-Level Metrics

- `ad_set_name` / `adset_name` - Ad set name
- `ad_set_id` - Unique ad set identifier
- `optimization_goal` - Optimization goal (LINK_CLICKS, CONVERSIONS, REACH, etc.)
- `bid_strategy` - Bid strategy (LOWEST_COST_WITHOUT_CAP, COST_CAP, etc.)
- `targeting` - Targeting details (age, gender, location, interests)

### Performance Metrics

- `impressions` - Total impressions
- `reach` - Unique users reached
- `frequency` - Average impressions per user
- `clicks` / `link_clicks` - Total clicks
- `spend` / `amount_spent` - Total spend
- `ctr` / `link_click_through_rate` - Click-through rate (%)
- `cpc` / `cost_per_link_click` - Cost per click
- `cpm` / `cost_per_1000_impressions` - Cost per thousand impressions
- `cpp` / `cost_per_unique_click` - Cost per unique click

### Conversion Metrics

- `conversions` / `actions` - Total conversions
- `conversion_value` / `action_values` - Total conversion value
- `cost_per_conversion` / `cost_per_action` - Cost per conversion
- `roas` / `purchase_roas` - Return on ad spend

### Placement & Device

- `placement` - Placement (Facebook Feed, Instagram Stories, Audience Network, etc.)
- `device_platform` - Device platform (Mobile, Desktop)
- `publisher_platform` - Publisher (Facebook, Instagram, Messenger, Audience Network)

### Creative Metrics

- `ad_name` - Ad creative name
- `ad_id` - Unique ad identifier
- `video_play_actions` - Video plays
- `video_avg_time_watched_actions` - Average video watch time
- `outbound_clicks` - Clicks to external destinations

## Calculated Metrics

- **ROAS** = conversion_value / spend
- **CTR** = (clicks / impressions) × 100
- **Frequency** = impressions / reach
- **Conversion Rate** = (conversions / clicks) × 100
- **CPM** = (spend / impressions) × 1000

## XML Structure Examples

### Standard Format

```xml
<data>
  <campaign>
    <campaign_name>Summer Sale Campaign</campaign_name>
    <campaign_id>123456789</campaign_id>
    <impressions>50000</impressions>
    <reach>35000</reach>
    <frequency>1.43</frequency>
    <clicks>1500</clicks>
    <spend>750.00</spend>
    <conversions>75</conversions>
    <conversion_value>15000.00</conversion_value>
  </campaign>
</data>
```

### Alternative Format

```xml
<report>
  <row>
    <campaign_name>Summer Sale Campaign</campaign_name>
    <impressions>50000</impressions>
    <reach>35000</reach>
    <frequency>1.43</frequency>
    <link_clicks>1500</link_clicks>
    <amount_spent>750.00</amount_spent>
    <purchase>75</purchase>
    <purchase_value>15000.00</purchase_value>
  </row>
</report>
```

## Creative Fatigue Indicators

Monitor these metrics for creative fatigue:

- **Frequency > 2.5–3.5** with declining ROAS
- **CTR drop > 30–40%** after 4–7 days
- **CPM increasing** while CTR decreasing
- **Relevance score declining** (if available)

## Placement Performance

Key placements to monitor:

- **High performers**: Facebook Feed, Instagram Feed, Instagram Stories
- **Monitor closely**: Audience Network (often lower quality)
- **Red flags**: Audience Network Rewarded Video (typically poor ROAS)

## Notes

- Spend values typically in standard currency format
- Frequency = impressions / reach (higher = more ad fatigue risk)
- Action types vary by objective (purchase, lead, add_to_cart, etc.)
- Date fields typically in YYYY-MM-DD format
