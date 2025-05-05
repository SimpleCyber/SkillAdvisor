import json
import requests
from bs4 import BeautifulSoup

# Load the original JSON
with open('individual.json', 'r') as f:
    data = json.load(f)

output_data = []

for index, item in enumerate(data):
    url = item.get("url", "")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data from HTML
        def extract_text_by_heading(soup, heading_text):
            tag = soup.find('h4', string=heading_text)
            if tag:
                p = tag.find_next_sibling('p')
                return p.get_text(strip=True) if p else "NA"
            return "NA"

        description = extract_text_by_heading(soup, "Description")
        job_level = extract_text_by_heading(soup, "Job levels")
        language = extract_text_by_heading(soup, "Languages")
        assessment_length = extract_text_by_heading(soup, "Assessment length")

    except Exception as e:
        print(f"Failed to process URL: {url}, Error: {str(e)}")
        description = job_level = language = assessment_length = "NA"

    output_data.append({
        "name": item.get("name", "NA"),
        "url": url,
        "remote_testing": item.get("remote_testing", "NA"),
        "adaptive_irt": item.get("adaptive_irt", "NA"),
        "test_types": item.get("test_types", []),
        "description": description,
        "job_level": job_level,
        "assessment_length": assessment_length,
        "language": language
    })

    print(f"{index + 1} done")

# Save the output to a new JSON file
with open('individual2.json', 'w') as f:
    json.dump(output_data, f, indent=4)

print("Scraping complete. Data saved to individual2.json.")
