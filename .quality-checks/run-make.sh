#!/bin/bash

cmds=("make" "make test")

result=0
for cmd in "${cmds[@]}"; do
	echo "Executing $cmd"
	$cmd
	((result+=$?))
done
exit $result
