import POSTagger 
import time


# Initialize Tagger. 
c = POSTagger.load_corpus("brown_corpus.txt")
start= time.time()
tagger = POSTagger.Tagger(c)
end = time.time()
print 'Initialization took:' , end-start, 'seconds.'

# Print out POS using most probable tags
start = time.time()
print ['The','man','walks','.']
print tagger.most_probable_tags(['The','man','walks','.'])
print ''

print ['The','blue','bird','sings']
print tagger.most_probable_tags(['The','blue','bird','sings'])
print ''


# Compare most probable tags with Viterbi method
s= 'I am waiting to reply'.split()
print s
print tagger.most_probable_tags(s)
print tagger.viterbi_tags(s)
print ''

s= 'I saw the play'.split()
print s
print tagger.most_probable_tags(s)
print tagger.viterbi_tags(s)
print ''

end = time.time()
print 'Calculating tags took:', end-start, 'seconds.'