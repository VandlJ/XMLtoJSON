import json
from typing import List, Optional

class Person:
    def __init__(
        self,
        publication_date: str,
        namespace: str,
        full_name: str,
        first_name: str,
        last_name: str,
        references_list: List[str],
        artwork_list: List[str],
        additional_info: List[str],
        authority: Optional[str],
        file_name: str,
    ):
        """
        Initialize a Person object.

        :param publication_date: The publication date of the person record.
        :param namespace: The XML namespace.
        :param full_name: The full name of the person.
        :param first_name: The first name of the person.
        :param last_name: The last name of the person.
        :param references_list: A list of references related to the person.
        :param artwork_list: A list of artworks related to the person.
        :param additional_info: Additional information about the person.
        :param authority: The authority of the person (can be None).
        :param file_name: The file name of the person record.
        """
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

    def to_json(self) -> str:
        """Convert the object to a JSON string."""
        return json.dumps(self.__dict__, indent=2)