import faiss
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FaissIndexHandler: 
    def __init__(self, embedding_dim=384):  
        self.embedding_dim = embedding_dim
        self.faiss_index = faiss.IndexFlatL2(self.embedding_dim)
        self.document_chunks = []
        logger.info(f"FAISS index initialized with embedding dimension {self.embedding_dim}.")

    def add_embeddings(self, embeddings): # add the embeddings to faiss
        if len(embeddings) == 0:
            logger.warning("No embeddings to add to the FAISS index.")
            return
        
        if isinstance(embeddings, list):
            embeddings = np.array(embeddings).astype("float32") # giving the type coercion by float32

        self.faiss_index.add(embeddings)
        logger.info(f"Added {len(embeddings)} embeddings to FAISS index.")

    def add_document_chunks(self, chunks):
        self.document_chunks.extend(chunks)
        logger.info(f"Added {len(chunks)} document chunks.")

    def search(self, query_embedding, top_k=3): # retrve the 3 documents based on query
        if isinstance(query_embedding, list):
            query_embedding = np.array(query_embedding).astype("float32")
        
        distances, indices = self.faiss_index.search(query_embedding, top_k)

        logger.debug(f"Distances: {distances}")
        logger.debug(f"Indices: {indices}")

        relevant_chunks = []
        for idx in indices[0]:
            if 0 <= idx < len(self.document_chunks):
                relevant_chunks.append(self.document_chunks[idx])
            else:
                logger.warning(f"Invalid index {idx} returned by FAISS search. Skipping.")
        
        if not relevant_chunks:
            logger.error(f"No valid document chunks retrieved. Check the FAISS index and document chunks.")
        
        logger.info(f"Retrieved {len(relevant_chunks)} relevant document chunks based on query.")
        return relevant_chunks
