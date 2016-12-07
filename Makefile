
build_folder := build
temp_folder := temp

run_main := python3 traffic_index.py
run_get_image := python3 get_static_map_image.py
run_get_traffic := python3 get_static_traffic_analysis.py
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
	mkdir -p $(build_folder)
	$(run_main) --city Karlsruhe --lat 49.0068900 --lng 8.4036530 --zoom 14 --debug --stdout

tile-download:
	$(run_get_image) --lat 49.0068900 --lng 8.4036530 --zoom 14 --tiles 2 --dest "temp"

tile-download-hamburg:
	$(run_get_image) --lat 53.5510850 --lng 9.9936820 --zoom 18 --tiles 2 --dest "temp"

traffic-download:
	$(run_get_traffic) --lat 49.0068900 --lng 8.4036530 --zoom 14 --tiles 2 --dest "temp"

