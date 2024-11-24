import requests
import json
import os

# Create the downloads directory
downloads_dir = 'downloads'
os.makedirs(downloads_dir, exist_ok=True)

# Base URLs and headers for the API requests
url1 = "https://www.dgft.gov.in/CP/webHP?requestType=ApplicationRH&screenId=90000802&actionVal=getChapterDetails&_csrf=7dfdaab0-72ea-4cc7-ac24-f00ede4cf9bb"
url2 = "https://www.dgft.gov.in/CP/webHP?requestType=ApplicationRH&actionVal=listner&print=true&moduleName=90000802&screenId=9000012349&dataSubmission=&mpgId=34&_csrf=5796419c-e09c-484d-b29e-93f81ea28793"
headers1 = {
    'Cookie': 'AWSALB=DYd95NLIIqshFP4g/pfPwqO/xH8H5O9M9UI48D2FfHBHn22jYQQQhcOyE+hwm8mkKthxhFNolwH/akbLXG8NqS6x5x8uiIK+JiaP3CEIq6SRtOXKxA0G2bPBmW+P; AWSALBCORS=DYd95NLIIqshFP4g/pfPwqO/xH8H5O9M9UI48D2FfHBHn22jYQQQhcOyE+hwm8mkKthxhFNolwH/akbLXG8NqS6x5x8uiIK+JiaP3CEIq6SRtOXKxA0G2bPBmW+P'
}
headers2 = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Iterate over itcCode values
for i in range(78, 100):
    itcCode = f"{i:02}"  # Format as two-digit number
    print(f"Processing itcCode: {itcCode}")

    # Step 1: Fetch the summary.json data
    payload1 = {
        'itcCode': itcCode,
        'expType': '2'
    }
    response1 = requests.post(url1, headers=headers1, data=payload1)

    if response1.status_code == 200:
        try:
            summaryjson_data = response1.json()  # Assuming the response is JSON
        except json.JSONDecodeError:
            print(f"Failed to decode JSON for itcCode {itcCode}. Skipping.")
            continue
    else:
        print(f"First request failed for itcCode {itcCode} with status code: {response1.status_code}")
        continue

    # Step 2: Use the fetched summary.json data in the second API request
    formdata = {
        "summaryjson": json.dumps(summaryjson_data)
    }
    response2 = requests.post(url2, data=formdata, headers=headers2)

    if response2.status_code == 200:
        # Extract PDF content from the second response
        script_content = response2.text
        start = script_content.find("var bytes = new Uint8Array([") + len("var bytes = new Uint8Array([")
        end = script_content.find("]);", start)
        byte_array = script_content[start:end].strip().split(',')
        byte_array = [int(byte.strip()) for byte in byte_array]
        byte_array = [(byte % 256) for byte in byte_array]
        pdf_data = bytes(byte_array)

        # Save PDF to the downloads folder
        pdf_filename = f"{i}.pdf"
        pdf_path = os.path.join(downloads_dir, pdf_filename)

        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(pdf_data)
        
        print(f"PDF for itcCode {itcCode} downloaded successfully and saved as {pdf_filename}")
    else:
        print(f"Second request failed for itcCode {itcCode} with status code: {response2.status_code}")
