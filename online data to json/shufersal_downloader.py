import os
from datetime import datetime
from typing import Optional
import requests
from bs4 import BeautifulSoup


# Orchestrates the download process of files from the Shufersal website.
def shufersal_downloader():
    gz_dir = r"GZ files\shufersal"
    url = "http://prices.shufersal.co.il"
    iterate_through_pages(gz_dir, url)


# Function to iterate through pages and download files until no more pages are available.
def iterate_through_pages(base_dir: str, start_url: str):
    """
    Iterates through pages, downloading files until no more pages are available.

    Args:
    - base_dir (str): Base directory for file downloads.
    - start_url (str): URL of the initial page.

    Prints:
    - Information on file downloads and a message when there are no more pages left.
    """
    current_url = start_url + "?sort=Time&sortdir=DESC"  # adding a decreasing time sort to the starting url
    while current_url:
        if exist_update(get_latest_update(base_dir), current_url):
            response = requests.get(current_url)
            if response.status_code == 200:
                local_file_urls, local_branch_names = parse_html_table(response.text)
                download_files(base_dir, local_file_urls, local_branch_names)
                current_url = start_url + find_next_page_link(response.text)
                if current_url == start_url:
                    print("There are no more pages left.")
                    break
            else:
                print(f"Failed to fetch page: {current_url}. Status code: {response.status_code}")
        else:
            print("There are no updates on shufersal database.")
            break


#    Retrieves the timestamp of the latest update within the specified directory.
def get_latest_update(base_dir: str) -> datetime:
    # Get a list of all files in the directory
    files = [os.path.join(base_dir, f) for f in os.listdir(base_dir)]

    # Get the latest modification time among all files in the directory
    latest_change = max(os.path.getmtime(f) for f in files)

    # Convert the timestamp to a readable date
    latest_change_date = datetime.fromtimestamp(latest_change)

    print("Latest change in the shufersal directory occurred on:", latest_change_date)
    return latest_change_date


# Checks if there are updates on the provided website URL compared to the latest update.
def exist_update(latest_update: datetime, time_sorted_url: str) -> bool:
    response = requests.get(time_sorted_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='webgrid')

        # Get the first row from the table body
        first_row = table.find('tbody').find('tr')

        # Find the cell containing the date
        date_cell = first_row.find_all('td')[1]  # Assuming the date is in the second cell of the row

        date = date_cell.get_text(strip=True) if date_cell else "Date not found"
        date_format = "%m/%d/%Y %I:%M:%S %p"
        date = datetime.strptime(date, date_format)
        print("Date in the first row of shufersal prices website:", date)
        if date > latest_update:
            return True
        else:
            return False
    else:
        print("Failed to fetch data from the URL")
        return False


# Parses HTML content to extract file URLs and corresponding branch names.
def parse_html_table(html: str) -> tuple:
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


# Function to download files from the webpage
def download_files(base_dir: str, local_file_urls: list, local_branch_names: list):
    for file_url, branch_name in zip(local_file_urls, local_branch_names):
        if branch_name:
            file_name = file_url.split("/")[-1]
            sanitized_branch_name = branch_name.replace(' ', '_').replace('"', '.').replace("'", '')
            # Remove everything after ".gz" in the file name
            gz_index = file_name.find('.gz')
            if gz_index != -1:
                sanitized_file_name = file_name[:gz_index + 3]
            else:
                sanitized_file_name = file_name
            branch_dir = os.path.join(base_dir, sanitized_branch_name)
            os.makedirs(branch_dir, exist_ok=True)
            file_path = os.path.join(branch_dir, sanitized_file_name)

            # Check if the file already exists
            if not os.path.exists(file_path):
                # Download the file
                response = requests.get(file_url)
                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"File downloaded: {file_path}")
                else:
                    print(f"Failed to download file from {file_url}. Status code: {response.status_code}")
            else:
                print(f"File already exists: {file_path}")


# Function to find the next page link
def find_next_page_link(html: str) -> Optional[str]:
    """
    Finds the link for the next page in the HTML content.

    Args:
    - html (str): HTML content of the current page.

    Returns:
    - Optional[str]: The URL of the next page if found, otherwise None.
    """
    soup = BeautifulSoup(html, 'html.parser')
    next_link = soup.find('a', string='>')
    if next_link:
        return next_link['href']
    return ""
