import json
from typing import List

class ArchiveLinkEncoder(json.JSONEncoder):
    def default(self, obj):
        """Override the default method to serialize ArchiveLink objects."""
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
        """
        Initialize an ArchiveLink object.

        :param name: The name of the archive link.
        :param hasSublink: Boolean indicating if the link has sublinks.
        :param linkTo: The URI the link points to.
        :param sublinks: A list of sublinks.
        """
        self.name = name
        self.hasSublink = hasSublink
        self.linkTo = linkTo
        self.sublinks = sublinks
        self.next_link = None

    def to_json(self):
        """Convert the object to a JSON string."""
        return json.dumps(self, cls=ArchiveLinkEncoder, indent=2)

    def set_next(self, next_link):
        """Set the next link."""
        self.next_link = next_link