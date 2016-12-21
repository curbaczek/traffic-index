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
    parser.add_argument("-i", "--input",
                        dest="input",
                        help="read this file",
                        metavar="FILE",
                        default="",
                        required=False)
    parser.add_argument('--lat',
                        type=str,
                        help="latitude of the city")
    parser.add_argument('--lng',
                        type=str,
                        help="longitude of the city")
    parser.add_argument('--zoom',
                        type=int,
                        default=14,
                        help="zoom level to analyse")
    parser.add_argument('--dest',
                        type=str,
                        default="temp",
                        help="dir to save the images",
                        dest='dest_dir')
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

    if (args.input == ""):

        temp_dir = args.dest_dir
        os.makedirs(temp_dir, exist_ok=True)

        if (args.lat == ""):
            print("[WARNING] latitude value should be set")
        if (args.lng == ""):
            print("[WARNING] longitude value should be set")

        tile_center = traffic_handler.getTileImage(args.lat, args.lng, 0, 0, args.zoom, temp_dir)
        Image.open(tile_center).show()
        print("loaded new image: {}".format(tile_center))

    else:

        tile_center = args.input
        print("loaded saved image: {}".format(tile_center))

    (img_width, img_height) = Image.open(tile_center).size

    color_classes = get_color_classes(tile_center, [
        ("green", (125, 190, 25)),
        ("green", (125, 190, 75)),
        ("green", (125, 190, 125)),
        ("green", (154, 205, 50)),
        ("green", (154, 205, 100)),
        ("green", (100, 170, 75)),
        ("green", (150, 180, 122)),
        ("green", (170, 255, 25)),
        ("green", (170, 255, 75)),
        ("green", (170, 255, 100)),
        ("green", (170, 255, 150)),
        ("green", (170, 215, 25)),
        ("green", (170, 215, 75)),
        ("green", (170, 215, 100)),
        ("green", (170, 215, 150)),
        ("green", (205, 255, 100)),
        ("green", (205, 255, 150)),
        ("green", (205, 255, 200)),
        ("red", (210, 80, 70)),
        ("red", (210, 100, 70)),
        ("orange", (230, 200, 75)),
        ("orange", (230, 200, 125)),
        ("orange", (230, 200, 160)),
        ("yellow", (244, 236, 87)),
        ("yellow", (205, 180, 50)),
        ("yellow", (255, 255, 25)),
        ("yellow", (255, 255, 75)),
        ("yellow", (255, 255, 125)),
        ("yellow", (255, 255, 175)),
        ("yellow", (255, 255, 200)),
        ("yellow", (255, 255, 210)),
        ("black", (0, 0, 0)),
        ("white", (255, 255, 255)),
    ], threshold=25)

    heavy_traffic = color_classes["red"]["count"]
    moderate_traffic = color_classes["orange"]["count"]
    light_traffic = color_classes["yellow"]["count"]
    no_traffic = color_classes["green"]["count"]
    no_information = color_classes["black"]["count"] + color_classes["white"]["count"]
    unassigned = color_classes["unknown"]["count"]

    traffic_analysis = model.TrafficAnalysis(
        heavy_traffic,
        moderate_traffic,
        light_traffic,
        no_traffic,
        no_information,
        unassigned)

    assert traffic_analysis.get_overall_sum() == img_width * img_height

    print("*** full color analysis result ***")
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(color_classes)

    print("*** unknown color analysis result ***")
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(color_classes["unknown"])

    print("*** area analysis result ***")
    print(traffic_analysis)

    print("images loaded.")
