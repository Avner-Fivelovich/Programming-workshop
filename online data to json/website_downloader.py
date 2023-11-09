import requests
from bs4 import BeautifulSoup
import os


# Function to download files from the webpage
def download_files(base_dir, local_file_urls, local_branch_names):
    for file_url, branch_name in zip(local_file_urls, local_branch_names):
        if branch_name:
            file_name = file_url.split("/")[-1]
            sanitized_branch_name = branch_name.replace(' ', '_').replace('"', '').replace("'", '')
            # Remove everything after ".gz" in the file name
            gz_index = file_name.find('.gz')
            if gz_index != -1:
                sanitized_file_name = file_name[:gz_index + 3]
            else:
                sanitized_file_name = file_name
            branch_dir = os.path.join(base_dir, sanitized_branch_name)
            os.makedirs(branch_dir, exist_ok=True)
            file_path = os.path.join(branch_dir, sanitized_file_name)

            # Download the file
            response = requests.get(file_url)
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"File downloaded: {file_path}")
            else:
                print(f"Failed to download file from {file_url}. Status code: {response.status_code}")


# Function to parse HTML table and extract file URLs and branch names
def parse_html_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='webgrid')

    local_file_urls = []
    local_branch_names = []

    if table:
        for row in table.find_all('tr',
                                  class_=lambda x: x and ('webgrid-row-style' in x or 'webgrid-alternating-row' in x)):
            columns = row.find_all('td')
            if len(columns) >= 7:
                file_url = columns[0].find('a')['href']
                branch_name = columns[5].text.strip()
                local_file_urls.append(file_url)
                local_branch_names.append(branch_name)

    return local_file_urls, local_branch_names
