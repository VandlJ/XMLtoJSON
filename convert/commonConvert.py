import xml.etree.ElementTree as ET

def getNamespace(tree: ET.ElementTree) -> str:
    """Extract the namespace from an XML tree."""
    namespace = ""

    # Iterate over elements in the tree
    for element in tree.iter():
        # Skip the root element
        if element == tree.getroot():
            continue
        # Get the namespace of the element
        namespace = element.tag[1:].split("}")[0]
        break

    return namespace