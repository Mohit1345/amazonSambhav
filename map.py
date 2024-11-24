import requests
import time
import random

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": "Bearer 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"}
# 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
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


import json
def find_max_similarity_index(query_sentence, sentences):
    time.sleep(random.randint(5, 10))
    output = query({
        "inputs": {
            "source_sentence": query_sentence,
            "sentences": sentences
        },
    })

    try:
        max_similarity_index = output.index(max(output))
    except:
        max_similarity_index = 0
        return max_similarity_index
    # print(len(output))
    

    return max_similarity_index

# query_sentence = "A beautiful blue background"
# sentences = [
#     'hd background',
#     'a blue hd',
#     'a bokeh of blue wallpaper'
# ]

# print(find_max_similarity_index(query_sentence,sentences))


def semantic_search(api_jsons, query2,type):
    final_sentences = []

    if "macmap" in type:
        for obj in api_jsons:
            final_sentences.append(obj['Name'])
    elif "dgft" in type:
        for obj in api_jsons:
            final_sentences.append(obj['name'])
    elif "amazon" in type:
        for obj in api_jsons:
            sentence = obj['name']['localizedStringLookupId']
            products = obj['productSubtypes']
            for pro in products:
                sentence = sentence + " "
                sentence = sentence + pro['name']['localizedStringLookupId']
            final_sentences.append(sentence)
    elif "drawback" in type or "rodtep" in type:
        for obj in api_jsons:
            final_sentences.append(obj['description'])


    if(len(api_jsons)<=0):
        return ""

    try:
        max_similarity_index = find_max_similarity_index(query2, final_sentences)
    except:
        time.sleep(5)
        print("retrying ")
        max_similarity_index = find_max_similarity_index(query2, final_sentences)

    # if "one" in type:
    #     if max_similarity_index>=0 and max_similarity_index<len(api_jsons):
    #         return api_jsons[max_similarity_index]['Code']
    #     try:
    #         return api_jsons[random.randint(0, len(api_jsons)-1)]['Code']
    #     except:
    #         return "empty input"
    # else:
    #     if max_similarity_index>=0 and max_similarity_index<len(api_jsons):
    #         return api_jsons[max_similarity_index]
    #     try:
    #         return api_jsons[random.randint(0, len(api_jsons)-1)]['id']
    #     except:
    #         return "empty input"
    return api_jsons[max_similarity_index]


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
# print(semantic_search(two,"sports","amazon"))