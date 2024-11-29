input("Нажмите Enter для запуска программы")

import os
# Install required packages via pip if not already installed
os.system("pip install requests")
os.system("pip install openpyxl")

import requests
import openpyxl

def download_file_from_google_drive(file_id, destination):
    # Create a session to handle cookies
    session = requests.Session()
    
    # Get the confirmation token
    url = f"https://drive.google.com/uc?id={file_id}"
    response = session.get(url, params={'confirm': 't'}, stream=True)
    
    # Check if the response is valid
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"Downloaded: {destination}")
    else:
        print(f"Failed to download: {destination}")

def extract_file_id(google_drive_link):
    # Extract the file ID from the Google Drive link
    if "drive.google.com" in google_drive_link:
        if "/d/" in google_drive_link:
            return google_drive_link.split("/d/")[1].split("/")[0]
        elif "file/d/" in google_drive_link:
            return google_drive_link.split("/d/")[1].split("/")[0]
    return None

def main():
    # Load the workbook and select the active sheet
    workbook = openpyxl.load_workbook('gdrive_links.xlsx')
    sheet = workbook.active
    
    for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
        link = row[0]  # Assuming the link is in the first column
        filename = row[1]  # Assuming the filename is in the second column
        extension = row[2]  # Assuming the extension is in the third column
        
        file_id = extract_file_id(link)
        if file_id:
            destination = os.path.join(os.getcwd(), f"{filename}.{extension}")  # Use filename and extension
            download_file_from_google_drive(file_id, destination)
        else:
            print(f"Invalid link: {link}")

if __name__ == "__main__":
    main()

input("Файлы загружены. Нажмите Enter для закрытия окна")

# softy_plug