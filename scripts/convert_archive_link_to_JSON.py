import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from convert.archiveLinkConvert import parseArchiveLinkXML

from model.ArchiveLink import ArchiveLink

# Set the path to the input and output folders
input_folder = "../test_data/Archiv"
output_folder = "../test_data/Archiv_JSON/"

# Create the output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

#input_file_path = "../test_data/Archiv/A_0_Archive.xml"
#output_file_path = "../test_data/Archiv_Link_JSON/LinkStructure.json"
#output_file_path = "../test_data/Archiv_Link_JSON/ArchiveA0.json"


# Iterate through the files in the input folder
for file_name in os.listdir(input_folder):
    # Construct the full paths to the input and output files
    input_file_path = os.path.join(input_folder, file_name)
    output_file_path = os.path.join(output_folder, file_name[:-4] + ".json")
    print(input_file_path)
    print(output_file_path)
    al = parseArchiveLinkXML(input_file_path)
    with open(output_file_path, "w") as output_file:
        output_file.write(al.to_json())
    print("Done")




