
build_folder := build
temp_folder := temp

run_main := python3 traffic_index.py
run_get_area := python3 get_static_map_area_analysis.py
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
	$(run_get_area) --lat 49.0068900 --lng 8.4036530 --zoom 17 --tiles 3

traffic-analysis:
	$(run_get_traffic) --lat 49.0068900 --lng 8.4036530 --zoom 14 --dest "temp"
