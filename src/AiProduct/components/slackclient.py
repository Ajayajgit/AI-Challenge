from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from src.AiProduct.config.configuration import Config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
class SlackHandler:
    """
    A class to handle Slack message posting.
    """

    def __init__(self, token=Config.get_slack_api_key, channel=Config.get_slack_channel):
        """
        Initializes the Slack WebClient with API and sets the default channel.

        Parameters:
            token (str): The Slack API token.
            channel (str): The Slack channel ID to post messages to.
        """
        self.client = WebClient(token=token)
        self.channel = channel
        logger.info("Slack client initialized.")

    def post_message(self, message: str):
        """
        Posts a message to the configured Slack channel.

        Parameters:
            message (str): The message text to send to Slack.

        Returns:
            dict: The response from the Slack API if successful, None otherwise.
        """
        try:
            logger.info(f"Posting message to Slack channel {self.channel}.")
            response = self.client.chat_postMessage(
                channel=self.channel,
                text=message
            )
            logger.info("Message posted successfully.")
            return response

        except SlackApiError as e:
            logger.error(f"Error posting message: {e.response['error']}")
            return None
