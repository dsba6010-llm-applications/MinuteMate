import fitz  # PyMuPDF
import easyocr
from PIL import Image
from io import BytesIO
import numpy as np
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
        raw_content = download_from_azure("raw", raw_file_name, as_text=False)

        # Step 2: Open the PDF content
        pdf_document = fitz.open(stream=raw_content, filetype="pdf")
        text = ""
        reader = easyocr.Reader(['en'])  # Initialize EasyOCR for English

        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]

            # Attempt to extract text directly
            page_text = page.get_text()
            if page_text.strip():  # If direct text is available
                print(f"Text extracted directly from page {page_num + 1}.")
                text += page_text
            else:  # Fallback to OCR for scanned pages
                print(f"Applying OCR on page {page_num + 1} of {raw_file_name}.")
                pix = page.get_pixmap(dpi=300)  # Render page to an image
                img = Image.open(BytesIO(pix.tobytes("png")))
                img_array = np.array(img)  # Convert PIL Image to NumPy array for EasyOCR
                ocr_text = reader.readtext(img_array, detail=0)  # Extract text with EasyOCR
                text += "\n".join(ocr_text)

        pdf_document.close()
        print(f"Successfully extracted text from {raw_file_name}.")
        return text

    except Exception as e:
        print(f"Error in OCR for {raw_file_name}: {e}")
        return None
