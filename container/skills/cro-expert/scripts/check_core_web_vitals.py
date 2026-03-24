#!/usr/bin/env python3
import sys
import requests
import json

def get_psi_results(url, strategy='desktop'):
    # The PageSpeed Insights API is free and doesn't require an API key.
    api_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={strategy}&category=PERFORMANCE'
    try:
        response = requests.get(api_url)
        response.raise_for_status() # Raises an exception for 4XX/5XX errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {url} ({strategy}): {e}", file=sys.stderr)
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python check_core_web_vitals.py <URL>", file=sys.stderr)
        sys.exit(1)

    target_url = sys.argv[1]

    print(f'Running Core Web Vitals audit for: {target_url}')
    print('-' * 50)

    for strategy in ['desktop', 'mobile']:
        print(f'\nAnalyzing {strategy.capitalize()} experience...')
        results = get_psi_results(target_url, strategy)

        if not results:
            continue

        loading_experience = results.get('loadingExperience', {})
        metrics = loading_experience.get('metrics', {})

        lcp = metrics.get('LARGEST_CONTENTFUL_PAINT_MS', {})
        fid = metrics.get('FIRST_INPUT_DELAY_MS', {})
        cls = metrics.get('CUMULATIVE_LAYOUT_SHIFT_SCORE', {})

        lcp_value = lcp.get('percentile', 'N/A')
        fid_value = fid.get('percentile', 'N/A')
        # CLS score is not in ms and is formatted differently
        cls_value = cls.get('percentile', 'N/A')
        if isinstance(cls_value, int):
             cls_value = cls_value / 100.0


        print(f"  - Largest Contentful Paint (LCP): {lcp_value} ms")
        print(f"  - First Input Delay (FID): {fid_value} ms")
        print(f"  - Cumulative Layout Shift (CLS): {cls_value}")

        # Provide context based on Google's thresholds
        print("\n  Recommendations:")
        print("  - LCP should be < 2500 ms (2.5s)")
        print("  - FID should be < 100 ms")
        print("  - CLS should be < 0.1")

if __name__ == '__main__':
    main()
