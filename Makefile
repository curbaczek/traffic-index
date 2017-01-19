
build_folder := build
temp_folder := temp

python3 := python3
run_main := $(python3) traffic_index.py
run_get_area := $(python3) get_static_map_area_analysis.py
run_get_traffic := $(python3) get_static_traffic_analysis.py
run_get_all_traffic := $(python3) get_all_tiles_traffic_analysis.py
run_quick_tests := ./.quality-checks/pep8.sh
run_detailed_tests := ./.quality-checks/pep8-detailed.sh

quick_check:
	$(run_quick_tests)

check:
	$(run_detailed_tests)

clean:
	rm -Rf $(build_folder)
	rm -Rf $(temp_folder)
	find . -name "*.pyc" -exec rm {} \;
	find . -name "*~" -exec rm {} \;
	find . -name "__pycache__" -exec rmdir {} \;

karlsruhe:
	$(run_get_area) --lat 49.0068900 --lng 8.4036530 --zoom 17 --tiles 5 --skip "(-4,-4),(-3,-4),(-2,-4),(-1,-4),(4,4)" --show_grid_image

berlin:
	$(run_get_area) --lat 52.5171480 --lng 13.3936320 --zoom 14 --tiles 3 --csv "temp/berlin_area_analysis.csv" --show_grid_image

sf:
	$(run_get_area) --lat 37.7532400 --lng -122.4473590 --zoom 15 --tiles 3 --csv "temp/sf_area_analysis.csv" --show_grid_image

shanghai:
	$(run_get_area) --lat 31.2243220 --lng 121.4691240 --zoom 17 --tiles 3 --csv "temp/shanghai_area_analysis.csv" --show_grid_image

stuttgart:
	$(run_get_area) --lat 48.7775610 --lng 9.1785610 --zoom 14 --tiles 3 --csv "temp/stuttgart_area_analysis.csv" --show_grid_image

freiburg:
	$(run_get_area) --lat 47.9938040 --lng 7.8325110 --zoom 15 --tiles 3 --csv "temp/freiburg_area_analysis.csv" --show_grid_image


traffic-karlsruhe:
	$(run_get_traffic) --lat 49.0068900 --lng 8.4036530 --zoom 15 --tiles 2 --show_grid_image --check_latest_tile

traffic-berlin:
	$(run_get_traffic) --lat 52.517148 --lng 13.393632 --zoom 14 --tiles 1 --show_color_classes_image

alltraffic-berlin:
	$(run_get_all_traffic) --lat 52.517148 --lng 13.393632 --zoom 14 --csv "temp/analysis-result-berlin.csv"

traffic-paris:
	$(run_get_traffic) --lat 48.8566140 --lng 2.3522220 --zoom 14 --tiles 1 --threshold=20 --show_color_classes_image
