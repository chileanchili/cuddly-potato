# -*- coding: utf-8 -*-
#import sys
#sysVersion = sys.version_info [0] == 2    # check for Python 2 or 3 for the correct unicode function
# def main (main_parameters):
#    global globalVar
#    number1 = ord (main_parameters [-1])
#    text1 = main_parameters [:-1]
#    if sysVersion: #Python 2
#        sysV_check = unicode () .join ([unichr (ord (char) - 2048 - (text5 + number1) % 7) for text5, char in enumerate (text1)])
#    else: #Python 3
#        sysV_check = str () .join ([chr (ord (char) - 2048 - (text5 + number1) % 7) for text5, char in enumerate (text1)])
#    return eval (sysV_check)
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import os,itertools,re,sys,urlresolver
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
# Watchseries - originally by Mucky Duck (03/2015) - updated by koreanwarrior (12/2017)
strAddonID = xbmcaddon.Addon().getAddonInfo('id')
MDWS = Addon(strAddonID, sys.argv)
strAddonName = MDWS.get_name()
mdwsPath = MDWS.get_path()
md = md(strAddonID, sys.argv)
bEnableMeta = MDWS.get_setting('enable_meta')
bEnableFavs = MDWS.get_setting('enable_favs')
bEnableAddonSettings = MDWS.get_setting('add_set')
bEnableMetaSettings = MDWS.get_setting('enable_meta_set')
bEnableUrlResolverSettings = MDWS.get_setting('enable_resolver_set')
strArtDir = md.get_art() # Returns the full path to the addon's art directory, equal to:
# strArtDir = os.path.join(self.addon.get_path(), 'resources', 'art', '')
hIcon = MDWS.get_icon()
hFanart = MDWS.get_fanart()
strBaseURL =  MDWS.get_setting('base_url') # currently 'http://itswatchseries.to'
reload(sys)
sys.setdefaultencoding('utf-8')
def MainMenu(): # Building main menu
	md.addDir({'mode':'4', 'name':'[B][COLOR yellow]A-Z[/COLOR][/B]', 'url':strBaseURL+'/letters/A'}, fan_art={'icon':strArtDir+'mdws.png'})
	md.addDir({'mode':'search', 'name':'[B][COLOR yellow]Search[/COLOR][/B]', 'url':'url'}, fan_art={'icon':strArtDir+'mdws.png'})
	md.addDir({'mode':'6', 'name':'[B][COLOR yellow]TV Schedule[/COLOR][/B]', 'url':strBaseURL+'/tvschedule'}, fan_art={'icon':strArtDir+'mdws.png'})
	if bEnableFavs == 'true': # Favourites enabled?
		md.addDir({'mode': 'fetch_favs', 'name':'[COLOR yellow][B]My Favourites[/B][/COLOR]', 'url':'url'})
	md.addDir({'mode':'7', 'name':'[B][COLOR yellow]TV Shows Years[/COLOR][/B]', 'url':strBaseURL+'/years/2017'}, fan_art={'icon':strArtDir+'mdws.png'})
	md.addDir({'mode':'5', 'name':'[B][COLOR yellow]TV Shows Genres[/COLOR][/B]', 'url':strBaseURL+'/genres/action'}, fan_art={'icon':strArtDir+'mdws.png'})
	md.addDir({'mode':'1', 'name':'[B][COLOR yellow]Newest Episodes Added[/COLOR][/B]', 'url':strBaseURL+'/latest', 'content':'episodes'}, fan_art={'icon':strArtDir+'mdws.png'})
	md.addDir({'mode':'1', 'name':"[B][COLOR yellow]This Week's Popular Episodes[/COLOR][/B]", 'url':strBaseURL+'/new', 'content':'episodes'}, fan_art={'icon':strArtDir+'mdws.png'})
	if bEnableUrlResolverSettings == 'true': # UrlResolver-Settings enabled?
		md.addDir({'mode':'urlresolver_settings', 'name':'[COLOR yellow][B]UrlResolver Settings[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
	if bEnableAddonSettings == 'true': # Addon-Settings enabled?
		md.addDir({'mode':'addon_settings', 'name':'[COLOR yellow][B]Add-on Settings[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
	if bEnableMeta == 'true':
		if bEnableMetaSettings == 'true': # Meta-Settings menu enabled?
			md.addDir({'mode':'meta_settings', 'name':'[COLOR yellow][B]Meta Settings[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
	funcMDLibraryCheck()
	setView(strAddonID, 'files', 'menu-view')
	MDWS.end_of_directory()
def function2(url,title,modeid,content):
	link = open_url(url).content
	if modeid == '6':
		link = md.regex_get_all(link, title, '<ul class="tabs">')
	strRegex1 = md.regex_get_all(str(link), '"listings">', '</ul>')
	strRegex2 = md.regex_get_all(str(strRegex1), '<li', '</li')
	items = len(strRegex2)
	for a in strRegex2:
		name = md.regex_from_to(a, 'title="', '"').replace("\\'","'")
		name = MDWS.unescape(name)
		url = md.regex_from_to(a, 'href="', '"')
		if 'javascript:' in url:
                        url = md.regex_get_all(a, 'href="', '"', True)[1]
                if 'javascript:' in url:
                        url = md.regex_get_all(a, 'href="', '"', True)[2]
		strRegex3 = md.regex_from_to(a, 'src="', '"')
                if not strRegex3:
                        strRegex3 = strArtDir+'mdws.png'
		if strBaseURL not in url:
			url = strBaseURL + url
		if content == 'episodes':
			info = name.split('- Season')
			title = info[0].strip()
			try:
                                sep = md.regex_from_to(a, '<br/>', '<br/>')
                                episode = sep.split('Episode')[1]
                                season = sep.split('Episode')[0]
                        except:
                                season = info[1].split('Episode')[0]
                                episode = info[1].split('Episode')[1].split('-')[0]
                        md.remove_punctuation(title)
                        md.addDir({'mode':'8','name':'[B][COLOR white]%s[/COLOR][COLOR yellow][I] - Season %s[/I][/COLOR][/B]' %(title,info[1]),
				   'url':url, 'content':content, 'title':title, 'season':season, 'iconimage':strRegex3,
                                   'episode':episode}, {'sorttitle':title, 'season':season, 'episode':episode},
                                  fan_art={'icon':strRegex3}, item_count=items)
		else:
			if modeid == '4':
				infolabels = {}
			else:
				infolabels = {'sorttitle':name}
			md.remove_punctuation(name)
			md.addDir({'mode':'2', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url,
				   'title':title, 'iconimage':strRegex3, 'content':content},
				  infolabels, fan_art={'icon':strRegex3}, item_count=items)
	try:
                rePatternObject = re.compile('<li ><a href="([^"]+)">Next Page</a></li>').findall(link)[0]
                md.addDir({'mode':'1','name':'[COLOR yellow][B][I]>>Next Page>>>[/I][/B][/COLOR]', 'url':rePatternObject,
			   'title':title, 'content':content, 'mode_id':modeid}, fan_art={'icon':strArtDir+'mdws.png'})
        except:pass
	if content == 'tvshows':
		setView(strAddonID, 'tvshows', 'show-view')
	elif content == 'episodes':
		setView(strAddonID,'episodes', 'epi-view')
	MDWS.end_of_directory()
def function3(url,title):
	link = open_url(url).content
	match = re.compile('<a href="([^"]+)" itemprop="url"><span itemprop="name">([^<>]*)</span>').findall(link)
	items = len(match)
	try:
		strRegex3 = re.compile('<meta property="og:image" content="([^"]+)" />').findall(link)[0]
	except:
		strRegex3 = strArtDir+'mdws.png'
	try:
		year = re.compile('href=.*?/years/.*?>([^<>]*)</a></span>').findall(link)[0]
	except:
		year = ''
	md.remove_punctuation(title)
	for url,name in match:
		md.addDir({'mode':'3','name':'[COLOR yellow][B][I]%s[/I][/B][/COLOR]' %name, 'url':url,
			   'title':title, 'iconimage':strRegex3, 'content':'tvshows', 'season':name},
			  {'sorttitle':title, 'year':year}, fan_art={'icon':strRegex3}, item_count=items)
	setView(strAddonID, 'tvshows', 'show-view')
	MDWS.end_of_directory()
def funcMDLibraryCheck():
	link = open_url('https://pastebin.com/raw/Cf4C3uH1').content # str(link) should return 'version = "1.3.5"'
	version = re.findall('version = "([^"]+)"', str(link), re.I|re.DOTALL)[0]
	with open(xbmc.translatePath('special://home/addons/script.module.muckys.common/addon.xml'), 'r+') as f:
		strFile = f.read()
		if re.search('version="%s"' %version, strFile):
			MDWS.log('Version Check OK')
		else:
			strText1 = 'Wrong Version Of Muckys Common Module'
			strText2 = 'Please Install Correct Version From The Repo'
			strText3 = '@[COLOR red]http://muckys.mediaportal4kodi.ml[/COLOR]'
			MDWS.show_ok_dialog([strText1, strText2, strText3], strAddonName)
			xbmc.executebuiltin('XBMC.Container.Update(path,replace)')
			xbmc.executebuiltin('XBMC.ActivateWindow(Home)')
def function5(url,iconimage,title,season,infolabels):
	if iconimage is None:
		fan_art = {'icon':strArtDir+'mdws.png'}
	else:
		fan_art = {'icon':iconimage}
	try:
		code = re.compile("'imdb_id': u'([^']+)'").findall(infolabels)[0]
	except:
		code = ''
	link = open_url(url).content
	strRegex2 = md.regex_get_all(link, '<li id="episode_', '</li>')
	items = len(strRegex2)
	for a in strRegex2:
		name = md.regex_from_to(a, '"name">', '<')
		name = MDWS.unescape(name)
		date = md.regex_from_to(a, '"datepublished">', '<')
		links = md.regex_from_to(a, '<b>', '<')
		url = md.regex_from_to(a, 'href="', '"')
		episode = name.split('&')[0]
		name = name.replace('&amp;','&').replace('&nbsp;',' ')
		md.addDir({'mode':'8', 'name':'[B][COLOR white]%s[/COLOR][/B][B][I][COLOR yellow]%s%s[/COLOR][/I][/B]' %(name,links,date),
			   'url':url, 'iconimage':iconimage, 'content':'episodes'},
			  {'sorttitle':title, 'code':code, 'season':season, 'episode':episode},
			  fan_art, item_count=items)
	setView(strAddonID,'episodes', 'epi-view')
	MDWS.end_of_directory()
def function6(url):
	link = open_url(url).content
	strRegex1 = md.regex_get_all(link, '"pagination">', '</ul>')
	strRegex2 = md.regex_get_all(str(strRegex1), '<li', '</li')
	items = len(strRegex2)
	for a in strRegex2:
		name = md.regex_from_to(a, 'href=.*?>', '<')
		url = md.regex_from_to(a, 'href="', '"')
		if strBaseURL not in url:
			url = strBaseURL + url
		if 'NEW' not in name:
			md.addDir({'mode':'1','name':'[COLOR yellow][B][I]%s[/I][/B][/COLOR]' %name,
				   'url':url, 'mode_id':'4', 'content':'tvshows'},
				  fan_art={'icon':strArtDir+'mdws.png'}, item_count=items)
	setView(strAddonID, 'files', 'menu-view')
	MDWS.end_of_directory()
def function7(url):
	link = open_url(url).content
	strRegex1 = md.regex_get_all(link, '"pagination" style', '</ul>')
	strRegex2 = md.regex_get_all(str(strRegex1), '<li', '</li')
	items = len(strRegex2)
	for a in strRegex2:
		name = md.regex_from_to(a, 'href=.*?>', '<')
		url = md.regex_from_to(a, 'href="', '"')
		url = url + '/1/0/0'
		if strBaseURL not in url:
			url = strBaseURL + url
		md.addDir({'mode':'1','name':'[COLOR yellow][B][I]%s[/I][/B][/COLOR]' %name,
                           'url':url, 'content':'tvshows'}, fan_art={'icon':strArtDir+'mdws.png'}, item_count=items)
	setView(strAddonID, 'files', 'menu-view')
	MDWS.end_of_directory()
def function8(url):
        year = []
        ukwnParameter = []
        link = open_url(url).content
	strRegex1 = md.regex_get_all(link, '"pagination" style', '</ul>')
	strRegex2 = md.regex_get_all(str(strRegex1), '<li', '</li')
	for a in strRegex2:
		name = md.regex_from_to(a, 'href=.*?>', '<')
		url = md.regex_from_to(a, 'href="', '"')
		if strBaseURL not in url:
			url = strBaseURL + url
		year.append(name)
		ukwnParameter.append(url)
	match = re.compile('value="([^"]+)".*?>([^<>]*)</option>').findall(link)
	for loop1,loop2 in match:
                if '/years/' in loop1:
                        year.append(loop2)
                        ukwnParameter.append(loop1)
        items = len(year)
        for dirPart,mdwsURL in itertools.izip_longest(year,ukwnParameter):
                md.addDir({'mode':'1','name':'[COLOR yellow][B][I]%s[/I][/B][/COLOR]' %dirPart,
                           'url':mdwsURL, 'content':'tvshows'}, fan_art={'icon':strArtDir+'mdws.png'}, item_count=items)
	setView(strAddonID, 'files', 'menu-view')
	MDWS.end_of_directory()
def function9(url):
	link = open_url(url).content
	match = re.compile('<div style="width: 153px;">([^<>]*)<').findall(link)
	items = len(match)
	for name in match:
		md.addDir({'mode':'1','name':'[COLOR yellow][B][I]%s[/I][/B][/COLOR]' %name,
			   'url':url, 'mode_id':'6', 'content':'episodes', 'title':name},
			  fan_art={'icon':strArtDir+'mdws.png'}, item_count=items)
	setView(strAddonID, 'files', 'menu-view')
	MDWS.end_of_directory()
def function10(content, query):
        if content is None:
                content = 'tvshows'
	try:
		if query:
			search = query.replace(' ', '%20')
		else:
			search = md.search('%20')
			if search == '':
				md.notification('[COLOR gold][B]EMPTY QUERY[/B][/COLOR],Aborting search',hIcon)
				return
			else:
				pass
		url = '%s/search/%s' %(strBaseURL,search)
                link = open_url(url).content
                strRegex2 = md.regex_get_all(link, 'ih-item', 'Add Link')
                items = len(strRegex2)
                for a in strRegex2:
                        name = md.regex_from_to(a, '<strong>', '</').replace("\\'","'")
                        name = MDWS.unescape(name)
                        url = md.regex_get_all(a, 'href="', '"', bTrue=True)[2]
                        strRegex3 = md.regex_from_to(a, 'src="', '"')
                        if not strRegex3:
                                strRegex3 = strArtDir+'mdws.png'
                        if strBaseURL not in url:
                                url = strBaseURL + url
                        md.remove_punctuation(name)
                        md.addDir({'mode':'2', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url,
                                   'title':name, 'iconimage':strRegex3, 'content':content},
                                  {'sorttitle':name}, fan_art={'icon':strRegex3}, item_count=items)
                setView(strAddonID, 'tvshows', 'show-view')
                MDWS.end_of_directory()
        except:
		md.notification('[COLOR gold][B]Sorry No Results[/B][/COLOR]',hIcon)
def FindURLs(url,iconimage,title,season,episode,infolabels): # Finds the URLs of the different hosters
	if iconimage is None or iconimage == '':
		hFanart = {'icon':strArtDir+'mdws.png'}
	else:
		hFanart = {'icon':iconimage}
	link = open_url(url).content
	# cale.html gets passed a code. This code is actually the link to the hoster, and is just "encrypted" with base64-encoding
	match = re.compile('cale\\.html\\?r=(.*?)" class="watchlink" title="([^"]+)"').findall(link) # changed from "buttonlink" to "watchlink" (Dec1,2017)
	items = len(match)
	for url,name in match: # loop through the list of all hosters
		url = url.decode('base64') # and decode the "encrypted" URL
		if urlresolver.HostedMediaFile(url): # Check if URLResolver supports this hoster, and if yes/true to add it to the list
			md.addDir({'mode':'9','name':'[COLOR yellow][B][I]%s[/I][/B][/COLOR]' %name, 'url':url},
				  fan_art=hFanart, is_folder=False, item_count=items)
	setView(strAddonID, 'files', 'menu-view')
	MDWS.end_of_directory()
def function12(url,name,fan_art,infolabels):
	try:
		mdwsURL = urlresolver.resolve(url) # Resolve the URL of the media file (NOT the hoster!)
		md.resolved(mdwsURL, name, fan_art, infolabels)
	except:
		md.notification('[COLOR gold][B]SORRY LINK DOWN PLEASE TRY ANOTHER ONE[/B][/COLOR]', hIcon)
	MDWS.end_of_directory()
# md.check_source() # check_source checks if Mucky repo is installed - we don't want that!
mode = md.args['mode']
url = md.args.get('url', None)
name = md.args.get('name', None)
query = md.args.get('query', None)
title = md.args.get('title', None)
year = md.args.get('year', None)
season = md.args.get('season', None)
episode = md.args.get('episode' ,None)
infolabels = md.args.get('infolabels', None)
content = md.args.get('content', None)
modeid = md.args.get('mode_id', None)
iconimage = md.args.get('iconimage', None)
fan_art = md.args.get('fan_art', None)
is_folder = md.args.get('is_folder', True)

if mode is None or url is None or len(url)<1:
	MainMenu()
elif mode == '1':
	function2(url,title,modeid,content)
elif mode == '2':
	function3(url,title)
elif mode == '3':
	function5(url,iconimage,title,season,infolabels)
elif mode == '4':
	function6(url)
elif mode == '5':
	function7(url)
elif mode == '6':
	function9(url)
elif mode == '7':
	function8(url)
elif mode == '8':
	FindURLs(url,iconimage,title,season,episode,infolabels)
elif mode == '9':
	function12(url,name,fan_art,infolabels)
elif mode == 'search':
	function10(content, query)
elif mode == 'addon_search':
	md.addon_search(content,query,fan_art,infolabels)
elif mode == 'add_remove_fav':
	md.add_remove_fav(name,url,infolabels,fan_art,
			  content,modeid,is_folder)
elif mode == 'fetch_favs':
	md.fetch_favs(strBaseURL)
elif mode == 'addon_settings':
	MDWS.show_settings()
elif mode == 'meta_settings':
	import metahandler
	metahandler.display_settings()
elif mode == 'urlresolver_settings':
	urlresolver.display_settings()
MDWS.end_of_directory()