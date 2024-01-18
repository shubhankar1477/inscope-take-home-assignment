import re
from langchain.schema import Document

class clsCleaner:
    
    @staticmethod
    def clean_text_comprehend(text):
        # Remove non-ASCII characters
        text = ''.join(char for char in text if ord(char) < 128)

        # Remove whitespace and special characters
        text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespaces with a single space
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove non-alphanumeric characters

        return text.strip()
    
    @staticmethod
    def create_half_text(original_text, characters_per_word=4):
        """
        Create a new text with half the words of the original text,
        taking 10% from the start and 10% from the end.

        :param original_text: The original text string.
        :param characters_per_word: Average number of characters per word.
        :return: New text composed of 10% words from the start and end of the original text.
        """
        text_length = len(original_text)

        # Calculating the total number of words in the text
        total_words = text_length // characters_per_word

        # Calculating the number of words for the new text (half of the total words)
        new_text_word_count = total_words // 2

        # Calculating the number of words to take from the start and end (10% of the new text word count)
        start_end_word_count = new_text_word_count // 10

        # Taking 10% words from the start and 10% words from the end of the text
        start_text = original_text[:start_end_word_count * characters_per_word]
        end_text = original_text[-start_end_word_count * characters_per_word:]

        # Concatenating the start and end parts to form the new text
        new_text = start_text + end_text

        return new_text

    @staticmethod
    def extract_values(data_dict, keys):
        """
        Extract values from a dictionary for the specified keys.

        :param data_dict: The dictionary from which to extract values.
        :param keys: A list of keys for which values are required.
        :return: A list of values corresponding to the specified keys.
        """
        return [data_dict.get(key, None) for key in keys]
    
    @staticmethod
    def create_document(company_metadata, summary):
        return Document(page_content=summary, metadata=company_metadata)




