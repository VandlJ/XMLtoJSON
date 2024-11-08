from datetime import datetime
import json

from typing import Dict

class Document():

    collection_name = "Document"

    def __init__(self, uri: str, publication_date: str, date: str, index: str, namespace: str,
                 title: str, archives: Dict[str, str], referedIn: [str], text: str,
                 names: Dict[str, str], copyRight: [str], metaData: [str]):
        self.uri = uri
        self.publication_date = publication_date
        self.date = date
        self.index = index
        self.namespace = namespace
        self.title = title
        self.archives = archives
        self.referedIn = referedIn
        self.text = text
        self.names = names
        self.copyRight = copyRight
        self.metaData = metaData

    @classmethod
    def from_dict(cls, doc: Dict):
        # Create a new Document object from a dictionary
        return cls(doc["uri"], doc["publication_date"], doc["date"], doc["index"], doc["namespace"], doc["title"],
                   doc["archives"], doc["referedIn"], doc["text"], doc["names"], doc["copyRight"], doc["metaData"])

    def to_dict(self):
        # Convert the Document object to a dictionary
        return {
            "uri": self.uri,
            "publication_date": self.publication_date,
            "date": self.date,
            "index": self.index,
            "namespace": self.namespace,
            "title": self.title,
            "archives": self.archives,
            "referedIn": self.referedIn,
            "text": self.text,
            "names": self.names,
            "copyRight": self.copyRight,
            "metaData": self.metaData
        }
        
    def to_json(self):
        # Convert the object to a dictionary
        obj_dict = self.__dict__

        # Return the dictionary as a JSON string
        return json.dumps(obj_dict)





