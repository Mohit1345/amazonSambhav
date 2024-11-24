import json

with open('productsListDemo.json', 'r') as input_file:
    original_data = json.load(input_file)

converted_data = []
for product in original_data:
    item = {
        "Type": product["name"]["defaultString"],
        "Subtypes": [subtype["name"]["defaultString"] for subtype in product["productSubtypes"]]
    }
    converted_data.append(item)

with open('productsListDemo2.json', 'w') as output_file:
    json.dump(converted_data, output_file, indent=4)

print("Data conversion successful!")
