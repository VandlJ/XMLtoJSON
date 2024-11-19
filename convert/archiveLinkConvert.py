import os
import xml.etree.ElementTree as ET

from model.ArchiveLink import ArchiveLink

namespace = {
    "dr": "http://documenta.rudolphina.org/",
    "xhtml": "http://www.w3.org/1999/xhtml",
}
data_folder = "../test_data/Archiv/"


def file_exists(file_path):
    return os.path.exists(file_path) and os.path.isfile(file_path)


def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    return root


def convert_to_json(xml_root, processed_links):
    link_to = xml_root.get("uri")

    if link_to in processed_links:
        return None

    processed_links.add(link_to)

    ul_elements = xml_root.findall(".//xhtml:ul", namespaces=namespace)[0].findall(
        ".//xhtml:a", namespaces=namespace
    )
    cnt = len(ul_elements)
    # hasSublink je nastaveno dle toho, zda daný subjekt má v XML sublinky - né dle toho, zda ty soubory existují
    has_sublink = True if cnt > 0 else False

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

            xml_file = link
            if "test_data" not in xml_file:
                xml_file = f"{data_folder}{xml_file}.xml"
            if file_exists(xml_file):
                sublink_data = convert_to_json(parse_xml(xml_file), processed_links)

                if sublink_data:
                    subs.append(sublink_data)

    al = ArchiveLink(
        json_data["name"], json_data["hasSublink"], json_data["linkTo"], subs
    )

    return al


def set_next_links(archive_links):
    for i in range(len(archive_links[0].sublinks) - 1):
        archive_links[0].sublinks[i].next_link = archive_links[0].sublinks[i + 1].linkTo
    return archive_links[0]


def parseArchiveLinkXML(in_file):
    archive_links = []
    processed_links = set()
    root = parse_xml(in_file)
    data = convert_to_json(root, processed_links)
    archive_links.append(data)

    ret = set_next_links(archive_links)

    return ret


if __name__ == "__main__":
    ## Use this for converting Archives to JSON
    input_directory = "../test_data/Archiv/"
    output_directory = "../test_data/Archiv_JSON/"  # Výstupní soubory budou uloženy do aktuálního adresáře

    # Získání seznamu souborů v adresáři
    files = os.listdir(input_directory)

    # Procházení každého souboru v adresáři
    for file_name in files:
        xml_file_path = os.path.join(input_directory, file_name)
        name = xml_file_path.rsplit("/", 1)[-1]
        name = name.rstrip(".xml")
        name = output_directory + name
        print(xml_file_path)
        print(name)
        print("")
        data3 = parseArchiveLinkXML(xml_file_path)
        with open(name, "w") as output_file2:
            output_file2.write(data3.to_json())
