import logging 
from src.AiChallenge.components.llm_handler import LLMHandler
from src.AiChallenge.components.document_handler import DocumentHandler
from pydantic import BaseModel
from fastapi import APIRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentInput(BaseModel): # creating a baseclass from pydantic to give it as input for add_routes
    text: str

class ApiRoutes:
    def __init__(self, llm_handler: LLMHandler, document_handler: DocumentHandler):
        self.llm_handler = llm_handler
        self.document_handler = document_handler 
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):
        @self.router.post("/add-document")
        async def add_document_route(doc: DocumentInput):
            logger.info("Received request to add document.")
            return await self.document_handler.add_document(doc)

        @self.router.post("/get-answer")
        async def get_answer_route(query: dict):
            logger.info(f"Received query: {query}")
            return await self.llm_handler.get_answer_from_pdf(query["query"])

    def get_router(self):
        return self.router
