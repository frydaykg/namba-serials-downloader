import urllib
import urllib2

def GetSerialPage(link):
	data=urllib2.urlopen(link).read().decode('utf8')
	return data
