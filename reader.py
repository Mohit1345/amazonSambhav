# def read_compliance(file):
#     # check file type and as per that read content
#     # it can be pdf or if not got any data as pdf then vision model gemini
#     data = file
#     return data

import PyPDF2
import camelot
import pandas as pd
from tabula import read_pdf
import pdfplumber
# Function to read text data from a PDF
def read_pdf_data(pdf_path):
    """
    Reads text data from a PDF file.
    :param pdf_path: Path to the PDF file
    :return: Text content as a string
    """
    try:
        text = ""
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# # Function to extract tables from a PDF and save them to an Excel file
# def extract_tables_to_excel(pdf_path, excel_path):
#     """
#     Extracts tables from a PDF and saves them to an Excel file.
#     :param pdf_path: Path to the PDF file
#     :param excel_path: Path to the output Excel file
#     :return: Success message or error
#     """
#     try:
#         # Extract tables using Camelot
#         tables = camelot.read_pdf(pdf_path, pages='all')
#         print("tables we got are", tables)

#         if not tables:
#             return "No tables found in the PDF."

#         # Write tables to Excel
#         with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
#             for i, table in enumerate(tables):
#                 df = table.df  # Get the DataFrame
#                 sheet_name = f"Table_{i+1}"
#                 df.to_excel(writer, index=False, sheet_name=sheet_name)

#         return f"Tables successfully extracted and saved to {excel_path}."
#     except Exception as e:
#         return f"An error occurred: {str(e)}"
#         # return ""
# def extract_tables_to_excel(pdf_path, excel_path):
#     """
#     Extracts tables from a PDF and saves them to an Excel file.
#     :param pdf_path: Path to the PDF file
#     :param excel_path: Path to the output Excel file
#     :return: Success message or error
#     """
#     try:
#         # Extract tables using Tabula
#         tables = read_pdf(pdf_path, pages="all", multiple_tables=True, pandas_options={"header": None})

#         if not tables or len(tables) == 0:
#             return "No tables found in the PDF."

#         # Write tables to Excel
#         with pd.ExcelWriter(excel_path, engine='openpyxl',encoding = "utf-8") as writer:
#             for i, table in enumerate(tables):
#                 sheet_name = f"Table_{i+1}"
#                 table.to_excel(writer, index=False, sheet_name=sheet_name)

#         return f"Tables successfully extracted and saved to {excel_path}."
#     except Exception as e:
#         return f"An error occurred: {str(e)}"

def extract_tables_to_excel(pdf_path, excel_path):
    """
    Extracts tables from a PDF and saves them to an Excel file using pdfplumber.
    :param pdf_path: Path to the PDF file
    :param excel_path: Path to the output Excel file
    :return: Success message or error
    """
    try:
        tables_found = False
        with pdfplumber.open(pdf_path) as pdf:
            # Create an Excel writer
            with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
                for i, page in enumerate(pdf.pages, start=1):
                    tables = page.extract_tables()
                    if tables:
                        tables_found = True
                        for j, table in enumerate(tables, start=1):
                            df = pd.DataFrame(table)
                            sheet_name = f"Page_{i}_Table_{j}"
                            df.to_excel(writer, index=False, header=False, sheet_name=sheet_name)

        if not tables_found:
            return "No tables found in the PDF."
        return f"Tables successfully extracted and saved to {excel_path}."
    except Exception as e:
        return f"An error occurred: {str(e)}"
# Example Usage
# if __name__ == "__main__":
#     pdf_file_path = "example.pdf"
#     excel_file_path = "output.xlsx"

#     # Read text data from the PDF
#     text_data = read_pdf_data(pdf_file_path)
#     print("PDF Text Content:\n", text_data)

#     # Extract tables and save to Excel
#     result = extract_tables_to_excel(pdf_file_path, excel_file_path)
#     print(result)

from vector_dbs import *

def read_data(pdf_path):
    # excel_file_path = f'{product_name}.xlsx'
    text_data = read_pdf_data(pdf_path)
    # print("PDF Text Content:\n", text_data)

    # Extract tables and save to Excel
    # result = extract_tables_to_excel(pdf_path, excel_file_path)
    # print(result)
    return text_data


# one= read_data("drawback.pdf")
# print(one)
# print("two is ", two)
# save_vcdb(one,"Drawback_db",metadata={"name":"drawback_scehem_data"})
