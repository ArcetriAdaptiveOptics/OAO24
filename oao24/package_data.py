import os
from pathlib import Path
ROOT_DIR_KEY = 'OAO24_ROOT_DIR'


def set_data_root_dir(folder):
    os.environ[ROOT_DIR_KEY] = folder


def data_root_dir():

    try:
        return Path(os.environ[ROOT_DIR_KEY])
    except KeyError:
        import pkg_resources
        dataroot = pkg_resources.resource_filename(
            'oao24',
            'data')
        return Path(dataroot)


def tuto2_folder():
    return data_root_dir() / "tuto2"


def tuto3_folder():
    return data_root_dir() / "tuto3"
