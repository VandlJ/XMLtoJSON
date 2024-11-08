import json
from typing import List


class Person():

    def __init__(self, publication_date: str, namespace: str, full_name: str, first_name: str, last_name: str, references_list: List[str], artwork_list: List[str], additional_info: List[str], authority: None, file_name: str):
        self.publication_date = publication_date
        self.namespace = namespace
        self.full_name = full_name
        self.first_name = first_name
        self.last_name = last_name
        self.references_list = references_list
        self.artwork_list = artwork_list
        self.additional_info = additional_info
        self.authority = authority
        self.file_name = file_name
    
    def to_json(self):
        return json.dumps(self.__dict__)