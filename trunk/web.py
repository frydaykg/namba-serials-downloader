import urllib
import urllib2

def GetSerialPage(link):
	data=urllib2.urlopen(link).read().decode('utf8')
	return data

def GetBinaryDataChunk(link,chunksize):
	r=urllib2.urlopen(link)
	while True:
		chunk=r.read(chunksize)
		if len(chunk)!=0:
			yield chunk
		else:
			break

def GetFileSize(link):
	r=urllib2.urlopen(link)
	return int(r.info()['Content-Length'])

