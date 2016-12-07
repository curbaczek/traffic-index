# import math
from time import sleep

from lib.tile_handler import TrafficTileHandler
from lib.util.file import download_file
from os.path import join
from lib.data_handler import get_location_tile_filename
# from lib.util import image


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

    def getMapLink(self, lat, lng, zoom, file_type, width, height):
        return "{}/{},{}/{}?mapLayer={}&format={}&mapSize={},{}&labelOverlay=hidden&key={}".format(
            "http://dev.virtualearth.net/REST/V1/Imagery/Map/Road",
            lat, lng, zoom, "TrafficFlow", file_type, width, height, self.BING_API_KEY)

    def getTileImage(self, lat, lng, x, y, zoom, local_directory):
        map_url = self.getMapLink(lat, lng, zoom, self.FILE_FORMAT, self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        tile = self.createTile(x, y, zoom)
        tile_filename = join(local_directory, get_location_tile_filename(tile))
        download_file(map_url, tile_filename)
        sleep(self.SLEEP_TIME)
        return tile_filename

    def getTiles(self, lat, lng, zoom, tile_count, local_directory, printProgress=False):
        for x in range(1-tile_count, tile_count):
            for y in range(1-tile_count, tile_count):
                if (printProgress):
                    print("load image {:+d}x{:+d}".format(x, y))
                self.getTileImage(lat, lng, x, y, zoom, local_directory)
