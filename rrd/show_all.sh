#!/bin/bash

hosts=("twin13030.sandai.net" "twin13a055.sandai.net" "twin13a057.sandai.net" "twin13a058.sandai.net" "twin13a059.sandai.net")
for h in ${hosts[@]}
do
	echo "=======================================$h========================================"
	curl "http://${h}/stat"
done
