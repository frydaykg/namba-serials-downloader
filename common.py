from  xml.dom.minidom import *

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
