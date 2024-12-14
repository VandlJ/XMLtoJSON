import os
import xml.etree.ElementTree as ET
from model.ArchiveLink import ArchiveLink

# Define XML namespaces
namespace = {
    "dr": "http://documenta.rudolphina.org/",
    "xhtml": "http://www.w3.org/1999/xhtml",
}

def file_exists(file_path):
    """Check if a file exists and is a valid file."""
    return os.path.exists(file_path) and os.path.isfile(file_path)

async def parse_xml(xml_file):
    """Parse an XML file and return its root element."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return root

async def convert_to_json(xml_root, processed_links, data_folder):
    """Convert an XML root element to JSON, handling sublinks."""
    link_to = xml_root.get("uri")

    # Avoid processing the same link multiple times
    if link_to in processed_links:
        return None

    processed_links.add(link_to)

    # Find all <ul> elements containing <a> tags
    ul_elements = xml_root.findall(".//xhtml:ul", namespaces=namespace)[0].findall(
        ".//xhtml:a", namespaces=namespace
    )
    has_sublink = len(ul_elements) > 0

    # Create a dictionary to hold JSON data
    json_data = {
        "name": xml_root.find(".//xhtml:title", namespaces=namespace).text,
        "hasSublink": has_sublink,
        "linkTo": link_to,
        "sublinks": [],
    }

    subs = []

    # Process <ul> elements and convert them to sublinks
    for ul_element in xml_root.findall(".//xhtml:ul", namespaces=namespace):
        for a_tag in ul_element.findall(".//xhtml:a", namespaces=namespace):
            link_to_res = a_tag.get("href").replace("../", "")
            base_name = os.path.basename(link_to_res)
            link, _ = os.path.splitext(base_name)

            xml_file = os.path.join(data_folder, f"{link}.xml")
            if file_exists(xml_file):
                sublink_data = await convert_to_json(await parse_xml(xml_file), processed_links, data_folder)

                if sublink_data:
                    subs.append(sublink_data)

    # Return an ArchiveLink object with the JSON data
    return ArchiveLink(
        json_data["name"], json_data["hasSublink"], json_data["linkTo"], subs
    )

def set_next_links(archive_link):
    """Set the `next_link` attribute for sequential sublinks."""
    for i in range(len(archive_link.sublinks) - 1):
        archive_link.sublinks[i].next_link = archive_link.sublinks[i + 1].linkTo
        set_next_links(archive_link.sublinks[i])
    if archive_link.sublinks:
        set_next_links(archive_link.sublinks[-1])

async def parseArchiveLinkXML(in_file, data_folder):
    """Parse a single XML file and convert it to a JSON-compatible object."""
    processed_links = set()
    root = await parse_xml(in_file)
    archive_link = await convert_to_json(root, processed_links, data_folder)
    set_next_links(archive_link)
    return archive_link