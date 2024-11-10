from src.AiChallenge.config.configuration import Config, OPENAI_API_KEY
from src.AiChallenge.components.document_handler import DocumentHandler
import openai
import logging

# Configure OpenAI API key
openai_config_object = Config()
openai.api_key = OPENAI_API_KEY

# logging the necessary info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMHandler:
    def __init__(self, model_name="gpt-4o-mini"): # using this as per given
        self.model_name = model_name
        self.document_handler = DocumentHandler()  

    async def get_answer_from_pdf(self, query: str): #this will get answer from pdf
        logger.info("Retrieving relevant documents for the query.")
        relevant_docs = self.document_handler.retrieve_relevant_docs(query)  
        context = " ".join(relevant_docs)
        input_text = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"

        try:
            logger.info("Generating response using OpenAI's API.")
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": input_text}
                ],
                temperature=0.3,
                max_tokens=300,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            answer = response['choices'][0]['message']['content'].strip()
            logger.info("Generated answer: %s", answer)
            return {"answer": answer}

        except Exception as e:
            logger.error("Error retrieving answer: %s", e)
            raise Exception("Error retrieving answer: " + str(e))
