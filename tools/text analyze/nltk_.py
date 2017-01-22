from nltk import FreqDist
from nltk import word_tokenize
from nltk import Text

# object Text

tokens = word_tokenize("Here is some not very interesting text")
text = Text(tokens)
print(tokens)

# ***************************************************** #
# ngrams

from nltk.book import *
from nltk import ngrams
fourgrams = ngrams(text6, 4)
fourgramsDist = FreqDist(fourgrams)

print(fourgramsDist['Well', ',', 'that', "'"])

for fourgram in fourgrams:
    if fourgram[0] == "coconut":
        print(fourgram)

fdist = FreqDist(text6)
print(fdist.most_common(10))

# ***************************************************** #
# Lexicographic Analysis

from nltk import word_tokenize, sent_tokenize, pos_tag

text = word_tokenize("""Strange women lying in ponds distributing swords is no
basis for a system of government. Supreme executive power derives from a mandate
from the masses, not from some farcical aquatic ceremony.""")
print(pos_tag(text))

sentences = sent_tokenize("Google is one of the best companies in the world. I constantly google myself to see what I'm up to.")
nouns = ['NN', 'NNS', 'NNP', 'NNPS']

for sentence in sentences:
    if "google" in sentence.lower():
        taggedWords = pos_tag(word_tokenize(sentence))
        for word in taggedWords:
            if word[0].lower() == "google" and word[1] in nouns:
                print(sentence)
