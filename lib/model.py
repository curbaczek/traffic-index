from __future__ import division

import os

from lib.data_handler import get_tile_filename
from lib.util.image import generate_grid_image

SOURCE_GMAP = 'GMAP'
SOURCE_BING = 'BING'


class Location(object):

    def __init__(self, name, lat, lng, tile_map):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.tile_map = tile_map

    def __str__(self):
        return "{} ({}, {})\n{}".format(self.name, str(self.lat), str(self.lng), str(self.tile_map))


class TileMap(object):

    def __init__(self):
        self.resetTiles()

    def resetTiles(self):
        self.tiles = []
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0

    def setTiles(self, tiles):
        self.resetTiles()
        for tile in tiles:
            self.appendTile(tile)

    def appendTile(self, tile):
        if (tile.x < self.minX):
            self.minX = tile.x
        if (tile.x > self.minX):
            self.maxX = tile.x
        if (tile.y < self.minY):
            self.minY = tile.y
        if (tile.y > self.maxY):
            self.maxY = tile.y
        self.tiles.append(tile)

    # TODO
    # def getActiveTiles(self):
    # def getTraffic...
    # def __str__(self):

    def saveTileMapImage(self, filename, tile_directory):
        index_shift_x = abs(self.minX)
        index_shift_y = abs(self.minY)
        matrix_width = self.maxX - self.minX + 1
        matrix_height = self.maxY - self.minY + 1
        matrix = [[0 for x in range(matrix_width)] for y in range(matrix_height)]
        for tile in self.tiles:
            matrix_x = tile.x + index_shift_x
            matrix_y = tile.y + index_shift_y
            tile_filename = get_tile_filename(tile.x, tile.y, tile.data_src, tile.zoom, tile.timestamp, tile.file_format)
            tile_filename = os.path.join(tile_directory, tile_filename)
            matrix[matrix_x][matrix_y] = (tile.x, tile.y, tile_filename)
        generate_grid_image(filename, matrix)


class Tile(object):

    def __init__(self, x, y, data_src, zoom, timestamp, file_format):
        self.x = x
        self.y = y
        self.data_src = data_src
        self.zoom = zoom
        self.timestamp = timestamp
        self.file_format = file_format
        self.active = True

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def __str__(self):
        return "{},{} @ zoom {} from {} at {}".format(self.x, self.y, self.zoom, self.data_src, self.timestamp)


class AreaAnalysis(object):

    def __init__(self, roadmap, highway, manmade, nature, transit, unassigned):
        self.roadmap = roadmap
        self.highway = highway
        self.manmade = manmade
        self.nature = nature
        self.transit = transit
        self.unassigned = unassigned

    def get_overall_sum(self):
        return self.get_assigned_sum() + self.unassigned

    def get_assigned_sum(self):
        return self.roadmap + self.highway + self.manmade + self.nature + self.transit

    def get_roadmap_portion(self):
        return self.roadmap/self.get_overall_sum()

    def get_highway_portion(self):
        return self.highway/self.get_overall_sum()

    def get_manmade_portion(self):
        return self.manmade/self.get_overall_sum()

    def get_nature_portion(self):
        return self.nature/self.get_overall_sum()

    def get_transit_portion(self):
        return self.transit/self.get_overall_sum()

    def get_unassigned_portion(self):
        return self.unassigned/self.get_overall_sum()

    def __str__(self):
        return (
            "roadmap: {:.4f}%\n" +
            "highway: {:.4f}%\n" +
            "man-made: {:.4f}%\n" +
            "nature: {:.4f}%\n" +
            "transit: {:.4f}%").format(
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

    def get_overall_sum(self):
        return self.get_assigned_sum() + self.unassigned

    def get_assigned_sum(self):
        return self.get_traffic_sum() + self.noinformation

    def get_traffic_sum(self):
        return self.heavy + self.moderate + self.light + self.notraffic

    def get_heavy_portion(self):
        return self.heavy/self.get_overall_sum()

    def get_moderate_portion(self):
        return self.moderate/self.get_overall_sum()

    def get_light_portion(self):
        return self.light/self.get_overall_sum()

    def get_notraffic_portion(self):
        return self.notraffic/self.get_overall_sum()

    def get_noinformation_portion(self):
        return self.noinformation/self.get_overall_sum()

    def get_unassigned_portion(self):
        return self.unassigned/self.get_overall_sum()

    def __str__(self):
        traffic_sum = self.get_traffic_sum()
        return (
            "heavy: {}px, {:.4f}% of total, {:.4f}% of traffic\n" +
            "moderate: {}px, {:.4f}% of total, {:.4f}% of traffic\n" +
            "light: {}px, {:.4f}% of total, {:.4f}% of traffic\n" +
            "no-traffic: {}px, {:.4f}% of total, {:.4f}% of traffic\n" +
            "no-information: {}px, {:.4f}% of total").format(
            self.heavy,
            self.get_heavy_portion()*100,
            0.0 if traffic_sum == 0 else 100*self.heavy/traffic_sum,
            self.moderate,
            self.get_moderate_portion()*100,
            0.0 if traffic_sum == 0 else 100*self.moderate/traffic_sum,
            self.light,
            self.get_light_portion()*100,
            0.0 if traffic_sum == 0 else 100*self.light/traffic_sum,
            self.notraffic,
            self.get_notraffic_portion()*100,
            0.0 if traffic_sum == 0 else 100*self.notraffic/traffic_sum,
            self.noinformation,
            self.get_noinformation_portion()*100)
