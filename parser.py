import os
import re
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    from docx import Document
except ImportError:
    Document = None


class ResumeParser:
    """Parse resume files (PDF and DOCX) to extract text content."""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt']
    
    def parse_file(self, file_path):
        """Parse resume file and extract text."""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self._parse_pdf(file_path)
        elif file_ext == '.docx':
            return self._parse_docx(file_path)
        elif file_ext == '.txt':
            return self._parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def _parse_pdf(self, file_path):
        """Extract text from PDF file."""
        if PyPDF2 is None:
            raise ImportError("PyPDF2 not installed. Install with: pip install PyPDF2")
        
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
        
        return text
    
    def _parse_docx(self, file_path):
        """Extract text from DOCX file."""
        if Document is None:
            raise ImportError("python-docx not installed. Install with: pip install python-docx")
        
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")
        
        return text
    
    def _parse_txt(self, file_path):
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            raise Exception(f"Error parsing TXT: {str(e)}")
        
        return text
    
    def extract_keywords(self, text):
        """Extract keywords from resume text."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace and special characters
        text = re.sub(r'\s+', ' ', text)
        
        # Extract words (3+ characters)
        words = re.findall(r'\b[a-z]{3,}\b', text)
        
        # Remove common stop words
        stop_words = {
            'the', 'and', 'for', 'with', 'that', 'from', 'are', 'have', 'has',
            'was', 'were', 'been', 'being', 'this', 'can', 'could', 'would',
            'should', 'may', 'might', 'must', 'will', 'your', 'our', 'their'
        }
        
        keywords = [w for w in words if w not in stop_words]
        
        # Return unique keywords with frequency
        from collections import Counter
        return Counter(keywords)
    
    def extract_contact_info(self, text):
        """Extract contact information from resume."""
        contact_info = {}
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        contact_info['email'] = emails[0] if emails else None
        
        # Extract phone
        phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
        phones = re.findall(phone_pattern, text)
        contact_info['phone'] = phones[0] if phones else None
        
        # Extract LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+|linkedin\.com/profile/[\w-]+'
        linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
        contact_info['linkedin'] = linkedin[0] if linkedin else None
        
        return contact_info
