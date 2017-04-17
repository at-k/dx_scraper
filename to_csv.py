#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import json
import os.path
import datetime
import re
import BeautifulSoup

# init global param
in_file = ''
out_file = ''

# extract argument
argvs = sys.argv
argc = len(argvs)

if ( argc < 3 ):
    print 'Error : argument is inadequate\n'
    print 'Usage : python ' + argvs[0] + ' input_file output_file opt[dram|fm] -d\n'
    quit()

in_file = argvs[1]
out_file = argvs[2]
date_flag = False
act_mode = "FM"

if argc > 3 and argvs[3] == '-dram':
    act_mode = "DRAM"

if argc > 4 and argvs[4] == '-d':
    date_flag = True

# load html
try:
    f = open(in_file,'r')
    html = f.read()
    f.close()
except:
    print 'Error : file open was failed : ' + in_file + '\n'
    quit()

soup = BeautifulSoup.BeautifulSoup( html )

# arrange html
[tag.replaceWithChildren() for tag in soup.findAll('em')]
[tag.replaceWithChildren() for tag in soup.findAll('a')]
[tag.replaceWithChildren() for tag in soup.findAll('span')]
[tag.replaceWithChildren() for tag in soup.findAll('img')]
[tag.replaceWithChildren() for tag in soup.findAll('br')]

# extract header
try:
    if act_mode == 'FM':
        header_tag = soup.find(attrs =  {'id' : 'tb_Flash_Spot_Price_List'} )
    else:
        header_tag = soup.find(attrs =  {'id' : 'tb_Dram_Spot_Price_List'} )

    header_tag = header_tag.find('tr')
    header_tag = header_tag.findAll('th')

    header = []

    for h in header_tag:
        txt_tmp = h.contents[0]
        txt_tmp = txt_tmp.replace('\n','')
        txt_tmp = txt_tmp.replace(' ','')
        header = header + [txt_tmp]

    header = ['Date'] + header

    # extract data
    single = soup.findAll( attrs = {'class' : 'single-row'})
    double = soup.findAll( attrs = {'class' : 'double-row'})

    item_tag = single + double

    result_list = []
    date_str = ''

    if date_flag == True:
# YYYYMMDD.csv -> YYYYMMDD
        date_str = in_file.split("_")[1].split(".")[0]
#        date_str = '/'.join([date_str[:4], date_str[4:]])
#        date_str = '/'.join([date_str[:7], date_str[7:]])
    else:
        date_str = datetime.date.today().strftime(u'%Y%m%d')

    for i in item_tag:
        item_info = []
        td_list = i.findAll('td')

        for t in td_list:
#            txt_tmp = str(t.contents[1])
#            txt_tmp = txt_tmp.replace('\n','')
#            txt_tmp = txt_tmp.replace(' ','')
            item_info = item_info + [t.text]

        item_info = [date_str] + item_info
        result_list = result_list + [item_info]

except:
    print 'Error : tag analysis was failed\n'
    quit()

# header check
cur_header = []
if os.path.exists(out_file):
    try:
        readcsv = csv.reader(file(out_file,'r'))
        cur_header = next(readcsv)
    except:
        print 'Error : file open was failed :' + out_file + '\n'
        quit()

    if cur_header != []:
        index_num = len(cur_header)
        for i in range(index_num):
            if cur_header[i] != header[i]:
                print 'Error : header compatibility error ' + cur_header[i] + header[i] + '\n'
                quit()

else:
# write header
    try:
        writecsv = csv.writer(file(out_file, 'w'))
        writecsv.writerow(header)
    except:
        print 'Error : file open was failed :' + out_file + '\n'
        quit()

# write item
try:
    writecsv = csv.writer(file(out_file, 'a'))
    for item in result_list:
        writecsv.writerow(item)

except:
    print 'Error : file open was failed : ' + out_file + '\n'
    quit()
