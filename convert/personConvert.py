import os
from xml.dom import minidom
from model.Person import Person
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON


def get_additional_info(artist):
    query = """
    select ?Subject ?Term {
        ?Subject a gvp:PersonConcept; luc:term ' "%s" ';
        gvp:prefLabelGVP [xl:literalForm ?Term].
    }
    """ % artist

    sparql = SPARQLWrapper("http://vocab.getty.edu/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    additional_info = []
    try:
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            uri = result["Subject"]["value"]
            full_name = result["Term"]["value"]
            last_name, first_name = get_name(full_name)
            additional_info.append(
                {
                    "uri": uri,
                    "full_name": full_name,
                    "last_name": last_name,
                    "first_name": first_name
                }
            )
    except Exception as e:
        print(f"An error occurred when querying name {artist}: {e}")
    return additional_info


def get_name(name):
    """Extract first and last names from a name string."""
    if "," in name:
        names = name.split(",")
        last_name = names[0].strip()
        first_name = names[1].strip()
    else:
        last_name = name.strip()
        first_name = ""
    return last_name, first_name


def get_references_list(element):
    """Parse reference list from the XML."""
    references = []
    for child in element.getElementsByTagName("a"):
        try:
            href = child.getAttribute("href").split("/")[-1].rsplit(".", 1)[0]
            title = child.getAttribute("title")
            date = child.firstChild.data.strip() if child.firstChild else ""
            references.append({"title": title, "uri": href, "date": date})
        except Exception as e:
            print(f"Error processing reference: {e}")
    return references


def parse_person_xml(file_path: str, data_folder: str) -> Person:
    """Parse XML and return a Person object."""
    try:
        doc = minidom.parse(file_path)

        # Extract top-level attributes
        publication_date = doc.documentElement.getAttribute("v")
        namespace = doc.documentElement.getAttribute("xmlns")

        file_name = os.path.basename(file_path).rsplit(".", 1)[0]

        # Initialize person fields
        full_name = ""
        first_name = ""
        last_name = ""
        references_list = []
        artwork_list = []
        additional_info = []

        # Process child nodes
        for element in doc.documentElement.childNodes:
            if element.nodeType == element.TEXT_NODE and not element.data.strip():
                continue
            if element.nodeName == "title":
                last_name, first_name = get_name(
                    element.firstChild.data.strip())
            elif element.nodeName == "h3":
                full_name = element.firstChild.data.strip()
                additional_info = get_additional_info(full_name)
            elif element.nodeName == "div" and element.getAttribute("class") == "docindex":
                references_list = get_references_list(element)

        return Person(
            publication_date=publication_date,
            namespace=namespace,
            full_name=full_name,
            first_name=first_name,
            last_name=last_name,
            references_list=references_list,
            artwork_list=artwork_list,
            additional_info=additional_info,
            file_name=file_name,
            authority=None,
        )
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None
