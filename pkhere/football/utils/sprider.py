#-*- coding: UTF-8 -*-
import urllib2
import cookielib
from bs4 import BeautifulSoup

MATCH_CNT = 0
MATCH_INFO = {}
OLD_MATCH_INFO ={}
PREFIX_PATH = "https://mobile.28365365.com/sport"
class Sprider(object):
    _instance = None
    def __init__(self):
        self.headers  = {}
        self.postData = {}
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
        titleName,details = self.parseMatchDetailsByContent(content)
        return titleName,details


    def parseMatchDetailsByContent(self,content):
        global MATCH_CNT,MATCH_INFO,OLD_MATCH_INFO
        MATCH_INFO ={}
        soup = BeautifulSoup(content)
        #print soup
        titleName =  soup.find('div',attrs={'class':'title',} ).text
        results =  soup.find('div',attrs={'id':'signals',} )
        details = []
        for content in results.contents:
            content = unicode(content)
            print content.find('http:'), content.find('www.zhibo8.cc')==-1 , content.find('www.188bifen.com')==-1,content
            if content.find('http:')!=-1 and content.find('www.zhibo8.cc')==-1 and content.find('www.188bifen.com')==-1:
                details.append(content)
        print '------------------',details
        return titleName,details
