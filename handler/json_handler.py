import json
import os
from enum import Enum


class JsonErrorState(Enum):
    JSON_FILE_NOT_FOUND = "Json file not found."
    JSON_FAILED_TO_DECODE = "Failed to decode JSON file."
    JSON_FAILED_TO_SAVE = "Failed to save JSON file."
    JSON_SAVE_DIRECTORY_NOT_FOUND = "Failed to locate save json directory."
    JSON_SAVE_PATH_IS_DIRECTORY = "JSON save path is a directory."
    JSON_SAVE_PERMISSION_DENIED = "Json save permission denied."
    JSON_UNHANDLED_EXCEPTION_OCCURRED = "Json save/load unhandled exception occurred."


class JsonFileHandler:
    def __init__(self):
        self.debug = False
        self._json_file = None

    def save_to_file(self, path: str) -> JsonErrorState:
        try:
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(path, "w+") as json_file:
                json.dump(self._json_file, json_file, indent=4)
        except FileNotFoundError:
            return JsonErrorState.JSON_SAVE_DIRECTORY_NOT_FOUND
        except IsADirectoryError:
            return JsonErrorState.JSON_SAVE_PATH_IS_DIRECTORY
        except PermissionError:
            return JsonErrorState.JSON_SAVE_PERMISSION_DENIED
        except Exception as e:
            if self.debug:
                print(e)
            return JsonErrorState.JSON_UNHANDLED_EXCEPTION_OCCURRED

    def load_from_file(self, path: str) -> JsonErrorState:
        try:
            with open(path, "r") as json_file:
                self._json_file = json.load(json_file)
        except FileNotFoundError:
            return JsonErrorState.JSON_SAVE_DIRECTORY_NOT_FOUND
        except json.JSONDecodeError:
            return JsonErrorState.JSON_FAILED_TO_DECODE
        except Exception as e:
            if self.debug:
                print(e)
            return JsonErrorState.JSON_UNHANDLED_EXCEPTION_OCCURRED

    def load_from_string(self, json_string: str) -> JsonErrorState:
        try:
            self._json_file = json.loads(json_string)
        except json.JSONDecodeError:
            return JsonErrorState.JSON_FAILED_TO_DECODE
        except Exception as e:
            if self.debug:
                print(e)
            return JsonErrorState.JSON_UNHANDLED_EXCEPTION_OCCURRED
