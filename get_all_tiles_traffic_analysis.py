"""
analyzes all given traffic tiles of a given location and writes the analysis
result to a csv file
"""

import os
import time
from time import strftime
from datetime import datetime

from lib.tile_analysis import TrafficTileAnalysis, DEFAULT_TRAFFIC_TILE_COLOR_THRESHOLD
from lib.data_handler import get_tile, get_tile_list, SUBDIR_TRAFFIC
from lib.bing_tile_handler import BingTileHandler
from lib.csv_handler import write_csv_data
from lib.util.file import remove_file, open_file_from_shell, get_target_directory

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
    parser.add_argument('--threshold',
                        type=int,
                        default=DEFAULT_TRAFFIC_TILE_COLOR_THRESHOLD,
                        help="threshold of the image analysis")
    parser.add_argument('--csv',
                        type=str,
                        help="file to save the analysis results as csv",
                        default="",
                        dest='csv_out',
                        required=True)

    return parser


def write_csv_headline(filename):
    write_csv_data(filename, [
        'x', 'y', 'time', 'traffic_portion_heavy [%]', 'traffi_portion_moderate [%]', 'traffic_portion_light [%]',
        'traffic_portion_notraffic [%]', 'heavy [px]', 'moderate [px]', 'light [px]', 'notraffic [px]',
        'noinformation [px]', 'unassigned [px]', 'calculation time [ms]', 'tile filename'])


def write_analysis_result(filename, tile_filename, analysis_result, duration):
    tile = get_tile(tile_filename)
    traffic_sum = analysis_result.result.get_traffic_sum()
    write_csv_data(filename, [
        tile.x, tile.y,
        datetime.fromtimestamp(tile.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
        0.0 if traffic_sum == 0 else 100*analysis_result.result.heavy/traffic_sum,
        0.0 if traffic_sum == 0 else 100*analysis_result.result.moderate/traffic_sum,
        0.0 if traffic_sum == 0 else 100*analysis_result.result.light/traffic_sum,
        0.0 if traffic_sum == 0 else 100*analysis_result.result.notraffic/traffic_sum,
        analysis_result.result.heavy,
        analysis_result.result.moderate,
        analysis_result.result.light,
        analysis_result.result.notraffic,
        analysis_result.result.noinformation,
        analysis_result.result.unassigned,
        duration,
        tile_filename])


def generate_csv(args):
    csv_file = args.csv_out
    if (csv_file != ""):
        remove_file(csv_file)
        write_csv_headline(csv_file)
    return csv_file


if __name__ == "__main__":

    args = get_parser().parse_args()
    csv_file = generate_csv(args)

    target_dir = get_target_directory(args.lat, args.lng, SUBDIR_TRAFFIC)
    os.makedirs(target_dir, exist_ok=True)
    print("target directory '{}'".format(target_dir))

    assert args.threshold > 0, "threshold must be positive"
    traffic_handler = BingTileHandler()
    traffic_handler.printer.setDebugMode(DEBUG_MODE)

    search_data_src = traffic_handler.getDataSource()
    search_file_format = traffic_handler.getFileFormat()
    all_traffic_tile_list = get_tile_list(target_dir, search_data_src, args.zoom, search_file_format)
    print("loaded traffic tile list: {}".format(all_traffic_tile_list))

    tile_no = 0
    overall_start_time = time.time()
    for tile_name in all_traffic_tile_list:
        tile_no += 1
        print("{:4d}/{:4d}: {}".format(tile_no, len(all_traffic_tile_list), tile_name))
        tile = get_tile(os.path.join(target_dir, tile_name))
        tile_analysis = TrafficTileAnalysis(tile, args.threshold)
        write_analysis_result(csv_file, tile_name, tile_analysis, tile_analysis.duration)

    print("tiles analyzed, result written to {}".format(csv_file))
