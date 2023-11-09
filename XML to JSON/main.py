import os
import json
import xml.etree.ElementTree as ET
from xml_extractor import extract_xml_from_gz

xml_dir = "XML files"
json_dir = "JSON files"
gz_dir = "GZ files"


def convert_element_to_dict(element):
    result = {}

    for child in element:
        child_data = convert_element_to_dict(child)

        # Check if the key already exists
        if child.tag in result:
            # Convert to a list if there are multiple occurrences of the same tag
            if isinstance(result[child.tag], list):
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data

    if not result:
        return element.text
    return result


def convert_xml_to_json(target_xml_file, target_json_file):
    tree = ET.parse(target_xml_file)
    root = tree.getroot()

    # Convert XML to a dictionary
    xml_data = {root.tag: convert_element_to_dict(root)}

    # Dump the dictionary to a JSON file without escaping non-ASCII characters
    with open(target_json_file, "w", encoding="utf-8") as json_output:
        json.dump(xml_data, json_output, indent=2, ensure_ascii=False)


for gz_file in os.listdir(gz_dir):
    if gz_file.endswith(".gz"):
        gz_path = os.path.join(gz_dir, gz_file)

        # Extract XML from GZ, perform checks, and delete GZ file
        extract_xml_from_gz(gz_path, xml_dir)

for xml_file in os.listdir(xml_dir):
    if xml_file.endswith(".xml"):
        xml_path = os.path.join(xml_dir, xml_file)

        # Generate corresponding JSON file name
        json_file = os.path.join(json_dir, os.path.splitext(xml_file)[0] + ".json")

        # Convert XML to JSON
        convert_xml_to_json(xml_path, json_file)
