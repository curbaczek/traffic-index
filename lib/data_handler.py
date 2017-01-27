import os
import re
import glob

SUBDIR_TILES = "tiles"
SUBDIR_TRAFFIC = "traffic"

REG_PART_X = 1
REG_PART_Y = 2
REG_PART_DATASRC = 3
REG_PART_ZOOM = 4
REG_PART_TIMESTAMP = 5
REG_PART_FILEFORMAT = 6


def get_tile_filename_parts(filename):
    pattern = re.compile("^(\-?\d+)_(\-?\d+)_([A-Z]+)_(\d+)_(\d+)\.([A-Z]+)")
    match = pattern.match(os.path.basename(filename).upper())
    return match


def get_tile_filename(x, y, data_src, zoom, timestamp, file_format):
    return "{}_{}_{}_{}_{}.{}".format(x, y, data_src, zoom, timestamp, file_format)


def get_tile_part(filename, part):
    return get_tile_filename_parts(filename).group(part)


def get_tile_x(filename):
    return int(get_tile_part(filename, REG_PART_X))


def get_tile_y(filename):
    return int(get_tile_part(filename, REG_PART_Y))


def get_tile_data_src(filename):
    return get_tile_part(filename, REG_PART_DATASRC)


def get_tile_zoom(filename):
    return int(get_tile_part(filename, REG_PART_ZOOM))


def get_tile_timestamp(filename):
    return int(get_tile_part(filename, REG_PART_TIMESTAMP))


def get_tile_fileformat(filename):
    return get_tile_part(filename, REG_PART_FILEFORMAT)


def get_latest_tile(directory, x, y, data_src, zoom, file_format):
    search_pattern = get_tile_filename(x, y, data_src, zoom, "*", file_format)
    file_list = glob.glob(os.path.join(directory, search_pattern))

    latest_timestamp = 0
    latest_tile = ""
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        file_timestamp = get_tile_timestamp(file_name)
        if (file_timestamp > latest_timestamp):
            latest_tile = file_name
            latest_timestamp = file_timestamp

    return None if (latest_tile == "") else latest_tile


def get_tile_list(directory, data_src, zoom, file_format, order_by=None):
    """ get all tiles in a directory that match the given parameters """
    search_pattern = get_tile_filename("*", "*", data_src, zoom, "*", file_format)
    file_list = glob.glob(os.path.join(directory, search_pattern))
    tile_list = list(map(os.path.basename, file_list))
    if order_by is not None:
        tile_list = sorted(tile_list, key=lambda tile_name: get_tile_part(tile_name, order_by))
    return tile_list


def get_tilemap_list(directory, data_src, zoom, file_format):
    """ get the tilemaps from all single tiles in a directory """
    tile_list = get_tile_list(directory, data_src, zoom, file_format, REG_PART_TIMESTAMP)
    tile_map_list = []
    from lib import model
    import copy
    current_tile_map = model.TileMap()
    for tile_filename in tile_list:
        tile_path = os.path.join(directory, tile_filename)
        x = get_tile_x(tile_filename)
        y = get_tile_y(tile_filename)
        if current_tile_map.getPositionTile(x, y) is not None:
            tile_map_list.append(copy.deepcopy(current_tile_map))
            current_tile_map = model.TileMap()
        current_tile_map.appendTile(model.Tile.fromfile(tile_path))
    tile_map_list.append(copy.deepcopy(current_tile_map))

    return tile_map_list

"""
def get_area_tile_map(location_dir):
    tile_dir = os.path.join(location_dir, SUBDIR_TILES)
    tile_list = [get_tile(f) for f in os.listdir(tile_dir) if os.path.isfile(os.path.join(tile_dir, f))]
    result_map = model.TileMap()
    result_map.setTiles(tile_list)
    return result_map


def load_location(data_dir, name, lat, lng):
    location_dir = "{}_{}".format(str(lat), str(lng))
    location_data_dir = os.path.join(data_dir, location_dir)
    if not os.path.exists(location_data_dir):
        os.makedirs(location_data_dir)
    return model.Location(name, lat, lng, get_area_tile_map(location_data_dir))
"""
