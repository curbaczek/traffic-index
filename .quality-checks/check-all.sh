#!/bin/bash

checks=(pep8.sh run-make.sh)

result=0
for check in ${checks[@]}; do
	./.quality-checks/$check
	((result+=$?))
done
exit $result
