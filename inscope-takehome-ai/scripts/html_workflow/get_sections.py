from html_workflow.parser import ExtractItems



class clsGetSection:
    
    def __init__(self) -> None:
        """
        Initialize the clsGetSection object.

        Initializes the extraction settings using the ExtractItems class.

        Settings:
        - remove_tables (bool): Whether to remove tables from the extracted content.
        - items_to_extract (list): A list of section item numbers to extract (e.g., "1", "1A", "1B", ...).
        """
        self.extraction = ExtractItems(
                remove_tables=True,
                items_to_extract=[
                    "1", "1A", "1B", "2", "5", "7"
                ])

    def process_file(self,file_path):
        """
        Process an HTML file and extract specific sections.

        Args:
            file_path (str): The path to the HTML file to be processed.

        Returns:
            dict: A dictionary containing the extracted sections and their content.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.extraction.extract_items(content=content)
