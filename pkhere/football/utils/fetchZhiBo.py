#-*- coding: UTF-8 -*-
import fetchMathInfo
import globals


def parseZhiBoByContent():
    urlPath = 'http://www.zhibo8.cc'
    tableName = 'football_livematchzhibo'
    headers  = {}
    sp = fetchMathInfo.ZhiBoSprider(urlPath,globals.DBFILEPATH,tableName)
    sp.setHeader(headers)
    sp.updateMatchZhiBoInfo()
if __name__ == '__main__':
    parseZhiBoByContent()