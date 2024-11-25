# import json

# some = """['User: explain about products complaince', 'Bot: The provided text is a disclaimer, not an explanation of product compliance.  It emphasizes that regulations change and that the exporter should seek legal counsel before relying on any information, including this disclaimer.  To explain product compliance, I need more information.  Please specify:\n\n1.  The product(s) you intend to import or export.  Be precise with product descriptions, including materials, intended use, and any relevant certifications (e.g., CE marking, RoHS).\n2.  The country of origin and the destination country.  Different countries have vastly different regulations.\n3.  The quantity and value of the goods being shipped.  This affects customs duties and potential thresholds for simplified procedures or additional paperwork.\n4.  The method of transportation (sea, air, land).  Each mode has specific documentation requirements.\n\nWith this information, I can provide detailed guidance on relevant compliance requirements, including but not limited to:\n\n   Relevant product standards and certifications\n   Customs duties and taxes\n   Import/export licenses or permits\n*   Sanctions and embargoes\n*   Marking and labeling requirements\n*   Safety and environmental regulations\n\n\nWithout these specifics, any advice I provide would be incomplete and potentially misleading.\n']"""

# json_like_str = some.replace("'", '"')

# # Escape backslashes (to handle \n, \t, etc.)
# json_like_str = json_like_str.replace("\\", "\\\\")
# json_like_str = json_like_str.replace("*", " ")

# # Ensure JSON newlines are escaped correctly
# some = some.replace("\n", "\\n")
# # Load the JSON string
# parsed_data = json.loads(some)

# # Print the parsed JSON
# print(parsed_data)

# import ast

# def convert_to_valid_list(py_list_str):
#     """
#     Converts a Python-style list string into a valid Python list.
    
#     Args:
#         py_list_str (str): A string in Python-style list syntax.
    
#     Returns:
#         list: A Python list converted from the string.
#     """
#     try:
#         # Safely evaluate the Python-style list string
#         parsed_data = ast.literal_eval(py_list_str)
#         return parsed_data
#     except (ValueError, SyntaxError) as e:
#         print(f"Error parsing string: {e}")
#         return None

# # Input: Python-style list string
# some = """['User: onion export compliance', 'Bot: To advise you on onion export compliance, I need more information. The provided text mentions Indian regulations (FSSAI, APEDA) and US FDA requirements (for labeling and color additives if applicable), but lacks crucial details. To give you accurate and actionable advice, please specify:\n\n1. **Origin Country:** Where are the onions being exported *from*? Regulations vary significantly by country of origin.\n2. **Destination Country:** Where are the onions being exported *to*? Each country has its import regulations, including phytosanitary requirements (plant health), customs duties, and potentially labeling stipulations.\n3. **Onion Type and Variety:** Specific onion types might have unique compliance requirements.\n4. **Quantity and Packaging:** This impacts transportation and associated documentation.\n5. **Intended Use:** Are these onions for fresh consumption, processing, or another use?\n\nOnce I have this information, I can provide guidance on:\n\n* **Necessary registrations and licenses:** (e.g., APEDA registration in India if exporting from there).\n* **Required documentation:** (e.g., phytosanitary certificates, commercial invoices, packing lists).\n* **Labeling requirements:** (specifics vary by country).\n* **Applicable tariffs and duties:** (destination country-specific).\n* **Potential incentive schemes:** (available in both exporting and importing countries).\n\n\nThe provided links are helpful but only offer general information. Precise compliance depends on the specifics of your export operation.']
# """
# some = some.replace(",","\n")
# # Convert to Python list
# converted_list = convert_to_valid_list(some)

# if converted_list is not None:
#     print("Converted List:", converted_list)
# else:
#     print("Failed to convert to Python list.")

import json

# Load the JSON data from the file
with open('amazon-sambhav/macmap/products.json', 'r') as file:
    data = json.load(file)

# Filter the data to include only objects where the length of the "Code" is exactly 6
filtered_data = [item for item in data if len(item.get('Code', '')) == 6]

# Save the filtered data back to a file
with open('filtered_data.json', 'w') as file:
    json.dump(filtered_data, file, indent=4)

print("Filtered data has been saved to 'filtered_data.json'.")


