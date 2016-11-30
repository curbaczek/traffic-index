
SOURCE_GMAP = 'GMAP'
SOURCE_BING = 'BING'
SOURCE_OST = 'OPENSTREETMAP'


class Location(object):

    def __init__(self, title, lat, lng, tile_map):
        self.title = title
        self.lat = lat
        self.lng = lng
        self.tile_map = tile_map


class TileMap(object):

    def __init__(self):
        self.tiles = []

    def appendTile(self, tile):
        self.tiles.append(tile)

    # TODO
    # def getActiveTiles(self):
    # def getTraffic...
    # def __str__(self):


class Tile(object):

    def __init__(self, x, y, zoom, data_src, time, area_analysis, traffic_snapshot):
        self.x = x
        self.y = y
        self.zoom = zoom
        self.data_src = data_src
        self.time = time
        self.active = True
        self.area_analysis = area_analysis
        self.traffic_snapshot = traffic_snapshot

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False


class GMapTile(Tile):

    def __init__(self, x, y, zoom, time, area_analysis, traffic_snapshot):
        Tile.__init__(self, x, y, zoom, SOURCE_GMAP, time, area_analysis, traffic_snapshot)


class BingTile(Tile):

    def __init__(self, x, y, zoom, time, area_analysis, traffic_snapshot):
        Tile.__init__(self, x, y, zoom, SOURCE_BING, time, area_analysis, traffic_snapshot)


class AreaAnalysis(object):

    def __init__(self, roadmap, highway, manmade, nature, transit, unassigned):
        self.roadmap = roadmap
        self.highway = highway
        self.manmade = manmade
        self.nature = nature
        self.transit = transit
        self.unassigned = unassigned

    def value_sum(self):
        return self.roadmap + self.highway + self.manmade + self.nature + self.transit + self.unassigned

    def get_roadmap_portion(self):
        return self.roadmap/self.value_sum()

    def get_highway_portion(self):
        return self.highway/self.value_sum()

    def get_manmade_portion(self):
        return self.manmade/self.value_sum()

    def get_nature_portion(self):
        return self.nature/self.value_sum()

    def get_transit_portion(self):
        return self.transit/self.value_sum()

    def __str__(self):
        return """
            roadmap: {:.0f}%\n
            highway: {:.0f}%\n
            man-made: {:.0f}%\n
            nature: {:.0f}%\n
            transit: {:.0f}%\n
            TOTAL: {:.0f}%""".format(
            self.get_roadmap_portion()*100,
            self.get_highway_portion()*100,
            self.get_manmade_portion()*100,
            self.get_nature_portion()*100,
            self.get_transit_portion()*100)


class TrafficSnapshot(object):

    def __init__(self, time, data_src, zoom_level, traffic_analysis):
        self.time = time
        self.data_src = data_src
        self.zoom_level = zoom_level
        self.traffic_analysis = traffic_analysis


class TrafficAnalysis(object):

    def __init__(self, heavy, moderate, light, notraffic, noinformation, unassigned):
        self.heavy = heavy
        self.moderate = moderate
        self.light = light
        self.notraffic = notraffic
        self.noinformation = noinformation
        self.unassigned = unassigned

    def value_sum(self):
        return self.heavy + self.moderate + self.light + self.notraffic + self.noinformation + self.unassigned

    def get_heavy_portion(self):
        return self.heavy/self.value_sum()

    def get_moderate_portion(self):
        return self.moderate/self.value_sum()

    def get_light_portion(self):
        return self.light/self.value_sum()

    def get_notraffic_portion(self):
        return self.notraffic/self.value_sum()

    def get_noinformation_portion(self):
        return self.noinformation/self.value_sum()

    def __str__(self):
        return """
            heavy: {:.0f}%\n
            moderate: {:.0f}%\n
            light: {:.0f}%\n
            notraffic: {:.0f}%\n
            noinformation: {:.0f}%\n
            TOTAL: {:.0f}%""".format(
            self.get_heavy_portion()*100,
            self.get_moderate_portion()*100,
            self.get_light_portion()*100,
            self.get_notraffic_portion()*100,
            self.get_noinformation_portion()*100)
