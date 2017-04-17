#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib as mpl
import dateutil.parser as parser
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv

# const parameter
in_file = 'fm_price.csv'
out_file = ''
#tgt_item = ['128Gb 16Gx8 MLC','16Gb 2Gx8 MLC','256Gb 32Gx8 MLC','32Gb 4Gx8 MLC','64Gb  8Gx8 MLC']
#tgt_item_slc = ['16Gb 2Gx8 SLC','1Gb 128Mx8 SLC','2Gb 256Mx8 SLC','32Gb 4Gx8 SLC','4Gb 512Mx8 SLC','8Gb 1Gx8 SLC']

tgt_src = ['mlc', 'slc']

for tgt in tgt_src:

    tgt_item = []
    tgt_file = tgt + '_tgt.txt'
    out_file = tgt + '.png'

    # load target
    for line in open(tgt_file, 'r'):
        txt = line.replace('\n', '')
        tgt_item += [txt]

    item_col = 2
    date_col = 0
    tgt_col_name ='SessionAverage'

    # initialize variables
    tgt_col_indx = -1
    data_set = {}

    # open file
    readcsv = csv.reader(file(in_file,'r'))
    header = next(readcsv)

    # search target col index
    for i in range(0,len(header)):
        if tgt_col_name == header[i]:
            tgt_col_index = i
            break

    # init data set
    # [key,[ [day],[val] ]
    for tgt in tgt_item:
        data_set.setdefault(tgt, [[],[]])

    if tgt_col_index == -1:
        print 'Target Column is not found\n'
        exit()

    # search data
    for row in readcsv:
        item_name = row[item_col]
        for tgt_i in tgt_item:
            if tgt_i == item_name:
                capacity = float(item_name.split(' ')[0].replace('Gb',''))/8
                data_set[item_name][0] += [row[date_col]]
                data_set[item_name][1] += [float(row[tgt_col_index])/capacity]

    # output figure
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    for data in data_set:
        xval = [parser.parse(xv) for xv in data_set[data][0]]
        yval = [float(yv) for yv in data_set[data][1]]
        ax.plot(xval, yval, marker='o', label=data)

    #ax.set_ylim(18,25)
    ax.set_xlabel("Day")
    ax.set_ylabel("Dollar/GB")
    ax.legend(loc = "upper right")
    ax.grid()

    days = mdates.AutoDateLocator()
    daysFmt = mdates.DateFormatter('%m/%d')
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)

    #fig.autofmt_xdate()

    plt.savefig( out_file )

    #mpl.use('PNG')
    #plt.savefig('output')
