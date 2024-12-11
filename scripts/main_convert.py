import sys
import os
import argparse

# Import the conversion functions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from convert.archiveLinkConvert import parseArchiveLinkXML
from convert.artworkConvert import parseDocumentXML
from convert.personConvert import parse_person_xml

def convert_files(convert_function, input_folder, output_folder, data_folder):
    """Generic function to convert XML files to JSON."""
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists

    for file_name in os.listdir(input_folder):
        if not file_name.endswith(".xml"):  # Skip non-XML files
            continue

        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name[:-4] + ".json")

        try:
            # Call the specific parse function
            # FIXME: This could be multithreaded and waaay faster. This will improve performance drastically when querying the GETTY endpoint.
            parsed_data = convert_function(input_file_path, data_folder)
            if parsed_data:
                # Write the parsed data to a JSON file
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(parsed_data.to_json())
            else:
                print(f"Failed to parse {file_name}.")
        except Exception as e:
            # Print any errors that occur during processing
            print(f"Error processing {file_name}: {e}")

    print(f"Conversion complete from {input_folder} to {output_folder}.")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert XML files to JSON.")
    parser.add_argument(
        "--type",
        choices=["archive", "registers", "names", "all"],
        required=True,
        help="Type of XML files to convert (archive, registers, names, or all).",
    )
    parser.add_argument(
        "--input-path",
        required=True,
        help="Path to the input folder containing XML files.",
    )
    parser.add_argument(
        "--output-path",
        required=True,
        help="Path to the output folder for JSON files.",
    )

    # TODO: Add a flag that specifies whether the program should query for more accurate info at the GETTY dataset.
    #       The conversion is damn fucking slow because of the load of queries we make to the API endpoint.

    args = parser.parse_args()

    # Define subfolder mappings for each type
    type_to_subfolder = {
        "archive": "Archiv",
        "registers": "Regesten",
        "names": "Namen",
    }

    # Dispatch the appropriate function(s) based on the type
    if args.type in ["archive", "all"]:
        print("Converting Archive XML files...")
        convert_files(
            parseArchiveLinkXML,
            os.path.join(args.input_path, type_to_subfolder["archive"]),
            os.path.join(args.output_path, "Archiv_JSON"),
            os.path.join(args.input_path, "Archiv"),
        )

    if args.type in ["registers", "all"]:
        print("Converting Regesten (Document) XML files...")
        convert_files(
            parseDocumentXML,
            os.path.join(args.input_path, type_to_subfolder["registers"]),
            os.path.join(args.output_path, "Regesten_JSON"),
            os.path.join(args.input_path, "Regesten"),
        )

    if args.type in ["names", "all"]:
        print("Converting Names XML files...")
        convert_files(
            parse_person_xml,
            os.path.join(args.input_path, type_to_subfolder["names"]),
            os.path.join(args.output_path, "Namen_JSON"),
            os.path.join(args.input_path, "Names"),
        )

if __name__ == "__main__":
    main()
