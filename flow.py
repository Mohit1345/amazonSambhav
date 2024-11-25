# user will put his product name , import country name

# will check if product data already exist in db or not
# then will rereive that products export, amazon, import complaince data from amazon , dgft and macmap
# once data is there will structure it save it in db
# but if data is already there then will serve that

from flask import Flask, request, jsonify
from back import process_data
import google.generativeai as genai
genai.configure(api_key="API_KEY")
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import re

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem

from document_guide_generation import create_guide_document, upload_pdf_to_cloudinary

from flask_cors import CORS
import json
import os
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 
# Sample storage for products and related data (in-memory for simplicity)
products = {}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction = (
    "You are an expert in international trade compliance, import/export requirements, and incentive schemes. "
    "Your task is to guide the user in importing or exporting products to specific countries. "
    "Using the provided context from a vector database, respond with clear, accurate, and actionable advice tailored to the user's query.\n\n"
    "Guidelines:\n"
    "- Focus your response on the compliance requirements, regulations, and schemes relevant to the query and context provided.\n"
    "- Ensure your guidance is concise, professional, and easy to understand.\n"
    "- If the context lacks sufficient information, state what is missing and suggest additional details the user could provide.\n"
    "- If the user provides sensitive or irrelevant content, respond with: 'Please ask relevant questions related to international trade compliance and regulations.'\n"
    "Don't include any markdown-related notation or syntax such as ** or / or any other; just return a pure string."
)

)

def get_context(prompt, vector_db_name="universal"):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    print("connecting vector db")
    try:
        vectorstore = Chroma(persist_directory=vector_db_name, embedding_function=embeddings)
    except FileNotFoundError:
        raise ValueError(f"Vector database '{vector_db_name}' does not exist.")
    print("vector db connected")
    results = vectorstore.similarity_search(prompt, k=1)  # Retrieve top 5 matches
    retrieved_data = [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]

    context  = ""
    for data in retrieved_data:
        context += data['content'] + "\n"

    if retrieved_data==[]:
        return "No Information Available"
    
    return retrieved_data


chat = model.start_chat(history=[])

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    query = data.get("message", "")
    history = data.get("history", [])
    # json_like_str = history.replace("'", '"')
    
    # Escape backslashes (to handle \n, \t, etc.)
    # json_like_str = json_like_str.replace("\\", "\\\\")
    
    # Ensure JSON newlines are escaped correctly
    # history = history.replace("\n", "\\n")
    print(type(history))
    print("history",history)
    if history=="":
        history = []
    else:   
        print("history in else ", type(history))
        # history = json.loads(history)
        pass
    print(type(history))

    if not query:
        return jsonify({"error": "Message is required"}), 400

    context = get_context(query)

    # Prepare the prompt with the existing history
    prompt = "\n".join(history) + f"\nUser: {query}\n Context:{context} \nAnswer:"
    
    # Send message to the chatbot
    response = chat.send_message(prompt, stream=True)
    
    # Collect the response text from the stream
    response_text = ""
    for chunk in response:
        if chunk.text:
            response_text += chunk.text

   # Update the history with the new query and response
    history.append(f"User: {query}")
    history.append(f"Bot: {response_text}") 

    return jsonify({"response": response_text, "history": history})



@app.route('/submit-product', methods=['POST'])
def submit_product():
    """
    Endpoint to receive and process product name and import country.
    """
    try:
        data = request.get_json()


        product_name = data.get('product_name')
        import_country = data.get('import_country')

        if not product_name or not import_country:
            return jsonify({
                "status": "error",
                "message": "Both 'product_name' and 'import_country' are required."
            }), 400


        product_id = len(products) + 1 
        products[product_id] = {
            "product_name": product_name,
            "import_country": import_country
        }
        final_json = process_data(product_name,import_country)
        file_name = create_guide_document(product_name)

        return jsonify({
            "status": "success",
            "message": "Product information received and processed successfully.",
            "product_id": product_id,
            "scheme_json":final_json,
            "data":file_name,
            "market_data":""
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500



@app.route('/generate-guide', methods=['POST'])
def generate_guide():
    data = request.json

    # Extract the product name from the request
    product_name = data.get("product_name")

    if not product_name:
        return jsonify({"error": "Product name is required"}), 400

    # Create the guide document
    try:
        file_name = create_guide_document(product_name)

        # Return the file path instead of uploading to Cloudinary
        file_path = os.path.abspath(file_name)
        
        return jsonify({"file_path": file_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)