import os
import sys
import glob
import json


def sys_exit(message: str):
    sys.exit(message)


def check_directory(dir_path: str):
    if not os.path.isdir(dir_path):
        message = ' '.join(['Path does not exist:', dir_path])
        sys_exit(message)
    return True


def check_file(file_path: str):
    if not os.path.isfile(file_path):
        message = ' '.join(['Path does not exist:', file_path])
        sys_exit(message)


def get_file_dir(file=None):
    if not file:
        file = __file__
    file_path = os.path.abspath(file)
    dir_path = os.path.dirname(file_path)
    return dir_path


def get_head_tail_ext(path):
    ext = None
    dir_path, file_name = os.path.split(path)
    if file_name:
        file_name, ext = os.path.splitext(file_name)
    return dir_path, file_name, ext


def create_dir(dir_name: str, file: str = None):
    current_path = get_file_dir()
    dir_path = os.path.join(current_path, dir_name)
    if not os.path.isdir(dir_path):
        try:
            # print(dir_path)
            os.mkdir(dir_path)
        except OSError:
            description = 'Creation of the directory failed:'
            message = ' '.join([description, dir_path])
            sys_exit(message)
        else:
            description = 'Successfully created the directory:'
            message = ' '.join([description, dir_path])
            print(message)
    else:
        description = 'Directory already exists:'
        message = ' '.join([description, dir_path])
        print(message)
    return dir_path


def files_in_dir(dir_path: str, ext: str = None):
    check_directory(dir_path)
    if not dir_path.endswith('/'):
        dir_path = ''.join([dir_path, '/'])
    if ext:
        path = ''.join([dir_path, '*', ext])
    else:
        path = dir_path
    return glob.glob(path)


def join_path(*args):
    array = list(args)
    return '/'.join(array)


def read_json(path):
    check_file(path)
    with open(path) as f:
        data = json.load(f)
    return data
