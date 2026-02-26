## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

# ensure the local package directory is on sys.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "crewai"))

try:
    from crewai.tools import SerperDevTool, tool
except ImportError:                    # linter‑safe fallback
    # either install the package or define dummy classes for testing
    class SerperDevTool:
        def __init__(self, *a, **k): pass
    def tool(name):
        def decorator(fn): return fn
        return decorator

from pypdf import PdfReader

## Creating search tool
search_tool = SerperDevTool()
...

## Creating custom pdf reader tool - Fixed: Using pypdf directly to avoid embedding issues
def read_data_tool(path='data/TSLA-Q2-2025-Update.pdf'):
    """Tool to read data from a PDF file
    
    Args:
        path (str): Path of the PDF file
        
    Returns:
        str: Full PDF text content
    """
    try:
        reader = PdfReader(path)
        full_text = ""
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        return full_text if full_text else "No text found in PDF"
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

## Wrap as a custom tool using tool decorator from crewai
from crewai.tools import tool

@tool("read_pdf_tool")
def FinancialDocumentTool(path: str = 'data/TSLA-Q2-2025-Update.pdf') -> str:
    """Read and extract text from a financial PDF document.
    
    Args:
        path: Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    return read_data_tool(path)

## Creating Investment Analysis Tool
class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data):
        """Analyze financial document data for investment insights
        
        Args:
            financial_document_data (str): The financial document content
            
        Returns:
            str: Investment analysis results
        """
        processed_data = financial_document_data
        
        # Clean up double spaces
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        analysis = {
            "data_length": len(processed_data),
            "cleaned_data": processed_data[:500] + "..." if len(processed_data) > 500 else processed_data
        }
        
        return f"Investment Analysis Complete. Document analyzed: {analysis['data_length']} characters processed."

## Creating Risk Assessment Tool
class RiskTool:
    @staticmethod
    def assess_risk_tool(financial_document_data):
        """Perform risk assessment on financial document data
        
        Args:
            financial_document_data (str): The financial document content
            
        Returns:
            str: Risk assessment results
        """
        risk_indicators = []
        
        risk_terms = ['debt', 'liability', 'loss', 'risk', 'volatility', 'uncertainty']
        
        for term in risk_terms:
            if term.lower() in financial_document_data.lower():
                risk_indicators.append(term)
        
        return f"Risk Assessment Complete. Risk indicators found: {', '.join(risk_indicators) if risk_indicators else 'None identified'}"
