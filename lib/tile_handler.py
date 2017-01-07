from abc import ABC, abstractmethod
import time
import math
from time import sleep
from lib import model
from lib.data_handler import get_latest_tile, get_tile_filename
from lib.util.file import download_file
from os.path import join
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


class TileHandler(ABC):

    debug_mode = False

    @abstractmethod
    def getFileFormat(self):
        pass

    @abstractmethod
    def getDataSource(self):
        pass

    @abstractmethod
    def getTileWidth(self):
        pass

    @abstractmethod
    def getTileHeight(self):
        pass

    @abstractmethod
    def getTileBottomMargin(self):
        pass

    @abstractmethod
    def getSleepTime(self):
        pass

    def getLatestTile(self, x, y, zoom, directory):
        latest_tile = get_latest_tile(directory, x, y, self.getDataSource(), zoom, self.getFileFormat())
        if (latest_tile is None):
            self.printIndentedDebugMsg("no local file found")
        else:
            self.printIndentedDebugMsg("tile '{}' found, download skipped".format(latest_tile))
        return latest_tile

    def createTile(self, x, y, zoom):
        current_time = int(time.time())
        return model.Tile(x, y, self.getDataSource(), zoom, current_time, self.getFileFormat())

    @abstractmethod
    def getTileLink(self, centerLatLng, zoom):
        pass

    def getMapCenter(self, lat, lng, zoom, tile_x, tile_y):
        """ calculates the new map center with the given tile offset """
        """ @see https://developers.google.com/maps/documentation/javascript/maptypes?hl=de#MapCoordinates """
        scale = 2**zoom
        proj = MercatorProjection()
        centerPoint = proj.fromLatLngToPoint(G_LatLng(lat, lng))
        newCenterPoint = G_Point(
            centerPoint.x + (tile_x * self.IMAGE_WIDTH) / scale,
            centerPoint.y + (tile_y * (self.IMAGE_HEIGHT - self.IMAGE_BOTTOM_MARGIN)) / scale)
        return proj.fromPointToLatLng(newCenterPoint)

    def setDebugMode(self, value):
        self.debug_mode = bool(value)

    def isDebugMode(self):
        return self.debug_mode

    def printDebugMsg(self, msg):
        if (self.isDebugMode()):
            print("[Debug] {}".format(msg))

    def printIndentedDebugMsg(self, msg):
        self.printDebugMsg("--- {}".format(msg))

    def getTileFilename(self, x, y, zoom):
        tile = self.createTile(x, y, zoom)
        return get_tile_filename(
            tile.x, tile.y, tile.data_src, tile.zoom, tile.timestamp, tile.file_format)

    def getTileImage(self, lat, lng, x, y, zoom, local_directory):
        self.printDebugMsg("load image {:+d}x{:+d}".format(x, y))
        tile_center = self.getMapCenter(lat, lng, zoom, x, y)
        tile_url = self.getTileLink(tile_center, zoom)
        tile_filename = self.getLatestTile(x, y, zoom, local_directory)
        if (tile_filename is None):
            tile_filename = self.getTileFilename(x, y, zoom)
            tile_path = join(local_directory, tile_filename)
            download_file(tile_url, tile_path)
            image.bottom_crop_image(tile_path, self.getTileBottomMargin())
            self.printIndentedDebugMsg("new tile downloaded")
            sleep(self.getSleepTime())
        return tile_filename

    def getTiles(self, lat, lng, zoom, tile_count, local_directory):
        tile_list = []
        for x in range(1-tile_count, tile_count):
            for y in range(1-tile_count, tile_count):
                new_tile = self.getTileImage(lat, lng, x, y, zoom, local_directory)
                tile_list.append(new_tile)
        return tile_list


class AreaTileHandler(TileHandler):

    def setRoadAreaColor(self, value):
        self.road_area_color = str(value)

    def getRoadAreaColor(self):
        return self.road_area_color

    def setHighwayAreaColor(self, value):
        self.highway_area_color = str(value)

    def getHighwayAreaColor(self):
        return self.highway_area_color

    def setManMadeAreaColor(self, value):
        self.manmade_area_color = str(value)

    def getManMadeAreaColor(self):
        return self.manmade_area_color

    def setNaturalAreaColor(self, value):
        self.natural_area_color = str(value)

    def getNaturalAreaColor(self):
        return self.natural_area_color

    def setTransitAreaColor(self, value):
        self.transit_area_color = str(value)

    def getTransitAreaColor(self):
        return self.transit_area_color


class TrafficTileHandler(TileHandler):

    def setHeavyTrafficColor(self, value):
        self.heavy_traffic_color = value

    def getHeavyTrafficColor(self):
        return self.heavy_traffic_color

    def setModerateTrafficColor(self, value):
        self.moderate_traffic_color = value

    def getModerateTrafficColor(self):
        return self.moderate_traffic_color

    def setLightTrafficColor(self, value):
        self.light_traffic_color = value

    def getLightTrafficColor(self):
        return self.light_traffic_color

    def setNoTrafficColor(self, value):
        self.no_traffic_color = value

    def getNoTrafficColor(self):
        return self.no_traffic_color

    def setNoInformationColor(self, value):
        self.noinformation_traffic_color = value

    def getNoInformationTrafficColor(self):
        return self.noinformation_traffic_color
