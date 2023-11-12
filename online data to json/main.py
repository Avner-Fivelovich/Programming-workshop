from shufersal_downloader import shufersal_downloader
from GZ_extractor import gz_extractor

# Define directories for XML, JSON, and GZ files
xml_dir = "XML files"
json_dir = "JSON files"
gz_dir = "GZ files"

# Download files from shufersal prices website and organize them into the shufersal directories
shufersal_downloader()

gz_extractor(gz_dir, xml_dir,json_dir)