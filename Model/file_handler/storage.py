from Interfaces.model.storage_interface import IStorage
from Model.algorithm.frame import Frame

import os
import errno
import datetime

import json


# A json-oriented file handler class
class Storage(IStorage):
    def __init__(self, config_path: str, storage_path: str, config: dict = None):
        # Path to default configurations file
        self.__config = config_path

        # Path to the default storage directory
        self.__storage = storage_path

        # Default configuration
        if config is None:
            config = {"mode": None,
                      "step_by_step": False}

        self.__options = config

    # helper method to generate path to stored sessions location
    def __data_path(self, session: str) -> str:
        return self.__storage + session + "/"

    # helper method to generate path to the specific stored file
    def __json_file(self, session: str, step: float) -> str:
        return self.__data_path(session) + f"step_{step}.json"

    # helper method to check the existence of given directory
    @staticmethod
    def check_dir(path: str) -> bool:
        return os.path.exists(os.path.dirname(path))

    # helper method to check if the given sessions is compatible with json
    @staticmethod
    def check_data(data) -> bool:
        try:
            json.dumps(data)
            return True
        except (TypeError, OverflowError):
            return False

    # helper method to create missing directory
    def __create_dir(self, path: str) -> None:
        try:
            os.makedirs(os.path.dirname(path))

        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    # Writes to json file located at given directory, creates one if the file is missing
    def write(self, path: str, data, rewrite: bool = False) -> None:
        if self.check_data(data):
            if not self.check_dir(path):
                self.__create_dir(path)

            with open(path, "w+" if rewrite else "w") as src:
                json.dump(data, src, indent="\t")

        else:
            raise TypeError("Data is not json-serializable!")

    # Reads from file located at given directory
    def read(self, path: str) -> dict:
        if self.check_dir(path):

            with open(path, "r") as src:
                data = json.load(src)

            return data

        else:
            raise FileNotFoundError(f"{path} does not exist!")

    # Sets the config for the program to use
    def set_config(self, options: dict = None, path: str = None) -> None:
        if path is not None:
            self.__config = path

        if options is None:
            self.write(self.__config, self.__options, True)
        else:
            self.write(self.__config, options, True)

    # Reads config file for the program
    def get_config(self, path: str = None) -> dict:
        if path is not None:
            return self.read(path)

        try:
            return self.read(self.__config)

        except FileNotFoundError:
            pass

        self.set_config()
        return self.get_config()

    # Creates a directory to store current session and returns directory's name
    def start_session(self) -> str:
        timestamp = datetime.datetime.now()
        session = timestamp.strftime("session %d-%b-%Y %I-%M-%S %p")

        self.__create_dir(self.__data_path(session))

        return session

    # Sets storage directory
    def set_storage(self, path: str) -> None:
        self.__storage = path

    # Cache the step to given session
    def store(self, session: str, step: int, frame: Frame) -> None:
        path = self.__json_file(session, step)
        self.write(path, frame.cache(), True)

    # Returns step from a given session
    def get_step(self, session: str, step: float) -> Frame:
        path = self.__json_file(session, step)
        data = self.read(path)

        return Frame(data.pop("step"), data)
