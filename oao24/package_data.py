import os
import numpy as np
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


class InfraredExampleData():

    @staticmethod
    def get_open_loop_data_cube():
        image = np.load(tuto3_folder() / "ID_105.npy")
        return np.atleast_3d(image)

    @staticmethod
    def get_camera_dark_data():
        return np.load(tuto3_folder() / "ID_110.npy")

    @staticmethod
    def get_close_loop_data_cube():
        return np.load(tuto3_folder() / "ID_109_red_16.npy")


class VisibleExampleData():

    @staticmethod
    def get_open_loop_data_cube():
        with np.load(tuto3_folder() / "ORCA_478.npz") as data:
            image = data['arr_0']
        return np.atleast_3d(image)

    @staticmethod
    def get_camera_dark_data():
        with np.load(tuto3_folder() / "ORCA_494.npz") as data:
            image = data['arr_0']
        return np.atleast_3d(image)

    @staticmethod
    def get_close_loop_data_cube():
        with np.load(tuto3_folder() / "ORCA_477.npz") as data:
            image = data['arr_0']
        return np.atleast_3d(image)
