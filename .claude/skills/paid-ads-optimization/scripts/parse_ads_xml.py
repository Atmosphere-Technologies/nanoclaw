#!/usr/bin/env python3
"""
Parse XML exports from Google Ads and Meta Ads to extract campaign performance metrics.

Usage:
    python parse_ads_xml.py <input_xml_file> [--output <output_json_file>]

Outputs structured JSON with key metrics for analysis.
"""

import xml.etree.ElementTree as ET
import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any


def parse_google_ads_xml(xml_file: str) -> Dict[str, Any]:
    """Parse Google Ads XML export."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    campaigns = []
    
    # Google Ads XML structure varies, this handles common report formats
    for row in root.findall('.//row') or root.findall('.//table/row'):
        campaign_data = {}
        for attr in row:
            tag = attr.tag.replace('-', '_').lower()
            campaign_data[tag] = attr.text
        
        if campaign_data:
            campaigns.append(campaign_data)
    
    return {
        'platform': 'Google Ads',
        'total_campaigns': len(campaigns),
        'campaigns': campaigns
    }


def parse_meta_ads_xml(xml_file: str) -> Dict[str, Any]:
    """Parse Meta Ads XML export."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    campaigns = []
    
    # Meta Ads XML structure
    for campaign in root.findall('.//campaign') or root.findall('.//row'):
        campaign_data = {}
        for child in campaign:
            tag = child.tag.replace('-', '_').lower()
            campaign_data[tag] = child.text
        
        if campaign_data:
            campaigns.append(campaign_data)
    
    return {
        'platform': 'Meta Ads',
        'total_campaigns': len(campaigns),
        'campaigns': campaigns
    }


def detect_platform(xml_file: str) -> str:
    """Detect whether XML is from Google Ads or Meta Ads."""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Check root tag and common elements
        root_tag = root.tag.lower()
        xml_content = ET.tostring(root, encoding='unicode').lower()
        
        if 'google' in root_tag or 'adwords' in xml_content or 'google-ads' in xml_content:
            return 'google'
        elif 'facebook' in xml_content or 'meta' in xml_content or 'instagram' in xml_content:
            return 'meta'
        else:
            # Generic fallback
            return 'unknown'
    except Exception as e:
        print(f"Error detecting platform: {e}", file=sys.stderr)
        return 'unknown'


def parse_xml_file(xml_file: str) -> Dict[str, Any]:
    """Parse XML file and return structured data."""
    platform = detect_platform(xml_file)
    
    if platform == 'google':
        return parse_google_ads_xml(xml_file)
    elif platform == 'meta':
        return parse_meta_ads_xml(xml_file)
    else:
        # Generic parser for unknown formats
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        data = []
        for elem in root.iter():
            if elem.text and elem.text.strip():
                data.append({
                    'tag': elem.tag,
                    'text': elem.text.strip(),
                    'attrib': elem.attrib
                })
        
        return {
            'platform': 'Unknown (generic parse)',
            'total_elements': len(data),
            'data': data
        }


def main():
    parser = argparse.ArgumentParser(description='Parse Google Ads or Meta Ads XML exports')
    parser.add_argument('input_file', help='Path to XML file')
    parser.add_argument('--output', '-o', help='Output JSON file (optional, prints to stdout if not specified)')
    
    args = parser.parse_args()
    
    if not Path(args.input_file).exists():
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        result = parse_xml_file(args.input_file)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"✅ Parsed data saved to: {args.output}")
        else:
            print(json.dumps(result, indent=2))
    
    except Exception as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
