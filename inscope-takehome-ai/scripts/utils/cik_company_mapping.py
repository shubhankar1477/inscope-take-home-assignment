import os
import pandas as pd
from bs4 import BeautifulSoup
import tqdm



class clsCompanyMapping():
    
    def __init__(self,path) -> None:
        """
        Initialize the clsCompanyMapping object.

        Args:
        - path (str): The path to the directory containing HTML files.

        Attributes:
        - path (str): The path to the directory containing HTML files to be processed.
        """
        self.path = path
        
    
    def create_mapping(self) -> pd.DataFrame :
        """
        Create a mapping between CIK and company names from HTML files.

        Returns:
        pd.DataFrame: A Pandas DataFrame with columns "CIK" and "Company_Name" containing the mapping.
        """
        
        filter_files = self.filter_sp_companies()
        company_mapping_list = []
        for file in tqdm.tqdm((filter_files)):
            file_path  = os.path.join(self.path,file)
            CIK = os.path.splitext(os.path.basename(file_path))[0]
            print(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                # Use lxml for better performance
                html_content = BeautifulSoup(f.read(), 'lxml')

            tag = html_content.find('ix:nonnumeric', {'name': 'dei:EntityRegistrantName'})
            company_name = tag.get_text() if tag else ""

            company_mapping_list.append((CIK, company_name))

        # Convert the list of tuples to a Pandas DataFrame
        columns = ["CIK", "Company_Name"]
        company_mapping_df = pd.DataFrame(company_mapping_list, columns=columns) 
        return company_mapping_df
    
    
    def filter_sp_companies(self):
        with open(".../SP500.txt",'r') as f:
            data = f.readlines()
        data = [file.replace("\n" , "") for file in data]
        files_list = os.listdir(self.path)
        filtered_files = [file for file in files_list if os.path.splitext(os.path.basename(file))[0] in data]
        print(filtered_files)
        return filtered_files

    
if __name__ == '__main__' :

    objCompanyMapping = clsCompanyMapping('.../data')
    data = objCompanyMapping.create_mapping()
    print(data.to_csv("comapny_mapping.csv"))

        
        
        