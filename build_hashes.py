import sys
import json

spamtokens = {}
notspamtokens = {}
probabilities = {}

spam_count = 0
notspam_count = 0

print 'building dictionaries...'
f = open('spam', 'r')
for line in f:
  tokens = line.split()
  for token in tokens:
    if token == "bbSEP":
      spam_count = spam_count + 1
      continue
    token = token.lower()
    if token in spamtokens:
      spamtokens[token] = spamtokens[token] + 1
    else:
      spamtokens[token] = 1

f.close()

f = open('notspam', 'r')
for line in f:
  tokens = line.split()
  for token in tokens:
    if token == "bbSEP":
      notspam_count = notspam_count + 1
    token = token.lower()
    if token in notspamtokens:
      notspamtokens[token] = notspamtokens[token] + 1
    else:
      notspamtokens[token] = 1

f.close()


for k in spamtokens:
  num_in_spam = spamtokens[k]
  if k in notspamtokens:
    num_in_notspam = notspamtokens[k] * 2
  else:
    num_in_notspam = 0
  p = ( num_in_spam / float(spam_count)) / ( (num_in_spam / float(spam_count)) + (num_in_notspam / float(notspam_count)))
  probabilities[k] = p

for k in notspamtokens:
  if not (k in spamtokens):
    probabilities[k] = 0

print "saving dictionaries as json..."
# save the hashes as json
f = open('spam.dict.json', 'w')
f.write(json.dumps(spamtokens))
f.close()

f = open('notspam.dict.json', 'w')
f.write(json.dumps(notspamtokens))
f.close()

f = open('probabilities.dict.json', 'w')
f.write(json.dumps(probabilities))
f.close()