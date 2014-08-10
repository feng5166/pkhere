#-*- coding: UTF-8 -*-
import os
from django.http import HttpResponse
from django.shortcuts import render_to_response
from football.models import liveMatchZhiBo
from football.models import liveMatchInfo


# Create your views here.
def index(response):
    return render_to_response('football/template/index.html')

OLDMATCHS =[]
MATCHCNT = 0
FILEPATH = './utils/fetch.lock'
def score(response):
    global FILEPATH,OLDMATCHS,MATCHCNT
    e = os.path.exists(FILEPATH)
    if e:
        print 'file is exist'
        liveMatchs = OLDMATCHS
        matchCnt = MATCHCNT
    else:
        liveMatchs = liveMatchInfo.objects.order_by('-matchMinute')
        matchCnt = len(liveMatchs)
    return render_to_response('football/template/bf.html',
                              {'liveMatchs': liveMatchs,
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
    idNo = response.GET.get('id')
    liveMatch = liveMatchZhiBo.objects.get(id=idNo)
    matchDetails = liveMatch.linkDetail
    titleName    = liveMatch.matchName
    return render_to_response('football/template/zbDetails.html',
                                {'titleName': titleName,
                                'matchDetails':  matchDetails,
                                }
                            )