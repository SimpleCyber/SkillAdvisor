import requests
from bs4 import BeautifulSoup
import json
import time

base_url = "https://www.shl.com/products/product-catalog/"
json_data = []
start_values = list(range(0, 200, 12))  # Includes 0 to 132 (inclusive), step 12

headers = {
    "User-Agent": "Mozilla/5.0"
}

for start in start_values:
    url = f"{base_url}?start={start}&type=2"
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

    rows = table.find_all("tr", attrs={"data-course-id": True})
    
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue  # safety check
        
        # Product name and URL
        name_tag = cols[0].find("a")
        product_name = name_tag.text.strip()
        product_url = "https://www.shl.com" + name_tag["href"]

        # Remote Testing (2nd column)
        remote_testing = "yes" if cols[1].find("span", class_="-yes") else "no"

        # Adaptive/IRT (3rd column)
        adaptive_irt = "yes" if cols[2].find("span", class_="-yes") else "no"

        # Test Types (4th column)
        test_types = [span.text.strip() for span in cols[3].find_all("span", class_="product-catalogue__key")]

        json_data.append({
            "name": product_name,
            "url": product_url,
            "remote_testing": remote_testing,
            "adaptive_irt": adaptive_irt,
            "test_types": test_types
        })

    time.sleep(1)  # polite scraping delay

# Save to JSON
with open("shl_products_full.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4)

print("✅ Scraping complete. Data saved to 'shl_products_full.json'")
