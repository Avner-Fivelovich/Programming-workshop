import os
import requests
from xml_extractor import extract_xml_from_gz
from xml_to_json_converter import convert_xml_to_json
from website_downloader import download_files, parse_html_table
import requests


# Define directories for XML, JSON, and GZ files
xml_dir = "XML files"
json_dir = "JSON files"
gz_dir = "GZ files"

# Replace 'websites URLs.txt' with the path to your file containing URLs
#### url_file_path = 'websites URLs.txt'

# Call the function from website_downloader.py
##### download_files(url_file_path)

# URL of the webpage with the table
url = "http://prices.shufersal.co.il/"

# Download webpage content
html_content = requests.get(url).content

# Parse HTML table and get file URLs and branch names
file_urls, branch_names = parse_html_table(html_content)

# Download files and organize them into directories
download_files(gz_dir, file_urls, branch_names)




'''
# Iterate over GZ files and extract XML, perform checks, and delete GZ file
for gz_file in os.listdir(gz_dir):
    if gz_file.endswith(".gz"):
        gz_path = os.path.join(gz_dir, gz_file)

        # Extract XML from GZ, perform checks, and delete GZ file
        extract_xml_from_gz(gz_path, xml_dir)

# Iterate over XML files and convert each to JSON
for xml_file in os.listdir(xml_dir):
    if xml_file.endswith(".xml"):
        xml_path = os.path.join(xml_dir, xml_file)

        # Generate corresponding JSON file name by replacing '.xml' with '.json'
        json_file = os.path.join(json_dir, os.path.splitext(xml_file)[0] + ".json")

        # Convert XML to JSON
        convert_xml_to_json(xml_path, json_file)
'''


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