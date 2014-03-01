#!/bin/bash

set -e
set -o nounset
clean() {
  ps -ef | grep python | grep '^root' | \
    sed -s 's/  */ /g' | cut -f2 -d' ' | xargs kill -9 2> /dev/null
  mn -c
}
ctrlc() {
  clean
  exit
}
trap ctrlc SIGINT
rm -rf ./client
rm -rf ./serverlogs
./tfo-test/disable_tfo.sh
echo "TFO: `./tfo-test/status_tfo.sh`"
for delay in 10 50 100
do
  DISPLAY=:1 ./tfo.py --delaynet=$delay --name=Paper --tfo=0
done
killall -9 python

./tfo-test/enable_tfo.sh
echo "TFO: `./tfo-test/status_tfo.sh`"
for delay in 10 50 100
do
  DISPLAY=:1 ./tfo.py --delaynet=$delay --name=Paper --tfo=1
done
killall -9 python

mkdir -p output-figures
DISPLAY=:1 ./plot.py

exit 0
