############################################################
# Author: Nebil Ali
# Date: Friday, March 6, 2015
# Desc: Takes a sentence and guesses POS of each word
############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
from collections import Counter
import itertools

############################################################
# Part of Speech Tagger
############################################################

def tokenize(line):
	return [tuple(x.split('=')) for x in line.split()]


def load_corpus(path):
	f = open(path)
	return [tokenize(line) for line in f]

def viterbiHelp (obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
 
    # Initialize base cases (t == 0)
    for y in states:
        if (obs[0],y) in emit_p:
            V[0][y] = start_p[y] + emit_p[(obs[0],y)]
            path[y] = [y]
        else:
            V[0][y] = start_p[y] + emit_p[('unk',y)]
            path[y] = [y]
 
    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
 
        for y in states:

            if (obs[t],y) in emit_p:
                (prob, state) = max((V[t-1][y0] * trans_p[(y0,y)] * emit_p[(obs[t],y)], y0) if (y0,y) in trans_p else (V[t-1][y0] * trans_p[('unk',y)] * emit_p[(obs[t],y)], y0) for y0 in states)
                V[t][y] = prob
                newpath[y] = path[state] + [y]
            else:
                (prob, state) = max((V[t-1][y0] * trans_p[(y0,y)] * emit_p[('unk',y)], y0) for y0 in states)
                V[t][y] = prob
                newpath[y] = path[state] + [y]
        # Don't need to remember the old paths
        path = newpath
    n = 0           # if only one element is observed max is sought in the initialization values
    if len(obs) != 1:
        n = t
    #print_dptable(V)
    (prob, state) = max((V[n][y], y) for y in states)
    return path[state]


class Tagger(object):

    def __init__(self, sentences):
        smooth = 1e-15
        counts = Counter()
        bigramCounts = Counter()        
        wordTagCounts = Counter()
        tagCounts = Counter()

        words = [word for sent in sentences for word in sent]
        v = set([word for word,pos in words])
        lenv = len(v)
        
        tagCounts.update([pos for word,pos in words])
        
        wordTagCounts.update(words)
        bigramCounts.update([(sent[i][1],sent[i+1][1])for sent in sentences for i in range(len(sent)-1)])
        sentStart = [sent[0][1] for sent in sentences]
        counts.update(sentStart)
        
        lengthSentStart = len(sentences)
        self.a = {key:math.log( float(value+1*smooth)/(tagCounts[key[0]] +12*smooth) ) for key,value in bigramCounts.iteritems()}
        self.pi = {key:math.log( float(value+1*smooth)/(12*smooth+lengthSentStart) ) for key,value in counts.iteritems()}
        self.b = {key: math.log( float(value+1*smooth)/(lenv*smooth+tagCounts[key[1]]) )for key,value in wordTagCounts.iteritems()}

        POS = ['NOUN','VERB','ADJ','ADV','PRON','DET','ADP','NUM','CONJ','PRT','.','X']
        for pos in POS: 
            self.b[('unk',pos)] =  math.log( float(1*smooth)/(lenv*smooth+tagCounts[pos]) )
            self.a[(pos,'unk')] = math.log( float(1*smooth)/(tagCounts[pos] +12*smooth) )
            if pos not in self.pi:  
                self.pi[pos] = math.log( float(1*smooth)/(12*smooth+lengthSentStart))
        
    def most_probable_tags(self, tokens):
        POS = ['NOUN','VERB','ADJ','ADV','PRON','DET','ADP','NUM','CONJ','PRT','.','X']
        x = [[(word,pos) for pos in POS] for word in tokens]
        y = [[(self.b[tok],tok[1]) if tok in self.b else (self.b[('unk', tok[1])],tok[1])for tok in toktup] for toktup in x ]
        return  [max(i)[1] for  i in y]
        
    def viterbi_tags(self, tokens):
        return viterbiHelp(tokens, ['NOUN','VERB','ADJ','ADV','PRON','DET','ADP','NUM','CONJ','PRT','.','X'],self.pi,self.a,self.b)
        
############################################################
