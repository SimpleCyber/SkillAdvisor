import requests
from bs4 import BeautifulSoup
import json
import time

base_url = "https://www.shl.com/products/product-catalog/"
json_data = []
start_values = list(range(0, 372, 12))  # Paginated steps

headers = {
    "User-Agent": "Mozilla/5.0"
}

for start in start_values:
    url = f"{base_url}?start={start}&type=1"
    print(f"Scraping: {url}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to retrieve page {start}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("div", class_="custom__table-responsive")

    if not table:
        print(f"⚠️ No table found on page {start}")
        continue

    rows = table.find_all("tr", attrs={"data-entity-id": True})
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        # Product name and URL
        a_tag = cols[0].find("a")
        if not a_tag:
            continue
        product_name = a_tag.text.strip()
        product_url = "https://www.shl.com" + a_tag["href"]

        # Remote Testing
        remote_testing = "yes" if cols[1].find("span", class_="-yes") else "no"

        # Adaptive/IRT
        adaptive_irt = "yes" if cols[2].find("span", class_="-yes") else "no"

        # Test Types
        test_types = [
            span.text.strip()
            for span in cols[3].find_all("span", class_="product-catalogue__key")
        ]

        json_data.append({
            "name": product_name,
            "url": product_url,
            "remote_testing": remote_testing,
            "adaptive_irt": adaptive_irt,
            "test_types": test_types
        })

    time.sleep(1)  # Be polite with the server

# Save data to JSON file
with open("type1_detailed_products.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4)

print("✅ Scraping complete. Data saved to 'type1_detailed_products.json'")
