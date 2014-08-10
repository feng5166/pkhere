#-*- coding: UTF-8 -*-
import os
import fetchMathInfo
import globals
import timeHelper

headers  = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
            'Host': 'www.28365365.com',
            'Content-Type':'text/html; charset=utf-8',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0',
            'Cookie':'aps03=tzi=27&oty=2&bst=1&hd=Y&lng=10&cf=E&ct=42&cst=132&v=1&cg=0&ltwo=False; rmbs=3; usdi=uqid=BC192014%2D5EE0%2D47AF%2D8404%2D5C3EE5C0B53B',
            }
urlPath = 'http://www.28365365.com/Lite/cache/api/?&rw=in-play/overview&lng=10'
tableName = 'football_liveMatchInfo'
sp = fetchMathInfo.BiFenSprider(urlPath,globals.DBFILEPATH,tableName)
def parseBifenByContent():
    sp.setHeader(headers)
    sp.setUrlPath(urlPath)
    lock=open('fetch.lock','w')
    sp.startFetchBifen()
    os.remove('fetch.lock')
if __name__ == '__main__':
    #parseBifenByContent()
    timeHelper = timeHelper.Timer(parseBifenByContent,sleep=20)
    timeHelper.run()