"""
This file is only for check debug mode in settings
"""
import json

FILE_PATH = "/home/pi/.bnote/settings.txt"
def check_settings() -> bool:
    """
    Check if debug mode is enabled in settings
    """
    try:
        with open(FILE_PATH, "r") as file:
            settings = json.load(file)
            if settings['system']['debug']:
                return True
            return False
    except FileNotFoundError:
        return False