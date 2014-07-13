#-*- coding: UTF-8 -*-
import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import socket

MATCH_CNT = 0
MATCH_INFO = {}
class Sprider(object):
    _instance = None
    def __init__(self):
        self.headers  = {
                        'Accept':'application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*',
                        #S'Accept-Encoding':'gzip, deflate',
                        'Accept-Language':'zh-CN',
                        'Connection': 'Keep-Alive',
                        #'Cookie': 'aps03=lng=2&tzi=27&ct=42&cst=132&cg=0; session=processform=0; lng=2; pstk=0E49F90691A84947A853A8106B32ED3F000003',
                        'Host': 'mobile.28365365.com',
                        #'Referer': 'https://mobile.28365365.com/sport/default.aspx?ID=200%3a0&key=&ip=1&clvl=&lvl=&t=&bsd=',
                        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
        }
        self.postData = {'Sport': 1,
                         'key': 1,
                         'L': 2,
                         'ip': 1,
                         'accesskey':'1',
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

        #postdata = urllib.urlencode(self.postData)
        request = urllib2.Request(urlPath,headers=self.headers)
        #print request.get_full_url(),request.get_data(),postdata,dir(request)
        content = urllib2.urlopen(request).read()
        #print 'getContentByUrl:',content
        return content
    def parseContentByUrl(self,urlPath):
        content = self.getContentByUrl(urlPath)
        self.parseMatchInfoByContent(content)


    def parseMatchInfoByContent(self,content):
        global MATCH_CNT
        global MATCH_INFO
        soup = BeautifulSoup(content)
        s = soup.find_all('a')
        matchNumber = self.getMatchNumbers(s)
        print matchNumber
        i = 0
        for j in s[:-15]:
            MATCH_INFO[i]={}
            if j.text == '':
                continue
            team1,team2 = self.getTeamSplitName(j)
            score1,score2 = self.getTeamSplitScore(j)
            time1,time2 = self.getMatchTime(j)
            MATCH_INFO[i]['team1'] = team1
            MATCH_INFO[i]['team2'] = team2
            MATCH_INFO[i]['score1'] = score1
            MATCH_INFO[i]['score2'] = score2
            MATCH_INFO[i]['time1'] = time1
            MATCH_INFO[i]['time2'] = time2
            i+=1
        #for i in MATCH_INFO:
            #print str(MATCH_INFO[i]['time1'])+":"+str(MATCH_INFO[i]['time1']) +"     " + MATCH_INFO[i]['team1'] +"vs"+MATCH_INFO[i]['team2']






    def getMatchNumbers(self,matches):
        matchNumber = (len(matches)-16)
        return matchNumber

    def getTeamSplitName(self,contents):
        try:
            teamNames = contents.contents[0]
        except:
            teamNames = 'NA v NA'
        names = teamNames.split('v')
        return names[0],names[1]

    def getTeamSplitScore(self,contents):
        try:
            teamScores = contents.contents[2].text
            if not teamScores:
                teamScores = '0-0'
        except:
            teamScores = '0-0'
        scores = teamScores.split('-')
        return scores[0],scores[1]

    def getMatchTime(self,contents):
        try:
            matchTimes = contents.contents[3].text
            if not matchTimes:
                matchTimes = '00:00'
        except:
            matchTimes = '00:00'
        times = matchTimes.split(':')
        return times[0],times[1]


sp = Sprider()
#https://mobile.28365365.com/sport/splash/Default.aspx?Sport=1&key=1&L=2&ip=1
sp.parseContentByUrl('https://mobile.28365365.com/sport/splash/Default.aspx?Sport=1&key=1&L=2&ip=1')
