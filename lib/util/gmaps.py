import time

from lib.util.file import download_file
from lib.util import image_analysis

GMAP_IMAGE_WIDTH = 640
GMAP_IMAGE_HEIGHT = 640
GMAP_IMAGE_BOTTOM_MARGIN = 22

FILE_TYPE = "png"

SLEEP_TIME = 2

COLOR_WANTED_AREA = "FFFFFF"
COLOR_UNWANTED_AREA = "000000"


def get_file_type():
    return FILE_TYPE


def get_map_image_width():
    return GMAP_IMAGE_WIDTH


def get_map_image_height():
    return GMAP_IMAGE_HEIGHT-GMAP_IMAGE_BOTTOM_MARGIN


def download_static_map(lat, lng, zoom, map_style, local_filename):
    map_link = """
        https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom={}&format={}&maptype=roadmap&style={}&
        size={}x{}""".strip().format(
        lat, lng, zoom, FILE_TYPE, map_style, GMAP_IMAGE_WIDTH, GMAP_IMAGE_HEIGHT)
    download_file(map_link, local_filename)
    image_analysis.bottom_crop_image(local_filename, GMAP_IMAGE_BOTTOM_MARGIN)
    time.sleep(SLEEP_TIME)


def download_static_road_map(lat, lng, zoom, local_filename):
    style = """
        color:0x{0}%7Cvisibility:on&style=element:labels%7Cvisibility:off&style=feature:road.arterial%7Ccolor:0x{1}
        %7Cvisibility:on&style=feature:road.arterial%7Celement:labels%7Cvisibility:off&style=feature:road.local
        %7Ccolor:0x{1}%7Cvisibility:on&style=feature:road.local%7Celement:labels%7Cvisibility:off""".strip().format(
        COLOR_UNWANTED_AREA, COLOR_WANTED_AREA)
    download_static_map(lat, lng, zoom, style, local_filename)


def download_static_highway_map(lat, lng, zoom, local_filename):
    style = """
        color:0x{0}%7Cvisibility:on&style=element:labels%7Cvisibility:off&style=feature:road.highway%7Ccolor:0x{1}
        %7Cvisibility:on&style=feature:road.highway%7Celement:labels%7Cvisibility:off""".strip().format(
        COLOR_UNWANTED_AREA, COLOR_WANTED_AREA)
    download_static_map(lat, lng, zoom, style, local_filename)


def download_static_manmade_map(lat, lng, zoom, local_filename):
    style = """
        visibility:off&style=feature:landscape%7Ccolor:0x{0}%7Cvisibility:on&style=feature:landscape.man_made
        %7Ccolor:0x{1}%7Cvisibility:on&style=feature:poi.park%7Ccolor:0x{0}%7Cvisibility:on&style=feature:road
        %7Ccolor:0x{0}%7Cvisibility:on&style=feature:road%7Celement:labels%7Cvisibility:off&style=feature:transit
        %7Ccolor:0x{0}%7Cvisibility:on&style=feature:transit%7Celement:labels%7Cvisibility:off&style=feature:water
        %7Ccolor:0x{0}%7Cvisibility:on&style=feature:water%7Celement:labels%7Cvisibility:off""".strip().format(
        COLOR_UNWANTED_AREA, COLOR_WANTED_AREA)
    download_static_map(lat, lng, zoom, style, local_filename)


def download_static_natural_map(lat, lng, zoom, local_filename):
    style = """
        visibility:off&style=element:labels%7Cvisibility:off&style=feature:landscape
        %7Cvisibility:on&style=feature:landscape.man_made%7Ccolor:0x{0}
        %7Cvisibility:on&style=feature:landscape.man_made%7Celement:labels
        %7Cvisibility:off&style=feature:landscape.natural%7Ccolor:0x{1}
        %7Cvisibility:on&style=feature:landscape.natural%7Celement:labels
        %7Cvisibility:off&style=feature:poi.park%7Ccolor:0x{1}
        %7Cvisibility:on&style=feature:poi.park%7Celement:labels
        %7Cvisibility:off&style=feature:road%7Ccolor:0x{0}
        %7Cvisibility:on&style=feature:road%7Celement:labels
        %7Cvisibility:off&style=feature:transit%7Ccolor:0x{0}
        %7Cvisibility:on&style=feature:transit%7Celement:labels
        %7Cvisibility:off&style=feature:water%7Ccolor:0x{1}
        %7Cvisibility:on&style=feature:water%7Celement:labels
        %7Cvisibility:off""".strip().format(COLOR_UNWANTED_AREA, COLOR_WANTED_AREA)
    download_static_map(lat, lng, zoom, style, local_filename)


def download_static_transit_map(lat, lng, zoom, local_filename):
    style = """
        color:0x{0}%7Cvisibility:on&style=element:labels
        %7Cvisibility:off&style=feature:transit%7Ccolor:0x{1}
        %7Cvisibility:on&style=feature:transit%7Celement:labels
        %7Cvisibility:off""".strip().format(COLOR_UNWANTED_AREA, COLOR_WANTED_AREA)
    download_static_map(lat, lng, zoom, style, local_filename)
