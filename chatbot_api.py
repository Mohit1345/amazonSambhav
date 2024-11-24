import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY2"))
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import re
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "You are an expert in international trade compliance, import/export requirements, and incentive schemes. "
        "Your task is to guide the user in importing or exporting products to specific countries. "
        "Using the provided context from a vector database, respond with clear, accurate, and actionable advice tailored to the user's query.\n\n"
        "Guidelines:\n"
        "- Focus your response on the compliance requirements, regulations, and schemes relevant to the query and context provided.\n"
        "- Ensure your guidance is concise, professional, and easy to understand.\n"
        "- If the context lacks sufficient information, state what is missing and suggest additional details the user could provide."
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
    history = json.loads(data.get("history", []))

    if not query:
        return jsonify({"error": "Message is required"}), 400

    context = get_context(query)

    prompt = "\n".join(history) + f"\nUser: {query}\n Context:{context} \nAnswer:"
    
    response = chat.send_message(prompt, stream=True)
    
    response_text = ""
    for chunk in response:
        if chunk.text:
            response_text += chunk.text

    history.append(f"User: {query}")
    history.append(f"Bot: {response_text}")

    return jsonify({"response": response_text, "history": str(history)})

if __name__ == '__main__':
    app.run(debug=True)
