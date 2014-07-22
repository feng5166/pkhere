#-*- coding: UTF-8 -*-
import urllib2
import urllib
import time
import cookielib
import re
import StringIO
import gzip
from bs4 import BeautifulSoup

MATCH_CNT = 0
MATCH_INFO = {}
OLD_MATCH_INFO ={}
PREFIX_PATH = "https://mobile.28365365.com/sport"
class Sprider(object):
    _instance = None
    def __init__(self):
        self.headers  = {
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        #'Accept-Encoding':'gzip, deflate',
                        'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                        #'Connection': 'Keep-Alive',
                        'Host': 'www.28365365.com',
                        'Content-Type':'text/html; charset=utf-8',
                        #'Referer': 'http://www.28365365.com/lite/',
                        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0',
                        'Cookie':'aps03=tzi=27&oty=2&bst=1&hd=Y&lng=10&cf=E&ct=42&cst=132&v=1&cg=0&ltwo=False; rmbs=3; usdi=uqid=BC192014%2D5EE0%2D47AF%2D8404%2D5C3EE5C0B53B',

                        }
        self.postData = {
                        }
        return


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Sprider, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    #通过url获取网页的内容
    def getContentByUrl(self,urlPath):
        if urlPath == '':
            return ''


        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        request = urllib2.Request(urlPath,headers=self.headers)
        print request.get_full_url(),request.get_data()
        content = urllib2.urlopen(request).read()
        #print 'getContentByUrl:',content
        return content
    def parseContentByUrl(self,urlPath):
        content = self.getContentByUrl(urlPath)
        self.parseMatchInfoByContent(content)


    def parseMatchInfoByContent(self,content):
        global MATCH_CNT,MATCH_INFO,OLD_MATCH_INFO
        MATCH_INFO ={}
        soup = BeautifulSoup(content)
        content = soup.prettify()
        soup = BeautifulSoup(content)
        s = soup.find('a',attrs={'class':'hdrlnk hdrlnksec nav-level-one cat_1 current-nav',} )
        if not s:
            return
        tbody = soup.find('tbody')
        findCats = tbody.findAll('th',attrs={'class':'c1 vx__sub-name algnl',})
        matchCategory =[]
        for cat in findCats:
            #=print cat.text.strip()
            matchCategory.append(cat.text.strip())
        matchinfoText=tbody.text.strip()
        matchinfoText = matchinfoText.split('\n')
        matchinfo = []
        for info in matchinfoText:
            info = info.strip()
            if info == u'':
                continue
            print info
            matchinfo.append(info)
        self.getRealMatchInfo(matchinfo,matchCategory)
        MATCH_CNT = len(MATCH_INFO)
        return

    def getInfoInOldIndex(self):
        global OLD_MATCH_INFO
    def getRealMatchInfo(self, matchinfo ,matchCategory):
        global MATCH_INFO,OLD_MATCH_INFO
        mCat = u'未知'
        index = 0
        i = 0
        offset = 0
        while(i<len(matchinfo)):
            if self.isMatchCategory(matchinfo[i], matchCategory):
                mCat = matchinfo[i]
                offset = 4
            else:
                offset = 0
            MATCH_INFO[index] = {}
            #print 'offset',offset
            MATCH_INFO[index]['matchCategory'] =  mCat
            try:
                MATCH_INFO[index]['time1'] = matchinfo[i+offset].split(':')[0]
                MATCH_INFO[index]['time2'] = matchinfo[i+offset].split(':')[1]
            except:
                MATCH_INFO[index]['time1'] = '00'
                MATCH_INFO[index]['time2'] = '00'
                offset -=1
            MATCH_INFO[index]['team1'] = matchinfo[i+offset+1]
            MATCH_INFO[index]['score1'] = matchinfo[i+offset+2]
            MATCH_INFO[index]['team2'] = matchinfo[i+offset+3]
            MATCH_INFO[index]['score2'] = matchinfo[i+offset+4]
            if len(matchinfo)>(i+offset+5) and matchinfo[i+offset+5].find('.')!=-1:
                MATCH_INFO[index]['oupei'] = '('+matchinfo[i+offset+5] +' '+ matchinfo[i+offset+6] + ' ' + matchinfo[i+offset+7] +')'
            else:
                offset-=3
                MATCH_INFO[index]['oupei'] = u'(停盘)'
            i=i+offset+8
            print  str(index) + '   '+MATCH_INFO[index]['matchCategory'] + "   "+ MATCH_INFO[index]['time1']+'   '+MATCH_INFO[index]['oupei'] +"     " + MATCH_INFO[index]['team1'] +"vs"+MATCH_INFO[index]['team2']
            index+=1
        return index

    def isMatchCategory(self,match,matchCategory):
        return match in matchCategory

#sp = Sprider()
#urlPath = 'https://mobile.28365365.com/sport/splash/Default.aspx?Sport=1&key=1&L=2&ip=
#urlPath = 'http://www.28365365.com/Lite/cache/api/?&rw=in-play/overview&lng=10'

#sp.parseContentByUrl(urlPath)
#sp.getMatchDetails('https://mobile.28365365.com/sport/coupon/?ptid=0&key=1-1-5-26336398-2-0-0-1-1-0-0-0-0-0-1-0-0-0-0-0-0')
#sp.parseContentByUrl(urlPath)