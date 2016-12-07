import os
from PIL import Image
from lib.gmap_tile_handler import GMapTileHandler


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
                        help="number of tiles taken around the center one",
                        dest='tile_count',
                        required=True)
    parser.add_argument('--dest',
                        type=str,
                        help="dir to save the images",
                        dest='dest_dir',
                        required=True)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    area_handler = GMapTileHandler()

    temp_dir = args.dest_dir
    os.makedirs(temp_dir, exist_ok=True)

    tile_center = area_handler.getTileImage(args.lat, args.lng, 0, 0, args.zoom, temp_dir)
    Image.open(tile_center).show()
    print(tile_center)
    tile_center = area_handler.getTileImage(args.lat, args.lng, -1, 0, args.zoom, temp_dir)
    Image.open(tile_center).show()
    print(tile_center)
    tile_center = area_handler.getTileImage(args.lat, args.lng, 0, 1, args.zoom, temp_dir)
    Image.open(tile_center).show()
    print(tile_center)
    # area_handler.getTiles(args.lat, args.lng, args.zoom, args.tile_count, temp_dir, printProgress=True)

    print("images loaded.")
