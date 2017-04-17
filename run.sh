#!/bin/sh

get_script=dxchg_get_price.py
csv_script=tocsv_v2.py
error_file=error.log

today=`date +%Y%m%d`

fm_file=fm_$today.html
dram_file=dram_$today.html

if [ ! -d data ] ; then
    mkdir data
fi

# get price
python $get_script

if [ ! -f data/$fm_file ] ; then
    echo "$today -- Error: fail to get fm price" > $error_file
    exit
fi

if [ ! -f data/$dram_file ] ; then
    echo "$today -- Error: fail to get dram price" > $error_file
    exit
fi

# convert to csv
python $csv_script data/$fm_file fm_price.csv -fm
python $csv_script data/$dram_file dram_price.csv -dram

# extract target
cut -d, -f3 fm_price.csv| sort | uniq | grep MLC > mlc_tgt.txt
cut -d, -f3 fm_price.csv| sort | uniq | grep SLC > slc_tgt.txt

# output graph
python matplot.py

cp *.png /var/www/data/
