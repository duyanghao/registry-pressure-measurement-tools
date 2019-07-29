#!/bin/bash

cat pull_results.csv | grep -v false|cut -d, -f3| grep -v spent_time|sort -n|awk 'BEGIN {max = 0} {if ($1+0 > max+0) max=$1} END {print "Max=", max}'
cat pull_results.csv | grep -v false|cut -d, -f3| grep -v spent_time|sort -n|awk 'BEGIN {min = 65536} {if ($1+0 < min+0) min=$1} END {print "Min=", min}'
cat pull_results.csv | grep -v false|cut -d, -f3| grep -v spent_time|sort -n|awk '{sum+=$1} END {print "Avg= ", sum/NR}'
cat pull_results.csv | grep -v false|cut -d, -f3| grep -v spent_time|sort -n|head -$1|awk '{sum+=$1} END {print "Avg= ", sum/NR}'
