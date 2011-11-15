from  xml.dom.minidom import *
import os

def GetSetting(name):
	doc=parse('settings.xml')	
	text=doc.getElementsByTagName(name)[0].childNodes[0].wholeText
	text=text.encode('utf8')
	return str.strip(text).decode('utf8')

def GetUniqueList(L):
	found = set()
	for i in L:
		if i not in found:
			found.add(i)
	return list(found)

def CreateSerialDirectories(savePath,name,seasons):
	root=os.path.normpath(savePath+'/'+name)
	if not os.path.exists(root):
		os.makedirs(root)
	for i in seasons:
		p=os.path.normpath(root+'/'+i)
		if not os.path.exists(p):
			os.makedirs(p)
