import tempfile

from lib.tile_handler import TrafficTileHandler, MercatorProjection, G_LatLng, G_Point


class BingTileHandler(TrafficTileHandler):

    """
    Handler to get tiles from the static bing map API
    @see https://msdn.microsoft.com/en-us/library/ff701724.aspx
    """

    FILE_FORMAT = "PNG"

    DATA_SRC = "BING"

    IMAGE_WIDTH = 1400
    IMAGE_HEIGHT = 1400
    IMAGE_BOTTOM_MARGIN = 22

    SLEEP_TIME = 2

    BING_API_KEY = "Ai0rTccAvUMSnqQgoBn0_PQZDlqkri9n_N9DcG_x6bQ2e7n2b3orpTWl9T22NZQV"

    def __init__(self):
        assert self.IMAGE_WIDTH in range(80, 2000), "tile width must be between 80 and 2000, {:d} set".format(
            self.IMAGE_WIDTH)
        assert self.IMAGE_HEIGHT in range(80, 1500), "tile height must be between 80 and 1500, {:d} set".format(
            self.IMAGE_HEIGHT)
        return

    def getFileFormat(self):
        return self.FILE_FORMAT

    def getDataSource(self):
        return self.DATA_SRC

    def getTileWidth(self):
        return self.IMAGE_WIDTH

    def getTileHeight(self):
        return self.IMAGE_HEIGHT - self.IMAGE_BOTTOM_MARGIN

    def getTileBottomMargin(self):
        return self.IMAGE_BOTTOM_MARGIN

    def getSleepTime(self):
        return self.SLEEP_TIME

    def getTileLink(self, centerLatLng, zoom):
        return "{}/{},{}/{}?mapLayer={}&format={}&mapSize={},{}&labelOverlay=hidden&key={}".format(
            "http://dev.virtualearth.net/REST/V1/Imagery/Map/Road",
            centerLatLng.lat, centerLatLng.lng, zoom, "TrafficFlow",
            self.FILE_FORMAT, self.IMAGE_WIDTH, self.IMAGE_HEIGHT, self.BING_API_KEY)
