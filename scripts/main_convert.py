import os
import sys
import argparse
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from convert.archiveLinkConvert import parseArchiveLinkXML
from convert.artworkConvert import parseDocumentXML
from convert.personConvert import parse_person_xml

async def process_file(convert_function, input_file_path, output_file_path, data_folder, semaphore):
    async with semaphore:
        try:
            parsed_data = await convert_function(input_file_path, data_folder)
            if parsed_data:
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(parsed_data.to_json())
            else:
                print(f"Failed to parse {input_file_path}.")
        except Exception as e:
            print(f"Error processing {input_file_path}: {e}")

async def convert_files_async(convert_function, input_folder, output_folder, data_folder):
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists

    tasks = []
    semaphore = asyncio.Semaphore(10)  # Limit the number of concurrent tasks

    for file_name in os.listdir(input_folder):
        if not file_name.endswith(".xml"):  # Skip non-XML files
            continue

        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name[:-4] + ".json")

        task = process_file(convert_function, input_file_path, output_file_path, data_folder, semaphore)
        tasks.append(task)

    await asyncio.gather(*tasks)
    print(f"Conversion complete from {input_folder} to {output_folder}.")

async def main():
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

    args = parser.parse_args()

    type_to_subfolder = {
        "archive": "Archiv",
        "registers": "Regesten",
        "names": "Namen",
    }

    if args.type in ["archive", "all"]:
        print("Converting Archive XML files...")
        await convert_files_async(
            parseArchiveLinkXML,
            os.path.join(args.input_path, type_to_subfolder["archive"]),
            os.path.join(args.output_path, "Archiv_JSON"),
            os.path.join(args.input_path, "Archiv"),
        )

    if args.type in ["registers", "all"]:
        print("Converting Regesten (Document) XML files...")
        await convert_files_async(
            parseDocumentXML,
            os.path.join(args.input_path, type_to_subfolder["registers"]),
            os.path.join(args.output_path, "Regesten_JSON"),
            os.path.join(args.input_path, "Regesten"),
        )

    if args.type in ["names", "all"]:
        print("Converting Names XML files...")
        await convert_files_async(
            parse_person_xml,
            os.path.join(args.input_path, type_to_subfolder["names"]),
            os.path.join(args.output_path, "Namen_JSON"),
            os.path.join(args.input_path, "Names"),
        )

if __name__ == "__main__":
    asyncio.run(main())