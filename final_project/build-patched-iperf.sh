#!/bin/bash
PA2_DIR=`pwd`
IPERF_VER='iperf-2.0.5'


cd $HOME
wget http://downloads.sourceforge.net/project/iperf/iperf-2.0.5.tar.gz
tar -zxf ${IPERF_VER}.tar.gz
cd ${IPERF_VER}/src
patch -p1 < $PA2_DIR/${IPERF_VER}-wait-syn.patch
cd ..
./configure
make
cd $HOME
rm ${IPERF_VER}.tar.gz
mv ${IPERF_VER} iperf-patched
cd $PA2_DIR
