import os
import glob


def file_directory():
    file_path = os.path.realpath(__file__)
    return os.path.dirname(file_path)

def file_path():
    return os.path.realpath(__file__)

def file_list(path):
    return glob.glob(path)
