#!/usr/bin/python

import sys
import json

def sort_func(x):
  return abs(token_probs[x] - 0.5)

f = open('probabilities.dict.json', 'r')
json_probs = f.read()
probabilities = json.loads(json_probs)
f.close()


comment = sys.stdin.read()

token_probs = {}
tokens = comment.split()
for token in tokens:
  token = token.lower()
  if token in probabilities:
    token_probs[token] = probabilities[token]
  else:
    token_probs[token] = 0.4


# sort token probabilities by distance from .5
# and pull out the top X ones to use to calculate total probability
max_tokens = 10
interesting_tokens = []
c=0
for w in sorted(token_probs, key=sort_func, reverse=True):
  interesting_tokens.append(token_probs[w])
  if c >= max_tokens:
    break
  c = c+1

# calculate real probabilitiy
a=1
b=1
for token in interesting_tokens:
  a = a * token
  b = b * (1-token)
if a + b == 0:
  print "0"
  sys.exit()
spam_probability = a / ( a + b)
print spam_probability


