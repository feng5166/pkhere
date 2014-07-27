#-*- coding: UTF-8 -*-
import urllib2
import cookielib
from bs4 import BeautifulSoup
from datetime import date

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
        print request.get_full_url(),request.get_data()
        content = urllib2.urlopen(request).read()
        return content


class BiFenSprider(Sprider):
    def __init__(self,urlPath,dataBasePath,sqlTable):
        super(Sprider, self).__init__(urlPath,dataBasePath,sqlTable)
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
            print info
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
            self.match_info[index]['initYaPeiBet'] = u'停盘'
            self.match_info[index]['currentBigBall'] = u'停盘'
            self.match_info[index]['currentCorner'] = u'停盘'
            self.match_info[index]['currentYaPeiBet'] = u'停盘'
            self.match_info[index]['isOver'] = False
            try:
                self.match_info[index]['linkPath'] = matchLinks[index]
                print self.match_info[index]['linkPath']
            except:
                print len(self.match_info),len(matchLinks),index,self.match_info[index]['homeTeam']
            if len(matchinfo)>(i+offset+5) and matchinfo[i+offset+5].find('.')!=-1:
                self.match_info[index]['currentOupeiBet'] = '('+matchinfo[i+offset+5] +' '+ matchinfo[i+offset+6] + ' ' + matchinfo[i+offset+7] +')'
            else:
                offset-=3
                self.match_info[index]['currentOupeiBet'] = u'(停盘)'
            i=i+offset+8
            print  str(index) + '   '+self.match_info[index]['matchType'] + "   "+ self.match_info[index]['matchMinute']+'   '+self.match_info[index]['currentOupeiBet'] +"     " + self.match_info[index]['homeTeam'] +"vs"+self.match_info[index]['awayTeam']
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

    def updateMatchInfo(self):
        fetchall_sql = '''SELECT * FROM football_liveMatchInfo'''
        find = False
        try:
            self.sqlliteHelper.fetchall(fetchall_sql)
            find = True
        except:
            find = False
        print find
        if find:
            save_sql = '''INSERT INTO football_liveMatchInfo values (?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            data = []
            for index in self.match_info:
                info = (self.match_info[index]['homeTeam'],self.match_info[index]['awayTeam'],self.match_info[index]['matchType'],\
                        self.match_info[index]['matchDate'],self.match_info[index]['matchMinute'],self.match_info[index]['initOupeiBet'],\
                        self.match_info[index]['currentOupeiBet'],self.match_info[index]['homeGoal'],self.match_info[index]['awayGoal'],\
                        self.match_info[index]['homeCorner'],self.match_info[index]['awayCorner'],self.match_info[index]['initBigBall'],\
                        self.match_info[index]['initCorner'],self.match_info[index]['initYaPeiBet'],self.match_info[index]['currentBigBall'], \
                        self.match_info[index]['currentCorner'],self.match_info[index]['currentYaPeiBet'],self.match_info[index]['linkPath'],\
                        self.match_info[index]['isOver'],\
                        )
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
        self.realZhiBoInfo(boxResult[2])
        #self.realZhiBoInfo(boxResult[3])

    def realZhiBoInfo(self,boxResult):
        content = boxResult
        dateTime =  content.find('div',attrs={'class':'titlebar',} ).text
        matchList = content.findAll('li')
        for match in matchList:
            contents = match.contents
            matchName = u''
            for name in contents:
                self.match_zhibo[self.index] = {}
                print 'realZhiBoInfo:',name,contents
                if name.name=='a':
                    if name['href'].find('http') ==-1:
                        zhiboName = name.get_text()
                        zhiboLink = "http://www.pkhere.com/zhiboDetails?path=" + name['href']
                        nameAndLink = '@' + zhiboName + '@' + zhiboLink
                else:
                    matchName = matchName + unicode(name)
            self.match_zhibo[self.index]['matchName'] = matchName.strip()
            self.match_zhibo[self.index]['dateTime']  =  dateTime
            self.match_zhibo[self.index]['linkPath']  =  nameAndLink
            print self.match_zhibo[self.index]['linkPath'],self.match_zhibo[self.index]['linkPath']
            self.index = self.index + 1
        #for index in self.match_zhibo:
            #print self.match_zhibo[index]['dateTime'] + u'   ' + self.match_zhibo[index]['matchName'] + u'   ' + str(self.match_zhibo[index]['linkPath'])
    def updateMatchZhiBoInfo(self):
        #self.sqlliteHelper.drop_table('football_livematchzhibo')
        #return
        self.parseZhiBoMatch()
        fetchall_sql = '''SELECT * FROM football_livematchzhibo'''
        self.sqlliteHelper.fetchall(fetchall_sql)
        delete_sql = ''' DELETE FROM football_livematchzhibo '''
        self.sqlliteHelper.delete(delete_sql,None)
        save_sql = '''INSERT INTO football_livematchzhibo values (?, ?, ?,?)'''
        datainfo = []
        for index in self.match_zhibo:
            print '------',self.match_zhibo[index]['dateTime']
            data =(index,self.match_zhibo[index]['matchName'],self.match_zhibo[index]['dateTime'],self.match_zhibo[index]['linkPath'])
            datainfo.append(data)
        self.sqlliteHelper.save(save_sql, datainfo)
        fetchall_sql = '''SELECT * FROM football_livematchzhibo'''
        self.sqlliteHelper.fetchall(fetchall_sql)

#urlPath = 'https://mobile.28365365.com/sport/splash/Default.aspx?Sport=1&key=1&L=2&ip=


detailPath ='http://www.28365365.com/Lite/cache/api/?clt=9994&op=14&rw=in-play/&cid=9998&cpid=1-1-5-26350354-2-0-0-1-1-0-0-0-0-0-1-0-0-0-0-0-0&wg=False&cf=E&lng=10&cty=42&fm=1&tzi=27&oty=2&hd=Y&mlive=0'

#sp.parseContentByUrl(urlPath)
#sp.getMatchDetails('https://mobile.28365365.com/sport/coupon/?ptid=0&key=1-1-5-26346041-2-0-0-1-1-0-0-0-0-0-1-0-0-0-0-0-0')
#sp.parseContentByUrl(urlPath)
#sp.getMatchDetails(detailPath)checkInDateBase



def parseZhiBoByContent():
    dbFilePath ='/Users/DullBaby/Desktop/code/www/pkhere/db.sqlite3'
    urlPath = "http://www.zhibo8.cc"
    tableName = 'football_liveMatchInfo'
    headers = {}
    sp = ZhiBoSprider(urlPath,dbFilePath,tableName)
    sp.setHeader(headers)
    sp.updateMatchZhiBoInfo()

def parseBifenByContent():
    dbFilePath ='/Users/DullBaby/Desktop/code/www/pkhere/db.sqlite3'
    urlPath = 'http://www.28365365.com/Lite/cache/api/?&rw=in-play/overview&lng=10'
    tableName = 'football_liveMatchInfo'
    headers  = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                'Host': 'www.28365365.com',
                'Content-Type':'text/html; charset=utf-8',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0',
                'Cookie':'aps03=tzi=27&oty=2&bst=1&hd=Y&lng=10&cf=E&ct=42&cst=132&v=1&cg=0&ltwo=False; rmbs=3; usdi=uqid=BC192014%2D5EE0%2D47AF%2D8404%2D5C3EE5C0B53B',
                }
    sp = BiFenSprider(urlPath,dbFilePath,tableName)
    sp.setHeader(headers)
    sp.parseContentByUrl()
    sp.updateMatchInfo()

if __name__ == '__main__':
    parseZhiBoByContent()


