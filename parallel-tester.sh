#!/usr/bin/env bash

# Use for optimizing just the cost
fulldomainpath=$(realpath "robustColoring-constant_K.lp")

# Use for optimizing the number of colors and the cost
# fulldomainpath=$(realpath "robustColoring.lp")
fullclingopath="/usr/bin/clingo"

for i in instances/*
do
	instancename=$(basename -- "$i")
	instancename="${instancename%.*}"
	fullinstancepath=$(realpath "$i")

	if test -f "$i"
	then
		echo "Now testing for $instancename!"
		start=$(date +%s.%N)
		$fullclingopath $fullinstancepath $fulldomainpath "--quiet=2,0,2" "--time-limit=3600" "--parallel-mode=20" > "results/result-$instancename.txt"
		end=$(date +%s.%N)
		time_elapsed=$(echo "$end - $start" | bc)
		echo "elapsed time for $instancename was $time_elapsed seconds"
		echo "elapsed time for $instancename was $time_elapsed seconds" >> "results/result-$instancename.txt"
	fi
done
