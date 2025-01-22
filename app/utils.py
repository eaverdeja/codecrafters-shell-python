import os


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
