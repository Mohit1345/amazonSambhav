# create a dictionary of duty drawback product,and values

# duty drawback (incetives and grants)
# dgft export secton (export compliance)

# rodtep - maintain a table there can be over writing like updation of percetentages or adding of new products

# for dgft


# import os
# import json
# with open("amazon-sambhav\\dgft\\extracted_data.json","r",encoding="utf-8") as f:
#     json_data = json.load(f)

# print(json_data)

# # Specify the directory path
# directory = "amazon-sambhav/dgft/Export Policy - ITC(HS) 2018"

# files = []

# # Iterate over files in the directory
# for filename in os.listdir(directory):
#     filepath = os.path.join(directory, filename)
#     # Check if it's a file
#     files.append(filepath)
#     if os.path.isfile(filepath):
#         print(f"File: {filename}")

# from vector_dbs import save_vcdb
# from reader import read_data
# print("files contain, ",files)


# for file, name_json in zip(files, json_data.values()):
#     one, two = read_data("","first")
#     save_vcdb(one, "dgft", metadata={"name":name_json['name']},is_table=False)

import os
import json
from vector_dbs import save_vcdb
from reader import read_data

# Read and parse JSON data
with open("amazon-sambhav\\dgft\\extracted_data.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)  # Parse JSON into a Python dictionary

print("Parsed JSON data:", json_data)

# Specify the directory path
directory = "amazon-sambhav/dgft/Export Policy - ITC(HS) 2018"

# Collect all valid file paths
files = [os.path.join(directory, filename) for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]
print("Files:", files)

# Ensure the number of files matches the JSON entries
if len(files) != len(json_data):
    print("Warning: Number of files and JSON entries do not match!")

# Iterate over files and JSON values
for file, name_json in zip(files, json_data):
    print(f"Processing file: {file}, JSON metadata: {name_json}")
    one, two = read_data(file, "first")  # Assuming file is the input for read_data
    save_vcdb(one, "dgft", metadata={"name": name_json['name']}, is_table=False)
