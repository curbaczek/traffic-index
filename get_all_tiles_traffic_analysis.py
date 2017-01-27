"""
analyses all given traffic tilemaps of a given location and writes the analysis
result to a csv file
"""

import os
import time
from time import strftime
from datetime import datetime
from lib import model

from lib.tile_analysis import TrafficTileMapAnalysis, DEFAULT_TRAFFIC_TILE_COLOR_THRESHOLD
from lib.data_handler import get_tilemap_list, SUBDIR_TRAFFIC
from lib.bing_tile_handler import BingTileHandler
from lib.util.file import get_target_directory

DEBUG_MODE = False


def get_parser():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--lat',
                        type=str,
                        help="latitude of the city",
                        required=True)
    parser.add_argument('--lng',
                        type=str,
                        help="longitude of the city",
                        required=True)
    parser.add_argument('--zoom',
                        type=int,
                        help="zoom level to analyse",
                        required=True)
    parser.add_argument('--threshold',
                        type=int,
                        default=DEFAULT_TRAFFIC_TILE_COLOR_THRESHOLD,
                        help="threshold of the image analysis")
    parser.add_argument('--csv',
                        type=str,
                        help="file to save the analysis results as csv",
                        default=None,
                        dest='csv_out',
                        required=True)

    return parser


if __name__ == "__main__":

    args = get_parser().parse_args()

    target_dir = get_target_directory(args.lat, args.lng, SUBDIR_TRAFFIC)
    os.makedirs(target_dir, exist_ok=True)
    print("target directory '{}'".format(target_dir))

    assert args.threshold > 0, "threshold must be positive"
    traffic_handler = BingTileHandler()
    traffic_handler.printer.setDebugMode(DEBUG_MODE)
    search_data_src = traffic_handler.getDataSource()
    search_file_format = traffic_handler.getFileFormat()
    all_traffic_tilemaps = get_tilemap_list(target_dir, search_data_src, args.zoom, search_file_format)
    print("found {} traffic tile maps in target directory".format(len(all_traffic_tilemaps)))

    tile_map_id = 0
    for tile_map in all_traffic_tilemaps:
        tile_map_id += 1
        print("analyse tilemap {:3d}/{:3d}".format(tile_map_id, len(all_traffic_tilemaps)))
        analysis = TrafficTileMapAnalysis(
            tile_map, args.threshold, args.csv_out, DEBUG_MODE, init_csv=(tile_map_id == 1))

    print("tiles analyzed, result written to {}".format(args.csv_out))
