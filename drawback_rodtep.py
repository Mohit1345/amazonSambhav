import pdfplumber
import json

# Function to extract the table from all pages of the PDF and process it into JSON
def extract_data_from_pdf(pdf_path):
    # Initialize a list to store JSON objects
    json_data = []

    # Open the PDF using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        # Loop through all pages
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            
            # Extract the table from the page
            table = page.extract_table()

            # Skip the first two rows as they are headers or irrelevant
            if not table:
                continue

            # Process the table, starting from the first data row
            for row in table[3:]:  # Skip header row and first two rows
                if len(row) >= 6 and row[0] is not None:
                    index = row[0].strip() if row[0] else ""
                    tariff_item = row[1].strip() if row[1] else ""
                    description = row[2].strip() if row[2] else ""
                    uqc = row[3].strip() if row[3] else ""
                    rate = row[4].strip() if row[4] else ""
                    cap = row[5].strip() if row[5] else None

                    # Add the extracted data to the list in JSON format
                    json_data.append({
                        "index": index,
                        "tariff_item": tariff_item,
                        "description": description,
                        "uqc": uqc,
                        "rate": rate,
                        "cap": cap
                    })

    return json_data
# Path to your PDF file
pdf_path = "rodtep.pdf"

# Extract data from the PDF and convert to JSON
json_data = extract_data_from_pdf(pdf_path)

# Convert the data to a JSON string with indentation for better readability
json_output = json.dumps(json_data, indent=4)

# Optionally, print the JSON output
print(json_output)

# Save the JSON data to a file
with open("output.json", "w", encoding="utf-8") as f:
    f.write(json_output)
