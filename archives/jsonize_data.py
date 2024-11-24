# Compliance
## Exports -> DGF
## Amazon Compliance
## Imports -> MacMap
# Tarif -> Macpmap, duty drawback and RoDTep

from gemini import llm
from google.ai.generativelanguage_v1beta.types import content
from reader import read_compliance

def save_to_db(data,collection):
    pass


# types can be amazon json style, detect standard docuemnt, DGF json 

def get_existing_doc():
    pass

def create_std_doc_json(file_data):
    prompt = "extract and save this given data into structured json"
    context = file_data
    strcutrued_std_json = llm(prompt, context, schema=None)
    strcutrued_std_json['std_name'] = ""
    save_to_db(strcutrued_std_json,"standard_coll")

def check_standard_doc(file):
    existing_docs = get_existing_doc()
    if file not in existing_docs:
        create_std_doc_json(file)
    
# Compliance

def amazon_json(file_data,product_type):
    prompt = "extract and save this given data into structured json"
    amazon_schema = content.Schema(
    type = content.Type.OBJECT,
    properties = {
      "mandatory_requriements": content.Schema(
        type = content.Type.ARRAY,
        items = content.Schema(
          type = content.Type.STRING,
        ),
      ),
      "recommended_requirements": content.Schema(
        type = content.Type.ARRAY,
        items = content.Schema(
          type = content.Type.STRING,
        ),
      ),
      "applicable_to": content.Schema(
        type = content.Type.STRING,
      ),
      "faqs": content.Schema(
        type = content.Type.ARRAY,
        items = content.Schema(
          type = content.Type.STRING,
        ),
      ),
      "references": content.Schema(
        type = content.Type.ARRAY,
        items = content.Schema(
          type = content.Type.STRING,
        ),
      ),
      "misc": content.Schema(
        type = content.Type.STRING,
      ),
    },
  )
    context = file_data
    strcutrued_amazon_json = llm(prompt, context,amazon_schema)
    strcutrued_amazon_json['product_type'] = product_type
    save_to_db(strcutrued_amazon_json,"product_json")


