import os
import time
from time import strftime

from PIL import Image
from lib import model
from datetime import datetime

from lib.data_handler import get_tile, get_tile_timestamp, get_tile_list, SUBDIR_TRAFFIC
from lib.bing_tile_handler import BingTileHandler
from lib.util.image_analysis import get_color_classes
from lib.csv_handler import write_csv_data
from lib.util.file import remove_file

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
    parser.add_argument('--threshold',
                        type=int,
                        default=30,
                        help="threshold of the image analysis")
    parser.add_argument('--csv',
                        type=str,
                        help="file to save the analysis results as csv",
                        default="",
                        dest='csv_out',
                        required=True)

    return parser


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
    return os.path.join(LOCATION_DIR, latlng_dir, SUBDIR_TRAFFIC)


def write_csv_headline(filename):
    write_csv_data(filename, [
        'x', 'y', 'time', 'traffic_portion_heavy [%]', 'traffi_portion_moderate [%]', 'traffic_portion_light [%]',
        'traffic_portion_notraffic [%]', 'heavy [px]', 'moderate [px]', 'light [px]', 'notraffic [px]',
        'noinformation [px]', 'unassigned [px]', 'calculation time [ms]', 'tile filename'])


def write_analysis_result(filename, tile_filename, analysis_result, duration):
    tile = get_tile(tile_filename)
    traffic_sum = analysis_result.get_traffic_sum()
    write_csv_data(filename, [
        tile.x, tile.y,
        datetime.fromtimestamp(tile.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
        0.0 if traffic_sum == 0 else 100*analysis_result.heavy/traffic_sum,
        0.0 if traffic_sum == 0 else 100*analysis_result.moderate/traffic_sum,
        0.0 if traffic_sum == 0 else 100*analysis_result.light/traffic_sum,
        0.0 if traffic_sum == 0 else 100*analysis_result.notraffic/traffic_sum,
        analysis_result.heavy,
        analysis_result.moderate,
        analysis_result.light,
        analysis_result.notraffic,
        analysis_result.noinformation,
        analysis_result.unassigned,
        duration,
        tile_filename])


def get_color_class_definition():
    return [
        ("green", [(122, 187, 68), (117, 183, 66), (97, 166, 69)]),
        ("red", [(210, 57, 64), (205, 63, 68), (206, 75, 76), (208, 59, 65)]),
        ("orange", [(251, 195, 75), (252, 186, 74), (240, 167, 61)]),
        ("yellow", [(244, 236, 87), (242, 232, 84), (240, 232, 86), (218, 194, 61)])
    ]


def generate_csv(args):
    csv_file = args.csv_out
    if (csv_file != ""):
        remove_file(csv_file)
        write_csv_headline(csv_file)
    return csv_file

if __name__ == "__main__":

    args = get_parser().parse_args()

    csv_file = generate_csv(args)

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

    tile_list = get_tile_list(target_dir, traffic_handler.getDataSource(), args.zoom, traffic_handler.getFileFormat())

    color_classes_definition = get_color_class_definition()
    tile_no = 0
    overall_start_time = time.time()
    for tile in tile_list:

        tile_no += 1
        print("{:4d}/{:4d}: {}".format(tile_no, len(tile_list), tile))

        tile_filename = os.path.join(target_dir, tile)
        start_time = time.time()
        color_classes = get_color_classes(tile_filename, color_classes_definition, threshold=ANALYSE_THRESHOLD)
        traffic_analysis = get_traffic_analysis(color_classes)
        end_time = time.time()

        (img_width, img_height) = Image.open(tile_filename).size
        assert traffic_analysis.get_overall_sum() == img_width * img_height, \
            "pixel sum {:d} does not equeal analysis pixel sum {:d}".format(
                img_width * img_height, traffic_analysis.get_overall_sum())

        executiontime = 1000*(end_time - start_time)
        write_analysis_result(csv_file, tile, traffic_analysis, executiontime)
