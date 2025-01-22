import os
import logging


def locate_executable(command):
    path = os.environ.get("PATH", "")
    for directory in path.split(os.pathsep):
        file_path = os.path.join(directory, command)

        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path


def list_executables():
    path = os.environ.get("PATH", "")
    executables = []
    for directory in path.split(os.pathsep):
        try:
            files = os.listdir(directory)
        except FileNotFoundError:
            # Ignore bad paths
            continue

        for file_name in files:
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                executables.append(file_name)

    return executables


def setup_logging():
    log_file = os.path.join(os.path.curdir, "tmp/autocompleter.log")

    logger = logging.getLogger("Autocompleter")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
