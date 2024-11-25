import json
import os
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def download_and_merge_files(reporter_id, product_id):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Build the URL dynamically based on parameters
    base_url = "https://www.macmap.org/en/query/results"
    query_url = f"{base_url}?reporter={reporter_id}&partner=699&product={product_id}&level=6"
    print(query_url)
    driver.get(query_url)

    # URLs to download and merge
    target_urls = {
        "https://www.macmap.org/api/results/customduties": "customduties",
        "https://www.macmap.org/api/results/ntm-measures": "ntm-measures",
    }

    
    merged_data = {}
    # Process requests and merge the desired JSON responses
    for request in driver.requests:
        if request.response:
            url = request.url
            for pattern, key in target_urls.items():
                if pattern in url:
                    response_body = request.response.body.decode('utf-8', errors='ignore')
                    print("response body , ",response_body)
                    try:
                        # Parse JSON response and add it to the merged data
                        print("response body ",response_body)
                        response_data = json.loads(response_body)
                        merged_data[key] = response_data
                        print(f"Captured and merged response from {url}")
                    except json.JSONDecodeError:
                        print(f"Non-JSON response from {url}")

    # Save merged data to a single JSON file
    
    output_file = 'merged_data.json'
    print("merged data ", merged_data)
    with open(output_file, 'w',encoding="utf-8") as f:
        json.dump(merged_data, f, indent=4)
    print(f"Merged data saved to {output_file}")

    # Quit the driver
    driver.quit()

# Example usage
# download_and_merge_files(reporter_id="842", product_id="09101100")
# 
def get_country_code(country_name):
    with open('amazon-sambhav/macmap/countries.json', 'r') as file:
        countries_data = json.load(file)
    # Loop through each country in the list
    for country in countries_data:
        if country["Name"].lower() == country_name.lower():
            return country["Code"]
    return None  # Return None if country is not found

