#!/usr/bin/env python
# -*- coding: utf-8 -*-

# memo
# mechanizeでformを探すとき。
# - 全てのformを出力
# for f in br.forms()
#    print f
# - 0番目のフォームを選択，表示
# br.select_form(0)
# print br.form

import mechanize
import BeautifulSoup
from BeautifulSoup import MinimalSoup
import os.path
import datetime

dram_base_name='dram_'
fm_base_name='fm_'
dir_name='data/'
ext_name='.html'

dram_base_name = 'dram_'
fm_base_name = 'fm_'
dir_name = 'data/'
ext_name = '.html'

price_url = {
        ("dram", "http://www.dramexchange.com/Price/Dram_Spot"),
        ("fm", "http://www.dramexchange.com/Price/Flash_Spot"),
        ("dram_c", "http://www.dramexchange.com/Price/NationalContractDramDetail"),
        ("fm_c","http://www.dramexchange.com/Price/NationalContractFlashDetail"),
        ("ssd","http://www.dramexchange.com/Price/SSD_Street"),
        ("mob","http://www.dramexchange.com/Price/MobileDramDetail"),
        ("card","http://www.dramexchange.com/Price/MemoryCard_Spot"),
        ("emmc","http://www.dramexchange.com/Price/eMMC")}

# 行儀の悪いページ向けのハンドラ
# BeautifulSoupでHTMLを整形してmechanizeに渡す
class PrettifyHandler(mechanize.BaseHandler):
    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = mechanize.response_seek_wrapper(response)
        # only use BeautifulSoup if response is html
        if response.info().dict.has_key('content-type') and ('html' in response.info().dict['content-type']):
            soup = MinimalSoup (response.get_data())
            response.set_data(soup.prettify())
        return response

br = mechanize.Browser()
br.add_handler(PrettifyHandler())

# User-Agent (this is cheating, ok?)
#br.addheaders = [('User-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1)Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0')]

# set proxy
br.set_proxies({"http" : http_proxy,})

# disable redirect
br.set_handle_redirect(False)

# open and login
try:
    br.open('http://www.dramexchange.com/Member/Login')
except:
    print 'Error : URL open error\n'

br.select_form(nr=0)
br.form['username']=dxchgID
br.form['pwd']=dxchgPW

# enable redirect
br.set_handle_redirect(True)

resp = br.submit()
date = datetime.date.today().strftime(u'%Y%m%d')

for p in price_url:
    resp = br.open(p[1])
    html = resp.read()

    filename = dir_name + p[0] + "_" + date + ext_name
    f = open(filename,'w' )
    f.write(html)
    f.close()


