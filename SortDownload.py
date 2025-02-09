# import modules
import os
import time as t
import json
from datetime import datetime, timedelta, time

from watchdog.events import FileSystemEvent, FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent
from watchdog.observers import Observer



# path to json
CACHE_FILE = 'SortDownloadCache.json'
OBSERVING_PATH = os.path.join(, 'downloads')


def create_last_run_file():
    """This function creates a new date in the SortDownloadCache.json.
    Based on this date we either run or don't run the script"""
    with open(CACHE_FILE, 'w') as cache:
        json.dump({"run_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, cache)


def check_run_date() -> json:
    """This function checks if there is a run date, and returns this date"""
    try:
        with open(CACHE_FILE, 'r') as cache:
            cache_data = json.load(cache)
            return datetime.strptime(cache_data[ 'run_date' ], '%Y-%m-%d %H:%M:%S')

    except (FileNotFoundError, json.JSONDecodeError) as exception:
        with open('SortDownload.log', 'a') as log:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log.write(f'{timestamp}: {exception}')


def compare_run_to_cache(last_run_date: datetime, event: DirCreatedEvent | FileCreatedEvent):
    """This function compares the date retrieved by the function check_run_date().
    It compares this date to the current date and moves the files and or folder to right folder"""
    current_run_date = datetime.today()
    if current_run_date.date() - last_run_date.date() > timedelta(0):
        if last_run_date.time() < time(23, 59, 59):
            determine_path()
    else:
        create_last_run_file()

def move_to_dated_folder(event: DirCreatedEvent | FileCreatedEvent, path: str) -> None:
    """This function moves folders and or files to the right folder """
    list_to_move = get_list_file_folder(path)
    path_to_save = os.path.join(path, 'Feb')
    for item in list_to_move:
        filename = item.name
        current_path = os.path.join(path, filename)
        destination_path = os.path.join(path_to_save, filename)

        os.replace(current_path, destination_path)

def get_list_file_folder(path) -> list:
    """This function creates a list of files currently in the downloads folder"""
    list_with_files = [ ]
    with os.scandir(path) as entries:  # Use os.scandir for efficient iteration over files
        for entry in entries:
            if entry.is_file():  # Check if the entry is a file
                list_with_files.append(entry)
    return list_with_files

def determine_path(path: str):
    month = datetime.today().strftime('%b')
    dated_folder_path = os.path.join(path, month)
    if os.path.exists(dated_folder_path):

    else:
        os.makedirs(dated_folder_path)

# create Event Handler class
class MyEventHandler(FileSystemEventHandler):
    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        run_date = check_run_date()
        compare_run_to_cache(run_date, event)


# create Event Handler, Observer object
event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, OBSERVING_PATH, recursive=True)
observer.start()

try:
    while True:
        t.sleep(1)
finally:
    observer.stop()
    observer.join()