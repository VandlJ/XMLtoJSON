import sys
import os
from xml.dom import minidom

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.Person import Person


def getName(name):
    if ',' in name:
        names = name.split(',')
        last_name = names[0]
        first_name = names[1][1:]
    else:
        last_name = name

    return last_name, first_name


def getReferencesList(element):
    reference_list = []
    for childNode in element.childNodes[1:]:
        href = childNode.attributes["href"].childNodes[0].data.split('/')[2].rsplit('.', 1)[0]
        title = childNode.attributes["title"].childNodes[0].data
        date = childNode.childNodes[0].data

        reference_list.append({"title": title,
                               "uri": href,
                               "date": date})
    return reference_list


def getArtworkList(text):
    list = []
    works = text.split("\n")
    for work in works:
        if work.strip() == "":
            continue
        list.append(work.strip())

    return list


def parsePersonXML(filePath: str) -> Person:

    # doc = minidom.parse(filePath)
    doc = minidom.parse("../test_data/Namen/Alexandrin_Julius.xml")

    full_name = ""
    first_name = ""
    last_name = ""

    print("File Path: ", filePath) 

    # file_name = filePath.split('\\')[1].rsplit('.', 1)[0]

    file_name = os.path.basename(filePath).rsplit('.', 1)[0]

    references_list = []
    artwork_list = []
    additional_info = []
    publication_date = doc.childNodes[1].attributes["v"].childNodes[0].data
    namespace = doc.childNodes[1].attributes["xmlns"].childNodes[0].data

    for element in doc.childNodes[1].childNodes:
        if element.nodeName == "#text" and element.data.strip() == "":
            continue
        if element.nodeName == "title":
            last_name, first_name = getName(element.childNodes[0].data)
        elif element.nodeName == "h3":
            full_name = element.childNodes[0].data
        elif element.previousSibling.nodeName == "h3":
            additional_info.append(element.data.strip())
        elif element.previousSibling.nodeName == "br":
            additional_info.append(element.data.strip())
        elif element.nodeName == "div":
            if element.attributes["class"].nodeValue == "docindex":
                references_list = getReferencesList(element)
        elif element.nodeName == "ul":
            artwork_list = getArtworkList(element.childNodes[0].data)

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
        authority=None
        )

# def parsePersonXML(xmlString : str) -> Person:
#
#     # parse the XML file
#     tree = ET.ElementTree(ET.fromstring(xmlString))
#
#     root = tree.getroot()
#
#     publication_date = root.attrib['v']
#
#     namespace = getNamespace(tree)
#
#     full_name = tree.find('.//{' + namespace + '}h3').text
#
#     first_name = ""
#     last_name = ""
#
#     short_name = tree.find('.//{' + namespace + '}title').text
#     if ',' in short_name:
#         names = short_name.split(',')
#         last_name = names[0]
#         first_name = names[1][1:]
#     else:
#         last_name = short_name
#
#     references_list = getReferencesList(tree, namespace)
#
#     artwork_list = getArtworkList(tree, namespace)
#
#     additional_info = getAdditionalInfo(tree, namespace)
#
#     return Person(
#         publication_date=publication_date,
#         namespace=namespace,
#         full_name=full_name,
#         first_name=first_name,
#         last_name=last_name,
#         references_list=references_list,
#         artwork_list=artwork_list,
#         additional_info=additional_info,
#         authority=None
#     )
#
#
# def getAdditionalInfo(tree : ET, namespace : str):
#
#     # Get the root element
#     root = tree.getroot()
#
#     additionalinfo = []
#
#     # Find the h3 element
#     h3_element = root.find('.//{' + namespace + '}h3')
#
#     next_element = h3_element.tail
#
#     if(next_element == None):
#         return additionalinfo
#
#     elements = next_element.split("\n")
#
#     for i in range(1, len(elements)-1):
#         additionalinfo.append(elements[i])
#
#     # look for br elements as well
#     if(len(additionalinfo) > 0):
#         br_elements = root.findall('.//{' + namespace + '}br')
#
#         for br_element in br_elements:
#             additionalinfo.append(br_element.tail.split("\n")[0])
#
#     return additionalinfo
#
#
# def getArtworkList(tree : ET, namespace : str):
#
#     ul_element = tree.find('.//{' + namespace + '}ul')
#
#     artwork_list = []
#
#     if(ul_element != None):
#         elements = ul_element.text.split("\n")
#
#         for i in range(1, len(elements)-1):
#             artwork_list.append(elements[i])
#
#     return artwork_list
#
# def getReferencesList(tree : ET, namespace : str):
#
#     element = tree.find('.//{' + namespace + '}div[@class="docindex"]')
#
#     a_elements = element.findall('.//{' + namespace + '}a')
#
#     # Extract the links and dates from the a elements
#     artwork_list = []
#
#     for a in a_elements:
#         artwork_list.append({"title" : a.get("title"), "date" : a.text, "uri" : a.get("href").split('/')[2].rsplit('.', 1)[0]})
#
#     return artwork_list
