from __future__ import division

import os
import yaml

from lib import model

from lib.util.file import clear_dir
from lib.util.file import copy_dir

from lib.data_handler import load_location

DEFAULT_BUILD_DIRECTORY = 'build'
LOCATION_DATA_DIRECTORY = 'data/locations'
RES_DIRECTORY = 'res'


def print_result_to_stdout(result):
    # TODO implement
    print("*** Analysis Result ***")
    print(result)


def generate_html(result, build_directory):
    # TODO implement
    print("[ERROR] html output not yet implemented")
    # html_generator.generate_html(build_directory, RES_DIRECTORY, result)


def analyse_city(name, lat, lng, zoom_level):
    location_data_dir = os.path.join(RES_DIRECTORY, LOCATION_DATA_DIRECTORY)
    location = load_location(location_data_dir, name, lat, lng)
    # TODO run area analysis
    # TODO run traffic analysis
    return location


def get_parser():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--debug',
                        action='store_true',
                        help='show debug information')
    parser.add_argument('--stdout',
                        action='store_true',
                        help="print to stdout")
    parser.add_argument('--target-folder',
                        type=str,
                        dest='target_folder',
                        default=DEFAULT_BUILD_DIRECTORY,
                        help="target folder for generated files")
    parser.add_argument('--city',
                        type=str,
                        help="name of the city to be analyzed",
                        required=True)
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
    parser.add_argument('--cache',
                        type=str,
                        dest='cache_file')
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()

    if args.cache_file and os.path.isfile(args.cache_file):
        location_result = yaml.load(open(args.cache_file, 'r'))
    else:
        location_result = analyse_city(args.city, args.lat, args.lng, args.zoom)
        if args.cache_file:
            yaml.dump(location_result, open(args.cache_file, 'w'))

    if args.stdout:
        print_result_to_stdout(location_result)
    else:
        generate_html(location_result, args.target_folder)
