# -*- coding: utf-8 -*-
from version import Version
UserSkinInfo='@j00zek %s' % Version

#stale
PluginName = 'UserSkin'
PluginGroup = 'Extensions'

#Plugin Paths
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, SCOPE_PLUGINS, SCOPE_SKIN
PluginFolder = PluginName
PluginPath = resolveFilename(SCOPE_PLUGINS, '%s/%s/' %(PluginGroup,PluginFolder))

#Current skin
from Components.config import *
SkinPath = resolveFilename(SCOPE_CURRENT_SKIN, '')
if not SkinPath.endswith('/'):
    SkinPath = SkinPath + '/'
CurrentSkinName=config.skin.primary_skin.value.replace('skin.xml', '').replace('/', '')

#translation
PluginLanguageDomain = "plugin-" + PluginName
PluginLanguagePath = resolveFilename(SCOPE_PLUGINS, '%s/%s/locale' % (PluginGroup,PluginFolder))

from Components.Language import language
currLang = language.getLanguage()[:2] #used for descriptions keep GUI language in 'pl|en' format

#DEBUG
myDEBUG=True
myDEBUGfile = '/tmp/%s.log' % PluginName

def getPixmapPath(Pixmap=None):
    from os import path
    if Pixmap is not None:
        #print "!!!!!!!!!!!!!!!!!!!!!!!!!",resolveFilename(SCOPE_SKIN, 'icons/%s' % Pixmap)
        if path.exists("%sUserSkinpics/%s" % (SkinPath,Pixmap)):
            return "%sUserSkinpics/%s" % (SkinPath,Pixmap)
        elif path.exists("%sicons/%s" % (SkinPath,Pixmap)):
            return "%sicons/%s" % (SkinPath,Pixmap)
        elif path.exists(resolveFilename(SCOPE_SKIN, 'skin_default/vfd_icons/%s' % Pixmap)):
            return resolveFilename(SCOPE_SKIN, 'skin_default/vfd_icons/%s' % Pixmap)
        elif path.exists(resolveFilename(SCOPE_SKIN, 'skin_default/icons/%s' % Pixmap)):
            return resolveFilename(SCOPE_SKIN, 'skin_default/icons/%s' % Pixmap)
        else:
            return "%spic/%s" % (PluginPath,Pixmap)

