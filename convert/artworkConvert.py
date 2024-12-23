import re
from xml.dom import minidom
from model.Document import Document

async def getNames(element):
    """Extract names and their aliases from the namindex element."""
    names = []

    for node in element.childNodes:
        if node.nodeName == "a":
            name_key_string = node.getAttribute("href")
            name_key = name_key_string.split("/")[-1].rsplit(".xml", 1)[0]
            display_name = node.firstChild.data.strip()  # Get the display name

            # Extract alias from the onmouseover attribute
            onmouseover = node.getAttribute("onmouseover")
            alias_match = re.search(r"highlightWords\(event, '([^']+)'\)", onmouseover)
            alias = alias_match.group(1) if alias_match else None

            # Populate the dictionary
            name_entry = {
                "name_key": name_key,
                "display_name": display_name,
                "alias": alias
            }
            names.append(name_entry)

    return names

async def getText(element):
    """Extract text in two formats: display text and processable text."""
    display_text = ""
    processable_text = ""

    for node in element.childNodes:
        if len(node.childNodes) == 0:
            if node.nodeName == "#text":
                display_text += node.data
                processable_text += " " + node.data.strip()  # Normalize for processing
        else:
            if node.tagName in ["ol", "ul"]:
                parts = node.childNodes[0].data.split("\n")
                display_text += f"<{node.tagName}>"
                for part in parts:
                    if part.strip():
                        display_text += f"<li>{part}</li>"
                        processable_text += " " + part.strip()  # Add plain list items
                display_text += f"</{node.tagName}>"
            else:
                content = node.childNodes[0].data.strip()
                display_text += f"<{node.tagName}>{content}</{node.tagName}>"
                processable_text += " " + content  # Add plain content

    # Final cleanup for processable text
    processable_text = re.sub(r"\s+", " ", processable_text).strip()  # Remove extra spaces

    return display_text, processable_text

async def getArchive(element):
    """Parse archives from the XML."""
    archives = {}

    # Iterate over the a elements
    for node in element.childNodes:
        if node.nodeName == "a":
            # Extract the archive code and name from the href attribute using a regular expression
            match = re.match(
                r"\.\./Archiv/A_(\d+)_(.+?)\.xml",
                node.attributes["href"].childNodes[0].data,
            )
            if match:
                archive_name = node.childNodes[0].data
                # Add the archive code and name to the dictionary
                code, name = match.groups()
                code_name = "A_" + str(code) + "_" + name
                archives[code_name] = archive_name

    return archives

async def getMetadataOfText(text):
    """Parse metadata from text."""
    metaD = []
    parts = text.split("\n")
    for part in parts:
        if part == "":
            continue
        metaD.append(part)

    return metaD

async def getReferredIn(text):
    """Parse references in the text."""
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

async def parseDocumentXML(filePath, data_folder):
    """Parse the XML and extract data."""
    doc = minidom.parse(filePath)

    uri = doc.childNodes[1].attributes["uri"].childNodes[0].data
    publication_date = doc.childNodes[1].attributes["v"].childNodes[0].data
    namespace = doc.childNodes[1].attributes["xmlns"].childNodes[0].data

    # Split the text by the hyphen character
    parts = uri.split("-")

    # The date is the second and third parts, in the format 'YYYY/MM/DD'
    date = f"{parts[0][1:]}-{parts[1]}-{parts[2]}"

    # The identification number is the fourth part
    index = parts[-1]

    title = ""
    names = []
    display_text = ""
    processable_text = ""
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
                names = await getNames(element)
            if element.attributes["class"].nodeValue == "zitat":
                # Extract both versions of the text
                display_text, processable_text = await getText(element)
            if element.attributes["class"].nodeValue == "archiv":
                archives = await getArchive(element)
        if element.nodeName == "#text":
            if element.previousSibling.nodeName == "title":
                metaData = await getMetadataOfText(element.data)
            if element.previousSibling.nodeName == "div":
                referredIn.append(await getReferredIn(element.data))

    return Document(
        uri=uri,
        publication_date=publication_date,
        date=date,
        index=index,
        namespace=namespace,
        title=title,
        archives=archives,
        text={"display": display_text, "processable": processable_text},
        names=names,
        copyRight=copyRight,
        metaData=metaData,
        referedIn=referredIn,
    )