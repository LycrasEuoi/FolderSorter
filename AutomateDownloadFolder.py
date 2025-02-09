#! python3

import os
import math
import datetime as dt

# Constant for the maximum length of file names
MAX_FILENAME_LENGTH = 60

# Function to truncate a file name if it exceeds the maximum length
def truncateFileName(file, max_length=MAX_FILENAME_LENGTH):
    if not file:
        return "Unnamed File"  # Return a default name if the file name is empty
    # Truncate the file name and append "..." if it exceeds the max length
    return file[:max_length - 3] + "..." if len(file) > max_length else file

# Function to print a formatted list of files
def printListOfFiles(fileList):
    if not fileList:
        print("No files found in the specified folder.")  # Display a message if the list is empty
        return

    # Sort the list of files by creation date in descending order (newest first)
    fileList.sort(reverse=True, key=lambda x: x[2])

    # Print the header with file name and date
    print(f'{"Name":<{MAX_FILENAME_LENGTH}}{"Date":>{MAX_FILENAME_LENGTH}}')
    print('-' * (math.ceil(MAX_FILENAME_LENGTH*2.25)))

    previous_date = None  # Track when the creation date changes

    for index, item in enumerate(fileList):
        if item[1] != previous_date:
            print()  # Add a blank line when the date changes
            previous_date = item[1]

        # Print the file with the truncated name and creation date
        print(f'[{index}] {item[0]:<{MAX_FILENAME_LENGTH}}{item[1]:>{MAX_FILENAME_LENGTH}}')

# Function to retrieve a list of files and their metadata
def getListOfFiles(folderPath):
    listOfFilesFormated = []
    with os.scandir(folderPath) as entries:  # Use os.scandir for efficient iteration over files
        for entry in entries:
            if entry.is_file():  # Check if the entry is a file
                shortendFile = truncateFileName(entry.name)  # Truncate the file name if necessary
                creationDate = entry.stat().st_birthtime  # Retrieve the file creation date
                # Format the creation date into a readable string
                creationDateReadable = dt.datetime.fromtimestamp(creationDate).strftime("%Y-%m-%d")
                # Append a tuple containing the file name, formatted date, and creation date timestamp
                listOfFilesFormated.append((shortendFile, creationDateReadable, creationDate))
    return listOfFilesFormated

# Main program loop to process user input
programLoop = True
while programLoop:
    print('Please enter a path to a directory (or type "cancel" to exit):')
    folderPath = input().strip()  # Get the directory path from the user

    if folderPath.lower() == "cancel":  # Check if the user wants to exit the program
        print("Exiting the program.")
        break

    if not os.path.exists(folderPath):  # Check if the path exists
        print(f'\nError: The path "{folderPath}" does not exist. Please try again.\n')
        continue

    if os.path.isfile(folderPath):  # Check if the path is a file
        print(f'\nError: "{folderPath}" is a file, not a directory. Please enter a valid directory path.\n')
        continue

    listOfFilesFormated = getListOfFiles(folderPath)  # Retrieve the list of files
    
    if not listOfFilesFormated:  # Check if the directory is empty
        print("\nThe directory is empty. Please select another directory.\n")
        continue

    printListOfFiles(listOfFilesFormated)  # Print the list of files
