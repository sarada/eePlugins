# -*- coding: utf-8 -*-
#
# WeatherPlugin E2
#
# Coded by Dr.Best (c) 2012-2013
# Support: www.dreambox-tools.info
# E-Mail: dr.best@dreambox-tools.info
#
# This plugin is open source but it is NOT free software.
#
# This plugin may only be distributed to and executed on hardware which
# is licensed by Dream Multimedia GmbH.
# In other words:
# It's NOT allowed to distribute any parts of this plugin or its source code in ANY way
# to hardware which is NOT licensed by Dream Multimedia GmbH.
# It's NOT allowed to execute this plugin and its source code or even parts of it in ANY way
# on hardware which is NOT licensed by Dream Multimedia GmbH.
#
# If you want to use or modify the code or parts of it,
# you have to keep MY license and inform me about the modifications by mail.
#

from Components.AVSwitch import AVSwitch
from Components.config import config
from Components.j00zekAccellPixmap import j00zekAccellPixmap 
from enigma import ePixmap, eSize, eTimer, ePicLoad
from random import randint
from Renderer import Renderer
from Tools.LoadPixmap import LoadPixmap
import os


class MSNWeatherPixmapNP(Renderer):
    
    def __init__(self):
        Renderer.__init__(self)
        self.pixdelay = int((randint(70,150) + randint(70,150)) / 2)
        self.picsIcons = []
        self.picsIconsCount = 0
        self.slideIcon = 0
        self.lastPic = ''
        self.height = 1
        self.width = 1
        self.timer = eTimer()
        self.timer.callback.append(self.timerEvent)
        self.pngAnimPath='/usr/share/enigma2/animatedWeatherIcons'
        if config.plugins.WeatherPlugin.ScalePicType.value == "self.instance.setScale":
            self.ePicLoadScale = False
        else:
            self.ePicLoadScale = True
        self.picload = ePicLoad()
        #self.picload.PictureData.get().append(self.paintIconPixmapCB)
        self.DEBUG('__init__ pixdelay=%s' % self.pixdelay)

    GUI_WIDGET = ePixmap

    def EXCEPTIONDEBUG(self, myFUNC = '' , myText = '' ):
        from Plugins.Extensions.MSNweather.debug import printDEBUG
        printDEBUG( myFUNC , myText , 'MSNWeatherPixmapRenderer.log' )
            
    def DEBUG(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugMSNWeatherPixmapRenderer.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText , 'MSNWeatherPixmapRenderer.log' )
    
    def applySkin(self, desktop, parent):
        self.DEBUG('applySkin >>>')
        attribs = self.skinAttributes[:]
        for attrib, value in self.skinAttributes:
            if attrib == "size":
                self.width = int(value.split(',')[0])
                self.height = int(value.split(',')[1])
            elif attrib == 'path':
                self.pngAnimPath = value
                attribs.remove((attrib, value))
        self.DEBUG("\t pngAnimPath set to '%s'" % self.pngAnimPath)

        try:
            self._scaleSize = eSize(self.width, self.height)
            sc = AVSwitch().getFramebufferScale()
            self._aspectRatio = eSize(sc[0], sc[1])
            self.picload.setPara((self._scaleSize.width(), self._scaleSize.height(), sc[0], sc[1], True, 2, '#ff000000')) 
        except Exception as e:
            self.DEBUG('setSize exception %s' % str(e))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent) 

    def doSuspend(self, suspended):
        if suspended:
            self.timer.stop()
            self.changed((self.CHANGED_CLEAR,))
        else:
            if self.picsIconsCount > 0: 
                self.timer.start(self.pixdelay, True)
            self.changed((self.CHANGED_DEFAULT,))
            
    def changed(self, what):
        if what[0] != self.CHANGED_CLEAR:
            if self.instance:
                if self.ePicLoadScale == False:
                    self.instance.setScale(1)
                self.updateIcon(self.source.iconfilename)
                
    def doAnimation(self, pngAnimPath):
        if config.plugins.WeatherPlugin.IconsType.value == 'animIcons' and os.path.exists(pngAnimPath):
            self.DEBUG('doAnimation(pngAnimPath=%s) returns True' % pngAnimPath)
            return True
        else:
            self.DEBUG('doAnimation(pngAnimPath=%s) returns False' % pngAnimPath)
            return False
                
    def updateIcon(self, filename):
        self.DEBUG('updateIcon(%s) lastPic= %s' % (filename,self.lastPic))
        if self.lastPic != filename and filename[-4:].lower() in ('.png','.jpg'):
            self.lastPic = filename
            IconName = os.path.basename(self.lastPic)
            pngAnimPath = os.path.join(self.pngAnimPath, IconName)[:-4]
            self.DEBUG('updateIcon pngAnimPath=%s' % pngAnimPath)
            if self.doAnimation(pngAnimPath):
                reverseSlides = False
                self.DEBUG('updateIcon pngAnimPath exists')
                if os.path.exists(os.path.join(pngAnimPath,'.ctrl')):
                    with open(os.path.join(pngAnimPath,'.ctrl')) as cf:
                        for line in cf:
                            lineArray = line.strip().split('=')
                            if lineArray[0] == 'delay':
                                self.pixdelay = int(lineArray[1])
                            if lineArray[0] == 'revert' and lineArray[1] == 'True':
                                reverseSlides = True
                        cf.close()
                      
                self.slideIcon = 0
                self.picsIcons = []
                pngfiles = [f for f in os.listdir(pngAnimPath) if (os.path.isfile(os.path.join(pngAnimPath, f)) and f.endswith(".png"))]
                pngfiles.sort()
                if reverseSlides:
                    pngfiles.reverse()
                for x in pngfiles:
                    self.picsIcons.append(LoadPixmap(os.path.join(pngAnimPath, x)))
                self.picsIconsCount = len(self.picsIcons)
                if self.picsIconsCount > 0: 
                    self.timer.start(self.pixdelay, True)
                    self.DEBUG('updateIcon picsIconsCount=%s' % self.picsIconsCount)
            else:
                self.instance.setPixmap(LoadPixmap(path=self.lastPic))

    def timerEvent(self):
        self.timer.stop()
        self.slideIcon += 1
        if self.slideIcon >= self.picsIconsCount:
                self.slideIcon = 0
        try:
            self.instance.setPixmap(self.picsIcons[self.slideIcon])
            self.timer.start(self.pixdelay, True)
        except Exception as e:
            self.EXCEPTIONDEBUG('timerEvent exception %s' % str(e))
