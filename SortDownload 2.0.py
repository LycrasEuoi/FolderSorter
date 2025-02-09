import os
import json
import time as t
from datetime import datetime, timedelta, time

from watchdog.events import FileSystemEvent, FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent
from watchdog.observers import Observer

class DownloadFolder:
    CACHE_FILE = os.path.join(os.path.expanduser('~'), 'SortDownload', 'Cache', 'SortDownloadCache.json')
    CACHE_PATH = os.path.join(os.path.expanduser('~'), 'SortDownload', 'Cache')
    OBSERVING_PATH = os.path.join(os.path.expanduser('~'), 'downloads')
    sorted_date = datetime.today()

# create Event Handler class
class MyEventHandler(FileSystemEventHandler):
    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:

        if not os.path.exists(download_folder.CACHE_PATH):
            os.makedirs(download_folder.CACHE_PATH, exist_ok = True)

        check_sorted_date()
        compare_sorted_date_to_cache_date()
        create_cache_file()

def check_sorted_date() -> None:
    """This function checks if there is a run date, and returns this date"""
    try:
        with open(download_folder.CACHE_FILE, 'r') as cache:
            cache_data = json.load(cache)
            download_folder.sorted_date = datetime.strptime(cache_data[ 'sorted_date' ], '%Y-%m-%d %H:%M:%S')

    except (FileNotFoundError, json.JSONDecodeError) as exception:
        error_to_logfile(exception)


def compare_sorted_date_to_cache_date() -> None:
    """This function compares the date retrieved by the function check_run_date().
    It compares this date to the current date and moves the files and or folder to right folder"""
    current_date = datetime.today()
    if current_date.date() - download_folder.sorted_date.date() > timedelta(0):
        if download_folder.sorted_date.time() < time(23, 59, 59):
            move_to_dated_folder()
    else:
        error_to_logfile("Sorted date and cache date did match, which mains it's running om the same day")

def determine_path() -> str:
    month = datetime.today().strftime('%b')
    dated_folder_path = os.path.join(download_folder.OBSERVING_PATH, month)
    if not os.path.exists(dated_folder_path):
        os.makedirs(dated_folder_path)
    return dated_folder_path


def get_list_file_folder() -> list:
    """This function creates a list of files currently in the downloads folder"""
    list_with_files = [ ]
    with os.scandir(download_folder.OBSERVING_PATH) as entries:  # Use os.scandir for efficient iteration over files
        for entry in entries:
            if entry.is_file():  # Check if the entry is a file
                list_with_files.append(entry.name)
    return list_with_files

def move_to_dated_folder() -> None:
    """This function moves folders and or files to the right folder """
    t.sleep(2)
    try:
        list_to_move = get_list_file_folder()
        path_to_save = determine_path()
        for item in list_to_move:
            current_path = os.path.join(download_folder.OBSERVING_PATH, item)
            destination_path = os.path.join(path_to_save, item)
            os.replace(current_path, destination_path)
    except PermissionError as exception:
        error_to_logfile(exception)


def error_to_logfile(exception: str | Exception) -> None:
    """This function take an exception and log it to the log file"""
    with open(os.path.join(download_folder.CACHE_PATH,'SortDownload.log'), 'a') as log:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log.write(f'\n{timestamp}: {exception}')

def create_cache_file() -> None:
    """This function write to or creates a new file are the last update dated is stored.
    Based on this date we either run or don't run the script"""
    with open(download_folder.CACHE_FILE, 'w') as cache:
        json.dump(obj = {"sorted_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, fp = cache)



download_folder = DownloadFolder()

# create Event Handler, Observer object
event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, download_folder.OBSERVING_PATH, recursive=True)
observer.start()

try:
    while True:
        t.sleep(1)
finally:
    observer.stop()
    observer.join()