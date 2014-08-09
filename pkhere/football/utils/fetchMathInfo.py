#-*- coding: UTF-8 -*-
import urllib2
import cookielib
import time
import re
from bs4 import BeautifulSoup
from datetime import date

import globals
import sqliteHelper

class Sprider(object):
    def __init__(self,dataBasePath,urlPath,sqlTable):
        self.headers  = {}
        self.postData = {}
        self.sqlliteHelper = sqliteHelper.SqliteHelper(dataBasePath)
        self.urlPath = urlPath
        self.sqlTable = sqlTable
        return

    def setHeader(self,headers):
        self.headers = headers

    def setPostData(self,postData):
        self.postData = postData

    def setUrlPath(self,urlpath):
        self.urlPath = urlpath

    #通过url获取网页的内容
    def getContentByUrl(self):
        if self.urlPath == '':
            return ''
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        request = urllib2.Request(self.urlPath,headers=self.headers)
        #print request.get_full_url(),request.get_data()
        fails = 0
        while True:
            print 'fails',fails
            if fails >= 3:
                break
            try:
                content = urllib2.urlopen(request,timeout=20).read()
                break
            except:
                fails+=1

        return content


class BiFenSprider(Sprider):
    def __init__(self,urlPath,dataBasePath,sqlTable):
        super(Sprider, self).__init__()
        self.match_info = {}
        self.match_cnt = 0
        self.sqlliteHelper = sqliteHelper.SqliteHelper(dataBasePath)
        self.urlPath = urlPath
        self.sqlTable = sqlTable

    def parseContentByUrl(self):
        content = self.getContentByUrl()
        self.parseMatchInfoByContent(content)


    def parseMatchInfoByContent(self,content):
        self.match_info ={}
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
            #print info
            matchinfo.append(info)
        self.match_cnt  = self.getRealMatchInfo(matchinfo,matchCategory,matchLinks)
        return

    def getRealMatchInfo(self, matchinfo ,matchCategory,matchLinks):
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
            self.match_info[index] = {}
            #print 'offset',offset
            self.match_info[index]['matchType'] =  matchType
            if(matchinfo[i+offset].find(':')>0):
                self.match_info[index]['matchMinute'] = matchinfo[i+offset].split(':')[0]
            else:
                self.match_info[index]['matchMinute'] = '00'
                offset -=1
            self.match_info[index]['homeTeam'] = matchinfo[i+offset+1]
            self.match_info[index]['homeGoal'] = matchinfo[i+offset+2]
            self.match_info[index]['awayTeam'] = matchinfo[i+offset+3]
            self.match_info[index]['awayGoal'] = matchinfo[i+offset+4]
            self.match_info[index]['matchDate'] = date.today()
            self.match_info[index]['initOupeiBet'] = u'停盘'
            self.match_info[index]['homeCorner'] = 0
            self.match_info[index]['awayCorner'] = 0
            self.match_info[index]['initBigBall'] = u'停盘'
            self.match_info[index]['initCorner'] = u'停盘'
            self.match_info[index]['initYaPeiBet'] = u'停盘'
            self.match_info[index]['currentBigBall'] = u'停盘'
            self.match_info[index]['currentCorner'] = u'停盘'
            self.match_info[index]['currentYaPeiBet'] = u'停盘'
            self.match_info[index]['isOver'] = False
            try:
                self.match_info[index]['linkPath'] = matchLinks[index]
                print self.match_info[index]['linkPath']
            except:
                self.match_info[index]['linkPath'] =""
                print len(self.match_info),len(matchLinks),index,self.match_info[index]['homeTeam']
            if len(matchinfo)>(i+offset+5) and matchinfo[i+offset+5].find('.')!=-1:
                self.match_info[index]['currentOupeiBet'] = '('+matchinfo[i+offset+5] +' '+ matchinfo[i+offset+6] + ' ' + matchinfo[i+offset+7] +')'
            else:
                offset-=3
                self.match_info[index]['currentOupeiBet'] = u'(停盘)'
            i=i+offset+8
            print  str(index) + '   '+self.match_info[index]['matchType'] + "   "+ self.match_info[index]['matchMinute']+'   '+self.match_info[index]['currentOupeiBet'] +"     " + self.match_info[index]['homeTeam'] +"vs"+self.match_info[index]['awayTeam']
            index+=1
        self.getMatchDetails()
        return index

    def isMatchCategory(self,match,matchCategory):
        return match in matchCategory


    def getMatchDetails(self):
        for index in self.match_info:
            urlPath = self.match_info[index]['linkPath']
            if urlPath == "":
                continue
            urlPath = "http://www.28365365.com/Lite/cache/api/?clt=9994&op=14&rw=in-play/&cid=9998&cpid="+urlPath +"&wg=False&cf=E&lng=10&cty=42&fm=1&tzi=27&oty=2&hd=Y&mlive=0"
            print 'urlPath:',urlPath
            #urlPath = "http://www.28365365.com/Lite/cache/api/?clt=9994&op=14&rw=in-play/&cid=9998&cpid=1-1-5-26381267-2-0-0-1-1-0-0-0-0-0-1-0-0-0-0-0-0&wg=False&cf=E&lng=10&cty=42&fm=1&tzi=27&oty=2&hd=Y&mlive=0"
            #print 'urlPath:',urlPath
            self.setUrlPath(urlPath)
            content = self.getContentByUrl()
            #print content
            soup = BeautifulSoup(content)
            content = soup.prettify()
            matchInfos = soup.findAll('div',attrs={'class':'cpnseccnt',},limit=2)
            findRangfenBet = False
            findBallBetBet = False
            for matchInfo in matchInfos:
                if matchInfo:
                    if matchInfo.contents[1].find('h3',attrs={'title':re.compile(u"亚洲让分盘")},):
                        if matchInfo.contents[3].findAll('a',attrs={'class':'btn-odds-lnk',},limit=2):
                            homeKeylink = matchInfo.contents[3].findAll('a',attrs={'class':'btn-odds-lnk',},limit=2)[0]['id']
                            awayKeylink = matchInfo.contents[3].findAll('a',attrs={'class':'btn-odds-lnk',},limit=2)[1]['id']
                            homeBet,rangqiu = self.getBetByPath(homeKeylink)
                            awayBet,_ = self.getBetByPath(awayKeylink)
                            currentYaPeiBet = str(homeBet) + ' ' + str(rangqiu) + ' ' + str(awayBet)
                            self.match_info[index]['currentYaPeiBet'] = currentYaPeiBet
                            findRangfenBet = True
                    elif matchInfo.contents[1].find('h3',attrs={'title':re.compile(u"大小盘")},):
                        if matchInfo.contents[3].findAll('a',attrs={'class':'btn-odds-lnk',},limit=2):
                            homeKeylink = matchInfo.contents[3].findAll('a',attrs={'class':'btn-odds-lnk',},limit=2)[0]['id']
                            awayKeylink = matchInfo.contents[3].findAll('a',attrs={'class':'btn-odds-lnk',},limit=2)[1]['id']
                            homeBet,rangqiu = self.getBetByPath(homeKeylink)
                            awayBet,_ = self.getBetByPath(awayKeylink)
                            currentBallBet = str(homeBet) + ' ' + str(rangqiu) + ' ' + str(awayBet)
                            self.match_info[index]['currentBigBall'] = currentBallBet
                            findBallBetBet = True
                            print currentBallBet
            if not findRangfenBet:
                self.match_info[index]['currentYaPeiBet'] = u'停盘'
            if not findBallBetBet:
                self.match_info[index]['currentBigBall'] = u'停盘'
            corners = soup.findAll('td',attrs={'class':'cst',} )
            self.match_info[index]['homeCorner'] =  corners[0].text.strip()
            self.match_info[index]['awayCorner'] = corners[5].text.strip()
            #break

    def getBetByPath(self,keyLink):
        print keyLink
        keyLink = keyLink.split('#')
        odd = keyLink[1].split('=')
        odd = odd[1].split('/')
        odd = float(odd[0])/float(odd[1])+1.0
        rangqiu = keyLink[5]
        rangqiu = rangqiu.split('=')
        rangqiu = float(rangqiu[1])
        return odd,rangqiu

    def updateMatchInfo(self):
        #self.sqlliteHelper.drop_table('football_liveMatchInfo')
        #return
        delete_sql = ''' DELETE FROM football_liveMatchInfo '''
        self.sqlliteHelper.delete(delete_sql,None)
        save_sql = '''INSERT INTO football_liveMatchInfo values (?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        data = []
        for index in self.match_info:
            info = (index,self.match_info[index]['homeTeam'],self.match_info[index]['awayTeam'],self.match_info[index]['matchType'],\
                    self.match_info[index]['matchDate'],self.match_info[index]['matchMinute'],self.match_info[index]['initOupeiBet'],\
                    self.match_info[index]['currentOupeiBet'],self.match_info[index]['homeGoal'],self.match_info[index]['awayGoal'],\
                    self.match_info[index]['homeCorner'],self.match_info[index]['awayCorner'],self.match_info[index]['initBigBall'],\
                    self.match_info[index]['initCorner'],self.match_info[index]['initYaPeiBet'],self.match_info[index]['currentBigBall'], \
                    self.match_info[index]['currentCorner'],self.match_info[index]['currentYaPeiBet'],self.match_info[index]['linkPath'],\
                    self.match_info[index]['isOver'],\
                    )
            print info
            data.append(info)
        self.sqlliteHelper.save(save_sql,data)
        #self.sqlliteHelper.fetchall(fetchall_sql)


class ZhiBoSprider(Sprider):
    def __init__(self,urlPath,dataBasePath,sqlTable):
        super(Sprider, self).__init__()
        self.sqlliteHelper = sqliteHelper.SqliteHelper(dataBasePath)
        self.urlPath = urlPath
        self.sqlTable = sqlTable
        self.match_zhibo = {}
        self.index = 0

    def parseZhiBoMatch(self):
        content = self.getContentByUrl()
        soup = BeautifulSoup(content)
        boxResult = soup.findAll('div',attrs={'class':'box',} )
        self.match_zhibo = {}
        self.index = 0
        print 'parseZhiBoMatch1------'
        self.realZhiBoInfo(boxResult[2])
        print 'parseZhiBoMatch2------'
        self.realZhiBoInfo(boxResult[3])
        print 'parseZhiBoMatch3------'

    def realZhiBoInfo(self,boxResult):
        content = boxResult
        dateTime =  content.find('div',attrs={'class':'titlebar',} ).text
        matchList = content.findAll('li')
        for match in matchList:
            contents = match.contents
            matchName = u''
            for name in contents:
                self.match_zhibo[self.index] = {}
                print 'realZhiBoInfo:',name.name,name,contents
                if name.name==u'a':
                    if name['href'].find('http') ==-1:
                        zhiboName = name.get_text()
                        zhiboLink = "http://www.zhibo8.cc" + name['href']
                        nameAndLink = '@' + zhiboName + '@' + globals.PREFIX_URL +str(self.index)
                else:
                    matchName = matchName + unicode(name)
            self.match_zhibo[self.index]['matchName'] = matchName.strip()
            self.match_zhibo[self.index]['dateTime']  =  dateTime
            self.match_zhibo[self.index]['linkPath']  =  nameAndLink
            self.match_zhibo[self.index]['zhiboLink']  =  zhiboLink
            self.setUrlPath(zhiboLink)
            _,self.match_zhibo[self.index]['linkDetail']=self.parseMatchDetailsByContent(zhiboLink)
            #print self.match_zhibo[self.index]['linkPath'],self.match_zhibo[self.index]['linkPath']
            self.index = self.index + 1
        for index in self.match_zhibo:
            print self.match_zhibo[index]['matchName']
    def updateMatchZhiBoInfo(self):
        #self.sqlliteHelper.drop_table('football_livematchzhibo')
        #return
        self.parseZhiBoMatch()
        #fetchall_sql = '''SELECT * FROM football_livematchzhibo'''
        #self.sqlliteHelper.fetchall(fetchall_sql)
        delete_sql = ''' DELETE FROM football_livematchzhibo '''
        self.sqlliteHelper.delete(delete_sql,None)
        save_sql = '''INSERT INTO football_livematchzhibo values (?, ?, ?,?,?)'''
        datainfo = []
        for index in self.match_zhibo:
            data =(index,self.match_zhibo[index]['matchName'],self.match_zhibo[index]['dateTime'],self.match_zhibo[index]['linkPath'],self.match_zhibo[index]['linkDetail'])
            datainfo.append(data)
        self.sqlliteHelper.save(save_sql, datainfo)
        fetchall_sql = '''SELECT * FROM football_livematchzhibo'''
        self.sqlliteHelper.fetchall(fetchall_sql)

    def parseMatchDetailsByContent(self,urlPath):
        #time.sleep(3)
        headers = {}
        self.setHeader(headers)
        self.setUrlPath(urlPath)
        content = self.getContentByUrl()
        soup = BeautifulSoup(content)
        #print soup
        titleName =  soup.find('div',attrs={'class':'title',} ).text
        results =  soup.find('div',attrs={'id':'signals',} )
        details = []
        for content in results.contents:
            content = unicode(content)
            print 'parseMatchDetailsByContent:',titleName,content
            print content.find('http:'), content.find('www.zhibo8.cc')==-1 , content.find('www.188bifen.com')==-1
            if content.find('<a')!=-1 and content.find('www.zhibo8.cc')==-1 and content.find('www.188bifen.com')==-1:
                details.append(content)
        htmlContent = ""
        if not details:
            htmlContent =u'<font color="red"><strong>直播信号(该赛事直播已结束)</strong></font>'
            return titleName,htmlContent
        for matchDetail in details:
            htmlContent = htmlContent +  "<li>" + matchDetail + "</li>"
        return titleName,htmlContent

#urlPath = 'https://mobile.28365365.com/sport/splash/Default.aspx?Sport=1&key=1&L=2&ip=


detailPath ='http://www.28365365.com/Lite/cache/api/?clt=9994&op=14&rw=in-play/&cid=9998&cpid=1-1-5-26350354-2-0-0-1-1-0-0-0-0-0-1-0-0-0-0-0-0&wg=False&cf=E&lng=10&cty=42&fm=1&tzi=27&oty=2&hd=Y&mlive=0'



if __name__ == '__main__':
    pass
    #parseBifenByContent()
    #parseZhiBoByContent()