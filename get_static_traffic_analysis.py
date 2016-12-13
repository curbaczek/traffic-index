import os
import pprint
from PIL import Image
from lib.bing_tile_handler import BingTileHandler
from lib.util.image_analysis import get_color_count, get_color_classes
from lib import model


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


def get_color_class_sum(color_class_result, colors):
    result = 0
    for color in color_class_result:
        if color in colors:
            result += color_class_result[color]["count"]
    return result


if __name__ == "__main__":
    args = get_parser().parse_args()
    traffic_handler = BingTileHandler()

    temp_dir = args.dest_dir
    os.makedirs(temp_dir, exist_ok=True)

    tile_center = traffic_handler.getTileImage(args.lat, args.lng, 0, 0, args.zoom, temp_dir)
    Image.open(tile_center).show()
    print(tile_center)

    color_classes = get_color_classes(tile_center, [
        ("green", (122, 187, 68)),
        ("dark-green", (98, 168, 69)),
        ("olive", (150, 180, 122)),
        ("red", (210, 57, 64)),
        ("orange", (253, 191, 76)),
        ("yellow", (244, 236, 87)),
        ("dark-yellow", (205, 180, 50)),
        ("black", (0, 0, 0)),
        ("white", (255, 255, 255)),
    ], threshold=25)

    heavy_traffic = get_color_class_sum(color_classes, ["red"])
    moderate_traffic = get_color_class_sum(color_classes, ["orange"])
    light_traffic = get_color_class_sum(color_classes, ["yellow", "dark-yellow"])
    no_traffic = get_color_class_sum(color_classes, ["green", "dark-green", "olive"])
    no_information = get_color_class_sum(color_classes, ["black", "white"])
    unassigned = get_color_class_sum(color_classes, ["z-no-class"])

    traffic_analysis = model.TrafficAnalysis(
        heavy_traffic,
        moderate_traffic,
        light_traffic,
        no_traffic,
        no_information,
        unassigned)

    print("*** color analysis result ***")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(color_classes)

    print("*** area analysis result ***")
    print(traffic_analysis)

    print("images loaded.")
