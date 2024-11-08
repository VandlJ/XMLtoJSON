from xml.dom import minidom
import re
from model.Document import Document


def getNames(element):
    names = []

    for node in element.childNodes:
        if node.nodeName == "a":
            tmp = {}
            name = node.childNodes[0].data
            name_key_string = node.attributes["href"].childNodes[0].data
            name_key = name_key_string[9:].split(".xml")[0]
            tmp[name_key] = name
            names.append(tmp)

    return names


def getText(element):
    text = ""

    for node in element.childNodes:
        if len(node.childNodes) == 0:
            if node.nodeName == "#text":
                text = text + node.data
        else:
            if node.tagName == "ol" or node.tagName == "ul":
                parts = node.childNodes[0].data.split("\n")
                text = text + "<" + node.tagName + ">"
                for part in parts:
                    if part != "":
                        text = text + "<" + "li" + ">" + part + "</" + "li" + ">"
                text = text + "<" + node.tagName + ">"
            else:
                text = text + "<" + node.tagName + ">" + node.childNodes[0].data + "</" + node.tagName + ">"

    return text


def getArchive(element):
    archives = {}

    # Iterate over the a elements
    for node in element.childNodes:
        if node.nodeName == "a":
            # Extract the archive code and name from the href attribute using a regular expression
            match = re.match(r'\.\./Archiv/A_(\d+)_(.+?)\.xml', node.attributes["href"].childNodes[0].data)
            if match:
                archive_name = node.childNodes[0].data
                # Add the archive code and name to the dictionary
                code, name = match.groups()
                code_name = "A_" + str(code) + "_" + name
                archives[code_name] = archive_name

    return archives


def getMetadataOfText(text):
    metaD = []
    parts = text.split("\n")
    for part in parts:
        if part == "":
            continue
        metaD.append(part)

    return metaD


def getReferredIn(text):
    reference = ""
    for part in text.split("\n"):
        if part == "":
            continue
        words = part.split(" ")
        if words[0] == "Copyright":
            continue
        else:
            reference = part

    return reference


def parseDocumentXML(filePath):

    # doc = minidom.parse("../test_data/Regesten/A1570-00-00-00013.xml")
    doc = minidom.parse(filePath)

    uri = doc.childNodes[1].attributes["uri"].childNodes[0].data
    publication_date = doc.childNodes[1].attributes["v"].childNodes[0].data
    namespace = doc.childNodes[1].attributes["xmlns"].childNodes[0].data

    # split the text by the hyphen character
    parts = uri.split('-')

    # the date is the second and third parts, in the format 'YYYY/MM/DD'
    date = f"{parts[0][1:]}-{parts[1]}-{parts[2]}"

    # the identification number is the fourth part
    index = parts[-1]

    title = ""
    names = {}
    text = ""
    archives = {}
    archives["None"] = "None"
    metaData = []
    referredIn = []
    copyRight = doc.childNodes[1].childNodes[-1].data.split("\n")[-2]

    for element in doc.childNodes[1].childNodes:
        if element.nodeName == "#text" and element.data.strip() == "":
            continue
        if element.nodeName == "title":
            title = element.childNodes[0].data
        if element.nodeName == "div":
            if element.attributes["class"].nodeValue == "namindex":
                names = getNames(element)
            if element.attributes["class"].nodeValue == "zitat":
                text = getText(element)
            if element.attributes["class"].nodeValue == "archiv":
                archives = getArchive(element)
        if element.nodeName == "#text":
            if element.previousSibling.nodeName == "title":
                metaData = getMetadataOfText(element.data)
            if element.previousSibling.nodeName == "div":
                referredIn.append(getReferredIn(element.data))

    return Document(
            uri=uri,
            publication_date=publication_date,
            date=date,
            index=index,
            namespace=namespace,
            title=title,
            archives=archives,
            referedIn=referredIn,
            text=text,
            names=names,
            copyRight=copyRight,
            metaData=metaData
        )
