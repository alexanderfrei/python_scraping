import PyPDF2
import os
import re
import string
from collections import OrderedDict

PDF_PATH = "./pdf"


def isCommon(ngram):
    stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
                  "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
                  "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't",
                  "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
                  "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him",
                  "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is",
                  "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
                  "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our",
                  "ours	ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's",
                  "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs",
                  "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
                  "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't",
                  "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's",
                  "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't",
                  "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
                  "yourselves"]
    for word in ngram.strip().split(' '):
        if word in stop_words:
            return True
    return False


def cleanInput(input):
    input = re.sub('\n+', " ", input)
    input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    cleanInput = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput


def get_ngrams(input, n):
    input = cleanInput(input)
    output = {}
    for i in range(len(input)-n+1):
        ngramTemp = " ".join(input[i:i+n])
        if not isCommon(ngramTemp):
            if ngramTemp not in output:
                output[ngramTemp] = 0
            output[ngramTemp] += 1
    return output

files = os.listdir(PDF_PATH)
files = [os.path.join(PDF_PATH,file) for file in files]

pdf_pattern = re.compile(".*\.pdf")
pdf_text = []

if files:
    for file in files:
        pdf_match = re.match(pdf_pattern, file)
        if pdf_match:
            stream = open(file, 'br')
            pdf_reader = PyPDF2.PdfFileReader(stream)
            for page_num in range(pdf_reader.getNumPages()):
            # for page_num in range(10):
                page = pdf_reader.getPage(page_num)
                pdf_text.append(page.extractText())
            stream.close()
else:
    print("No files in path")

ngrams = get_ngrams(" ".join(pdf_text), 1)
ngrams = OrderedDict(sorted(ngrams.items(), key=lambda t: t[1], reverse=True))
# print(ngrams)

with open(os.path.join(PDF_PATH,'pdf_ngrams.txt'), 'w') as output:
    for word, count in ngrams.items():
        if count > 10:
            output.write("{}: {}\n".format(word, count))

