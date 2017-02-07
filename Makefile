
build_folder := build
temp_folder := temp

python3 := python3
#python3 := /opt/python3/bin/python3
run_main := $(python3) traffic_index.py
run_get_area := $(python3) get_static_map_area_analysis.py
run_get_traffic := $(python3) get_static_traffic_analysis.py
run_get_all_traffic := $(python3) get_all_tiles_traffic_analysis.py
run_quick_tests := ./.quality-checks/pep8.sh
run_detailed_tests := ./.quality-checks/pep8-detailed.sh

# --- skip lists ---------------------------------------------------------------
skip_list_rheinbrucke := '(-2,-2),(-1,-2),(0,-2),(1,-1),(-1,1),(-2,1),(1,-2),(2,-2),(0,-1),(2,-1),(-2,2),(0,1),(1,1),(2,1),(-1,2),(0,2),(1,2),(2,2)'

# --- zoom levels and tiles ----------------------------------------------------
zoom_rheinbrucke = 17
tiles_rheinbrucke = 3


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
	$(run_get_area) --lat 49.0068900 --lng 8.4036530 --zoom 17 --tiles 3

area-berlin:
	$(run_get_area) --lat 52.5171480 --lng 13.3936320 --zoom 14 --tiles 3 --csv "temp/berlin_area_analysis.csv" --show_grid_image

area-san-fransisco:
	$(run_get_area) --lat 37.7532400 --lng -122.4473590 --zoom 15 --tiles 3 --csv "temp/sf_area_analysis.csv" --show_grid_image

area-shanghai:
	$(run_get_area) --lat 31.2243220 --lng 121.4691240 --zoom 17 --tiles 3 --csv "temp/shanghai_area_analysis.csv" --show_grid_image

area-stuttgart:
	$(run_get_area) --lat 48.7775610 --lng 9.1785610 --zoom 14 --tiles 3 --csv "temp/stuttgart_area_analysis.csv" --show_grid_image

area-freiburg:
	$(run_get_area) --lat 47.9938040 --lng 7.8325110 --zoom 15 --tiles 3 --csv "temp/freiburg_area_analysis.csv" --show_grid_image

area-rheinbrucke:
	$(run_get_area) --lat 49.0369910 --lng 8.3030190 --zoom $(zoom_rheinbrucke) --tiles $(tiles_rheinbrucke) --skip $(skip_list_rheinbrucke) --show_grid_image

traffic-karlsruhe:
	$(run_get_traffic) --lat 49.0068900 --lng 8.4036530 --zoom 17 --tiles 3

traffic-berlin:
	$(run_get_traffic) --lat 52.5171480 --lng 13.3936320 --zoom 14 --tiles 3
	#$(run_get_traffic) --lat 52.5171480 --lng 13.3936320 --zoom 14 --tiles 3 --show_color_classes_image

traffic-san-fransisco:
	$(run_get_traffic) --lat 37.7532400 --lng -122.4473590 --zoom 15 --tiles 3

traffic-shanghai:
	$(run_get_traffic) --lat 31.2243220 --lng 121.4691240 --zoom 17 --tiles 3

traffic-stuttgart:
	$(run_get_traffic) --lat 48.7775610 --lng 9.1785610 --zoom 14 --tiles 3

traffic-freiburg:
	$(run_get_traffic) --lat 47.9938040 --lng 7.8325110 --zoom 15 --tiles 3

traffic-rheinbrucke:
	#$(run_get_traffic) --lat 49.0369910 --lng 8.3030190 --zoom 17 --tiles 3 --skip $(skip_list_rheinbrucke) --show_grid_image
	$(run_get_traffic) --lat 49.0369910 --lng 8.3030190 --zoom $(zoom_rheinbrucke) --tiles $(tiles_rheinbrucke) --skip $(skip_list_rheinbrucke)

analyse-traffic-karlsruhe:
	$(run_get_all_traffic) --lat 49.0068900 --lng 8.4036530 --zoom 15 --csv "temp/karlsruhe_zoom-15_traffic-analysis-result.csv"

analyse-traffic-berlin:
	$(run_get_all_traffic) --lat 52.517148 --lng 13.393632 --zoom 14 --csv "temp/berlin_traffic-analysis-result.csv"

# --- analysis Rheinbrucke -----------------------------------------------------
analysis_csv := "temp/morning_traffic_rheinbrucke.csv"
analysis_gif := "temp/morning_traffic_rheinbrucke.gif"
analysis_start := "2017-02-06 00:00:00"
analysis_end := "2017-02-07 00:00:00"
analysis_gif_start := "2017-02-06 05:00:00"
analysis_gif_end := "2017-02-06 10:00:00"
analyse-traffic-rheinbrucke:
	$(run_get_all_traffic) --lat 49.0369910 --lng 8.3030190 --zoom $(zoom_rheinbrucke) --skip $(skip_list_rheinbrucke) --analysis-time-start $(analysis_start) --analysis-time-end $(analysis_end) --csv $(analysis_csv) --gif $(analysis_gif) --gif-size 800 --gif-duration 0.5 --gif-time-start $(analysis_gif_start) --gif-time-end $(analysis_gif_end)
