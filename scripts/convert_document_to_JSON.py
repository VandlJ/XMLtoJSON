from convert.artworkConvert import parseDocumentXML
import os

# Set the path to the input and output folders
input_folder = "../test_data/Regesten"  # not in gitlab (too large)
output_folder = "../test_data/Regesten_JSON_test"

# Iterate through the files in the input folder
for file_name in os.listdir(input_folder):
    # Construct the full paths to the input and output files
    input_file_path = os.path.join(input_folder, file_name)
    output_file_path = os.path.join(output_folder, file_name[:-4] + ".json")

    modified_text = parseDocumentXML(input_file_path).to_json()
    # Open the output file
    with open(output_file_path, "w") as output_file:
        # Write the modified text to the output file
        output_file.write(modified_text)

print("Transformation from XML in {0} to JSON {1} in is Done.".format(input_folder, output_folder))
