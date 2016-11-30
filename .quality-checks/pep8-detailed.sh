#!/bin/bash
find . -name \*.py -exec pep8 --max-line-length 120 --show-source {} +
exit $?
