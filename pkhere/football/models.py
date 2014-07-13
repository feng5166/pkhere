#-*- coding: UTF-8 -*-
from django.db import models

# Create your models here.
class HelloWorld(models.Model):
    def printHello(self):
        print 'Hello World'
