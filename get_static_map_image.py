import os
from PIL import Image
from lib.gmap_tile_handler import GMapTileHandler
from lib import data_handler

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
    return parser


def get_target_directory(args):
    latlng_dir = "{},{}".format(args.lat, args.lng)
    location_dir = os.path.join(LOCATION_DIR, latlng_dir, data_handler.SUBDIR_TILES)
    return location_dir if (args.dest_dir == "") else args.dest_dir


if __name__ == "__main__":
    args = get_parser().parse_args()

    target_dir = get_target_directory(args)
    print("set target directory '{}'".format(target_dir))
    os.makedirs(target_dir, exist_ok=True)

    area_handler = GMapTileHandler()
    area_handler.setDebugMode(True)
    tile_list = area_handler.getTiles(args.lat, args.lng, args.zoom, args.tile_count, target_dir)

    print("all images loaded in target directory")
