"""
File handling module for AI Contract Risk Analyzer
Supports multiple file formats: PDF, DOCX, TXT, CSV, XLSX
"""

import os
import pandas as pd
from pathlib import Path
import logging

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from docx import Document
except ImportError:
    Document = None

logger = logging.getLogger(__name__)


class FileHandler:
    """Handles file upload and text extraction from multiple formats"""
    
    SUPPORTED_FORMATS = {
        ".pdf": "PDF Document",
        ".docx": "Word Document",
        ".txt": "Text File",
        ".csv": "CSV File",
        ".xlsx": "Excel File"
    }
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Extract text from PDF file using PyMuPDF
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text from PDF
        """
        if not fitz:
            raise ImportError("PyMuPDF is required for PDF processing. Install it with: pip install PyMuPDF")
        
        try:
            doc = fitz.open(file_path)
            text = ""
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """
        Extract text from DOCX file
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text from DOCX
        """
        if not Document:
            raise ImportError("python-docx is required for DOCX processing. Install it with: pip install python-docx")
        
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            raise
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        """
        Extract text from TXT file
        
        Args:
            file_path: Path to TXT file
            
        Returns:
            Text content from file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error extracting text from TXT: {e}")
            raise
    
    @staticmethod
    def extract_text_from_csv(file_path: str) -> str:
        """
        Extract text from CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Formatted text from CSV
        """
        try:
            df = pd.read_csv(file_path)
            return df.to_string()
        except Exception as e:
            logger.error(f"Error extracting text from CSV: {e}")
            raise
    
    @staticmethod
    def extract_text_from_xlsx(file_path: str) -> str:
        """
        Extract text from XLSX file
        
        Args:
            file_path: Path to XLSX file
            
        Returns:
            Formatted text from XLSX
        """
        try:
            xls = pd.ExcelFile(file_path)
            text = ""
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                text += f"\n\n=== Sheet: {sheet_name} ===\n\n"
                text += df.to_string()
            return text
        except Exception as e:
            logger.error(f"Error extracting text from XLSX: {e}")
            raise
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text from file based on file extension
        
        Args:
            file_path: Path to file
            
        Returns:
            Extracted text from file
            
        Raises:
            ValueError: If file format is not supported
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == ".pdf":
            return FileHandler.extract_text_from_pdf(file_path)
        elif file_ext == ".docx":
            return FileHandler.extract_text_from_docx(file_path)
        elif file_ext == ".txt":
            return FileHandler.extract_text_from_txt(file_path)
        elif file_ext == ".csv":
            return FileHandler.extract_text_from_csv(file_path)
        elif file_ext == ".xlsx":
            return FileHandler.extract_text_from_xlsx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    @staticmethod
    def validate_file(file_path: str, max_size_mb: int = 50) -> bool:
        """
        Validate file exists and is within size limits
        
        Args:
            file_path: Path to file
            max_size_mb: Maximum file size in MB
            
        Returns:
            True if file is valid
            
        Raises:
            ValueError: If file is invalid
        """
        if not os.path.exists(file_path):
            raise ValueError(f"File does not exist: {file_path}")
        
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > max_size_mb:
            raise ValueError(f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed size ({max_size_mb} MB)")
        
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in FileHandler.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format. Supported formats: {', '.join(FileHandler.SUPPORTED_FORMATS.keys())}")
        
        return True
