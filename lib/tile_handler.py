from abc import ABC, abstractmethod
import time
from lib import model


class TileHandler(ABC):

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

    def createTile(self, x, y, zoom):
        current_time = int(time.time())
        return model.Tile(x, y, self.getDataSource(), zoom, current_time, self.getFileFormat())

    @abstractmethod
    def getTileImage(self, lat, lng, x, y, zoom, local_directory):
        pass

    @abstractmethod
    def getTiles(self, lat, lng, zoom, tile_count, local_directory):
        pass


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
