import os
from xml.dom import minidom
from model.Person import Person
import asyncio
from aiocache import Cache
from aiocache.decorators import cached
from aiohttp import ClientSession, ClientTimeout
from tenacity import retry, stop_after_attempt, wait_exponential

cache = Cache(Cache.MEMORY)

@cached(ttl=3600)  # Cache results for 1 hour
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def fetch_additional_info(session, artist):
    query = """
    select ?Subject ?Term {
        ?Subject a gvp:PersonConcept; luc:term ' "%s" ';
        gvp:prefLabelGVP [xl:literalForm ?Term].
    }
    """ % artist

    url = "http://vocab.getty.edu/sparql"
    headers = {"Accept": "application/sparql-results+json"}
    async with session.post(url, data={"query": query}, headers=headers) as response:
        return await response.json()

async def get_additional_info(artist):
    timeout = ClientTimeout(total=60)
    async with ClientSession(timeout=timeout) as session:
        try:
            results = await fetch_additional_info(session, artist)
            additional_info = []
            for result in results["results"]["bindings"]:
                uri = result["Subject"]["value"]
                full_name = result["Term"]["value"]
                last_name, first_name = get_name(full_name)
                additional_info.append(
                    {
                        "uri": uri,
                        "full_name": full_name,
                        "last_name": last_name,
                        "first_name": first_name
                    }
                )
            return additional_info
        except Exception as e:
            print(f"An error occurred when querying name {artist}: {e}")
            return []

def get_name(name):
    """Extract first and last names from a name string."""
    if "," in name:
        names = name.split(",")
        last_name = names[0].strip()
        first_name = names[1].strip()
    else:
        last_name = name.strip()
        first_name = ""
    return last_name, first_name

def get_references_list(element):
    """Parse reference list from the XML."""
    references = []
    for child in element.getElementsByTagName("a"):
        try:
            href = child.getAttribute("href").split("/")[-1].rsplit(".", 1)[0]
            title = child.getAttribute("title")
            date = child.firstChild.data.strip() if child.firstChild else ""
            references.append({"title": title, "uri": href, "date": date})
        except Exception as e:
            print(f"Error processing reference: {e}")
    return references

async def parse_person_xml(file_path: str, data_folder: str) -> Person:
    """Parse XML and return a Person object."""
    try:
        doc = minidom.parse(file_path)

        # Extract top-level attributes
        publication_date = doc.documentElement.getAttribute("v")
        namespace = doc.documentElement.getAttribute("xmlns")

        file_name = os.path.basename(file_path).rsplit(".", 1)[0]

        # Initialize person fields
        full_name = ""
        first_name = ""
        last_name = ""
        references_list = []
        artwork_list = []
        additional_info = []

        # Process child nodes
        for element in doc.documentElement.childNodes:
            if element.nodeType == element.TEXT_NODE and not element.data.strip():
                continue
            if element.nodeName == "title":
                last_name, first_name = get_name(element.firstChild.data.strip())
            elif element.nodeName == "h3":
                full_name = element.firstChild.data.strip()
                additional_info = await get_additional_info(full_name)
            elif element.nodeName == "div" and element.getAttribute("class") == "docindex":
                references_list = get_references_list(element)

        return Person(
            publication_date=publication_date,
            namespace=namespace,
            full_name=full_name,
            first_name=first_name,
            last_name=last_name,
            references_list=references_list,
            artwork_list=artwork_list,
            additional_info=additional_info,
            file_name=file_name,
            authority=None,
        )
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

async def process_file(convert_function, input_file_path, output_file_path, data_folder):
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
    semaphore = asyncio.Semaphore(5)  # Limit the number of concurrent tasks

    async def sem_task(task):
        async with semaphore:
            await task

    for file_name in os.listdir(input_folder):
        if not file_name.endswith(".xml"):  # Skip non-XML files
            continue

        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name[:-4] + ".json")

        task = sem_task(process_file(convert_function, input_file_path, output_file_path, data_folder))
        tasks.append(task)

    await asyncio.gather(*tasks)
    print(f"Conversion complete from {input_folder} to {output_folder}.")