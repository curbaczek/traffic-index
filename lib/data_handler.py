import os
import re

from lib import model

SUBDIR_TILES = "tiles"
SUBDIR_TRAFFIC = "traffic"


def get_location_tile_filename(tile):
    return "{}_{}_{}_{}_{}.{}".format(tile.x, tile.y, tile.data_src, tile.zoom, tile.timestamp, tile.file_format)


def get_location_tile(filename):
    pattern = re.compile("^(\-?\d+)_(\-?\d+)_([A-Z]+)_(\d+)_(\d+)\.([A-Z]+)")
    match = pattern.match(filename.upper())
    if match is not None:
        result_tile = model.Tile(
            int(match.group(1)), int(match.group(2)), match.group(3),
            int(match.group(4)), int(match.group(5)), match.group(6))
    else:
        result_tile = None
    return result_tile


def load_location_tile_map(location_dir):
    tile_dir = os.path.join(location_dir, SUBDIR_TILES)
    tile_list = [get_location_tile(f) for f in os.listdir(tile_dir) if os.path.isfile(os.path.join(tile_dir, f))]
    result_map = model.TileMap()
    result_map.setTiles(tile_list)
    return result_map


def load_location(data_dir, name, lat, lng):
    location_dir = "{}_{}".format(str(lat), str(lng))
    location_data_dir = os.path.join(data_dir, location_dir)
    if not os.path.exists(location_data_dir):
        os.makedirs(location_data_dir)
    return model.Location(name, lat, lng, load_location_tile_map(location_data_dir))
