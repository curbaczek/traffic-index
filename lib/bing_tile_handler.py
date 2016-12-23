# import math
import tempfile
from time import sleep

from lib.tile_handler import TrafficTileHandler
from lib.util.file import download_file
from lib.util import image_analysis
from os.path import join
from lib.data_handler import get_location_tile_filename_from_tile


class BingTileHandler(TrafficTileHandler):

    """
    Handler to get tiles from the static bing map API
    """

    FILE_FORMAT = "PNG"

    DATA_SRC = "BING"

    IMAGE_WIDTH = 640
    IMAGE_HEIGHT = 640

    SLEEP_TIME = 2

    COLOR_WANTED_AREA = "FFFFFF"
    COLOR_UNWANTED_AREA = "FDFDFD"

    BING_API_KEY = "Ai0rTccAvUMSnqQgoBn0_PQZDlqkri9n_N9DcG_x6bQ2e7n2b3orpTWl9T22NZQV"

    DATA_SRC = "GMAP"

    def __init__(self):
        # self.setHeavyTrafficColor(self.ROAD_AREA_COLOR)
        # self.setModerateTrafficColor(self.HIGHWAY_AREA_COLOR)
        # self.setLightTrafficColor(self.MANMADE_AREA_COLOR)
        # self.setNoTrafficColor(self.NATURAL_AREA_COLOR)
        # self.setNoInformationColor(self.TRANSIT_AREA_COLOR)
        return

    def getFileFormat(self):
        return self.FILE_FORMAT

    def getDataSource(self):
        return self.DATA_SRC

    def getTileWidth(self):
        return self.IMAGE_WIDTH

    def getTileHeight(self):
        return self.IMAGE_HEIGHT

    def getMapLink(self, lat, lng, zoom, map_type):
        return "{}/{},{}/{}?mapLayer={}&format={}&mapSize={},{}&labelOverlay=hidden&key={}".format(
            "http://dev.virtualearth.net/REST/V1/Imagery/Map/Road",
            lat, lng, zoom, map_type, self.FILE_FORMAT, self.IMAGE_WIDTH, self.IMAGE_HEIGHT, self.BING_API_KEY)

    def download_static_map(self, lat, lng, zoom, map_layer, local_filename):
        map_link = self.getMapLink(lat, lng, zoom, map_layer)
        download_file(map_link, local_filename)
        sleep(self.SLEEP_TIME)

    def download_temporary_static_map(self, lat, lng, zoom):
        tmp_file = tempfile.NamedTemporaryFile()
        tmp_file.close()
        self.download_static_map(lat, lng, zoom, "", tmp_file.name)
        return tmp_file.name

    def download_temporary_static_traffic_map(self, lat, lng, zoom):
        tmp_file = tempfile.NamedTemporaryFile()
        tmp_file.close()
        self.download_static_map(lat, lng, zoom, "TrafficFlow", tmp_file.name)
        return tmp_file.name

    def getTileImage(self, lat, lng, x, y, zoom, local_directory):
        tile = self.createTile(x, y, zoom)
        tile_filename = join(local_directory, get_location_tile_filename_from_tile(tile))
        tmp_static_traffic_map = self.download_temporary_static_traffic_map(lat, lng, zoom)
        tmp_static_map = self.download_temporary_static_map(lat, lng, zoom)
        image_analysis.get_difference_image(tmp_static_traffic_map, tmp_static_map, tile_filename)
        return tile_filename

    def getTiles(self, lat, lng, zoom, tile_count, local_directory, printProgress=False):
        """for x in range(1-tile_count, tile_count):
            for y in range(1-tile_count, tile_count):
                if (printProgress):
                    print("load image {:+d}x{:+d}".format(x, y))
                self.getTileImage(lat, lng, x, y, zoom, local_directory)"""
