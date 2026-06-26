import os
import docx
import pymupdf
from rich.console import Console

console = Console()


def _extract_pdf_text(file_path: str)-> str:
    """
        Extractor function for pdf document.
    @file_path: Document path.
    """

    doc = pymupdf.open(file_path)
    pages_text = []

    for page in doc:
        text = page.get_text()
        if isinstance(text, str) and text.strip():
            pages_text.append(text)
    doc.close()
    
    return "\n".join(pages_text)

def _extract_docx_text(file_path: str)-> str:
    """
        Extractor function for docx document.
    @file_path: Document path.
    """

    doc = docx.Document(file_path)
    paragraph_text = []

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            paragraph_text.append(text)
    
    return "\n".join(paragraph_text)

def _extract_txt_text(file_path: str)-> str:
    """
        Extractor function for txt document.
    @file_path: Document path.
    """

    with open(file_path, 'r', encoding='utf-8', errors="ignore") as f:
        txt_content = f.read()
    
    return txt_content


def check_file_type(file_path: str)-> str:
    """
        Detector function to check the good.
    document type (txt, docx, pdf).
    @file_path: Document path.
    """
    
    extensions = {
        ".md": _extract_txt_text,
        ".txt": _extract_txt_text,
        ".docx": _extract_docx_text,
        ".pdf": _extract_pdf_text,
    }
    
    _ext = os.path.splitext(file_path.lower())[1]

    if _ext not in extensions:
        console.print(f"[bold red] [POCKET-RAG]:（⊙ｏ⊙）Sorry, file {file_path} has unsupported file type: {_ext} !")
        exit(1)

    return extensions[_ext](file_path)

def load_and_chunk_file(file_path: str, chunk_size: int = 150)-> list[str]:
    """
        The small function witch cutting file content in
    chunk list.
    """

    if not os.path.exists(file_path):
        console.print(f'[bold red] [POCKET-RAG]:（⊙ｏ⊙）File {file_path} does not exist ![/]')
        exit(1)

    content = check_file_type(file_path) 
    if not content.strip():
       console.print(f"[bold red] [POCKET-RAG]:（⊙ｏ⊙）Content not found in {file_path} file.")
       exit(0)
    
    words = content.split() 
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk_words = words[i:i + chunk_size] # cut the words list into portions
        '''
            Example:
                len(words) = 1000
                - first round (chunk 1): chunk_words = words[0 : 0 + 150]  => (0-149) words
                - second round (chunk 2): chunk_words = words[150 : 150 + 150] => (150-299) words
                - etc...
        '''
        chunk_text = ' '.join(chunk_words)
        chunks.append(chunk_text)

    return chunks