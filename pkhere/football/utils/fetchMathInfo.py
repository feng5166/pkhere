#-*- coding: UTF-8 -*-
import urllib2
import cookielib
from bs4 import BeautifulSoup
#from football.models import liveMatchInfo

MATCH_CNT = 0
MATCH_INFO = {}
OLD_MATCH_INFO ={}
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
        matchLinks = []
        findLinks = tbody.findAll('div',attrs={'class':'vx__select-view',})
        for link in findLinks:
            matchLinks.append(link['data-sportskey'].strip())
            #print link['data-sportskey'].strip()
        #print len(matchLinks)
        matchinfoText=tbody.text.strip()
        matchinfoText = matchinfoText.split('\n')
        matchinfo = []
        for info in matchinfoText:
            info = info.strip()
            if info == u'':
                continue
            print info
            matchinfo.append(info)
        self.getRealMatchInfo(matchinfo,matchCategory,matchLinks)
        MATCH_CNT = len(MATCH_INFO)
        return

    def getRealMatchInfo(self, matchinfo ,matchCategory,matchLinks):
        global MATCH_INFO,OLD_MATCH_INFO
        mCat = u'未知'
        index = 0
        i = 0
        offset = 0
        while(i<len(matchinfo)):
            if self.isMatchCategory(matchinfo[i], matchCategory):
                matchType = matchinfo[i]
                offset = 4
            else:
                offset = 0
            MATCH_INFO[index] = {}
            #print 'offset',offset
            MATCH_INFO[index]['matchType'] =  matchType
            if(matchinfo[i+offset].find(':')>0):
                MATCH_INFO[index]['matchMinute'] = matchinfo[i+offset].split(':')[0]
            else:
                MATCH_INFO[index]['matchMinute'] = '00'
                offset -=1
            MATCH_INFO[index]['homeTeam'] = matchinfo[i+offset+1]
            MATCH_INFO[index]['homeGoal'] = matchinfo[i+offset+2]
            MATCH_INFO[index]['awayTeam'] = matchinfo[i+offset+3]
            MATCH_INFO[index]['awayGoal'] = matchinfo[i+offset+4]
            try:
                MATCH_INFO[index]['linkPath'] = matchLinks[index]
                print MATCH_INFO[index]['linkPath']
            except:
                print len(MATCH_INFO),len(matchLinks),index,MATCH_INFO[index]['homeTeam']
            if len(matchinfo)>(i+offset+5) and matchinfo[i+offset+5].find('.')!=-1:
                MATCH_INFO[index]['currentOupeiBet'] = '('+matchinfo[i+offset+5] +' '+ matchinfo[i+offset+6] + ' ' + matchinfo[i+offset+7] +')'
            else:
                offset-=3
                MATCH_INFO[index]['currentOupeiBet'] = u'(停盘)'
            i=i+offset+8
            print  str(index) + '   '+MATCH_INFO[index]['matchType'] + "   "+ MATCH_INFO[index]['matchMinute']+'   '+MATCH_INFO[index]['currentOupeiBet'] +"     " + MATCH_INFO[index]['homeTeam'] +"vs"+MATCH_INFO[index]['awayTeam']
            index+=1
        return index

    def isMatchCategory(self,match,matchCategory):
        return match in matchCategory


    def getMatchDetails(self,urlPath):
        content = self.getContentByUrl(urlPath)
        soup = BeautifulSoup(content)
        content = soup.prettify()
        soup = BeautifulSoup(content)
        #print soup
        homeTeamBet = soup.find('td',attrs={'class':'c1 bl ti',} )
        homeTeamBet= homeTeamBet.text.replace('\n','').strip()
        homeTeamBet = homeTeamBet.split(' ')
        awayTeamBet = soup.find('td',attrs={'class':'c2 bl ti',} )
        awayTeamBet= awayTeamBet.text.replace('\n','').strip()
        awayTeamBet = awayTeamBet.split(' ')
        print homeTeamBet[0],homeTeamBet[1],homeTeamBet[-1]
        print awayTeamBet[0],awayTeamBet[1],awayTeamBet[-1]
        betsInfo = soup.findAll('div',attrs={'class':'cpnseccnt',} )
        #print betsInfo
        for betInfo in betsInfo:
            betInfo =  betInfo.text.replace('\n','').strip()
            if betInfo.find(u'亚洲让分盘')!=-1:
                rangfenBet = betInfo.split(' ')
            elif betInfo.find(u'大小盘')!=-1:
                daxiaoBet = betInfo.split(' ')
        print rangfenBet
        print daxiaoBet
        corners = soup.findAll('td',attrs={'class':'cst',} )
        #for corner in corners:
        print corners[0].text.strip(),corners[5].text.strip()

#

sp = Sprider()
#urlPath = 'https://mobile.28365365.com/sport/splash/Default.aspx?Sport=1&key=1&L=2&ip=
urlPath = 'http://www.28365365.com/Lite/cache/api/?&rw=in-play/overview&lng=10'


detailPath ='http://www.28365365.com/Lite/cache/api/?clt=9994&op=14&rw=in-play/&cid=9998&cpid=1-1-5-26348303-2-0-0-1-1-0-0-0-0-0-1-0-0-0-0-0-0&wg=False&cf=E&lng=10&cty=42&fm=1&tzi=27&oty=2&hd=Y&mlive=0'

#sp.parseContentByUrl(urlPath)
#sp.getMatchDetails('https://mobile.28365365.com/sport/coupon/?ptid=0&key=1-1-5-26346041-2-0-0-1-1-0-0-0-0-0-1-0-0-0-0-0-0')
#sp.parseContentByUrl(urlPath)
sp.getMatchDetails(detailPath)

