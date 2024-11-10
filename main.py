from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.AiChallenge.components.document_handler import DocumentHandler
from src.AiChallenge.components.llm_handler import LLMHandler
from src.AiChallenge.pipeline.api_routes import ApiRoutes
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PDF Question Answering System",
    version="1.0",
    description="A PDF-based Q&A API server"
)

class DocumentInput(BaseModel):
    text: str

class QueryInput(BaseModel):
    query: str

document_handler = DocumentHandler()
llm_handler = LLMHandler()
api_routes = ApiRoutes(llm_handler, document_handler)

app.include_router(api_routes.get_router())

@app.post("/add-document")
async def add_document_route(doc: DocumentInput):
    logger.info(f"Document input: {doc}")
    try:
        return await document_handler.add_document(doc)
    except Exception as e:
        logger.error(f"Error adding document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get-answer")
async def get_answer_route(query: QueryInput):
    logger.info(f"Query input: {query}")
    try:
        return await llm_handler.get_answer_from_pdf(query.query)
    except Exception as e:
        logger.error(f"Error retrieving answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
