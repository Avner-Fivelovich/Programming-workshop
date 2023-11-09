import json
import xml.etree.ElementTree as ET


def convert_element_to_dict(element):
    """
    Recursively converts an XML element and its children into a nested dictionary.

    Parameters:
    - element (xml.etree.ElementTree.Element): The XML element to convert.

    Returns:
    - dict: A nested dictionary representing the XML element and its children.
    """
    result = {}

    for child in element:
        child_data = convert_element_to_dict(child)

        if child.tag in result:
            if isinstance(result[child.tag], list):
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data

    # If the element has no children, return its text content
    if not result:
        return element.text
    return result


def convert_xml_to_json(xml_file, json_file):
    """
    Converts an XML file to a JSON file.

    Parameters:
    - xml_file (str): Path to the XML file.
    - json_file (str): Path to the JSON file to be created.
    """
    # Parse the XML file and get the root element
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Convert the XML root element to a nested dictionary
    xml_data = {root.tag: convert_element_to_dict(root)}

    # Write the JSON data to the specified file with indentation for readability
    with open(json_file, "w") as json_output:
        json.dump(xml_data, json_output, indent=2)


"""
convert_element_to_dict Function:
    1. This function recursively converts an XML element and its children into a nested dictionary.
    2. It uses a depth-first approach to traverse the XML tree and build the corresponding dictionary structure.
    3. If an XML element has children with the same tag, it represents them as a list in the dictionary.

convert_xml_to_json Function:
    1. This function converts an entire XML file to a JSON file.
    2. It uses the convert_element_to_dict function to convert the root element of the XML file to a nested dictionary.
    3. The resulting dictionary is then written to a JSON file with specified indentation for readability.
"""