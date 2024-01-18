import os
from html_workflow.get_sections import clsGetSection
from inference.get_results import clsGetResults
import pandas as pd
from utils.text_cleaner import clsCleaner

class clsPipeline:
    
    def __init__(self) -> None:
        """
        Initialize the clsPipeline object.

        Initializes the clsGetSection and clsGetResults objects, and sets up the output JSON structure.
        """
        self.objGetSection = clsGetSection()
        self.objGetResults = clsGetResults()
        self.output_json = {"cluster_companies": {"company_name": [], "CIK": [], "score": []}}
        
    def run(self,cik,path,vector_db):
        """
        Run the pipeline to process a company's financial filings.

        Args:
            cik (str): The CIK (Central Index Key) of the company.
            path (str): The path to the raw filings directory.
            vector_db: The vector database for similarity search.

        Returns:
            dict: A dictionary containing the results of the pipeline analysis.
        """
        company_mapping = pd.read_csv("./comapny_mapping.csv",dtype={'CIK': str})
        record = company_mapping[company_mapping['CIK'] == str(cik)].to_dict(orient='records')
        summary = self.process_record(record[0],path,is_inference=True)
        result = vector_db.similarity_search_with_score(summary, k=3)
        for document, score in result:
            self.output_json['cluster_companies']['company_name'].append(document.metadata['company_name'])
            self.output_json['cluster_companies']['CIK'].append(document.metadata['CIK'])
            self.output_json['cluster_companies']['score'].append(str(score))
            self.output_json['inference_company_name'] = record[0]['Company_Name']
            self.output_json['inference_CIK'] = record[0]['CIK']

        return self.output_json
    
    def process_record(self,record, raw_fillings_dir, is_inference=False):
        """
        Process a record for a company's financial filings.

        Args:
            record (dict): A dictionary containing company information.
            raw_fillings_dir (str): The directory containing raw filings data.
            is_inference (bool): Whether the processing is for inference.

        Returns:
        
            str: The processed summary text or None if the file does not exist.
        """
        cik = record['CIK']
        company_name = record['Company_Name']
        file_path = os.path.join(raw_fillings_dir, cik + '.html')

        if os.path.exists(file_path):
            json_section = self.objGetSection.process_file(file_path)
            return self.generate_summary_or_document(cik, company_name, json_section, is_inference)
        return None
    
    def generate_summary_or_document(self,cik, company_name, json_section, is_inference=False):
        """
        Generate a summary or document for a company's financial filings.

        Args:
            cik (str): The CIK (Central Index Key) of the company.
            company_name (str): The name of the company.
            json_section (dict): JSON data representing document sections.
            is_inference (bool): Whether the processing is for inference.

        Returns:
            str or Document: The summary text or Document object, or None if no data is available.
        """
        if json_section:
            summary = self.objGetResults.get_summarise_text(json_section)
            if not is_inference:
                return clsCleaner.create_document({"CIK": cik, "company_name": company_name}, summary)
            else:
                return summary
        return None
