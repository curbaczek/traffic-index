
build_folder := build

run_main := python3 traffic_index.py
run_get_image := python3 get_static_map_image.py
run_quick_tests := ./.quality-checks/pep8.sh
run_detailed_tests := ./.quality-checks/pep8-detailed.sh

quick_check:
	$(run_quick_tests)

check:
	$(run_detailed_tests)

clean:
	rm -Rf $(build_folder)
	find . -name "*.pyc" -exec rm {} \;
	find . -name "*~" -exec rm {} \;
	find . -name "__pycache__" -exec rmdir {} \;

karlsruhe:
	mkdir -p $(build_folder)
	$(run_main) --city Karlsruhe --lat 49.0068900 --lng 8.4036530 --zoom 14 --debug --stdout

tile-download:
	$(run_get_image) --lat 49.0068900 --lng 8.4036530 --zoom 16 --tiles 2 --dest "temp"
