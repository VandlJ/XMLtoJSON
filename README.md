# XML to JSON Converter

## Table of Contents
- [XML to JSON Converter](#xml-to-json-converter)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Repository Structure](#repository-structure)
  - [Usage](#usage)
    - [Input Data Folder Structure](#input-data-folder-structure)
  - [Setup Instructions](#setup-instructions)
    - [Step 1: Clone the Repository](#step-1-clone-the-repository)
    - [Step 2: Run the Conversion](#step-2-run-the-conversion)

---

## Overview
This project provides a set of scripts and tools for converting XML files into JSON format. It is designed to work with different XML data sources and is fully customizable, supporting multiple conversion modules. The project is divided into separate Python modules for handling different kinds of data, including documents, persons, and archives.

The solution includes:
- Various XML parsing methods for extracting data from different types of XML files.
- Tools to handle specific document types like archives, artwork, and persons.
- A flexible structure for easy conversion and integration with other systems.

## Features
- **Custom Conversion Scripts**: Designed for different XML formats, including documents, persons, and archive links.
- **Flexible Data Handling**: The ability to handle text, metadata, and specific attributes such as aliases and references.
- **Modular Structure**: Each XML type is handled by separate scripts, making it easy to extend or modify.

## Repository Structure

```bash
convert/
  archiveLinkConvert.py      # Handles conversion of archive link XMLs
  artworkConvert.py          # Handles artwork XML data
  commonConvert.py           # Contains common conversion utilities
  personConvert.py           # Handles conversion of person-related XMLs
docs/
  pictures/                  # Picture documentation related to the project
  Analyza_SP.md              # Analysis related documentation
  documentaria_rudolphina.md # Project-specific documentation
model/
  ArchiveLink.py             # Data model for archive links
  Document.py                # Data model for documents
  Person.py                  # Data model for person records
scripts/
  main_convert.py            # Main script to execute conversion
  .gitignore                 # Git ignore configuration
  README.md                  # This documentation file
```

## Usage

To use this tool, you'll need Python and pip installed.

Then, run the following command:

```bash
pip install -r requirements.txt
```

This will install necessary libraries to run the script. Then simply run the `main_convert.py` script with the appropriate options. Here are the main commands to run the program from the `XMLtoJSON` directory:

- Display help information:
  ```bash
  python3 scripts/main_convert.py --help
  ```
  or
  ```bash
  python3 scripts/main_convert.py --h
  ```

- Convert all types of XML files:
  ```bash
  python3 scripts/main_convert.py --type all --input_path "path_for_input_data" --output_path "path_for_output_data"
  ```

- Convert name-related XML files:
  ```bash
  python3 scripts/main_convert.py --type names --input_path "path_for_input_data" --output_path "path_for_output_data"
  ```

- Convert register-related XML files:
  ```bash
  python3 scripts/main_convert.py --type registers --input_path "path_for_input_data" --output_path "path_for_output_data"
  ```

- Convert archive-related XML files:
  ```bash
  python3 scripts/main_convert.py --type archive --input_path "path_for_input_data" --output_path "path_for_output_data"
  ```

### Input Data Folder Structure

The input data folder should be structured as follows:

```bash
input_data/
  Archiv/                    # Archive-related XML files
  Regesten/                  # Register-related XML files
  Namen/                     # Name-related XML files
  Indicies/                  # Index-related XML files 
```

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/VandlJ.git
cd XMLtoJSON
```

### Step 2: Run the Conversion

To begin the conversion, use the main conversion script. For example, to convert all XML files:
```bash
python3 scripts/main_convert.py --type all --input_path "../test_data" --output_path "../test_data/output"
```

You can also check out all available options and get detailed information by running:
```bash
python3 scripts/main_convert.py --help
```

This command will start processing the XML files in the specified `--input_path` directory and output the results to the `--output_path` directory.