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




def main():
	argv=sys.argv[1:]

	
	link=GetLinkFromArgv(argv)
	pageData=GetSerialPage(link)
	seasons=sorted(GetUniqueList(GetSeasonsFromArgv(argv)))
	episodes=sorted(GetUniqueList(GetEpisodesFromArgv(argv)))
	av=ParseAvailableSeasonsAndEpisodes(pageData)
	

	if not seasons:
		pass
	else:
		unavSeasons=GetUnavailableSeasons(seasons,av.keys())
		if unavSeasons:
			print 'Seasons ' + str(unavSeasons).replace('\'','').replace(']','').replace('[','') + ' unvailable. Continue? (y/n)'
			answer=raw_input()
			if answer!='y':
				exit()
			else:
				temp={}
				for i in seasons:
					if i in av.keys():						
						temp[i]=av[i]
				seasons=temp


	print 'Seasons ' + str(seasons.keys()).replace('\'','').replace(']','').replace('[','') + ' will be proceed!'
	print 'Finish!'



if __name__== '__main__':
	main()


