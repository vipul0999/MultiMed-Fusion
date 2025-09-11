import os
import pdfplumber

# Input PDF path
pdf_path = "sample.pdf"

# Output folder and file
output_folder = "pdf/processed_text"
output_file = os.path.join(output_folder, "sample.txt")

# Make sure the folder exists
os.makedirs(output_folder, exist_ok=True)

# Extract text
text = ""
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text += page.extract_text() + "\n"

# Save to text file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Extracted text saved to: {output_file}")
