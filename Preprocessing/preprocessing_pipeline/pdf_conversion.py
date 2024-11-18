import fitz  # PyMuPDF
from utils.azure_blob_utils import download_from_azure

def convert_pdf_to_text(raw_file_name):
    """
    Extracts text from a PDF file.

    Args:
        raw_file_name (str): Name of the PDF file in Azure Blob Storage (raw folder).

    Returns:
        str: Extracted text from the PDF.
    """
    try:
        # Step 1: Download the raw file from Azure Blob Storage
        raw_content = download_from_azure("raw", raw_file_name, as_text=False)

        # Step 2: Open the PDF content and extract text
        text = ""
        pdf_document = fitz.open(stream=raw_content, filetype="pdf")
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        pdf_document.close()

        print(f"Successfully extracted text from {raw_file_name}.")
        return text

    except Exception as e:
        print(f"Error extracting text from PDF {raw_file_name}: {e}")
        return None
