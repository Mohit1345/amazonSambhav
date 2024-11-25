# 
# jsonize (amazon_formate,macmap,dfg_formate,duty_drawback, rodtep)
# amazon payment, shipping, and etc


# overall we have now 6 vc db's

# pdf reader
# metadata 
# save to corresponding vector db

# Creation of amazon vector db

# creation of macmap vector db
# creation of dgf vector db
# creation of duty drawback vector db
# creation of rodtep vector db


from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveJsonSplitter
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")
    

def chunking(pdf_data,type=""):
    if not pdf_data or pdf_data == {}:  # Check if pdf_data is empty or None
        print("No data provided to chunk.")
        return []  # Return an empty list or handle as desired

    if "macmap" in type:
        splitter = RecursiveJsonSplitter(max_chunk_size=300)
        docs = splitter.create_documents(texts=[pdf_data])
        return docs
        
    print("chunking")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    print("moving ")
    text_splitter = SemanticChunker(embeddings)
    print("after semnatics")
    # print("pdf data is ", pdf_data)
    docs = text_splitter.create_documents([pdf_data])
    # print("chunks is , ",docs)
    return docs

def save_vcdb(data, vector_db_name, metadata=None,is_table=False,type=""):

    # Step 1: Chunking using the provided chunking function
    # docs = chunking(data)
    if is_table:
        print("Processing table data...")
        # Convert tabular data into a text format for embedding
        if isinstance(data, pd.DataFrame):
            combined_text = data.to_string(index=False)
        else:
            raise ValueError("For table data, provide a pandas DataFrame.")
        docs = [{"page_content": combined_text, "metadata": metadata}]
    else:
        print("Processing textual data...")
        docs = chunking(data,type)

    # Step 2: Initialize the embedding model (must match the chunker embedding)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Step 3: Connect to or create the vector database
    try:
        vectorstore = Chroma(persist_directory=vector_db_name, embedding_function=embeddings)
    except FileNotFoundError:
        vectorstore = Chroma(persist_directory=vector_db_name, embedding_function=embeddings, create=True)

    # Step 4: Insert or update the vector database
    for doc in docs:
        vectorstore.add_texts([doc.page_content], metadata=[metadata or {}])

    # Persist the database
    # vectorstore.persist()

    print(f"Data saved successfully to the vector database: {vector_db_name}")




def retrieve_from_vcdb(prompt, vector_db_name):
    # Step 1: Initialize the embedding model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    print("connecting vector db")
    # Step 2: Connect to the vector database
    try:
        vectorstore = Chroma(persist_directory=vector_db_name, embedding_function=embeddings)
    except FileNotFoundError:
        raise ValueError(f"Vector database '{vector_db_name}' does not exist.")
    print("vector db connected")
    # Step 3: Perform a similarity search with the prompt
    results = vectorstore.similarity_search(prompt, k=1)  # Retrieve top 5 matches

    # Step 4: Extract and return results
    retrieved_data = [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]
    return retrieved_data

# print(retrieve_from_vcdb("compliance","Drawback_db"))