#-*- coding: UTF-8 -*-
import fetchMathInfo
import globals

detailPath ='http://www.28365365.com/Lite/cache/api/?clt=9994&op=14&rw=in-play/&cid=9998&cpid=1-1-5-26350354-2-0-0-1-1-0-0-0-0-0-1-0-0-0-0-0-0&wg=False&cf=E&lng=10&cty=42&fm=1&tzi=27&oty=2&hd=Y&mlive=0'
def parseBifenByContent():
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
    sp = fetchMathInfo.BiFenSprider(urlPath,globals.DBFILEPATH,tableName)
    sp.setHeader(headers)
    sp.parseContentByUrl()
    sp.updateMatchInfo()
if __name__ == '__main__':
    parseBifenByContent()