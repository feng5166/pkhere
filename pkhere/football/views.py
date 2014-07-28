#-*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from utils import sprider
from football.models import liveMatchZhiBo


# Create your views here.
def index(response):
    return render_to_response('football/template/index.html')

def score(response):
    sp = sprider.Sprider()
    urlPath = 'http://www.28365365.com/Lite/cache/api/?&rw=in-play/overview&lng=10'
    sp.parseContentByUrl(urlPath)
    matchInfo = sprider.MATCH_INFO
    matchCnt = len(matchInfo)
    return render_to_response('football/template/bf.html',
                              {'matchInfo': matchInfo,
                               'matchCnt':  matchCnt,
                              })

def zhibo(response):
    liveMatchs = liveMatchZhiBo.objects.all()
    for liveMatch in liveMatchs:
        liveMatch.matchName = liveMatch.matchName.replace('<b>','')
        liveMatch.matchName = liveMatch.matchName.replace('</b>','')
        liveMatch.matchName  = liveMatch.dateTime.strip().split(' ')[0]  + " " + liveMatch.matchName
        liveMatch.linkPath  = liveMatch.linkPath.split('@')[1:]
        liveMatch.linkPath = "<a href=" + liveMatch.linkPath[1] + ' target=\"_blank\">' + liveMatch.linkPath[0] + "</a>"
    return render_to_response('football/template/zb.html',
                              {'liveMatchs': liveMatchs,
                              } )

def zhiboDetails(response):
    path = response.GET.get('path')
    urlPath = 'http://www.zhibo8.cc'+path
    sp =sprider.Sprider()
    titleName,matchDetails = sp.parseContentByUrl(urlPath)
    if not matchDetails:
         matchDetails.append(u'<font color="red"><strong>直播信号(该赛事直播已结束)</strong></font>')
    print titleName
    print matchDetails
    return render_to_response('football/template/zbDetails.html',
                                {'titleName': titleName,
                                'matchDetails':  matchDetails,
                                }
                            )