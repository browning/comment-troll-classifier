import urllib
import urllib2
from xml.dom import minidom

data = None
headers = {   
    'GData-Version' : 2
}

spamfile = open('spam', 'w')
notspamfile = open('notspam', 'w')

# get list of most popular videos
url = 'http://gdata.youtube.com/feeds/api/videos?max-results=50&orderby=viewCount'
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
xmldata = response.read()
videos = minidom.parseString(xmldata)
video_entries = videos.getElementsByTagName("gd:feedLink")
for entry in video_entries:
  link = entry.attributes["href"].value
  print "processing: " + link
# get comments
  start = 1
  while start<=1000:
    url = link + '?max-results=50&start-index=' + str(start)

    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    xmldata = response.read()
    comments = minidom.parseString(xmldata)

    entries = comments.getElementsByTagName("entry")

    for entry in entries:
      content = entry.getElementsByTagName("content")
      spam = entry.getElementsByTagName("yt:spam")
      if len(spam) > 0:
        spamfile.write(content[0].firstChild.nodeValue.encode('utf8'))
        spamfile.write('\nbbSEP\n')
      else:
        notspamfile.write(content[0].firstChild.nodeValue.encode('utf8'))
        notspamfile.write('\nbbSEP\n')
    start += 50

spam.close()
notspam.close()