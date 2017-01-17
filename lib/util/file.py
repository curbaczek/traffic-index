import os
import shutil
import urllib.request
import sys
import subprocess

LOCATION_DIR = "res/data/locations"


def clear_dir(dir_path):
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def copy_dir(src, dest):
    shutil.copytree(src, dest)


def copy_file_makedirs(src, dst):
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    shutil.copyfile(src, dst)


def download_file(url, local_filename):
    urllib.request.urlretrieve(url, local_filename)


def remove_file(filename):
    if (os.path.isfile(filename)):
        os.remove(filename)


def open_file_from_shell(filename):
    if sys.platform.startswith('linux'):
        subprocess.call(["xdg-open", filename])
    elif sys.platform.startswith('win'):
        os.startfile(filename)
    elif sys.platform.startswith('darwin'):
        subprocess.call(["open", filename])


def get_target_directory(lat, lng, subdir):
    latlng_dir = "{},{}".format(lat, lng)
    location_dir = os.path.join(LOCATION_DIR, latlng_dir, subdir)
    return location_dir
