#-*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context,loader
from utils import sprider


# Create your views here.
def index(response):
    sp = sprider.Sprider()
    sp.parseContentByUrl('https://mobile.28365365.com/sport/splash/Default.aspx?Sport=1&key=1&L=2&ip=1')
    matchInfo = sprider.MATCH_INFO
    matchCnt = len(matchInfo)
    return render_to_response('football/template/index.html',
                              {'matchInfo': matchInfo,
                               'matchCnt':  matchCnt,
                              })

def details(response):
    id = response.GET.get('id')
    return HttpResponse(id)