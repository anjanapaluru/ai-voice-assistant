import pypdf
import os

def parse_resume(file_path):
    """
    Extracts text from a PDF resume.
    """
    if not os.path.exists(file_path):
        return "Resume file not found."
    
    try:
        text = ""
        with open(file_path, "rb") as file:
            reader = pypdf.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text.strip()
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"

if __name__ == "__main__":
    # Test (assuming a sample.pdf exists)
    # print(parse_resume("uploaded_resume/sample.pdf"))
    pass
