from fastapi import FastAPI

app = FastAPI(title="Backend API")


@app.get("/albums")
def get_albums():
    """
    Returns a list of image metadata.
    In real life, these could be URLs to images stored in blob/S3, etc.
    For now we just return some sample image URLs.
    """
    return {
        "items": [
            {
                "title": "Sunset Beach",
                "url": "https://via.placeholder.com/200x150?text=Sunset+Beach"
            },
            {
                "title": "Mountain View",
                "url": "https://via.placeholder.com/200x150?text=Mountain+View"
            },
            {
                "title": "City Lights",
                "url": "https://via.placeholder.com/200x150?text=City+Lights"
            },
        ]
    }


@app.get("/work")
def get_work_docs():
    """
    Returns a list of work documents.
    Here we just send mock names and descriptions.
    """
    return {
        "items": [
            {
                "name": "Design_Document_v1.pdf",
                "description": "System design for microservices"
            },
            {
                "name": "Runbook_Production.docx",
                "description": "Production support runbook"
            },
            {
                "name": "Requirements.xlsx",
                "description": "Feature requirements spreadsheet"
            },
        ]
    }


# Root endpoint (optional)
@app.get("/")
def root():
    return {"message": "Backend API is running. Try /albums or /work."}
