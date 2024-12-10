import json
from typing import Dict, List

class Document:
    collection_name = "Document"

    def __init__(
        self,
        uri: str,
        publication_date: str,
        date: str,
        index: str,
        namespace: str,
        title: str,
        archives: Dict[str, str],
        referedIn: List[str],
        text: str,
        names: Dict[str, str],
        copyRight: List[str],
        metaData: List[str],
    ):
        """
        Initialize a Document object.

        :param uri: The URI of the document.
        :param publication_date: The publication date of the document.
        :param date: The date of the document.
        :param index: The index of the document.
        :param namespace: The XML namespace.
        :param title: The title of the document.
        :param archives: A dictionary of archives related to the document.
        :param referedIn: A list of references in which the document is referred.
        :param text: The text content of the document.
        :param names: A dictionary of names related to the document.
        :param copyRight: A list of copyright information.
        :param metaData: A list of metadata related to the document.
        """
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
        """Create a new Document object from a dictionary."""
        return cls(
            doc["uri"],
            doc["publication_date"],
            doc["date"],
            doc["index"],
            doc["namespace"],
            doc["title"],
            doc["archives"],
            doc["referedIn"],
            doc["text"],
            doc["names"],
            doc["copyRight"],
            doc["metaData"],
        )

    def to_dict(self) -> Dict:
        """Convert the Document object to a dictionary."""
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
            "metaData": self.metaData,
        }

    def to_json(self) -> str:
        """Convert the object to a JSON string."""
        return json.dumps(self.to_dict(), indent=2)