#!/bin/bash

path="/usr/local/mm/rrd"
$path/cal_lf.py > $path/result
cat $path/result
publish_num=`cat $path/result | awk '{print $1}' | sort | uniq -c | wc -l`
#echo $publish_num

tol_lf=`cat $path/result | awk '{print $2}' | awk 'BEGIN{sum=0}{sum+=$1}END{print sum}'`
#echo $tol_lf

if [ $publish_num -eq 0 ]
then
	per_publish_sec=0
else
	per_publish_sec=`echo "scale=3;$tol_lf/($publish_num*60)" | bc`
fi
echo $publish_num $tol_lf $per_publish_sec >> $path/cal_lf.result
echo "---------------------------"
