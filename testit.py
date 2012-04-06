import urllib
import urllib2
import subprocess
from xml.dom import minidom

data = None
headers = {   
    'GData-Version' : 2
}
num_spam = 0
num_notspam = 0 
num_marked_as_spam = 0
num_marked_as_notspam = 0
false_positives = 0
false_negatives = 0

# get list of most popular videos
url = 'http://gdata.youtube.com/feeds/api/videos?max-results=2&start-index=50&orderby=viewCount'
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

      comment_string = content[0].firstChild.nodeValue.encode('utf8')
      print "checking: " + comment_string
      # get content score
      p = subprocess.Popen("./spamcheck.py", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
      p.stdin.write(comment_string)
      p.stdin.close()
      score = float(p.stdout.readline())
      p.kill()
      print "score: " + str(score)
      if score >= 0.9:
        num_marked_as_spam = num_marked_as_spam + 1
      else:
        num_marked_as_notspam = num_marked_as_notspam + 1

      spam = entry.getElementsByTagName("yt:spam")
      if len(spam) > 0:
        if score < 0.9:
          false_negatives = false_negatives + 1
        num_spam = num_spam + 1
      else:
        if score >= 0.9:
          false_positives = false_positives + 1
        num_notspam = num_notspam + 1
        
    start += 50

print "total comments: " +  str(num_spam + num_notspam)
print "Spams: " + str(num_spam)
print "Not spams: " + str(num_notspam)
print "Marked as spam: " + str(num_marked_as_spam)
print "Marked as notspam: " + str(num_marked_as_notspam)
print "False positives: " + str(false_positives)
print "False negatives: " + str(false_negatives)
