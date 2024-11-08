import xml.etree.ElementTree as ET


def getNamespace(tree : ET) -> str:
    namespace = ""

    # Get second element -> suggested by OPEN AI O.o
    for element in tree.iter():
        # Skip the first element
        if element == tree.getroot():
            continue
        # Get the namespace of the element
        namespace = element.tag[1:].split('}')[0]
        break

    return namespace
