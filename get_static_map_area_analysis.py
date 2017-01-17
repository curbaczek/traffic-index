"""
load area situation and analyzes it
"""

import os
import tempfile

from lib import model
from lib.tile_analysis import AreaTileMapAnalysis, DEFAULT_AREA_TILE_COLOR_THRESHOLD

from lib.data_handler import get_tile, SUBDIR_TILES
from lib.gmap_tile_handler import GMapTileHandler
from lib.util.file import open_file_from_shell, get_target_directory

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
    parser.add_argument('--tiles',
                        type=int,
                        help="number of tiles taken around the center one, (2n-1)² images will be generated, " +
                        "(8n-8) more than the previous tile level",
                        dest='tile_count',
                        required=True)
    parser.add_argument('--skip',
                        type=str,
                        help="comma-seperated list of tiles identified by their coordinates, e.g. '(0,0),(-1,-2)'",
                        required=False,
                        default="")
    parser.add_argument('--dest',
                        type=str,
                        help="dir to save the images",
                        default="",
                        dest='dest_dir',
                        required=False)
    parser.add_argument('--csv',
                        type=str,
                        help="file to save the analysis results as csv",
                        default="",
                        dest='csv_out',
                        required=False)
    parser.add_argument('--show_color_result',
                        help="shows the complete color result with all counts",
                        action='store_true')
    parser.add_argument('--show_unknown_colors',
                        help="shows the colors that can not be classified",
                        action='store_true')
    parser.add_argument('--show_grid_image',
                        help="generates and shows the grid image of the current tile map",
                        action='store_true')
    parser.add_argument('--show_detailed_analysis',
                        help="shows the area analysis of every tile",
                        action='store_true')

    parser.set_defaults(show_color_result=False)
    parser.set_defaults(show_unknown_colors=False)
    parser.set_defaults(show_grid_image=False)
    parser.set_defaults(show_detailed_analysis=False)

    return parser


if __name__ == "__main__":

    args = get_parser().parse_args()

    target_dir = get_target_directory(args.lat, args.lng, SUBDIR_TILES) if (args.dest_dir == "") else args.dest_dir
    os.makedirs(target_dir, exist_ok=True)
    print("target directory '{}'".format(target_dir))

    tile_handler = GMapTileHandler()
    tile_handler.printer.setDebugMode(DEBUG_MODE)
    tile_list = tile_handler.getTiles(args.lat, args.lng, args.zoom, args.tile_count, target_dir)
    tile_map = model.TileMap()
    tile_map.importFilelist(tile_list)
    tile_map.deactivateTiles(args.skip)
    print("all images loaded in target directory")

    analysis = AreaTileMapAnalysis(tile_map, DEFAULT_AREA_TILE_COLOR_THRESHOLD, args.csv_out, debug_mode=DEBUG_MODE)
    print(analysis)
    if args.csv_out != "":
        print("single area analysis results saved to {}".format(args.csv_out))

    if args.show_grid_image:
        tf = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tile_map.saveTileMapImage(tf.name, target_dir)
        print("grid image generated, try to open the image {}".format(tf.name))
        open_file_from_shell(tf.name)
