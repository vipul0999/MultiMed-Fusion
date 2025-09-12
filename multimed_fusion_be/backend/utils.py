import fitz  # PyMuPDF

def pdf_to_text(pdf_path: str) -> str:
    """
    Convert a PDF file into plain text.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text content from the PDF.
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text("text") + "\n"
    return text.strip()


# Example usage
if __name__ == "__main__":
    pdf_file = "sample.pdf"
    extracted_text = pdf_to_text(pdf_file)
    print(extracted_text[:1000])  # Print first 1000 chars
