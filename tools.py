from crewai_tools import tool,EXASearchTool
from PyPDF2 import PdfReader

search_tool = EXASearchTool()

@tool("PDFSearchTool")
def PDFSearchTool(pdf_path: str) -> str:
    """Reads a PDF file and returns the text format"""
    reader = PdfReader(pdf_path)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text()
    return text

