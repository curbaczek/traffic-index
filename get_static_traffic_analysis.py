"""
load current traffic situation or a given snapshot and analyse it
"""

import os
import tempfile

from lib import model
from lib.tile_analysis import TrafficTileMapAnalysis, TrafficTileAnalysis, DEFAULT_TRAFFIC_TILE_COLOR_THRESHOLD

from lib.data_handler import SUBDIR_TRAFFIC
from lib.bing_tile_handler import BingTileHandler
from lib.util.file import open_file_from_shell, get_target_directory
from lib.util.image_analysis import get_filled_up_image

DEBUG_MODE = False


def get_parser():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input",
                        dest="input",
                        help="read this file",
                        metavar="FILE",
                        default="")
    parser.add_argument('--lat',
                        type=str,
                        help="latitude of the city",
                        required=False)
    parser.add_argument('--lng',
                        type=str,
                        help="longitude of the city",
                        required=False)
    parser.add_argument('--zoom',
                        type=int,
                        help="zoom level to analyse",
                        required=False,
                        default=14)
    parser.add_argument('--tiles',
                        type=int,
                        help="number of tiles taken around the center one, (2n-1)² images will be generated, " +
                        "(8n-8) more than the previous tile level",
                        dest='tile_count',
                        required=False,
                        default=1)
    parser.add_argument('--skip',
                        type=str,
                        help="comma-seperated list of tiles identified by their coordinates, e.g. '(0,0),(-1,-2)'",
                        required=False,
                        default="")
    parser.add_argument('--threshold',
                        type=int,
                        default=30,
                        help="threshold of the image analysis")
    parser.add_argument('--dest',
                        type=str,
                        help="dir to save the images",
                        default="",
                        dest='dest_dir',
                        required=False)
    parser.add_argument('--check_latest_tile',
                        help="skips the download of new tiles and takes the latest tiles from the image directory",
                        action='store_true')
    parser.add_argument('--show_grid_image',
                        help="generates and shows the grid image of the current tile map",
                        action='store_true')
    parser.add_argument('--show_color_classes_image',
                        help="shows the tile with the identified color classes",
                        action='store_true')

    parser.set_defaults(check_latest_tile=False)
    parser.set_defaults(show_grid_image=False)
    parser.set_defaults(show_color_classes_image=False)

    return parser


def get_tile_list(args, traffic_handler, target_dir):

    tile_list = []

    if (args.input == ""):

        if (args.lat == ""):
            raise Exception("[ERROR] latitude value should be set")
        if (args.lng == ""):
            raise Exception("[ERROR] latitude value should be set")

        tile_list = traffic_handler.getTiles(
            args.lat, args.lng, args.zoom, args.tile_count, target_dir, args.check_latest_tile)

    else:
        tile_list.append(args.input)
        print("loaded saved image: {}".format(args.input))

    return tile_list

if __name__ == "__main__":

    args = get_parser().parse_args()

    target_dir = get_target_directory(args.lat, args.lng, SUBDIR_TRAFFIC) if (args.dest_dir == "") else args.dest_dir
    os.makedirs(target_dir, exist_ok=True)
    print("target directory '{}'".format(target_dir))

    tile_handler = BingTileHandler()
    tile_handler.printer.setDebugMode(DEBUG_MODE)
    tile_list = get_tile_list(args, tile_handler, target_dir)
    if len(tile_list) == 0:
        print("[ERROR] no images found and download of new tiles was not successfull, " +
              "please check your internet connection")
        exit()

    tile_map = model.TileMap()
    tile_map.importFilelist(tile_list)
    tile_map.deactivateTiles(args.skip)
    print("all images loaded in target directory")

    assert args.threshold > 0, "threshold must be positive"
    analysis = TrafficTileMapAnalysis(tile_map, args.threshold, csv_file=None, debug_mode=DEBUG_MODE)

    if args.show_grid_image:
        tf = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tile_map.saveTileMapImage(tf.name, target_dir)
        print("grid image generated, try to open the image {}".format(tf.name))
        open_file_from_shell(tf.name)

    if args.show_color_classes_image:
        tile_file = tile_list.pop(0)
        tile = model.Tile.fromfile(tile_file)
        print("*** generate fill-up image of {} ***".format(tile_file))

        color_green = (122, 187, 68)
        color_red = (210, 57, 64)
        color_orange = (251, 195, 75)
        color_yellow = (244, 236, 87)

        NOINFORMATION_COLOR = (255, 255, 255)

        color_translation = {
            "green": color_green,
            "red": color_red,
            "orange": color_orange,
            "yellow": color_yellow
        }

        fill_color_definiton = []
        color_classes_definition = TrafficTileAnalysis(tile, args.threshold).color_definitions
        for color_definition in color_classes_definition:
            for color in color_definition[1]:
                fill_color_definiton.append(
                    (color_translation[color_definition[0]], color)
                )

        tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        get_filled_up_image(
            tile_file, tmp_file.name, fill_color_definiton,
            threshold=args.threshold, unassigned_color=NOINFORMATION_COLOR)
        open_file_from_shell(tmp_file.name)
