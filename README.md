# XMLtoJSON - Documentaria Rudolphina

**Documentaria Rudolphina** is a project focused on managing and analyzing historical records stored in **XML** files. The goal is to provide digital access to historical documents through an archive that enables efficient searching, navigation, and display of archival records.

## Contents

- [XMLtoJSON - Documentaria Rudolphina](#xmltojson---documentaria-rudolphina)
  - [Contents](#contents)
  - [Project Overview](#project-overview)
  - [Project Structure](#project-structure)
  - [XML to JSON Transformation](#xml-to-json-transformation)
  - [Application Design](#application-design)
  - [Future Directions](#future-directions)

## Project Overview

The goal of this project is to create an archive application with features for full-text search and record browsing based on categories such as location, names, and timeframes. Each archival document should have a unique URL for citation purposes, and it is necessary to track changes in the data for accountability. Additionally, the archive will integrate with an authority database, allowing prioritization and standardization of results.

## Project Structure

The project contains four primary XML directories:

- **Archive**: A tree of locations representing the hierarchical structure of the archive with nine levels of nesting. Each record includes references to document transcriptions stored in the *Regesten* directory.
- **Indices**: Alphabetized lists of people that link to *Namen*, which provides further information on individuals. The detail view for each person includes links to specific record transcriptions in *Regesten*.
- **Namen**: Information on historical figures, including details like birth and death dates and a list of works in which they are mentioned.
- **Regesten**: Individual transcriptions of historical texts accessible through links from other sections of the archive.

All XML files are transformed into **HTML** using XSLT stylesheets, making them easier to view on web pages.

## XML to JSON Transformation

To optimize data handling, a transformation of XML files to **JSON** format was proposed, with storage in **MongoDB**. The project is organized into three main JSON collections:

1. **Person**: Contains data on individuals, including names and supplementary information like birth dates and work listings.
2. **Artwork**: Represents historical documents (originally from *Regesten*) with metadata such as title, document text, and archive references.
3. **ArchiveLinks**: Preserves the hierarchical archive structure, allowing clear display and navigation within the archive.

## Application Design

Based on analysis, two design options were proposed:

1. **Preserving the existing structure**: Restyling the current web application with added search functionality.
2. **Building a new system**: Using a modern three-layer architecture with frontend-backend-database, where the front end leverages libraries such as **React** and **SemanticUI**.

User interface designs were created in Figma, focusing on intuitive navigation and fast search within the archive.

## Future Directions

- Integrate APIs to connect with additional authority databases.
- Optimize data structures for faster search and retrieval.
- Add support for multiple languages and encodings, including non-ASCII characters for accurate representation of historical texts.

This project aims to expand further with new features and optimizations, making historical data more accessible and manageable.
