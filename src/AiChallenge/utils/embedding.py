import logging
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingHandler:
    def __init__(self, model_name="all-MiniLM-L6-v2"): # using the sentence transformer for embeddings
        logger.info(f"Initializing the SentenceTransformer model: {model_name}")
        self.model = None
        self.initialize_model(model_name)
        logger.info("SentenceTransformer model initialized successfully.")

    def initialize_model(self, model_name):
        if not self.model:
            logger.info(f"Loading the model: {model_name}")
            self.model = SentenceTransformer(model_name)
            logger.info(f"Model {model_name} loaded successfully.")

    def get_embeddings(self, texts): # getting the embeddings of the text
        if self.model is None:
            raise ValueError("Embedding model is not initialized. Please call 'initialize_model()' first.")
        
        logger.info(f"Generating embeddings for {len(texts)} texts.")
        embeddings = self.model.encode(texts)
        logger.info("Embeddings generated successfully.")
        return embeddings
