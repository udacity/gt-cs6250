#!/bin/bash

# Creates a graph of the bandwidth from a bandwidth log

# Usage: ./plot-rate.sh ./student_folder/bwm.txt
# To use this script pass the path of the bandwidth log as the first argument.

python util/plot_rate.py --rx \
        --maxy 10 \
        --xlabel 'Time (s)' \
        --ylabel 'Rate (Mbps)' \
        -i 's.*-eth2' \
        -f $1 \
        -o ./rate.png
