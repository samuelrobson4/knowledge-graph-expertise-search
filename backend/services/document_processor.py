"""Document text extraction service."""
import io
from typing import Optional
import fitz  # PyMuPDF
from docx import Document
from fastapi import UploadFile, HTTPException


async def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from PDF file.

    Args:
        file_bytes: PDF file content as bytes

    Returns:
        Extracted text as string
    """
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_content = []

        for page in doc:
            text = page.get_text()
            text_content.append(text)

        doc.close()
        return "\n\n".join(text_content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract PDF text: {str(e)}")


async def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extract text from DOCX file.

    Args:
        file_bytes: DOCX file content as bytes

    Returns:
        Extracted text as string
    """
    try:
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n\n".join(paragraphs)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract DOCX text: {str(e)}")


async def extract_text_from_txt(file_bytes: bytes) -> str:
    """
    Extract text from TXT file.

    Args:
        file_bytes: TXT file content as bytes

    Returns:
        Extracted text as string
    """
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        # Try other encodings if UTF-8 fails
        try:
            return file_bytes.decode("latin-1")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to decode text file: {str(e)}")


async def extract_text(file: UploadFile) -> str:
    """
    Extract text from uploaded file based on file type.

    Supports: PDF, DOCX, TXT

    Args:
        file: Uploaded file

    Returns:
        Extracted text as string

    Raises:
        HTTPException: If file type unsupported or extraction fails
    """
    # Read file content
    content = await file.read()

    # Determine file type from filename
    filename_lower = file.filename.lower() if file.filename else ""

    if filename_lower.endswith(".pdf"):
        return await extract_text_from_pdf(content)
    elif filename_lower.endswith(".docx"):
        return await extract_text_from_docx(content)
    elif filename_lower.endswith(".txt"):
        return await extract_text_from_txt(content)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Accepted: .pdf, .docx, .txt"
        )
