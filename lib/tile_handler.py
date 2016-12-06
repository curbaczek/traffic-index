from abc import ABC, abstractmethod


class TileHandler(ABC):

    @abstractmethod
    def getFileType(self):
        pass

    @abstractmethod
    def getTileWidth(self):
        pass

    @abstractmethod
    def getTileHeight(self):
        pass

    @abstractmethod
    def getTile(self, lat, lng, x, y, zoom):
        """ load tile and return temporary filename """
        pass

    @abstractmethod
    def getTiles(self, lat, lng, zoom, tile_count):
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

    def getHeavyTrafficColor(self):
        return self.heavy_traffic_color

    def getModerateTrafficColor(self):
        return self.moderate_traffic_color

    def getLightTrafficColor(self):
        return self.light_traffic_color

    def getNoTrafficColor(self):
        return self.no_traffic_color

    def getNoInformationTrafficColor(self):
        return self.noinformation_traffic_color
