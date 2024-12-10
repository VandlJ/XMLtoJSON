# XML to JSON Converter

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Usage](#usage)
- [Setup Instructions](#setup-instructions)
  - [Step 1: CLone the Repository](#step-1-clone-the-repository)
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

To use this tool, simply run the `main_convert.py` script. This will process the XML files in the specified directories and output the converted JSON files.

By default, the script looks for XML files in the `convert/sample/` directory, converts them, and saves the resulting JSON files in the output directory.

```bash
python3 scripts/main_convert.py
```

You can customize the conversion process by specifying options like the type of conversion and input/output paths.

## Setup Instructions

### Step 1: CLone the Repository

```bash
git clone https://github.com/VandlJ.git
cd XLMtoJSON
```

### Step 2: Run the Conversion

To begin the conversion, use the main conversion script. For example, to convert all XML files:
```bash
python3 scripts/main_convert.py --type all --input-path ../test_data --output-path ../test_data/output
```

The `--type` flag allows you to specify the type of conversion you want to perform:
- `archive` – Convert archive-related data.
- `registers` – Convert register-related data.
- `names` – Convert name-related data.
- `all` – Convert all types of data (default for full conversion).
- 
You can also check out all available options and get detailed information by running:
```bash
python3 scripts/main_convert.py --help
```

This command will start processing the XML files in the specified `--input-path` directory and output the results to the `--output-path` directory.
