import urllib
import urllib2
import re
import os
import sys
from parser import *
from web import *

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

def main():
	argv=sys.argv[1:]

	
	link=GetLinkFromArgv(argv)
	pageData=GetSerialPage(link)
	seasons=sorted(GetUniqueList(GetSeasonsFromArgv(argv)))
	episodes=sorted(GetUniqueList(GetEpisodesFromArgv(argv)))
	av=ParseAvailableSeasonsAndEpisodes(pageData)
	req=GetRequested(seasons,episodes)
	
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
		else:
			temp={}
			for i in seasons:
				if i in av.keys():						
					temp[i]=av[i]
			seasons=temp

	print 'Finish!'



if __name__== '__main__':
	main()


