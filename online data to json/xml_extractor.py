# xml_extractor.py

import os
import gzip
import tarfile


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

            # Delete the GZ file after successful extraction of all files
            os.remove(target_gz_file)
