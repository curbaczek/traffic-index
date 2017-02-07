"""
analyses all given traffic tilemaps of a given location and writes the analysis
result to a csv file
"""

import os
import imageio
import time
import tempfile
from time import strftime
from datetime import datetime
from lib import model

from lib.tile_analysis import TrafficTileMapAnalysis, DEFAULT_TRAFFIC_TILE_COLOR_THRESHOLD
from lib.data_handler import get_tilemap_list, SUBDIR_TRAFFIC
from lib.bing_tile_handler import BingTileHandler
from lib.util.file import get_target_directory, remove_dir

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
                        default=None,
                        dest='csv_out',
                        required=True)
    parser.add_argument('--gif',
                        type=str,
                        help="file to save the gif animation of the analysed tiles",
                        default=None,
                        dest='gif_out',
                        required=False)
    parser.add_argument('--gif-size',
                        type=int,
                        help="maximum image size of the resulting gif file",
                        default=0,
                        dest='gif_out_size',
                        required=False)
    parser.add_argument('--gif-duration',
                        type=float,
                        help="duration of each image in the resulting gif file",
                        default=0.5,
                        dest='gif_out_duration',
                        required=False)
    parser.add_argument('--gif-time-start',
                        type=str,
                        help="start time (YYYY-MM-DD HH:MM:SS) of the tilemaps shown in the gif file",
                        default=None,
                        dest='gif_out_time_start',
                        required=False)
    parser.add_argument('--gif-time-end',
                        type=str,
                        help="end time (YYYY-MM-DD HH:MM:SS) of the tilemaps shown in the gif file",
                        default=None,
                        dest='gif_out_time_end',
                        required=False)

    return parser


def get_timestamp(time_str):
    result = None
    if time_str is not None:
        ttuple = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").timetuple()
        result = time.mktime(ttuple)
    return result


def generate_gif(args, all_traffic_tilemaps):
    temp_gif_dir = tempfile.mkdtemp(prefix='gifgen_')

    filter_from_timestamp = get_timestamp(args.gif_out_time_start)
    filter_to_timestamp = get_timestamp(args.gif_out_time_end)

    print("--- save grid images of all tile maps that match time window ({}-{})".format(
        "..." if args.gif_out_time_start is None else args.gif_out_time_start,
        "..." if args.gif_out_time_end is None else args.gif_out_time_end))
    tile_map_id = 0
    prefix_length = len(str(len(all_traffic_tilemaps)))
    tile_map_size = (args.gif_out_size, args.gif_out_size)
    for tile_map in all_traffic_tilemaps:
        tile_map_id += 1
        if (filter_from_timestamp is not None and tile_map.timestamp < filter_from_timestamp) or\
           (filter_to_timestamp is not None and tile_map.timestamp > filter_to_timestamp):
            continue
        print("--- save tilemap {:3d}/{:3d}".format(tile_map_id, len(all_traffic_tilemaps)))
        tf_prefix = str(tile_map_id).zfill(prefix_length) + "_"
        tf = tempfile.NamedTemporaryFile(prefix=tf_prefix, suffix=".png", delete=False, dir=temp_gif_dir)
        tile_map.saveTileMapImage(tf.name, target_dir, show_grid_date=True, final_size=tile_map_size)

    file_names = sorted((os.path.join(temp_gif_dir, fn) for fn in os.listdir(temp_gif_dir) if fn.endswith('.png')))
    print("--- add all {} images to gif".format(len(file_names)))
    kargs = {'duration': args.gif_out_duration}
    with imageio.get_writer(args.gif_out, format="GIF", mode='I', **kargs) as writer:
        for file_name in file_names:
            image = imageio.imread(file_name)
            writer.append_data(image)
    print("--- gif file {} generated".format(args.gif_out))

    remove_dir(temp_gif_dir)


if __name__ == "__main__":

    args = get_parser().parse_args()

    target_dir = get_target_directory(args.lat, args.lng, SUBDIR_TRAFFIC)
    os.makedirs(target_dir, exist_ok=True)
    print("target directory '{}'".format(target_dir))

    assert args.threshold > 0, "threshold must be positive"
    traffic_handler = BingTileHandler()
    traffic_handler.printer.setDebugMode(DEBUG_MODE)
    search_data_src = traffic_handler.getDataSource()
    search_file_format = traffic_handler.getFileFormat()
    all_traffic_tilemaps = get_tilemap_list(target_dir, search_data_src, args.zoom, search_file_format)
    print("found {} traffic tile maps in target directory".format(len(all_traffic_tilemaps)))

    tile_map_id = 0
    for tile_map in all_traffic_tilemaps:
        tile_map_id += 1
        print("analyse tilemap {:3d}/{:3d}".format(tile_map_id, len(all_traffic_tilemaps)))
        analysis = TrafficTileMapAnalysis(
            tile_map, args.threshold, args.csv_out, DEBUG_MODE, init_csv=(tile_map_id == 1))

    print("tiles analyzed, result written to {}".format(args.csv_out))

    if args.gif_out is not None:
        print("generate gif image")
        generate_gif(args, all_traffic_tilemaps)
