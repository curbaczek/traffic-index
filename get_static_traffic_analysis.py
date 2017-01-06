import os
import pprint
import tempfile
from PIL import Image
from lib.bing_tile_handler import BingTileHandler
from lib.util.image_analysis import get_color_count, get_color_classes, get_filled_up_image
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
    parser.add_argument('--threshold',
                        type=int,
                        default=30,
                        help="threshold of the image analysis")
    parser.add_argument('--dest',
                        type=str,
                        default="temp",
                        help="dir to save the images",
                        dest='dest_dir')
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
        print("loaded new image: {}".format(tile_center))

    else:
        tile_center = args.input
        print("loaded saved image: {}".format(tile_center))

    ANALYSE_THRESHOLD = args.threshold
    assert ANALYSE_THRESHOLD > 0
    NOINFORMATION_COLOR = (255, 255, 255)

    color_green = (122, 187, 68)
    color_red = (210, 57, 64)
    color_orange = (251, 195, 75)
    color_yellow = (244, 236, 87)

    color_classes_definition = [
        ("green", [color_green, (117, 183, 66), (97, 166, 69)]),
        ("red", [color_red, (205, 63, 68), (206, 75, 76), (208, 59, 65)]),
        ("orange", [color_orange, (252, 186, 74), (240, 167, 61)]),
        ("yellow", [color_yellow, (242, 232, 84), (240, 232, 86), (218, 194, 61)])
    ]

    color_classes = get_color_classes(tile_center, color_classes_definition, threshold=ANALYSE_THRESHOLD)
    traffic_analysis = get_traffic_analysis(color_classes)

    print("*** full color analysis result ***")
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(color_classes)

    print("*** unknown color analysis result ***")
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(color_classes["unknown"])

    print("*** area analysis result ***")
    print(traffic_analysis)
    (img_width, img_height) = Image.open(tile_center).size
    assert traffic_analysis.get_overall_sum() == img_width * img_height

    if args.show_color_classes_image:

        print("*** generate fill-up image ***")

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
            tile_center, tmp_file.name, fill_color_definiton,
            threshold=ANALYSE_THRESHOLD, unassigned_color=NOINFORMATION_COLOR)
        color_classes = get_color_classes(tmp_file.name, color_classes_definition, threshold=ANALYSE_THRESHOLD)
        Image.open(tile_center).show()
        Image.open(tmp_file.name).show()

        traffic_analysis_check = get_traffic_analysis(color_classes)
        assert traffic_analysis.get_overall_sum() == img_width * img_height
        assert traffic_analysis.get_traffic_sum() == traffic_analysis_check.get_traffic_sum()
