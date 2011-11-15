import re
from common import *

def ParseAvailableSeasonsAndEpisodes(data):	
	pattern=GetSetting('seasonPattern')
	iter=re.finditer(pattern,data)

	ex=[]
	rex=[]
	result={}
	for i in iter:
		ex.append(i.group())
		rex.append(i.groups(1)[0].encode('utf8'))
		result[i.groups(1)[0].encode('utf8')]={}
	ex.append(data[-20:-1])

	pattern=GetSetting('episodePattern')
	for i in range(len(ex)-1):
		s=data[data.find(ex[i]):data.find(ex[i+1])]
		iter=re.finditer(pattern,s)
		for j in iter:
			result[rex[i]][j.groups(1)[1].encode('utf8')]='http://serials.namba.kg'+j.groups(1)[0].encode('utf8')
			
	return result

def ParseEpisodeMagicNumber(data):
	pattern=GetSetting('episodeMagicNumberPattern')
	r=re.search(pattern,data)
	return r.groups(1)[0]

def ParseSerialName(data):
	pattern=GetSetting('serialNamePattern')
	r=re.search(pattern,data)
	return r.groups(1)[0]

"""
Parse application arguments
------------------------------------------------------------------------
"""
def GetLinkFromArgv(argv):
	if '-l' in argv:
		
		linkIndex=argv.index('-l')
		if linkIndex>=0 and linkIndex<len(argv)-1:
			link=argv[linkIndex+1]
		else:
			raise Exception('Incorrect link parametr')
	else:
		raise Exception('No link parametr')
	return link

def GetSeasonsFromArgv(argv):
	seasons=[]
	if '-s' in argv:
		seasonIndex=argv.index('-s')
		if seasonIndex>=0 and seasonIndex<len(argv)-1:
			while seasonIndex+1<len(argv) and argv[seasonIndex+1].isdigit():
				seasons.append(argv[seasonIndex+1])
				seasonIndex+=1
	return seasons

def GetEpisodesFromArgv(argv):
	episodes=[]
	if '-e' in argv:
		episodeIndex=argv.index('-e')
		if episodeIndex>=0 and episodeIndex<len(argv)-1:
			while episodeIndex+1<len(argv) and argv[episodeIndex+1].isdigit():
				episodes.append(argv[episodeIndex+1])
				episodeIndex+=1
	return episodes
