from dotenv import load_dotenv
import os
import logging 

# Loading environment variables from a .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# logging the required info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """
    A configuration class to hold environment and application settings.
    """

    def __init__(self):
        self.API_URL = "http://localhost:8080"
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.SLACK_API = os.getenv("SLACK_API")
        self.SLACK_CHANNEL = "compliance"
        logger.info("Configuration loaded successfully.")

    def get_openai_api_key(self):
        """
        Returns the OpenAI API key.
        """
        return self.OPENAI_API_KEY

    def get_slack_api_key(self):
        """
        Returns the Slack API key.
        """
        return self.SLACK_API

    def get_slack_channel(self):
        """
        Returns the Slack channel ID.
        """
        return self.SLACK_CHANNEL

    @staticmethod
    def get_api_url():
        """
        Returns the API URL.
        """
        return "http://localhost:8080"
