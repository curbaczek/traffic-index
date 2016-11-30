import tempfile
import time

from lib.util.file import download_file
from lib.util import image_analysis

BING_IMAGE_WIDTH = 640
BING_IMAGE_HEIGHT = 640

FILE_TYPE = "png"

SLEEP_TIME = 2

COLOR_WANTED_AREA = "FFFFFF"
COLOR_UNWANTED_AREA = "FDFDFD"

BING_API_KEY = "Ai0rTccAvUMSnqQgoBn0_PQZDlqkri9n_N9DcG_x6bQ2e7n2b3orpTWl9T22NZQV"

def get_trafficmap_file_type():
    return FILE_TYPE


def get_map_image_width():
    return BING_IMAGE_WIDTH


def get_map_image_height():
    return BING_IMAGE_HEIGHT


def download_static_map(lat, lng, zoom, map_layer, local_filename):
    map_link = "http://dev.virtualearth.net/REST/V1/Imagery/Map/Road/{},{}/{}?mapLayer={}&format={}&mapSize={},{}&labelOverlay=hidden&key={}".format(
        lat, lng, zoom, map_layer, FILE_TYPE, BING_IMAGE_WIDTH, BING_IMAGE_HEIGHT, BING_API_KEY)
    download_file(map_link, local_filename)
    time.sleep(SLEEP_TIME)


def download_temporary_static_map(lat, lng, zoom):
    tmp_file = tempfile.NamedTemporaryFile()
    tmp_file.close()
    download_static_map(lat, lng, zoom, "", tmp_file.name)
    return tmp_file.name


def download_temporary_static_traffic_map(lat, lng, zoom):
    tmp_file = tempfile.NamedTemporaryFile()
    tmp_file.close()
    download_static_map(lat, lng, zoom, "TrafficFlow", tmp_file.name)
    return tmp_file.name


def download_static_traffic_map(lat, lng, zoom, local_filename):
    print "download static traffic map"
    tmp_static_traffic_map = download_temporary_static_traffic_map(lat, lng, zoom)
    print tmp_static_traffic_map
    print "download static map"
    tmp_static_map = download_temporary_static_map(lat, lng, zoom)
    print tmp_static_map
    image_analysis.get_difference_image(tmp_static_traffic_map, tmp_static_map, local_filename)
   

