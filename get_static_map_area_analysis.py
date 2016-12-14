import os
import pprint
import time

from PIL import Image

from lib import data_handler
from lib import model
from lib.data_handler import get_location_tile
from lib.gmap_tile_handler import GMapTileHandler
from lib.util.image_analysis import get_color_count, get_color_classes

LOCATION_DIR = "res/data/locations"


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
    parser.add_argument('--dest',
                        type=str,
                        help="dir to save the images",
                        default="",
                        dest='dest_dir',
                        required=False)
    parser.add_argument('--show_color_result',
                        help="shows the complete color result with all counts",
                        action='store_true')
    parser.add_argument('--show_unknown_colors',
                        help="shows the colors that can not be classified",
                        action='store_true')

    parser.set_defaults(show_color_result=False)
    parser.set_defaults(show_unknown_colors=False)

    return parser


def get_target_directory(args):
    latlng_dir = "{},{}".format(args.lat, args.lng)
    location_dir = os.path.join(LOCATION_DIR, latlng_dir, data_handler.SUBDIR_TILES)
    return location_dir if (args.dest_dir == "") else args.dest_dir


if __name__ == "__main__":
    args = get_parser().parse_args()

    print("*** download area tiles ***")

    target_dir = get_target_directory(args)
    print("set target directory '{}'".format(target_dir))
    os.makedirs(target_dir, exist_ok=True)

    area_handler = GMapTileHandler()
    area_handler.setDebugMode(True)
    tile_list = area_handler.getTiles(args.lat, args.lng, args.zoom, args.tile_count, target_dir)

    print("all images loaded in target directory")

    color_definitions = [
        ("red", (255, 0, 0)),
        ("green", (0, 255, 0)),
        ("blue", (0, 0, 255)),
        ("white", (255, 255, 255)),
        ("black", (0, 0, 0))
    ]
    color_threshold = 130

    overall_roadmap = 0
    overall_highway = 0
    overall_manmade = 0
    overall_nature = 0
    overall_transit = 0
    overall_unassigned = 0

    overall_start_time = time.time()

    for file_name in tile_list:
        tile = get_location_tile(file_name)
        file_path = os.path.join(target_dir, file_name)

        print("*** analyse area {:+d}x{:+d} ***".format(tile.x, tile.y))

        start_time = time.time()
        color_result = get_color_classes(file_path, color_definitions, threshold=color_threshold)
        end_time = time.time()

        analysis_roadmap = color_result["red"]["count"]
        analysis_highway = color_result["green"]["count"]
        analysis_manmade = color_result["blue"]["count"]
        analysis_nature = color_result["white"]["count"]
        analysis_transit = color_result["black"]["count"]
        analysis_unassigned = color_result["unknown"]["count"]

        area_analysis = model.AreaAnalysis(
            analysis_roadmap, analysis_highway, analysis_manmade,
            analysis_nature, analysis_transit, analysis_unassigned)

        overall_roadmap += analysis_roadmap
        overall_highway += analysis_highway
        overall_manmade += analysis_manmade
        overall_nature += analysis_nature
        overall_transit += analysis_transit
        overall_unassigned += analysis_unassigned

        if (args.show_color_result):
            print("--- color result")
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(color_result)

        if (args.show_unknown_colors):
            print("--- unknown color result")
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(color_result["unknown"])

        print(area_analysis)
        print("execution time: {:4f} ms".format(1000*(end_time - start_time)))

    overall_end_time = time.time()

    overall_area_analysis = model.AreaAnalysis(
        overall_roadmap, overall_highway, overall_manmade,
        overall_nature, overall_transit, overall_unassigned)

    print("*** overall analysis ***")
    print(overall_area_analysis)
    print("total execution time: {:4f} ms".format(1000*(overall_end_time - overall_start_time)))
