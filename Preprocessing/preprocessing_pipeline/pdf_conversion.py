import fitz  # PyMuPDF
import easyocr
from PIL import Image
from io import BytesIO
import numpy as np
import streamlit as st
from utils.azure_blob_utils import download_from_azure


def convert_pdf_to_text(raw_file_name):
    """
    Extracts text from a PDF file. Uses EasyOCR as a fallback for scanned PDFs.

    Args:
        raw_file_name (str): Name of the PDF file in Azure Blob Storage (raw folder).

    Returns:
        str: Extracted text from the PDF.
    """
    try:
        # Step 1: Download the raw file from Azure Blob Storage
        print(f"Downloading {raw_file_name} from Azure Blob Storage (raw folder)...")
        raw_content = download_from_azure("raw", raw_file_name, as_text=False)

        # Step 2: Open the PDF content using PyMuPDF (fitz)
        pdf_document = fitz.open(stream=raw_content, filetype="pdf")
        text = ""  # Initialize a string to hold extracted text
        reader = easyocr.Reader(['en'], gpu=False)  # Initialize EasyOCR for English (disable GPU for portability)

        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]

            # Attempt to extract text directly from the page
            page_text = page.get_text()
            if page_text.strip():  # If direct text extraction is successful
                print(f"Direct text extracted from page {page_num + 1}.")
                text += page_text
            else:  # Fallback to OCR for scanned pages
                print(f"Direct text extraction failed on page {page_num + 1}. Applying OCR.")
                pix = page.get_pixmap(dpi=300)  # Render the page as a high-resolution image
                img = Image.open(BytesIO(pix.tobytes("png")))  # Convert rendered image to a PIL Image
                img_array = np.array(img)  # Convert PIL Image to NumPy array for EasyOCR
                ocr_text = reader.readtext(img_array, detail=0)  # Perform OCR with EasyOCR
                text += "\n".join(ocr_text)  # Append the OCR results to the text string

        pdf_document.close()  # Close the PDF document
        print(f"Successfully extracted text from {raw_file_name}.")
        return text

    except Exception as e:
        print(f"Error processing PDF {raw_file_name}: {e}")
        return None
