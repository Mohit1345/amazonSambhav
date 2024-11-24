
from vector_dbs import save_vcdb
from map import semantic_search
from reader import read_data

import sys
sys.path.append('amazon-sambhav/amazon')
from download_compliance import download_product_compliance_file
sys.path.append('amazon-sambhav/macmap')
from macmap import download_and_merge_files,get_country_code
import os
import json


def get_data_file(data_key,data_value,id_json,country):
        if data_key == "amazon":
            print(id_json["productSubtypes"])
            data_file = download_product_compliance_file(id_json['id'],id_json['productSubtypes'][0]['id'])
        elif data_key=="dgft":
            directory = "amazon-sambhav/dgft/Export Policy - ITC(HS) 2018"
            files = []
            # Iterate over files in the directory
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                files.append(filepath)

            data_file = files[int(id_json['id'])]
        elif data_key == "macmap":
            product_id = id_json['Code']
            country_id = get_country_code(country)
            data_json = download_and_merge_files(country_id,product_id)
            return data_json
        elif data_key=="drawback" or data_key =="rodtep":
            return id_json
        else:
            pass
        return data_file

def process_data(product_name, country):

    with_prompt = {
        "rodtep":"",
        "drawback":""
    }
    # product name mapping with ids of datas (amazon,macmap,dgf)
    mapping_dict = {   
        "amazon":"amazon-sambhav/amazon/productsList.json",
        "dgft":"amazon-sambhav/dgft/extracted_data.json",     
        "macmap":"amazon-sambhav/macmap/products.json",
        "drawback":"amazon-sambhav/drawback/drawback.json",
        "rodtep":"amazon-sambhav/rodtep/rodtep.json"
    }


    for data_key,data_value in mapping_dict.items():
        with open(data_value, "r", encoding="utf-8") as f:
            json_data = json.load(f)  # Parse JSON into a Python dictionary
        
        id_json = semantic_search(json_data,product_name,data_key)

        print(id_json)
        data_file = get_data_file(data_key,data_value,id_json,country)

        no_reading = ['macmap','drawback','rodtep']
        if  data_key not in no_reading:
            pdf_data = read_data(data_file)
        else:
            pdf_data = data_file

        only_prompt = ['drawback','rodtep']
        if data_key not in only_prompt:
            save_vcdb(pdf_data, "universal", metadata={"name":f"{data_key}_{product_name}"},is_table=False,type=data_key)
        else:
            if "rodtep" in data_key:
                with_prompt['drawback'] = pdf_data
            else:
                with_prompt['rodtep'] = pdf_data
    
    return "universal",with_prompt
    


    # scrape and apis (amazon complaince, import compliance from macmap )
    
    # retrieval export compliance from dgf, and dutydrawback, rodtep
    
    # jsonize (amazon_formate,macmap,dfg_formate,duty_drawback, rodtep)
    
    # save to db

    # retrieve data (for each vector db) to create guide

    # will create guides for them with llm or let say (compliance guide,incetives and grants (duty drawback and rodtep), market based analysis and suggestions)
    
    # return {"urls":['guide_links']}
    


# local json file save 
# vector db (object->product_json)


# db savind and retrieval



# process_data("glass","united states of america")