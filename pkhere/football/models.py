#-*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings
class liveMatchInfo(models.Model):
    homeTeam = models.CharField(max_length=50)
    awayTeam = models.CharField(max_length=50)
    matchType = models.CharField(max_length=50)
    matchDate = models.DateField()
    matchMinute = models.CharField(max_length=10)
    initOupeiBet = models.CharField(max_length=30)
    currentOupeiBet = models.CharField(max_length=30)
    homeGoal = models.IntegerField()
    awayGoal = models.IntegerField()
    homeCorner = models.IntegerField()
    awayCorner = models.IntegerField()
    awayGoal = models.IntegerField()
    initBigBall = models.CharField(max_length=30)
    initCorner = models.CharField(max_length=30)
    initYaPeiBet = models.CharField(max_length=30)
    currentBigBall = models.CharField(max_length=30)
    currentCorner = models.CharField(max_length=30)
    currentYaPeiBet = models.CharField(max_length=30)
    linkPath = models.CharField(max_length=150)
    isOver = models.BooleanField()
    def __str__(self):
        return '%s vs %s' % (self.homeTeam, self.awayTeam)

class liveMatchZhiBo(models.Model):
    matchName = models.CharField(max_length=100)
    dateTime = models.CharField(max_length=50)
    linkPath = models.CharField(max_length=500)
    def __str__(self):
        return '%s %s' % (self.dateTime, self.matchName)

