import tempfile
import math
from time import sleep

from lib.tile_handler import AreaTileHandler
from lib.util.file import download_file
from os.path import join
from lib.data_handler import get_location_tile_filename
from lib.util import image

MERCATOR_RANGE = 256


class G_Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class G_LatLng:
    def __init__(self, lt, ln):
        self.lat = float(lt)
        self.lng = float(ln)


class MercatorProjection:

    """ mercator projection by jmague (http://stackoverflow.com/a/21116468) """

    def __init__(self):
        self.pixelOrigin_ = G_Point(MERCATOR_RANGE / 2, MERCATOR_RANGE / 2)
        self.pixelsPerLonDegree_ = MERCATOR_RANGE / 360
        self.pixelsPerLonRadian_ = MERCATOR_RANGE / (2 * math.pi)

    def bound(self, value, opt_min, opt_max):
        if (opt_min is not None):
            value = max(value, opt_min)
        if (opt_max is not None):
            value = min(value, opt_max)
        return value

    def degreesToRadians(self, deg):
        return deg * (math.pi / 180)

    def radiansToDegrees(self, rad):
        return rad / (math.pi / 180)

    def fromLatLngToPoint(self, latLng, opt_point=None):
        point = opt_point if opt_point is not None else G_Point(0, 0)
        origin = self.pixelOrigin_
        point.x = origin.x + latLng.lng * self.pixelsPerLonDegree_
        # NOTE(appleton): Truncating to 0.9999 effectively limits latitude to
        # 89.189.  This is about a third of a tile past the edge of the world tile.
        siny = self.bound(math.sin(self.degreesToRadians(latLng.lat)), -0.9999, 0.9999)
        point.y = origin.y + 0.5 * math.log((1 + siny) / (1 - siny)) * -self.pixelsPerLonRadian_
        return point

    def fromPointToLatLng(self, point):
        origin = self.pixelOrigin_
        lng = (point.x - origin.x) / self.pixelsPerLonDegree_
        latRadians = (point.y - origin.y) / -self.pixelsPerLonRadian_
        lat = self.radiansToDegrees(2 * math.atan(math.exp(latRadians)) - math.pi / 2)
        return G_LatLng(lat, lng)


class GMapTileHandler(AreaTileHandler):

    """
    Handler to get tiles from the static google map API
    @see https://developers.google.com/maps/documentation/static-maps/?hl=de
    """

    FILE_FORMAT = "PNG"

    IMAGE_WIDTH = 640
    IMAGE_HEIGHT = 640
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
        return self.IMAGE_WIDTH

    def getTileHeight(self):
        return self.IMAGE_HEIGHT - self.IMAGE_BOTTOM_MARGIN

    def getMapLink(self, centerLatLng, zoom, file_type, map_style, width, height):
        return """{}?center={},{}&zoom={}&format={}&maptype=roadmap&style={}&size={}x{}""".format(
            "https://maps.googleapis.com/maps/api/staticmap",
            centerLatLng.lat, centerLatLng.lng, zoom, file_type, map_style, width, height)

    def getMapCenter(self, lat, lng, zoom, tile_x, tile_y):
        """ calculates the new map center with the given tile offset """
        """ @see https://developers.google.com/maps/documentation/javascript/maptypes?hl=de#MapCoordinates """
        scale = 2**zoom
        proj = MercatorProjection()
        centerPoint = proj.fromLatLngToPoint(G_LatLng(lat, lng))
        newCenterPoint = G_Point(
            centerPoint.x + (tile_x * self.getTileWidth()) / scale,
            centerPoint.y + (tile_y * self.getTileHeight()) / scale)
        return proj.fromPointToLatLng(newCenterPoint)

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

    def getTileImage(self, lat, lng, x, y, zoom, local_directory):
        tileCenter = self.getMapCenter(lat, lng, zoom, x, y)
        map_style = self.getMapStyle()
        map_url = self.getMapLink(tileCenter, zoom, self.FILE_FORMAT, map_style, self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        tile = self.createTile(x, y, zoom)
        tile_filename = join(local_directory, get_location_tile_filename(tile))
        download_file(map_url, tile_filename)
        image.bottom_crop_image(tile_filename, self.IMAGE_BOTTOM_MARGIN)
        sleep(self.SLEEP_TIME)
        return tile_filename

    def getTiles(self, lat, lng, zoom, tile_count, local_directory, printProgress=False):
        for x in range(1-tile_count, tile_count):
            for y in range(1-tile_count, tile_count):
                if (printProgress):
                    print("load image {:+d}x{:+d}".format(x, y))
                self.getTileImage(lat, lng, x, y, zoom, local_directory)
