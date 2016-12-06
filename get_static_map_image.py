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
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    area_handler = GMapTileHandler()
    area_image = area_handler.getTile(args.lat, args.lng, 0, 0, args.zoom)
    image = Image.open(area_image)
    image.show()
