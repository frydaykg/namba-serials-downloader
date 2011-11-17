import urllib
import urllib2
import re
import os
import sys
from parser import *
from web import *
import json

def GetUnavailableSeasons(seasons,avSeasons):
	if not seasons:
		return None
	else:
		intersectSeasons=sorted(list(set(seasons) & set(avSeasons)))
		if intersectSeasons!=seasons:
			return sorted(list(set(seasons) ^ set(intersectSeasons)))

def GetRequested(seasons,episodes):
	result={}
	if not seasons:
		result['all']={}
	elif not episodes:
		for i in seasons:
			result[i]={'all':''}
	else:
		result[seasons[0]]={}
		for i in episodes:
			result[seasons[0]][i]=''
	return result


def GetProcAndDiff(req,av):
	notAv={}
	proc={}
	for i in req.keys():
		if i=='all':
			proc=av
		elif i not in av.keys():
			notAv[i]=req[i]
		else:
			for j in req[i]:
				if j=='all':
					proc[i]=av[i]
				elif j not in av[i].keys():
					if i not in notAv.keys():
						notAv[i]={}
					notAv[i][j]=req[i][j]
				else:
					if i not in proc.keys():
						proc[i]={}
					proc[i][j]=av[i][j]
	return (proc,notAv)

def GetDownloadLink(link):
	data=GetSerialPage(link)
	number=ParseEpisodeMagicNumber(data)
	jsonLink='http://video.namba.kg/json/?action=video&id='+number
	data=GetSerialPage(jsonLink)
	jsonDict=json.loads(data)
	return jsonDict['video']['download']['flv']

def DownloadAndSaveFile(filename, link):	
	chunksize=int(
	GetSetting('chunksize'))
	f=open(filename,'wb')
	filesize=GetFileSize(link)
	cursize=0
	chunks=GetBinaryDataChunk(link,chunksize)
	
	for data in chunks:
		cursize+=len(data)
		percent=cursize*100.0/filesize
		sys.stdout.write("%s (%0.2f%%)\r" % (filename, percent))
		f.write(data)
	print
	f.close()


def main():
	argv=sys.argv[1:]

	
	link=GetLinkFromArgv(argv)
	pageData=GetSerialPage(link)
	seasons=GetUniqueList(GetSeasonsFromArgv(argv))
	episodes=GetUniqueList(GetEpisodesFromArgv(argv))
	av=ParseAvailableSeasonsAndEpisodes(pageData)
	serialName=ParseSerialName(pageData)
	req=GetRequested(seasons,episodes)
	direct=GetDirectoryFromArgv(argv)
	
	(proc,notAv)=GetProcAndDiff(req,av)
	
	if notAv:
		if len(notAv)>1:			
			print 'Seasons ' + str(notAv.keys()).replace('\'','').replace(']','').replace('[','') + ' unvailable. Continue? (y/n)'
		elif 'all' in notAv[notAv.keys()[0]].keys():
			print 'Season ' + str(notAv.keys()).replace('\'','').replace(']','').replace('[','') + ' unvailable. Continue? (y/n)'
		elif len(notAv[notAv.keys()[0]])==1:
			print 'Episode ' + str(notAv[notAv.keys()[0]].keys()).replace('\'','').replace(']','').replace('[','') + ' unvailable. Continue? (y/n)'
		else:
			print 'Episodes ' + str(notAv[notAv.keys()[0]].keys()).replace('\'','').replace(']','').replace('[','') + ' unvailable. Continue? (y/n)'
		answer=raw_input()
		if answer!='y':
			exit()

	procSeasons=sorted(proc.keys())
	CreateSerialDirectories(direct,serialName,procSeasons)
	
	for season in procSeasons:
		procEpisodes=sorted(proc[season].keys())
		for episode in procEpisodes:
			episodeLink=proc[season][episode]
			downloadData=GetDownloadLink(episodeLink)
			filename='%s s%s.e%s.flv'%(serialName,season,episode)
			filename=os.path.normpath(direct+'/'+serialName+'/'+season+'/'+filename)
			DownloadAndSaveFile(filename,downloadData)
			
	print 'Finish!'



if __name__== '__main__':
	main()


