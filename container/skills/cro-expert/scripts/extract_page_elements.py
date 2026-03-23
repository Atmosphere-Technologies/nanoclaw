#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup

def extract_elements(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        results = {
            "url": url,
            "title": soup.title.string.strip() if soup.title else "N/A",
            "h1": [h1.get_text(strip=True) for h1 in soup.find_all('h1')],
            "h2": [h2.get_text(strip=True) for h2 in soup.find_all('h2')],
            "ctas": [],
            "forms": []
        }

        # Extract CTAs from buttons and links
        for button in soup.find_all('button'):
            results["ctas"].append(button.get_text(strip=True))
        for a in soup.find_all('a'):
            # Filter out non-CTA links
            link_text = a.get_text(strip=True)
            if len(link_text.split()) < 5 and len(link_text) > 3: # Simple heuristic for CTA-like links
                 results["ctas"].append(link_text)

        # Extract Form details
        for form in soup.find_all('form'):
            form_details = {
                "id": form.get("id", "N/A"),
                "action": form.get("action", "N/A"),
                "inputs": []
            }
            for input_tag in form.find_all(['input', 'textarea', 'select']):
                form_details["inputs"].append({
                    "type": input_tag.get("type", input_tag.name),
                    "name": input_tag.get("name", "N/A"),
                    "placeholder": input_tag.get("placeholder", "N/A")
                })
            results["forms"].append(form_details)

        return results

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or parsing URL {url}: {e}", file=sys.stderr)
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_page_elements.py <URL>", file=sys.stderr)
        sys.exit(1)

    target_url = sys.argv[1]
    elements = extract_elements(target_url)

    if elements:
        print("--- Key Page Element Extraction ---")
        print(f"URL: {elements['url']}")
        print(f"Title: {elements['title']}\n")
        print(f"H1 Headlines: {elements['h1']}\n")
        print(f"H2 Sub-Headlines: {elements['h2']}\n")
        print(f"Potential CTAs (Buttons & Links): {list(set(elements['ctas']))}\n") # Deduplicate for clarity
        print("Forms Found:")
        for i, form in enumerate(elements["forms"]):
            print(f"  - Form #{i+1}: id='{form['id']}', action='{form['action']}'")
            for input_field in form["inputs"]:
                print(f"    - Input: name='{input_field['name']}', type='{input_field['type']}', placeholder='{input_field['placeholder']}'")
        print("------------------------------------")

if __name__ == '__main__':
    main()
