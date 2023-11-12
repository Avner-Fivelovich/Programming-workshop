import os
import gzip
import tarfile
# from xml_to_json_converter import convert_xml_to_json


# Iterate over GZ files and extract XML, perform checks, and delete GZ file
def gz_extractor(gz_dir: str, xml_dir: str, json_dir: str):
    for gz_file in os.listdir(gz_dir):
        if gz_file.endswith(".gz"):
            gz_path = os.path.join(gz_dir, gz_file)

            # Extract XML from GZ, perform checks, and delete GZ file
            extract_xml_from_gz(gz_path, xml_dir)


"""
    TO DO: this file as of now only extract the XML file from all of the gz files in the gz dir.
        i need to decide what to do with the gz after extraction and exactly how to convert the xml to json
        
        # Iterate over XML files and convert each to JSON
    for xml_file in os.listdir(xml_dir):
        if xml_file.endswith(".xml"):
            xml_path = os.path.join(xml_dir, xml_file)

            # Generate corresponding JSON file name by replacing '.xml' with '.json'
            json_file = os.path.join(json_dir, os.path.splitext(xml_file)[0] + ".json")

            # Convert XML to JSON
            convert_xml_to_json(xml_path, json_file)
"""


def extract_xml_from_gz(target_gz_file, target_xml_dir):
    with gzip.open(target_gz_file, 'rb') as gz_content:
        with tarfile.open(fileobj=gz_content, mode="r:gz") as tar:
            # Extract each file from the tar archive
            for member in tar.getmembers():
                if not member.name.endswith(".xml"):
                    print(f"The file in {target_gz_file} is not an XML file: {member.name}")
                    continue

                # Extract the file content as bytes
                xml_content_bytes = tar.extractfile(member).read()

                # Decode the bytes to UTF-8
                xml_content = xml_content_bytes.decode('utf-8')

                # Create the XML file path
                xml_file_path = os.path.join(target_xml_dir, member.name)

                # Write the XML content to the XML file
                with open(xml_file_path, 'w', encoding='utf-8') as xml_file:
                    xml_file.write(xml_content)


""" 
Explanation:

Import Statements:
    1. import os: Imports the os module for interacting with the operating system (e.g., file operations).
    2. from xml_extractor import extract_xml_from_gz: 
        Imports the extract_xml_from_gz function from the xml_extractor module.
    3. from xml_to_json_converter import convert_xml_to_json: 
        Imports the convert_xml_to_json function from the xml_to_json_converter module.

Directory Definitions:
    1. xml_dir, json_dir, and gz_dir: Variables holding the directory paths for XML, JSON, and GZ files, respectively.

GZ File Processing:
    1. for gz_file in os.listdir(gz_dir):: Iterates over files in the GZ directory.
    2. if gz_file.endswith(".gz"):: Checks if the file has a ".gz" extension.
    3. gz_path = os.path.join(gz_dir, gz_file): 
        Combines the directory path and the file name to create the full path to the GZ file.
    4. extract_xml_from_gz(gz_path, xml_dir): 
        Calls the extract_xml_from_gz function to extract XML from the GZ file, perform checks, and delete the GZ file.

XML to JSON Conversion:
    1. for xml_file in os.listdir(xml_dir):: Iterates over files in the XML directory.
    2. if xml_file.endswith(".xml"):: Checks if the file has a ".xml" extension.
    3. xml_path = os.path.join(xml_dir, xml_file): 
        Combines the directory path and the file name to create the full path to the XML file.
    4. json_file = os.path.join(json_dir, os.path.splitext(xml_file)[0] + ".json"): 
        Generates the corresponding JSON file name by replacing '.xml' with '.json'.
    5. convert_xml_to_json(xml_path, json_file): Calls the convert_xml_to_json function to convert XML to JSON. 
"""