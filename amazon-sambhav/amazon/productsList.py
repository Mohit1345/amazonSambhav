import requests
import json

url = 'https://sellercentral.amazon.in/spec/api/getProductTypesWithSubtypes?origin=IN&destination=US'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    with open('product_types_with_subtypes.json', 'w') as file:
        json.dump(data, file, indent=4)
    print("Data saved successfully!")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")