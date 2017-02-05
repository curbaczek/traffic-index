from __future__ import division

import os
from ast import literal_eval
from lib import data_handler

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

    def getPositionTile(self, x, y):
        result = None
        for tile in self.tiles:
            if (tile.x, tile.y) == (x, y):
                result = tile
                break
        return result

    def appendTile(self, tile):
        # TODO exception handling
        assert self.getPositionTile(tile.x, tile.y) is None
        if (tile.x < self.minX):
            self.minX = tile.x
        if (tile.x > self.minX):
            self.maxX = tile.x
        if (tile.y < self.minY):
            self.minY = tile.y
        if (tile.y > self.maxY):
            self.maxY = tile.y
        self.tiles.append(tile)

    def importFilelist(self, tile_file_list):
        for tile_file in tile_file_list:
            tile = Tile.fromfile(tile_file)
            self.appendTile(tile)

    def getTiles(self):
        return self.tiles

    def getActiveTiles(self):
        return [tile for tile in self.tiles if tile.active]

    def deactivateTiles(self, tile_list):
        if isinstance(tile_list, str):
            tile_list = [] if tile_list == "" else [x for x in literal_eval(tile_list)]
        for tile in self.tiles:
            if (tile.x, tile.y) in tile_list:
                tile.deactivate()

    def saveTileMapImage(self, filename, tile_directory):
        assert len(self.tiles) > 0
        index_shift_x = abs(self.minX)
        index_shift_y = abs(self.minY)
        matrix_width = self.maxX - self.minX + 1
        matrix_height = self.maxY - self.minY + 1
        matrix = [[0 for x in range(matrix_width)] for y in range(matrix_height)]
        for tile in self.tiles:
            matrix_x = tile.x + index_shift_x
            matrix_y = tile.y + index_shift_y
            if tile.active:
                tile_filename = data_handler.get_tile_filename(
                    tile.x, tile.y, tile.data_src, tile.zoom, tile.timestamp, tile.file_format)
                tile_filename = os.path.join(tile_directory, tile_filename)
            else:
                tile_filename = None
            matrix[matrix_x][matrix_y] = (tile.x, tile.y, tile_filename)
        generate_grid_image(filename, matrix)


class Tile(object):

    def __init__(self, x, y, data_src, zoom, timestamp=0, file_format="png", path=None):
        self.x = x
        self.y = y
        self.data_src = data_src
        self.zoom = zoom
        self.timestamp = timestamp
        self.file_format = file_format
        self.active = True
        if path is None or os.path.isfile(path):
            self.path = path
        else:
            raise Exception("can not generate tile, file \"{}\" was not found".format(path))

    @classmethod
    def fromfile(cls, filename):
        return cls(
            data_handler.get_tile_x(filename),
            data_handler.get_tile_y(filename),
            data_handler.get_tile_data_src(filename),
            data_handler.get_tile_zoom(filename),
            data_handler.get_tile_timestamp(filename),
            data_handler.get_tile_fileformat(filename),
            filename)

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def __str__(self):
        return "{},{} @ zoom {} from {} at {} ({}), file located at {}".format(
            self.x, self.y, self.zoom, self.data_src, self.timestamp,
            "active" if self.active else "inactive", self.path)


class TrafficSnapshot(object):

    def __init__(self, time, data_src, zoom_level, traffic_analysis):
        self.time = time
        self.data_src = data_src
        self.zoom_level = zoom_level
        self.traffic_analysis = traffic_analysis


class ConsolePrinter(object):

    debug_mode = False

    def setDebugMode(self, value):
        self.debug_mode = bool(value)

    def isDebugMode(self):
        return self.debug_mode

    def printMsg(self, msg):
        print(msg)

    def printErrorMsg(self, msg):
        self.printMsg("[ERROR] {}".format(msg))

    def printHeadlineMsg(self, msg, return_str=False):
        msg = "*** {} ***".format(msg)
        return msg if return_str else self.printMsg(msg)

    def printIndentedMsg(self, msg, return_str=False):
        msg = "--- {}".format(msg)
        return msg if return_str else self.printMsg(msg)

    def printDebugMsg(self, msg):
        if (self.isDebugMode()):
            print("[Debug] {}".format(msg))

    def printDebugHeadlineDebugMsg(self, msg):
        self.printDebugMsg(self.printHeadlineMsg(msg, return_str=True))

    def printIndentedDebugMsg(self, msg):
        self.printDebugMsg(self.printIndentedMsg(msg, return_str=True))
