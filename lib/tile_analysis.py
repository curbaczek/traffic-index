from abc import ABC, abstractmethod
import time
from datetime import datetime

from lib.model import ConsolePrinter
from lib.csv_handler import write_csv_data
from lib.util.image_analysis import get_color_classes
from lib.util.file import remove_file

DEFAULT_AREA_TILE_COLOR_THRESHOLD = 130
DEFAULT_TRAFFIC_TILE_COLOR_THRESHOLD = 30


class AreaAnalysisResult(ABC):

    def __init__(self, roadmap, highway, manmade, nature, transit, unassigned):
        self.roadmap = roadmap
        self.highway = highway
        self.manmade = manmade
        self.nature = nature
        self.transit = transit
        self.unassigned = unassigned

    def get_overall_sum(self):
        return self.get_assigned_sum() + self.unassigned

    def get_assigned_sum(self):
        return self.roadmap + self.highway + self.manmade + self.nature + self.transit


class TrafficAnalysisResult(ABC):

    def __init__(self, heavy, moderate, light, notraffic, noinformation, unassigned):
        self.heavy = heavy
        self.moderate = moderate
        self.light = light
        self.notraffic = notraffic
        self.noinformation = noinformation
        self.unassigned = unassigned

    def get_overall_sum(self):
        return self.get_assigned_sum() + self.unassigned

    def get_assigned_sum(self):
        return self.get_traffic_sum() + self.noinformation

    def get_traffic_sum(self):
        return self.heavy + self.moderate + self.light + self.notraffic


class TileMapAnalysis(ABC):

    tile_map = None
    tile_analysis_list = []
    printer = ConsolePrinter()
    csvfile = None
    result = None
    color_threshold = 0

    def __init__(self, tile_map, color_threshold, csv_file="", debug_mode=False):
        self.printer.setDebugMode(debug_mode)
        self.color_threshold = color_threshold
        self.tile_map = tile_map
        self.init_csv_file(csv_file)
        self.analyze()

    @abstractmethod
    def get_tile_analysis(self, tile):
        pass

    def analyze(self):
        self.tile_analysis_list = []
        for tile in self.tile_map.getActiveTiles():
            tile_analysis = self.get_tile_analysis(tile)
            self.printer.printDebugMsg(tile_analysis)
            self.write_csv_analysis(tile, tile_analysis)
            self.tile_analysis_list.append(tile_analysis)

    def init_csv_file(self, filename):
        if (filename != ""):
            self.csvfile = filename
            remove_file(self.csvfile)
            self.write_csv_headline()
        else:
            self.csvfile = None

    @abstractmethod
    def write_csv_headline(self):
        pass

    @abstractmethod
    def write_csv_analysis(self, tile, tile_analysis):
        pass

    @abstractmethod
    def get_result(self):
        pass

    def generate_grid_image(self):
        pass

    def get_duration(self):
        return sum([tile_analysis.duration for tile_analysis in self.tile_analysis_list])


class AreaTileMapAnalysis(TileMapAnalysis):

    def get_tile_analysis(self, tile):
        return AreaTileAnalysis(tile, self.color_threshold)

    def write_csv_headline(self):
        write_csv_data(self.csvfile, [
            'x', 'y', 'roadmap_portion', 'highway_portion', 'manmade_portion',
            'nature_portion', 'transit_portion', 'unassigned_portion', 'roadmap_absolute',
            'highway_absolute', 'manmade_absolute', 'nature_absolute', 'transit_absolute',
            'unassigned_absolute', 'duration [ms]'])

    def write_csv_analysis(self, tile, tile_analysis):
        write_csv_data(self.csvfile, [
            tile.x, tile.y,
            tile_analysis.result.roadmap/tile_analysis.result.get_overall_sum()*100,
            tile_analysis.result.highway/tile_analysis.result.get_overall_sum()*100,
            tile_analysis.result.manmade/tile_analysis.result.get_overall_sum()*100,
            tile_analysis.result.nature/tile_analysis.result.get_overall_sum()*100,
            tile_analysis.result.transit/tile_analysis.result.get_overall_sum()*100,
            tile_analysis.result.unassigned/tile_analysis.result.get_overall_sum()*100,
            tile_analysis.result.roadmap,
            tile_analysis.result.highway,
            tile_analysis.result.manmade,
            tile_analysis.result.nature,
            tile_analysis.result.transit,
            tile_analysis.result.unassigned,
            tile_analysis.duration])

    def get_result(self):
        roadmap, highway, manmade, nature, transit, unassigned = 0, 0, 0, 0, 0, 0
        for tile_analysis in self.tile_analysis_list:
            roadmap += tile_analysis.result.roadmap
            manmade += tile_analysis.result.manmade
            highway += tile_analysis.result.highway
            nature += tile_analysis.result.nature
            transit += tile_analysis.result.transit
            unassigned += tile_analysis.result.unassigned
        return AreaAnalysisResult(
            roadmap, highway, manmade, nature, transit, unassigned)

    def __str__(self):
        analysis_result = self.get_result()
        overall_sum = analysis_result.get_overall_sum()
        return (
            "area tilemap analysis, executed in {:4f}ms:\n"
            "-- roadmap: {:.4f}% ({:d}px)\n" +
            "-- highway: {:.4f}% ({:d}px)\n" +
            "-- man-made: {:.4f}% ({:d}px)\n" +
            "-- nature: {:.4f}% ({:d}px)\n" +
            "-- transit: {:.4f}% ({:d}px)\n" +
            "-- unassigned: {:.4f}% ({:d}px)").format(
            self.get_duration(),
            0 if overall_sum == 0 else analysis_result.roadmap/overall_sum*100, analysis_result.roadmap,
            0 if overall_sum == 0 else analysis_result.highway/overall_sum*100, analysis_result.highway,
            0 if overall_sum == 0 else analysis_result.manmade/overall_sum*100, analysis_result.manmade,
            0 if overall_sum == 0 else analysis_result.nature/overall_sum*100, analysis_result.nature,
            0 if overall_sum == 0 else analysis_result.transit/overall_sum*100, analysis_result.transit,
            0 if overall_sum == 0 else analysis_result.unassigned/overall_sum*100, analysis_result.unassigned)


class TrafficTileMapAnalysis(TileMapAnalysis):

    def get_tile_analysis(self, tile):
        return TrafficTileAnalysis(tile, self.color_threshold)

    def write_csv_headline(self):
        write_csv_data(self.csvfile, [
            'x', 'y', 'time', 'traffic_portion_heavy [%]', 'traffi_portion_moderate [%]', 'traffic_portion_light [%]',
            'traffic_portion_notraffic [%]', 'heavy [px]', 'moderate [px]', 'light [px]', 'notraffic [px]',
            'noinformation [px]', 'unassigned [px]', 'calculation time [ms]', 'tile filename'])

    def write_csv_analysis(self, tile, tile_analysis):
        traffic_sum = tile_analysis.result.get_traffic_sum()
        write_csv_data(self.csvfile, [
            tile.x, tile.y,
            datetime.fromtimestamp(tile.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            0.0 if traffic_sum == 0 else 100*tile_analysis.result.heavy/traffic_sum,
            0.0 if traffic_sum == 0 else 100*tile_analysis.result.moderate/traffic_sum,
            0.0 if traffic_sum == 0 else 100*tile_analysis.result.light/traffic_sum,
            0.0 if traffic_sum == 0 else 100*tile_analysis.result.notraffic/traffic_sum,
            tile_analysis.result.heavy,
            tile_analysis.result.moderate,
            tile_analysis.result.light,
            tile_analysis.result.notraffic,
            tile_analysis.result.noinformation,
            tile_analysis.result.unassigned,
            tile_analysis.duration,
            tile.path])

    def get_result(self):
        roadmap, highway, manmade, nature, transit, unassigned = 0, 0, 0, 0, 0, 0
        for tile_analysis in self.tile_analysis_list:
            roadmap += tile_analysis.result.roadmap
            manmade += tile_analysis.result.manmade
            highway += tile_analysis.result.highway
            nature += tile_analysis.result.nature
            transit += tile_analysis.result.transit
            unassigned += tile_analysis.result.unassigned
        return AreaAnalysisResult(
            roadmap, highway, manmade, nature, transit, unassigned)

    def __str__(self):
        analysis_result = self.get_result()
        overall_sum = analysis_result.get_overall_sum()
        return (
            "area tilemap analysis, executed in {:4f}ms:\n"
            "-- roadmap: {:.4f}% ({:d}px)\n" +
            "-- highway: {:.4f}% ({:d}px)\n" +
            "-- man-made: {:.4f}% ({:d}px)\n" +
            "-- nature: {:.4f}% ({:d}px)\n" +
            "-- transit: {:.4f}% ({:d}px)\n" +
            "-- unassigned: {:.4f}% ({:d}px)").format(
            self.get_duration(),
            0 if overall_sum == 0 else analysis_result.roadmap/overall_sum*100, analysis_result.roadmap,
            0 if overall_sum == 0 else analysis_result.highway/overall_sum*100, analysis_result.highway,
            0 if overall_sum == 0 else analysis_result.manmade/overall_sum*100, analysis_result.manmade,
            0 if overall_sum == 0 else analysis_result.nature/overall_sum*100, analysis_result.nature,
            0 if overall_sum == 0 else analysis_result.transit/overall_sum*100, analysis_result.transit,
            0 if overall_sum == 0 else analysis_result.unassigned/overall_sum*100, analysis_result.unassigned)


class TileAnalysis(ABC):

    tile = None
    result = None
    duration = 0
    color_threshold = 0
    color_definitions = []

    def __init__(self, tile, color_threshold):
        self.tile = tile
        self.color_threshold = color_threshold
        self.analyze()

    @abstractmethod
    def save_analysis_result(self, color_result):
        pass

    def analyze(self):
        start_time = time.time()
        color_result = get_color_classes(self.tile.path, self.color_definitions, self.color_threshold)
        self.duration = 1000*(time.time() - start_time)
        self.save_analysis_result(color_result)

    @abstractmethod
    def __str__(self):
        pass


class AreaTileAnalysis(TileAnalysis):

    color_definitions = [
        ("red", [(255, 0, 0)]),
        ("green", [(0, 255, 0)]),
        ("blue", [(0, 0, 255)]),
        ("white", [(255, 255, 255)]),
        ("black", [(0, 0, 0)])
    ]

    def save_analysis_result(self, color_result):
        self.color_result = color_result
        self.result = AreaAnalysisResult(
            color_result["red"]["count"],
            color_result["green"]["count"],
            color_result["blue"]["count"],
            color_result["white"]["count"],
            color_result["black"]["count"],
            color_result["unknown"]["count"])

    def __str__(self):
        assert self.tile is not None and self.result is not None
        overall_sum = self.result.get_overall_sum()
        return (
            "area analysis of tile {:d}x{:d}, executed in {:4f}ms:\n"
            "-- roadmap: {:.4f}%\n" +
            "-- highway: {:.4f}%\n" +
            "-- man-made: {:.4f}%\n" +
            "-- nature: {:.4f}%\n" +
            "-- transit: {:.4f}%\n" +
            "-- unassigned: {:.4f}%").format(
            self.tile.x, self.tile.y, self.duration,
            0 if overall_sum == 0 else self.result.roadmap/overall_sum*100,
            0 if overall_sum == 0 else self.result.highway/overall_sum*100,
            0 if overall_sum == 0 else self.result.manmade/overall_sum*100,
            0 if overall_sum == 0 else self.result.nature/overall_sum*100,
            0 if overall_sum == 0 else self.result.transit/overall_sum*100,
            0 if overall_sum == 0 else self.result.unassigned/overall_sum*100)


class TrafficTileAnalysis(TileAnalysis):

    color_definitions = [
        ("green", [(122, 187, 68), (117, 183, 66), (97, 166, 69)]),
        ("red", [(210, 57, 64), (205, 63, 68), (206, 75, 76), (208, 59, 65)]),
        ("orange", [(251, 195, 75), (252, 186, 74), (240, 167, 61)]),
        ("yellow", [(244, 236, 87), (242, 232, 84), (240, 232, 86), (218, 194, 61)])
    ]

    def save_analysis_result(self, color_result):
        self.color_result = color_result
        self.result = TrafficAnalysisResult(
            color_result["red"]["count"],
            color_result["orange"]["count"],
            color_result["yellow"]["count"],
            color_result["green"]["count"],
            color_result["unknown"]["count"],
            unassigned=0)

    def __str__(self):
        assert self.tile is not None and self.result is not None
        overall_sum = self.result.get_overall_sum()
        return (
            "traffic analysis of tile {:d}x{:d}, executed in {:4f}ms:\n"
            "-- heavy: {:.4f}%\n" +
            "-- moderate: {:.4f}%\n" +
            "-- light: {:.4f}%\n" +
            "-- no-traffic: {:.4f}%\n" +
            "-- no-information: {:.4f}%\n" +
            "-- unassigned: {:.4f}%").format(
            self.tile.x, self.tile.y, self.duration,
            0 if overall_sum == 0 else self.result.heavy/overall_sum*100,
            0 if overall_sum == 0 else self.result.moderate/overall_sum*100,
            0 if overall_sum == 0 else self.result.light/overall_sum*100,
            0 if overall_sum == 0 else self.result.notraffic/overall_sum*100,
            0 if overall_sum == 0 else self.result.noinformation/overall_sum*100,
            0 if overall_sum == 0 else self.result.unassigned/overall_sum*100)
