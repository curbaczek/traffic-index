import os
import pprint
import tempfile

from PIL import Image
from lib import data_handler
from lib import model

from lib.bing_tile_handler import BingTileHandler
from lib.util.image_analysis import get_color_count, get_color_classes, get_filled_up_image

LOCATION_DIR = "res/data/locations"


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
    parser.add_argument('--show_color_classes_image',
                        help="shows the tile with the identified color classes",
                        action='store_true')

    parser.set_defaults(show_color_classes_image=False)

    return parser


def get_color_class_sum(color_class_result, colors):
    result = 0
    for color in color_class_result:
        if color in colors:
            result += color_class_result[color]["count"]
    return result


def get_traffic_analysis(color_analysis_result):
    heavy_traffic = color_analysis_result["red"]["count"]
    moderate_traffic = color_analysis_result["orange"]["count"]
    light_traffic = color_analysis_result["yellow"]["count"]
    no_traffic = color_analysis_result["green"]["count"]
    no_information = color_analysis_result["unknown"]["count"]

    return model.TrafficAnalysis(
        heavy_traffic,
        moderate_traffic,
        light_traffic,
        no_traffic,
        no_information,
        unassigned=0)


def get_target_directory(args):
    latlng_dir = "{},{}".format(args.lat, args.lng)
    location_dir = os.path.join(LOCATION_DIR, latlng_dir, data_handler.SUBDIR_TRAFFIC)
    return location_dir if (args.dest_dir == "") else args.dest_dir


def get_color_class_definition():
    return [
        ("green", [(122, 187, 68), (117, 183, 66), (97, 166, 69)]),
        ("red", [(210, 57, 64), (205, 63, 68), (206, 75, 76), (208, 59, 65)]),
        ("orange", [(251, 195, 75), (252, 186, 74), (240, 167, 61)]),
        ("yellow", [(244, 236, 87), (242, 232, 84), (240, 232, 86), (218, 194, 61)])
    ]


if __name__ == "__main__":

    args = get_parser().parse_args()

    target_dir = get_target_directory(args)
    print("set target directory '{}'".format(target_dir))
    os.makedirs(target_dir, exist_ok=True)

    traffic_handler = BingTileHandler()
    traffic_handler.setDebugMode(True)

    ANALYSE_THRESHOLD = args.threshold
    assert ANALYSE_THRESHOLD > 0, "threshold must be positive"
    NOINFORMATION_COLOR = (255, 255, 255)

    color_green = (122, 187, 68)
    color_red = (210, 57, 64)
    color_orange = (251, 195, 75)
    color_yellow = (244, 236, 87)

    tile_list = []
    if (args.input == ""):

        if (args.lat == ""):
            raise Exception("[ERROR] latitude value should be set")
        if (args.lng == ""):
            raise Exception("[ERROR] latitude value should be set")

        print("*** download traffic tiles ***")
        tile_list = traffic_handler.getTiles(args.lat, args.lng, args.zoom, args.tile_count, target_dir)
        print("all images loaded in target directory")

    else:
        tile_list.append(args.input)
        print("loaded saved image: {}".format(args.input))

    color_classes_definition = get_color_class_definition()
    for tile in tile_list:

        tile_filename = os.path.join(target_dir, tile)
        color_classes = get_color_classes(tile_filename, color_classes_definition, threshold=ANALYSE_THRESHOLD)
        traffic_analysis = get_traffic_analysis(color_classes)

        # print("*** full color analysis result ***")
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(color_classes)

        # print("*** unknown color analysis result ***")
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(color_classes["unknown"])

        print("*** area analysis {} ***".format(tile))
        print(traffic_analysis)
        (img_width, img_height) = Image.open(tile_filename).size
        assert traffic_analysis.get_overall_sum() == img_width * img_height, \
            "pixel sum {:d} does not equeal analysis pixel sum {:d}".format(
                img_width * img_height, traffic_analysis.get_overall_sum())

        if args.show_color_classes_image:

            print("*** generate fill-up image {} ***".format(tile))

            color_translation = {
                "green": color_green,
                "red": color_red,
                "orange": color_orange,
                "yellow": color_yellow
            }

            fill_color_definiton = []
            for color_definition in color_classes_definition:
                for color in color_definition[1]:
                    fill_color_definiton.append(
                        (color_translation[color_definition[0]], color)
                    )

            tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            get_filled_up_image(
                tile_filename, tmp_file.name, fill_color_definiton,
                threshold=ANALYSE_THRESHOLD, unassigned_color=NOINFORMATION_COLOR)
            color_classes = get_color_classes(tmp_file.name, color_classes_definition, threshold=ANALYSE_THRESHOLD)
            Image.open(tile_filename).show()
            Image.open(tmp_file.name).show()

            traffic_analysis_check = get_traffic_analysis(color_classes)
            assert traffic_analysis_check.get_overall_sum() == img_width * img_height, \
                "pixel sum {:d} does not equeal analysis pixel sum {:d}".format(
                    img_width * img_height, traffic_analysis_check.get_overall_sum())
            assert traffic_analysis.get_traffic_sum() == traffic_analysis_check.get_traffic_sum(), \
                "fill-up image analysis pixel sum {:d} differs from original image analysis {:d}".format(
                    traffic_analysis_check.get_traffic_sum(), traffic_analysis.get_traffic_sum())
