import requests

def download_product_compliance_file(product_type_id, product_subtype_id):
    # API URL
    api_url = f"https://sellercentral.amazon.in/spec/api/getProductComplianceRequirements?origin=IN&destination=US&productTypeId={product_type_id}&productSubtypeId={product_subtype_id}"
    
    # API Headers
    headers = {
        'Cookie': 'session-id=259-7517328-2360947'
    }
    
    # Make the API request
    response = requests.get(api_url)
    
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        if data and "details" in data[0] and "defaultFilename" in data[0]["details"]:
            file_id = data[0]["details"]["defaultFilename"]
            file_url = f"https://d30e13dxbd9wo.cloudfront.net/{file_id}"
            
            # Download the file
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                # Save the file
                file_name = file_id + ".pdf"
                with open(file_name, "wb") as file:
                    file.write(file_response.content)
                print(f"File downloaded successfully: {file_name}")
                return file_name
            else:
                print(f"Failed to download file from {file_url}. HTTP Status Code: {file_response.status_code}")
        else:
            print("Invalid API response format or missing details.")
    else:
        print(f"API request failed. HTTP Status Code: {response.status_code}, Response: {response.text}")

# Example usage
# download_product_compliance_file(
#     product_type_id="ca99cae2-c9ed-45e0-93de-24ca0b9db62d",
#     product_subtype_id="b017f29e-9156-4e23-961e-0333baddf6eb"
# )

#  headers=headers