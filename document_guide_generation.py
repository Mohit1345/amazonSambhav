from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
import google.generativeai as genai
import ast
genai.configure(api_key="AIzaSyC6SoO4TZWYmWvHa66f04osFHrEjsavjuY")

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import re
import json
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY2")

def upload_pdf_to_cloudinary(file_path):
    # Configure Cloudinary
    cloudinary.config(
        cloud_name="dde4uttp5",  # Replace with your Cloudinary cloud name
        api_key="176797228913411",        # Replace with your Cloudinary API key
        api_secret="w4M7UhrIOUmixDMpt_2LKMfX_ys",  # Replace with your Cloudinary API secret
    )

    try:
        response = cloudinary.uploader.upload(
            file_path,
            resource_type="raw",  # Specify raw to upload non-image files
            folder="pdf_uploads"  # Optional folder to organize files
        )
        # Return the secure URL of the uploaded file
        return response.get("secure_url", "Upload failed. No URL returned.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_context(prompt, vector_db_name="universal"):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY2"))
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    print("connecting vector db")
    try:
        vectorstore = Chroma(persist_directory=vector_db_name, embedding_function=embeddings)
    except FileNotFoundError:
        raise ValueError(f"Vector database '{vector_db_name}' does not exist.")
    print("vector db connected")
    results = vectorstore.similarity_search(prompt, k=1)  # Retrieve top 5 matches
    retrieved_data = [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]

    metadata = []
    context  = ""
    for data in retrieved_data:
        context += data['content'] + "\n"
        metadata.append(data['metadata'])

    print("metadata: ",metadata)
    print("Retrieved data:", retrieved_data)
    if retrieved_data==[]:
        return "No Information Available"
    
    return retrieved_data


def create_pdf(filename, head_json, sections_json):
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add Header Section
    if 'heading' in head_json:
        header_title = Paragraph(head_json['heading'], styles['Title'])
        story.append(header_title)
        story.append(Spacer(1, 12))

    if 'scope' in head_json:
        header_scope = Paragraph(head_json['scope'], styles['BodyText'])
        story.append(header_scope)
        story.append(Spacer(1, 24))

    # Add Sections
    for section in sections_json:
        if not section:  # Skip empty sections
            continue

        # Skip sections where Benefits contains "information not available"
        if 'Benefits' in section and "information not available" in section['Benefits']:
            continue

        # Add Section Title
        if 'title' in section:
            section_title = Paragraph(section['title'], styles['Heading1'])
            story.append(section_title)
            story.append(Spacer(1, 12))

        # Add Section Introduction
        if 'introduction' in section:
            introduction = Paragraph(section['introduction'], styles['BodyText'])
            story.append(introduction)
            story.append(Spacer(1, 12))

        # Add Benefits if available
        if 'Benefits' in section and section['Benefits']:
            story.append(Paragraph("Benefits:", styles['Heading2']))
            bullet_points = ListFlowable(
                [ListItem(Paragraph(point.strip(), styles['BodyText'])) for point in section['Benefits']],
                bulletType='bullet'
            )
            story.append(bullet_points)
            story.append(Spacer(1, 24))

        # Add Mandatory Requirements if available
        if 'Mandatory Requirements' in section:
            mandatory_requirements = section['Mandatory Requirements']
            if mandatory_requirements and mandatory_requirements != ["information not available"]:
                story.append(Paragraph("Mandatory Requirements:", styles['Heading2']))
                for i, requirement in enumerate(mandatory_requirements, start=1):
                    story.append(Paragraph(f"{i}. {requirement}", styles['BodyText']))
                story.append(Spacer(1, 12))

        # Add Recommended Requirements if available
        if 'Recommended Requirements' in section:
            recommended_requirements = section['Recommended Requirements']
            if recommended_requirements and recommended_requirements != ["information not available"]:
                story.append(Paragraph("Recommended Requirements:", styles['Heading2']))
                for i, requirement in enumerate(recommended_requirements, start=1):
                    story.append(Paragraph(f"{i}. {requirement}", styles['BodyText']))
                story.append(Spacer(1, 12))

        # Add Other Important Check Points if available
        if 'Other important check points' in section:
            other_check_points = section['Other important check points']
            if other_check_points:
                story.append(Paragraph("Other Important Check Points:", styles['Heading2']))
                bullet_points = ListFlowable(
                    [ListItem(Paragraph(point.strip(), styles['BodyText'])) for point in other_check_points],
                    bulletType='bullet'
                )
                story.append(bullet_points)
                story.append(Spacer(1, 12))

    # Build the PDF
    pdf.build(story)


def get_export_compliance_context(product_name):
    export_compliance_prompts = {
        "amazon_products_info": (
            f"Please provide the complete compliance requirements for exporting {product_name} in USA, "
            "including specific documentation, labeling requirements, any relevant FAQs, and references to Amazon's policies."
        ),
        "macmap_information": (
            f"Can you provide a detailed overview of the import compliance requirements for {product_name} when exporting to "
            "Europe and the USA, including necessary documentation, regulations, and any relevant certifications or permits?"
        ),
        "dgft_information": (
            f"What are the comprehensive export compliance requirements for {product_name} according to Indian government regulations? "
            "Please include necessary documents, procedures, and a summary of the key steps for obtaining export clearance under DGFT guidelines."
        ),
        "duty_drawbacks_information": (
            f"Please outline the duty drawback provisions applicable to {product_name}, including detailed eligibility criteria, "
            "application processes, and any available incentives for the export of this product along with necessary documentation."
        ),
        "rodtep_information": (
            f"What are the guidelines for claiming RoDTEP incentives for {product_name}? Include detailed eligibility criteria, "
            "application procedures, and any important deadlines or requirements related to the RoDTEP scheme for this product."
        ),
        "shipping paymentReconcillation and tax information": (
            f"What are the standard documents required for the export of {product_name}? Include a checklist of necessary documents, "
            "information on Amazon shipping requirements, and details regarding payment reconciliation for international transactions."
        )
    }

    # Initialize an empty dictionary to store the context for each query
    context_results = {}

    # Loop through the prompts and extract context using get_context function
    for key, query in export_compliance_prompts.items():
        context_results[key] = get_context(query)

    return context_results


def extract_json(s):
    pattern = r'```json(.*?)```'
    match = re.search(pattern, s, re.DOTALL)
    if match:
        return json.loads(match.group(1).strip())
    return None


def generate_checkpoint_section(section_name, product_name, context):
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY2")


    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction = """
You are an assistant designed to generate content for a procedural document that outlines the import/export process for {}, focusing on compliance and incentives. Your responses will be used to automate the creation of a PDF document.

For each section, please return the information in the following structured format:
{{
    "title": "[Title of the Section]",
    "introduction": "[Brief introduction explaining the importance of the section.]",
    "Mandatory Requirements": "[list of mandatory requirements (Keep Empty if not present in context, write  ['information not available'] instead)]",
    "Recommended Requirements": "[list of recommended requirements (Keep Empty if not present in context, write ['information not available'] instead)]",
    "Other important check points": [
        "[Checkpoint 1]",
        "[Checkpoint 2]",
        "[Checkpoint 3]"
    ]
}}

If any of the required information in the format is not present in the context, please write ['information not available'] for that section.

Don't use ** or any markdown element in the response.
Please ensure that the language is clear and professional, suitable for a formal document aimed at exporters and compliance officers. Your goal is to provide comprehensive and actionable information that can be easily translated into a PDF format.
Return the output in json format enclosed in ```json ``` 
""".format(product_name)
    )

    prompt = f'''Using the following context, please provide a detailed response on the {section_name}.'''

    user_prompt = f"User: {prompt}\n Context:{context}\n Answer: "
    response = model.generate_content(user_prompt)

    # print(response.text)
    return extract_json(response.text)


def extract_references(context):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction = (
            "Your task is to extract the reference links in the given input context"
            "Return a list of all the reference links present in the context provided!"
            "Output a python list without any other information. Dont enclose the output in anything like ```list ``` or anything. Just return poure python list. "
        )
    )

    prompt = f'''Context: {context} \n Answer:?'''
    response = model.generate_content(prompt)
    links = ast.literal_eval(response.text)

    return links


def generate_informative_sections(section_name, product_name, context):
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY2")
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction = """
You are an assistant designed to generate content for a procedural document that outlines the import/export process for {}, focusing on compliance and incentives. Your responses will be used to automate the creation of a PDF document.

For each section, please return the information in the following structured format:

{{
    "title": "[Title of the Section]",
    "introduction": "[very short introduction explaining the importance of the section.]",
    "Benefits": [
        "list of benefit points"
    ]
}}

Dont use ** or any markdown element in the response.
Please ensure that the language is clear and professional, suitable for a formal document aimed at exporters and compliance officers. Your goal is to provide comprehensive and actionable information that can be easily translated into a PDF format.
If any benefits are not available in given context, then write ["information not available"] in Benefits.
Return a empty json if context is not available.
Return the output in json format enclosed in ```json ``` 
""".format(product_name)
    )

    prompt = f'''Using the following context, please provide a detailed response for the section {section_name}.'''

    user_prompt = f"User: {prompt}\n Context:{context}\n Answer: "
    response = model.generate_content(user_prompt)

    # print(response.text)
    return extract_json(response.text)

def heading_information_generation(product_name, context_information_dict):
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY2")
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction = """
Given name of the product and information used for creating document.
Your task is to generate a headline and scope for a document related to product's import export compliance,  benefits and incentives.
Document contains following points: 
Amazon Product Compliance
Import Compliance
Export Compliance
Taxation and Incentives
Duty Drawbacks
RodTep Benefits

Output should be in following format:
{
    "heading": "Main headline of the document",
    "scope":"Write a introduction for complete document. Dont mentino about the subpoints in the document."
}

Dont use ** or any markdown element in the response. Strictly dont use ** in your response or any markdown.
Please ensure that the language is clear and professional, suitable for a formal document aimed at exporters and compliance officers. Your goal is to provide comprehensive and actionable information that can be easily translated into a PDF format.
Return the output in json format enclosed in ```json ``` 
"""
    )

    prompt = f'''Product Name: {product_name}\n Context Information: {context_information_dict}'''

    response = model.generate_content(prompt)

    json_info = extract_json(response.text)
    print(type(json_info))
    print(json_info)
    return json_info


def create_guide_document(product_name):
    context_information_dict = get_export_compliance_context(product_name)
    compliance_category_mapping = {
    'Amazon Product Compliance': 'amazon_products_info',
    'Import Compliance': 'macmap_information',
    'Export Compliance': 'dgft_information',
    'Duty Drawbacks': 'duty_drawbacks_information',
    'RodTep Benefits': 'rodtep_information',
    'Taxation and Incentives': 'shipping paymentReconcillation and tax information'
}
    checklist_sections = ["Amazon Product Compliance", "Import Compliance", "Export Compliance"]
    informative_sections = ["Taxation and Incentives", "Duty Drawbacks", "RodTep Benefits"]
    all_sections = []

    for checkpoint in checklist_sections:
        key = compliance_category_mapping.get(checkpoint)
        context = context_information_dict.get(key, ["Context Not Available"])
        all_sections.append(generate_checkpoint_section(checkpoint, product_name, context))
    
    for informative in informative_sections:
        key = compliance_category_mapping.get(informative)
        context = context_information_dict.get(key, ["Context Not Available"])
        all_sections.append(generate_informative_sections(informative, product_name, context))

    head_json = heading_information_generation(product_name, context_information_dict)
    print(all_sections)
    file_name = f"{product_name}_compliance_guide_documentation.pdf"
    create_pdf(file_name, head_json, all_sections)
    return file_name


create_guide_document("Notebooks")
# print(type(heading_information_generation("Mens T shirts", {})))

# print(upload_pdf_to_cloudinary("C:\\Users\\hp\\Desktop\\Sambhav Hackathon\\Apparel- Adults_Men or Women Accessories (1).pdf"))
