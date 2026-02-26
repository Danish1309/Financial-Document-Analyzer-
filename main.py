from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
from agents import financial_analyst, verifier
from task import analyze_financial_document as analyze_task  # Fixed: Renamed import to avoid collision

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run the financial analysis crew"""
    financial_crew = Crew(
        agents=[financial_analyst, verifier],  # Fixed: Added verifier agent
        tasks=[analyze_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = financial_crew.kickoff({'query': query, 'file_path': file_path})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Financial Document Analyzer API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.post("/analyze")
async def analyze_document_endpoint(  # Fixed: Renamed function to avoid collision
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate file size
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        # Validate and clean query - Fixed: Better validation
        if not query or query.strip() == "" or query.isspace():
            query = "Analyze this financial document for investment insights"
        else:
            query = query.strip()
            
        # Process the financial document with all analysts
        response = run_crew(query=query, file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename,
            "file_size": f"{file_size / 1024:.2f} KB"
        }
        
    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error processing document: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing financial document: {str(e)}"
        )
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as cleanup_error:
                # Log cleanup error but don't fail the request
                print(f"Cleanup error: {str(cleanup_error)}")

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "Financial Document Analyzer",
        "components": {
            "api": "operational",
            "crew_ai": "operational"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
