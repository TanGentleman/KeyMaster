from os import path
from utils.config import LOG_DIR, ABSOLUTE_REG_FILEPATH, ABSOLUTE_SIM_FILEPATH

def clean_filename(filename: str) -> str:
    """
    Clean the filename to load logs from.

    Args:
        filename (str): The name of the file to load logs from.

    Returns:
        str: The cleaned filename.
    """

    # Us os module to get the extension
    if len(filename) > 4:
        if filename[-5:] != '.json':
            filename = filename + '.json'
    # maximum length
    return filename[:255]

def get_filepath(filename: str | None) -> str | None:
    """
    Set the filename to load logs from.

    Args:
        filename (str): The name of the file to load logs from.
    """
    if filename is None:
        return None
    
    if not filename:
        print("No filename provided.")
        return None
    
    if path.isabs(filename):
        filepath = filename
    elif filename == 'REG':
        filepath = ABSOLUTE_REG_FILEPATH
    elif filename == 'SIM':
        filepath = ABSOLUTE_SIM_FILEPATH
    else:
        filepath = path.join(LOG_DIR, clean_filename(filename))
    return filepath

def is_filepath_valid(filename: str | None) -> bool:
    """
    Check if the path is valid.

    Args:
        filename (str): The name of the file to load logs from.

    Returns:
        bool: True if the path is valid, False otherwise.
    """
    if not filename:
        print("No filename provided.")
        return False
    
    filepath = get_filepath(filename)
    if not filepath:
        return False
    if not path.exists(filepath):
        print("File does not exist. (Yet?)")
        return False
    return True
