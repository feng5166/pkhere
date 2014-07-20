#-*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context,loader
from utils import sprider


# Create your views here.
def index(response):
    sp = sprider.Sprider()
    urlPath = 'http://www.28365365.com/Lite/cache/api/?&rw=in-play/overview&lng=10'
    sp.parseContentByUrl(urlPath)
    matchInfo = sprider.MATCH_INFO
    matchCnt = len(matchInfo)
    return render_to_response('football/template/index.html',
                              {'matchInfo': matchInfo,
                               'matchCnt':  matchCnt,
                              })

def details(response):
    id = response.GET.get('id')
    return HttpResponse(id)