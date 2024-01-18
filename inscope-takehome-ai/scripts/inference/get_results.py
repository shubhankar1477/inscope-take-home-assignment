from config import config
import requests
from utils.text_cleaner import clsCleaner

class clsGetResults:
    def __init__(self) -> None:
        """
        Initialize the clsGetResults object.

        Initializes the Hugging Face API token and model URL.

        Attributes:
        - HF_TOKEN (str): The Hugging Face API token for authentication.
        - API_URL (str): The URL of the summarization model.
        - headers (dict): HTTP headers including authorization with the API token.
        """
        self.HF_TOKEN = config['HF_TOKEN']
        self.API_URL = config['MODEL_URL']
        self.headers = {"Authorization": f"Bearer {self.HF_TOKEN}"}
        
    def query(self,payload):
        """
        Query the summarization model with a given payload.

        Args:
            payload (dict): The input data for the model query.

        Returns:
            dict: The response from the model containing summarized text.
        """
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        return response.json()
    
    def get_summarise_text(self,content_json):
        """
        Get summarized text from specific sections of content.

        Args:
            content_json (dict): JSON data representing document sections.

        Returns:
            str: The summarized text obtained from specified sections.
        """
        final_text = ''
        text_list = clsCleaner.extract_values(content_json, ['item_1', 'item_2', 'item_5'])
        for text in text_list:
            # text = clsCleaner.create_half_text(text)
            output = self.query({"inputs": f" {text}", })
            if len(output) > 0:
                final_text = final_text + output[0]['summary_text']
        return final_text