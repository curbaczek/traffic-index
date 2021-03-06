
build_folder := build
temp_folder := temp

python3 := python3

run_main := $(python3) traffic_index.py
run_get_area := $(python3) get_static_map_area_analysis.py
run_get_traffic := $(python3) get_static_traffic_analysis.py
run_get_all_traffic := $(python3) get_all_tiles_traffic_analysis.py
run_quick_tests := ./.quality-checks/pep8.sh
run_detailed_tests := ./.quality-checks/pep8-detailed.sh

# --- skip lists ---------------------------------------------------------------
skip_list_freiburg_15_3 := '(-1,2),(2,-2),(2,-1),(2,2)'
skip_list_stuttgart_14_3 := '(-1,2),(1,-2),(1,1),(1,2),(2,0),(2,2)'
skip_list_rheinbrucke_17_3 := '(-2,-2),(-1,-2),(0,-2),(1,-1),(-1,1),(-2,1),(1,-2),(2,-2),(0,-1),(2,-1),(-2,2),(0,1),(1,1),(2,1),(-1,2),(0,2),(1,2),(2,2)'
skip_list_karlsruhe_17_20 := '(-19,-19),(-19,-18),(-19,-17),(-19,-16),(-19,-15),(-19,-14),(-19,-13),(-19,-12),(-19,-11),(-19,-10),(-19,-9),(-19,-8),(-19,-7),(-19,-6),(-19,-5),(-19,-4),(-19,-3),(-19,-2),(-19,-1),(-19,0),(-19,1),(-19,2),(-19,3),(-19,4),(-19,5),(-19,6),(-19,7),(-19,8),(-19,9),(-19,10),(-19,11),(-19,12),(-19,13),(-19,14),(-19,15),(-19,16),(-19,17),(-19,18),(-19,19),(-18,-19),(-18,-18),(-18,-17),(-18,-16),(-18,-15),(-18,-14),(-18,-13),(-18,-12),(-18,-11),(-18,-10),(-18,-9),(-18,-8),(-18,-7),(-18,-6),(-18,-5),(-18,-4),(-18,-3),(-18,-2),(-18,-1),(-18,0),(-18,1),(-18,2),(-18,3),(-18,4),(-18,5),(-18,6),(-18,7),(-18,8),(-18,9),(-18,10),(-18,11),(-18,12),(-18,13),(-18,14),(-18,15),(-18,16),(-18,17),(-18,18),(-18,19),(-17,-19),(-17,-18),(-17,-17),(-17,-16),(-17,-15),(-17,-14),(-17,-13),(-17,-12),(-17,-11),(-17,-10),(-17,-9),(-17,-8),(-17,-7),(-17,-6),(-17,-5),(-17,-4),(-17,-3),(-17,-2),(-17,-1),(-17,0),(-17,1),(-17,2),(-17,3),(-17,4),(-17,5),(-17,6),(-17,7),(-17,8),(-17,9),(-17,10),(-17,11),(-17,12),(-17,13),(-17,14),(-17,15),(-17,16),(-17,17),(-17,18),(-17,19),(-16,-19),(-16,-18),(-16,-17),(-16,-16),(-16,-15),(-16,-14),(-16,-13),(-16,-12),(-16,-11),(-16,-10),(-16,-9),(-16,-8),(-16,-7),(-16,-6),(-16,-5),(-16,-4),(-16,-3),(-16,-2),(-16,-1),(-16,5),(-16,6),(-16,7),(-16,8),(-16,9),(-16,10),(-16,11),(-16,12),(-16,13),(-16,14),(-16,15),(-16,16),(-16,17),(-16,18),(-16,19),(-15,-19),(-15,-18),(-15,-17),(-15,-16),(-15,-15),(-15,-14),(-15,-13),(-15,-12),(-15,-11),(-15,-10),(-15,-9),(-15,-8),(-15,-7),(-15,-6),(-15,-5),(-15,4),(-15,5),(-15,6),(-15,7),(-15,8),(-15,9),(-15,10),(-15,11),(-15,12),(-15,13),(-15,14),(-15,15),(-15,16),(-15,17),(-15,18),(-15,19),(-14,-19),(-14,-18),(-14,-17),(-14,-16),(-14,-15),(-14,-14),(-14,-13),(-14,-12),(-14,-11),(-14,5),(-14,6),(-14,7),(-14,8),(-14,9),(-14,10),(-14,11),(-14,12),(-14,13),(-14,14),(-14,15),(-14,16),(-14,17),(-14,18),(-14,19),(-13,-19),(-13,-18),(-13,-17),(-13,-16),(-13,-15),(-13,-14),(-13,-13),(-13,-12),(-13,-11),(-13,5),(-13,6),(-13,7),(-13,8),(-13,9),(-13,10),(-13,11),(-13,12),(-13,13),(-13,14),(-13,15),(-13,16),(-13,17),(-13,18),(-13,19),(-12,-19),(-12,-18),(-12,-17),(-12,-16),(-12,-15),(-12,-14),(-12,4),(-12,5),(-12,6),(-12,7),(-12,8),(-12,9),(-12,10),(-12,11),(-12,12),(-12,13),(-12,14),(-12,15),(-12,16),(-12,17),(-12,18),(-12,19),(-11,-19),(-11,-18),(-11,-17),(-11,-16),(-11,4),(-11,5),(-11,6),(-11,7),(-11,8),(-11,9),(-11,10),(-11,11),(-11,12),(-11,13),(-11,14),(-11,15),(-11,16),(-11,17),(-11,18),(-11,19),(-10,-19),(-10,-18),(-10,-17),(-10,-16),(-10,4),(-10,5),(-10,6),(-10,7),(-10,8),(-10,9),(-10,10),(-10,11),(-10,12),(-10,13),(-10,14),(-10,15),(-10,16),(-10,17),(-10,18),(-10,19),(-9,-19),(-9,-18),(-9,-17),(-9,-16),(-9,-15),(-9,-14),(-9,5),(-9,6),(-9,7),(-9,8),(-9,9),(-9,10),(-9,11),(-9,12),(-9,13),(-9,14),(-9,15),(-9,16),(-9,17),(-9,18),(-9,19),(-8,-19),(-8,-18),(-8,-17),(-8,-16),(-8,-15),(-8,-14),(-8,6),(-8,7),(-8,8),(-8,9),(-8,10),(-8,11),(-8,12),(-8,13),(-8,14),(-8,15),(-8,16),(-8,17),(-8,18),(-8,19),(-7,-19),(-7,-18),(-7,-17),(-7,-16),(-7,-15),(-7,-14),(-7,7),(-7,8),(-7,9),(-7,10),(-7,11),(-7,12),(-7,13),(-7,14),(-7,15),(-7,16),(-7,17),(-7,18),(-7,19),(-6,-19),(-6,-18),(-6,-17),(-6,-16),(-6,-15),(-6,-14),(-6,7),(-6,8),(-6,9),(-6,10),(-6,11),(-6,12),(-6,13),(-6,14),(-6,15),(-6,16),(-6,17),(-6,18),(-6,19),(-5,-19),(-5,-18),(-5,-17),(-5,-16),(-5,-15),(-5,-14),(-5,8),(-5,9),(-5,10),(-5,11),(-5,12),(-5,13),(-5,14),(-5,15),(-5,16),(-5,17),(-5,18),(-5,19),(-4,-19),(-4,-18),(-4,-17),(-4,-16),(-4,-15),(-4,-14),(-4,8),(-4,9),(-4,10),(-4,11),(-4,12),(-4,13),(-4,14),(-4,15),(-4,16),(-4,17),(-4,18),(-4,19),(-3,-19),(-3,-18),(-3,-17),(-3,-16),(-3,-15),(-3,-14),(-3,8),(-3,9),(-3,10),(-3,11),(-3,12),(-3,13),(-3,14),(-3,15),(-3,16),(-3,17),(-3,18),(-3,19),(-2,-19),(-2,-18),(-2,-17),(-2,-16),(-2,-15),(-2,-14),(-2,10),(-2,11),(-2,12),(-2,13),(-2,14),(-2,15),(-2,16),(-2,17),(-2,18),(-2,19),(-1,-19),(-1,-18),(-1,-17),(-1,-16),(-1,-15),(-1,-14),(-1,11),(-1,12),(-1,13),(-1,14),(-1,15),(-1,16),(-1,17),(-1,18),(-1,19),(0,-19),(0,-18),(0,-17),(0,-16),(0,-15),(0,-14),(0,11),(0,12),(0,13),(0,14),(0,15),(0,16),(0,17),(0,18),(0,19),(1,-19),(1,-18),(1,-17),(1,-16),(1,-15),(1,-14),(1,11),(1,12),(1,13),(1,14),(1,15),(1,16),(1,17),(1,18),(1,19),(2,-19),(2,-18),(2,-17),(2,11),(2,12),(2,13),(2,14),(2,15),(2,16),(2,17),(2,18),(2,19),(3,11),(3,12),(3,13),(3,14),(3,15),(3,16),(3,17),(3,18),(3,19),(4,10),(4,11),(4,12),(4,13),(4,14),(4,15),(4,16),(4,17),(4,18),(4,19),(5,-19),(5,-18),(5,-17),(5,-16),(5,-15),(5,-14),(5,-13),(5,7),(5,8),(5,9),(5,10),(5,11),(5,12),(5,13),(5,14),(5,15),(5,16),(5,17),(5,18),(5,19),(6,-19),(6,-18),(6,-17),(6,-16),(6,-15),(6,-14),(6,-13),(6,-12),(6,-11),(6,9),(6,10),(6,11),(6,12),(6,13),(6,14),(6,15),(6,16),(6,17),(6,18),(6,19),(7,-19),(7,-18),(7,-17),(7,-16),(7,-15),(7,-14),(7,-13),(7,-12),(7,-11),(7,15),(7,16),(7,17),(7,18),(7,19),(8,-19),(8,-18),(8,-17),(8,-16),(8,-15),(8,-14),(8,-13),(8,-12),(8,-11),(8,-10),(8,-9),(8,15),(8,16),(8,17),(8,18),(8,19),(9,-19),(9,-18),(9,-17),(9,-16),(9,-15),(9,-14),(9,-13),(9,-12),(9,-11),(9,-10),(9,-9),(9,15),(9,16),(9,17),(9,18),(9,19),(10,-19),(10,-18),(10,-17),(10,-16),(10,-15),(10,-14),(10,-13),(10,-12),(10,-11),(10,-10),(10,-9),(10,15),(10,16),(10,17),(10,18),(10,19),(11,-19),(11,-18),(11,-17),(11,-16),(11,-15),(11,-14),(11,-13),(11,15),(11,16),(11,17),(11,18),(11,19),(12,-19),(12,-18),(12,-17),(12,-16),(12,-15),(12,-14),(12,-13),(12,-12),(12,-11),(12,16),(12,17),(12,18),(12,19),(13,-19),(13,-18),(13,-17),(13,-16),(13,-15),(13,-14),(13,-13),(13,-12),(13,-11),(13,16),(13,17),(13,18),(13,19),(14,-19),(14,-18),(14,-17),(14,-16),(14,-15),(14,-14),(14,-13),(14,-12),(14,-11),(14,-10),(14,-9),(14,15),(14,16),(14,17),(14,18),(14,19),(15,-19),(15,-18),(15,-17),(15,-16),(15,-15),(15,-14),(15,-13),(15,-12),(15,-11),(15,-10),(15,-9),(15,-8),(15,3),(15,4),(15,5),(15,6),(15,7),(15,15),(15,16),(15,17),(15,18),(15,19),(16,-19),(16,-18),(16,-17),(16,-16),(16,-15),(16,-14),(16,-13),(16,-12),(16,-11),(16,-10),(16,-9),(16,-8),(16,-7),(16,-6),(16,-5),(16,-4),(16,-3),(16,-2),(16,-1),(16,0),(16,1),(16,2),(16,3),(16,4),(16,5),(16,6),(16,7),(16,8),(16,9),(16,15),(16,16),(16,17),(16,18),(16,19),(17,-19),(17,-18),(17,-17),(17,-16),(17,-15),(17,-14),(17,-13),(17,-12),(17,-11),(17,-10),(17,-9),(17,-8),(17,-7),(17,-6),(17,-5),(17,-4),(17,-3),(17,-2),(17,-1),(17,0),(17,1),(17,2),(17,3),(17,4),(17,5),(17,6),(17,7),(17,8),(17,9),(17,13),(17,14),(17,15),(17,16),(17,17),(17,18),(17,19),(18,-19),(18,-18),(18,-17),(18,-16),(18,-15),(18,-14),(18,-13),(18,-12),(18,-11),(18,-10),(18,-9),(18,-8),(18,-7),(18,-6),(18,-5),(18,-4),(18,-3),(18,-2),(18,-1),(18,0),(18,1),(18,2),(18,3),(18,4),(18,5),(18,6),(18,7),(18,8),(18,9),(18,12),(18,13),(18,14),(18,15),(18,16),(18,17),(18,18),(18,19),(19,-19),(19,-18),(19,-17),(19,-16),(19,-15),(19,-14),(19,-13),(19,-12),(19,-11),(19,-10),(19,-9),(19,-8),(19,-7),(19,-6),(19,-5),(19,-4),(19,-3),(19,-2),(19,-1),(19,0),(19,1),(19,2),(19,3),(19,4),(19,5),(19,6),(19,7),(19,8),(19,9),(19,10),(19,11),(19,12),(19,13),(19,14),(19,15),(19,16),(19,17),(19,18),(19,19)'

# --- zoom levels and tiles ----------------------------------------------------
zoom_rheinbrucke = 17
tiles_rheinbrucke = 3
zoom_stuttgart = 14
tiles_stuttgart = 3

# --- organisation -------------------------------------------------------------

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
	find . -name "*.aux" -exec rm {} \;
	find . -name "*.out" -exec rm {} \;
	find . -name "*.toc" -exec rm {} \;

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
	$(run_get_traffic) --lat 52.517148 --lng 13.393632 --zoom 14 --tiles 1 --check_latest_tile --show_color_classes_image --show_grid_image

traffic-paris:
	$(run_get_traffic) --lat 52.5171480 --lng 13.3936320 --zoom 14 --tiles 3
	#$(run_get_traffic) --lat 52.5171480 --lng 13.3936320 --zoom 14 --tiles 3 --show_color_classes_image

traffic-san-fransisco:
	$(run_get_traffic) --lat 37.7532400 --lng -122.4473590 --zoom 15 --tiles 3 --check_latest_tile --show_grid_image --show_color_classes_image

traffic-shanghai:
	$(run_get_traffic) --lat 31.2243220 --lng 121.4691240 --zoom 17 --tiles 1 --threshold 1 --check_latest_tile --show_grid_image --show_color_classes_image

traffic-stuttgart:
	$(run_get_traffic) --lat 48.7775610 --lng 9.1785610 --zoom 14 --tiles 1 --check_latest_tile --show_grid_image --show_color_classes_image

traffic-freiburg:
	$(run_get_traffic) --lat 47.9938040 --lng 7.8325110 --zoom 15 --tiles 3

traffic-rheinbrucke:
	#$(run_get_traffic) --lat 49.0369910 --lng 8.3030190 --zoom 17 --tiles 3 --skip $(skip_list_rheinbrucke) --show_grid_image
	$(run_get_traffic) --lat 49.0369910 --lng 8.3030190 --zoom $(zoom_rheinbrucke) --tiles $(tiles_rheinbrucke) --skip $(skip_list_rheinbrucke)

analyse-traffic-karlsruhe:
		$(run_get_all_traffic)\
			--lat 49.0068900\
			--lng 8.4036530\
			--zoom 17\
			--csv "temp/monday_traffic_karlsruhe.csv"\
			--analysis-time-start "2017-01-30 00:00:00"\
			--analysis-time-end "2017-01-31 00:00:00"\
			--gif "temp/daily_traffic_karlsruhe.gif"\
			--gif-size 800\
			--gif-duration 0.5\
			--gif-time-start "2017-01-30 05:00:00"\
			--gif-time-end "2017-01-31 23:00:00"\

analyse-traffic-berlin:
	$(run_get_all_traffic)\
		--lat 52.517148\
		--lng 13.393632\
		--zoom 14\
		--csv "temp/monday_traffic_berlin.csv"\
		--analysis-time-start "2017-02-06 00:00:00"\
		--analysis-time-end "2017-02-07 00:00:00"\
		--gif "temp/morning_traffic_berlin.gif"\
		--gif-size 800\
		--gif-duration 0.5\
		--gif-time-start "2017-02-06 05:00:00"\
		--gif-time-end "2017-02-06 12:00:00"\

analyse-traffic-stuttgart:
	$(run_get_all_traffic)
		--lat 48.7775610\
		--lng 9.1785610\
		--zoom $(zoom_stuttgart)\
		--skip $(skip_list_stuttgart_14_3)\
		--analysis-time-start "2017-02-06 00:00:00"\
		--analysis-time-end "2017-02-07 00:00:00"\
		--csv "temp/monday_traffic_stuttgart.csv"\
		--gif "temp/morning_traffic_stuttgart.gif"\
		--gif-size 800\
		--gif-duration 0.5\
		--gif-time-start "2017-02-06 05:00:00"\
		--gif-time-end "2017-02-06 12:00:00"

analyse-traffic-rheinbrucke:
	$(run_get_all_traffic)
		--lat 49.0369910\
		--lng 8.3030190\
		--zoom $(zoom_rheinbrucke)\
		--skip $(skip_list_rheinbrucke_17_3)\
		--analysis-time-start "2017-02-06 00:00:00"\
		--analysis-time-end "2017-02-07 00:00:00"\
		--csv "temp/morning_traffic_rheinbrucke.csv"\
		--gif "temp/morning_traffic_rheinbrucke.gif"\
		--gif-size 800\
		--gif-duration 0.5\
		--gif-time-start "2017-02-06 05:00:00"\
		--gif-time-end "2017-02-06 10:00:00"
