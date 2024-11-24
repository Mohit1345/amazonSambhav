import requests
import time
import random


import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from dotenv import load_dotenv

load_dotenv()

def match_gemini(data_json,prompt):
    print("in gemini")

    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    # Create the model
    generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_schema": content.Schema(
    type = content.Type.OBJECT,
    properties = {
      "response": content.Schema(
        type = content.Type.INTEGER,
      ),
    },
  ),
  "response_mime_type": "application/json",
}

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
    ]
    )
    final_prompt = f"Return most relevant type index from given array of types {data_json}, for query {prompt}"
    print(final_prompt)
    response = chat_session.send_message(final_prompt)
    print("response we got is ", response.text)
    result = response.text
    if isinstance(result, str):
            import json
            try:
                result = json.loads(result)  # Convert JSON string to dictionary
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                raise

    # Access the 'response' key safely
    if 'response' not in result:
        raise KeyError("'response' key not found in the result")
    
    return result['response']
        


# query_sentence = "A beautiful blue background"
# sentences = [
#     'hd background',
#     'a blue hd',
#     'a bokeh of blue wallpaper'
# ]

# print(find_max_similarity_index(query_sentence,sentences))


def semantic_search(api_jsons, query2,type):
    final_sentences = []

    if "one" in type:
        for obj in api_jsons:
            final_sentences.append(obj['Name'])
    elif "dgft" in type:
        for obj in api_jsons:
            final_sentences.append(obj['name'])
    else:
        for obj in api_jsons:
            sentence = obj['name']['localizedStringLookupId']
            products = obj['productSubtypes']
            for pro in products:
                sentence = sentence + " "
                print("dfg", pro['name']['localizedStringLookupId'])
                sentence = sentence + pro['name']['localizedStringLookupId']
            final_sentences.append(sentence)


    if(len(api_jsons)<=0):
        return ""

        
    max_similarity_index = match_gemini(query2, final_sentences)

    if "one" in type:
        if max_similarity_index>=0 and max_similarity_index<len(api_jsons):
            return api_jsons[max_similarity_index]['Code']
        try:
            return api_jsons[random.randint(0, len(api_jsons)-1)]['Code']
        except:
            return "empty input"
    else:
        if max_similarity_index>=0 and max_similarity_index<len(api_jsons):
            return api_jsons[max_similarity_index]
        try:
            return api_jsons[random.randint(0, len(api_jsons)-1)]['id']
        except:
            return "empty input"


one = [
    {
        "Code": "I",
        "Name": "Live animals; animal products",
        "ParentCode": None
    },
    {
        "Code": "01",
        "Name": "Live animals",
        "ParentCode": "I"
    }
]

two = [
    {
        "id": "b12f0366-7a10-4055-b155-c53f3652c116",
        "name": {
            "localizedStringLookupId": "Sports- Basketball",
            "defaultString": "Sports- Basketball"
        },
        "originId": "d35c2f73-bb27-4ba5-b1e7-ff746ada95d5",
        "destinationId": "e1829d7c-2880-4121-ae35-3ec149a0cca9",
        "productSubtypes": [
            {
                "id": "819a8a6e-780a-4951-99d5-fa1b0d2d3172",
                "name": {
                    "localizedStringLookupId": "Basketball-Fangear - Equipment",
                    "defaultString": "Basketball-Fangear - Equipment"
                }
            },
            {
                "id": "e2653382-ba01-4013-9843-85a34dd72172",
                "name": {
                    "localizedStringLookupId": "Basketball-Systems",
                    "defaultString": "Basketball-Systems"
                }
            }
        ]
    },
    {
        "id": "90e84a9b-5b3e-4dfb-8ac3-57271c1e8bcf",
        "name": {
            "localizedStringLookupId": "Home- Lawn & Garden",
            "defaultString": "Home- Lawn & Garden"
        },
        "originId": "d35c2f73-bb27-4ba5-b1e7-ff746ada95d5",
        "destinationId": "e1829d7c-2880-4121-ae35-3ec149a0cca9",
        "productSubtypes": [
            {
                "id": "422d3727-2022-4991-a615-1b03698b8b5d",
                "name": {
                    "localizedStringLookupId": "Gardening",
                    "defaultString": "Gardening"
                }
            }
        ]
    }
]

import json
# with open("amazon-sambhav\\dgft\\extracted_data.json", "r", encoding="utf-8") as f:
#     json_data = json.load(f)  # Parse JSON into a Python dictionary
# print(semantic_search(json_data,"zinc","dgft"))