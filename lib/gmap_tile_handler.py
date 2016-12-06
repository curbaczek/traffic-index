import tempfile
from time import sleep

from lib.tile_handler import AreaTileHandler
from lib.util.file import download_file
from os.path import join


class GMapTileHandler(AreaTileHandler):

    FILE_FORMAT = "PNG"

    IMAGE_WIDTH = 640
    IMAGE_HEIGHT = 640
    IMAGE_BOTTOM_MARGIN = 22

    SLEEP_TIME = 2

    ROAD_AREA_COLOR = "000000"
    HIGHWAY_AREA_COLOR = "000000"
    MANMADE_AREA_COLOR = "000000"
    NATURAL_AREA_COLOR = "000000"
    TRANSIT_AREA_COLOR = "000000"

    DATA_SRC = "GMAP"

    def __init__(self):
        self.setRoadAreaColor(self.ROAD_AREA_COLOR)
        self.setHighwayAreaColor(self.HIGHWAY_AREA_COLOR)
        self.setManMadeAreaColor(self.MANMADE_AREA_COLOR)
        self.setNaturalAreaColor(self.NATURAL_AREA_COLOR)
        self.setTransitAreaColor(self.TRANSIT_AREA_COLOR)

    def getFileType(self):
        return self.FILE_FORMAT

    def getTileWidth(self):
        return self.IMAGE_WIDTH

    def getTileHeight(self):
        return self.IMAGE_HEIGHT - self.IMAGE_BOTTOM_MARGIN

    def getMapLink(self, center_lat, center_lng, zoom, file_type, map_style, width, height):
        return """{}?center={},{}&zoom={}&format={}&maptype=roadmap&style={}&size={}x{}""".format(
            "https://maps.googleapis.com/maps/api/staticmap",
            center_lat, center_lng, zoom, file_type, map_style, width, height)

    def getMapCenter(self, lat, lng, tile_x, tile_y):
        # TODO calculate center from x/y coordinates
        return {"lat": lat, "lng": lng}

    def getTile(self, lat, lng, x, y, zoom):
        map_center = self.getMapCenter(lat, lng, x, y)
        map_style = ""
        url = self.getMapLink(
            map_center["lat"], map_center["lng"], zoom, self.FILE_FORMAT, map_style,
            self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        temp_image = tempfile.NamedTemporaryFile(delete=False)
        print(url)
        download_file(url, temp_image.name)
        sleep(self.SLEEP_TIME)
        return temp_image.name

    def getTiles(self, lat, lng, zoom, tile_count):
        # TODO implement
        pass
