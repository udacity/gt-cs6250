#!/bin/bash

qlen=$1
rate=1.5Mbit
rate2=1.5Mbit

function add_qdisc {
    dev=$1
    tc qdisc del dev $dev root
    echo qdisc removed

    tc qdisc add dev $dev root handle 1:0 htb default 1
    echo qdisc added

    tc class add dev $dev parent 1:0 classid 1:1 htb rate $rate
    #tc class add dev $dev classid 1:10 parent 1:1 htb rate $rate2 ceil $rate
    echo classes created

    tc qdisc add dev $dev parent 1:1 handle 10: netem delay 10ms limit $qlen

    echo delay added
}

add_qdisc s0-eth1
add_qdisc s0-eth2
