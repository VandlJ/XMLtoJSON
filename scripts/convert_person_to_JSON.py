import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from convert.personConvert import parsePersonXML

# Set the path to the input and output folders
input_folder = "../test_data/Namen"
output_folder = "../test_data/Namen_JSON"

# Create the output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

# Iterate through the files in the input folder
for file_name in os.listdir(input_folder):
    # Construct the full paths to the input and output files
    input_file_path = os.path.join(input_folder, file_name)
    output_file_path = os.path.join(output_folder, file_name[:-4] + ".json")

    modified_text = parsePersonXML(input_file_path).to_json()
    # Open the output file

    with open(output_file_path, "w") as output_file:
        # Write the modified text to the output file
        output_file.write(modified_text)
