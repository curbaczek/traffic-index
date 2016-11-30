#!/bin/bash
echo "Python code style check (standard: pep8 `pep8 --version`, max line length 120)"
result=0
for f in `find . -name \*.py`; do
	error_count=$(pep8 --max-line-length 120 $f | wc -l)
	if [[ $error_count -eq 0 ]]; then
		echo -e "|- \e[32m$f\e[39m"
	else
		result=$(($result + $error_count))
		echo -e "|- \e[31m$f [$error_count]\e[39m"
	fi
done;
if [[ ! $result -eq 0 ]]; then
	echo "|= Detected $result errors. Run 'make check' for detailed error information."
fi
exit $result
