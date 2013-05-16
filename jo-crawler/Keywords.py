'''
Keywords

Used to extract keywords (originally ment for tweets) (rather greedy)
Includes method grammar: extract_keywords_grammer

@author: Oskar Bodemyr
'''

import nltk
from nltk.tag import _POS_TAGGER
import sys


# make sure we have the right tokenization data local
# use default storage location for now
# todo: maybe store this in a specified directory?
# note: uncopmment if running for the first time
# nltk.download('maxent_treebank_pos_tagger')
# nltk.download('brown')

def extract_keywords_grammar(text):
    '''Uses chunks matching to identify keywords in a tweet'''

    sequence = nltk.pos_tag(nltk.word_tokenize(text))
    if sequence == []:          # gets rid of all the 'Warning: parsing empty text' messages
        return []
    sequence = map(lambda (a,b): (a.lower(),b), sequence)
    words = []
    skiplistsingular = []

    '''Grammars to find words that usually are more important in a text'''
    grammar=''' Name: {(<NN>|<NNS>)(<NN>|<NNS>)+} 
                Name2: {(<NNP>|<NNPS>)(<NNP>|<NNPS>)+}
                Noun: {(((<NNP>|<NN>|<NNS>)<IN><DT>(<NNP>|<NN>|<NNS>))|((<JJ>|<JJR>)+(<NN>|<NNS>|<VBG>)+))}
                ToVerb: {<TO><VB>}
                XofY: {(<NNP>|<NN>|<NNS>)(<IN>(<NNP>|<NN>|<NNS>))+}
            '''
    grammarSingular='''
                        Noun: {(<NN>|<NNS>|<VBG>)}
                        Name: {(<NNP>|<NNPS>)}
                    '''
    chunks = nltk.RegexpParser(grammar)
    chunksSingular = nltk.RegexpParser(grammarSingular)
    
    def multiwords(t):
        return reduce(lambda x,y: x + " " + y, map(lambda (x,_1): x, t)) 
    
    '''After grammar, checks the different categories to handle them accordingly'''
    for t in chunks.parse(sequence).subtrees():
        if t.node == "Noun":
            keys = multiwords(t)            
            words.append(keys)
            if len(t)>1:
                if t[1][1]=="IN":
                    skiplistsingular.append(t[0][0])
                    skiplistsingular.append(t[3][0])
                if t[0][1]=="JJ":
                    t1 = t[1:]
                    keys = multiwords(t1)
                    words.append(keys)                  
        elif t.node == "ToVerb":
            words.append(t[1][0])
        elif t.node == "XofY":
            t = t[-3:]
            skiplistsingular.append(t[0][0])
            words.append(t[0][0])
            skiplistsingular.append(t[2][0])
            words.append(t[2][0])
            word = ""
            for x in t:
                word = word + x[0] + " "
            word = word.rstrip()
            words.append(word)  
        elif t.node == "Name" or t.node == "Name2":
            if len(t)>1:
                words.append((reduce(lambda x,y: x + " " + y if len(y)>2 else x, map(lambda (x,_1): x, t))))
                for x in t:           
                    words.append(x[0]) 
                    skiplistsingular.append(x[0])
            else:
                words.append(t[0][0])
                
    for s in chunksSingular.parse(sequence).subtrees():
        if s.node == "Noun" or s.node == "Name":
            if s[0][0] not in skiplistsingular:
                words.append(s[0][0])                  
    return list(set(words))

if __name__ == '__main__':
    text = True
    while text:
        print ">> "
        text = sys.stdin.readline()
        print extract_keywords_grammar(text.rstrip())

