from lib.tile_handler import AreaTileHandler, MercatorProjection, G_LatLng, G_Point


class GMapTileHandler(AreaTileHandler):

    """
    Handler to get tiles from the static google map API
    @see https://developers.google.com/maps/documentation/static-maps/?hl=de
    """

    FILE_FORMAT = "PNG"

    """
    Maximum size in free version is 640x640px, image scale is allowed to increase
    accuracy. The resulting image is scale * image size, so maximum of 1280x1280
    """
    IMAGE_WIDTH = 640
    IMAGE_HEIGHT = 640
    IMAGE_SCALE = 2
    IMAGE_BOTTOM_MARGIN = 22

    SLEEP_TIME = 2

    ROAD_AREA_COLOR = "FF0000"
    HIGHWAY_AREA_COLOR = "00FF00"
    MANMADE_AREA_COLOR = "0000FF"
    NATURAL_AREA_COLOR = "FFFFFF"
    TRANSIT_AREA_COLOR = "000000"

    DATA_SRC = "GMAP"

    def __init__(self):
        self.setRoadAreaColor(self.ROAD_AREA_COLOR)
        self.setHighwayAreaColor(self.HIGHWAY_AREA_COLOR)
        self.setManMadeAreaColor(self.MANMADE_AREA_COLOR)
        self.setNaturalAreaColor(self.NATURAL_AREA_COLOR)
        self.setTransitAreaColor(self.TRANSIT_AREA_COLOR)

    def getFileFormat(self):
        return self.FILE_FORMAT

    def getDataSource(self):
        return self.DATA_SRC

    def getTileWidth(self):
        return self.IMAGE_WIDTH * self.IMAGE_SCALE

    def getTileHeight(self):
        return (self.IMAGE_HEIGHT - self.IMAGE_BOTTOM_MARGIN) * self.IMAGE_SCALE

    def getTileBottomMargin(self):
        return self.IMAGE_BOTTOM_MARGIN * self.IMAGE_SCALE

    def getSleepTime(self):
        return self.SLEEP_TIME

    def getTileLink(self, centerLatLng, zoom):
        map_style = self.getMapStyle()
        return "{}?center={},{}&zoom={}&format={}&maptype=roadmap&style={}&size={}x{}&scale={}".format(
            "https://maps.googleapis.com/maps/api/staticmap",
            centerLatLng.lat, centerLatLng.lng, zoom, self.FILE_FORMAT, map_style,
            self.IMAGE_WIDTH, self.IMAGE_HEIGHT, self.IMAGE_SCALE)

    def getMapStyle(self):
        return (
            "visibility:off&" +
            "style=feature:landscape%7Celement:geometry%7Ccolor:0x{3}%7Cvisibility:on&" +
            "style=feature:landscape.man_made%7Celement:geometry%7Ccolor:0x{2}%7Cvisibility:on&" +
            "style=feature:poi.park%7Celement:geometry%7Ccolor:0x{3}%7Cvisibility:on&" +
            "style=feature:road.arterial%7Celement:geometry%7Ccolor:0x{0}%7Cvisibility:on&" +
            "style=feature:road.highway%7Celement:geometry%7Ccolor:0x{1}%7Cvisibility:on&" +
            "style=feature:road.local%7Celement:geometry%7Ccolor:0x{0}%7Cvisibility:on&" +
            "style=feature:transit%7Celement:geometry%7Ccolor:0x{4}%7Cvisibility:on&" +
            "style=feature:water%7Celement:geometry%7Ccolor:0x{3}%7Cvisibility:on").format(
            self.getRoadAreaColor(),
            self.getHighwayAreaColor(),
            self.getManMadeAreaColor(),
            self.getNaturalAreaColor(),
            self.getTransitAreaColor())
