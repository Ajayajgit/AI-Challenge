from src.AiChallenge.utils.embedding import EmbeddingHandler
from src.AiChallenge.components.faiss_index import FaissIndexHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentHandler: 
    def __init__(self, chunk_size=300): #given the chunk size as 300 as the pdf has huge text
        self.chunk_size = chunk_size
        self.embedding_handler = EmbeddingHandler()
        self.faiss_handler = FaissIndexHandler()

    async def add_document(self, doc):
        logger.info("Document received for addition.")
        
        chunks = [doc.text[i:i + self.chunk_size] for i in range(0, len(doc.text), self.chunk_size)]
        logger.debug(f"Chunks created: {chunks[:5]}...")
        
        embeddings = self.embedding_handler.get_embeddings(chunks)  
        logger.debug(f"Embeddings for chunks: {embeddings[:2]}...")
        
        self.faiss_handler.add_embeddings(embeddings)  
        self.faiss_handler.add_document_chunks(chunks)  
        
        logger.info("Document added successfully.")
        return {"message": "Document added successfully."}

    def retrieve_relevant_docs(self, query: str, top_k: int = 3):
        logger.info("Retrieving relevant documents for the query.")
        
        query_embedding = self.embedding_handler.get_embeddings([query])  
        logger.debug(f"Query embedding: {query_embedding}")
        
        relevant_docs = self.faiss_handler.search(query_embedding, top_k)  
        logger.info("Relevant document chunks retrieved.")
        return relevant_docs
