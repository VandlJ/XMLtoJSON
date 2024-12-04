import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from convert.personConvert import parse_person_xml

# Set the path to the input and output folders
input_folder = "../test_data/Namen"
output_folder = "../test_data/Namen_JSON"

# Create the output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

# Iterate through the files in the input folder
for file_name in os.listdir(input_folder):
    if not file_name.endswith(".xml"):
        continue

    # Construct the full paths to the input and output files
    input_file_path = os.path.join(input_folder, file_name)
    output_file_path = os.path.join(output_folder, file_name[:-4] + ".json")

    person = parse_person_xml(input_file_path)
    if person:
        try:
            # Write the JSON output
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(person.to_json())
            print(f"Converted {file_name} to JSON.")
        except Exception as e:
            print(f"Error writing JSON for {file_name}: {e}")
    else:
        print(f"Failed to parse {file_name}.")