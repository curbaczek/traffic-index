
build_folder := build

run_main := python main.py
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
