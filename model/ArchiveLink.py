import json
from typing import List


class ArchiveLinkEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ArchiveLink):
            sublinks = obj.sublinks if obj.sublinks is not None else []
            return {
                "name": obj.name,
                "hasSublink": obj.hasSublink,
                "linkTo": obj.linkTo,
                "next_link": obj.next_link,
                "sublinks": [self.default(sublink) for sublink in sublinks],
            }
        return json.JSONEncoder.default(self, obj)


class ArchiveLink:
    def __init__(
        self,
        name: str,
        hasSublink: bool = False,
        linkTo: str = None,
        sublinks: List[object] = None,
    ):
        self.name = name
        self.hasSublink = hasSublink
        self.linkTo = linkTo
        self.sublinks = sublinks
        self.next_link = None

    def to_json(self):
        # Convert the object to a dictionary
        obj_dict = self.__dict__

        # Return the dictionary as a JSON string
        return json.dumps(obj_dict, cls=ArchiveLinkEncoder, indent=2)

    # NOTE: This is not used anywhere, wtf?
    def set_next(self, next_link):
        # implement a method to set the 'next' link
        self.next = next_link
