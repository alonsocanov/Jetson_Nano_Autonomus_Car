import os


def directory():
    file_path = os.path.realpath(__file__)
    return os.path.dirname(file_path)