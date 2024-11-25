import json
import os
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get("https://www.macmap.org/en//query/results?reporter=842&partner=699&product=02044100&level=6")

url_to_filename = {
    "https://www.macmap.org/api/v2/ntlc-products": "ntlc-products.json",
    "https://www.macmap.org/api/results/customduties": "customduties.json",
    "https://www.macmap.org/api/results/ntm-measures": "ntm-measures.json",
    "https://www.macmap.org/api/results/traderemedy": "traderemedy.json",
    "https://www.macmap.org/api/results/taxes": "taxes.json",
}

downloads_dir = 'sample'
os.makedirs(downloads_dir, exist_ok=True)

for request in driver.requests:
    if request.response:
        url = request.url
        for pattern, filename in url_to_filename.items():
            if pattern in url:
                response_body = request.response.body.decode('utf-8', errors='ignore')

                try:
                    response_data = json.loads(response_body)
                    file_path = os.path.join(downloads_dir, filename)
                    with open(file_path, 'w') as f:
                        json.dump(response_data, f, indent=4)
                    print(f"Captured response from {url} and saved to {file_path}")
                except json.JSONDecodeError:
                    print(f"Non-JSON response from {url}")

driver.quit()