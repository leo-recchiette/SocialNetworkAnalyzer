#  coding: utf-8
import json
import sys

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

paths = sys.path

for p in paths:
    if p == '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python':
        sys.path.remove(p)

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer


def removeStopWords():
    stop_words = set(stopwords.words('italian'))

    english_stop_words = set(stopwords.words('english'))

    othersWords = ['.', '?', '??', '#', ',', ':', '*', '..', '...', '!', '(', ')', 'A', 'a', 'B', 'b', 'C', 'c', 'D',
                   'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N',
                   'n', 'O', 'o', 'P', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x',
                   'Y', 'y', 'Z', 'z', 'eh', 'si', '-', '--', '<', '>', '---', '&', '\'', '``', '', 'il', 'lo', 'la',
                   'i', 'gli', 'le', 'di', 'a', 'da', 'in', 'con', 'su', 'per', 'tra', 'fa', '\'\'']
    stop_words.update(list(set(othersWords)))

    stop_words.update(list(set(english_stop_words)))

    return stop_words


def normalizeCorpus(documents):
    corpus = []
    for d in documents:
        corpus.append(d['document'].encode('utf8'))

    return corpus


def calculateTFIDF(corpus):

    stop_words = removeStopWords()

    tfidf = TfidfVectorizer(stop_words = stop_words)
    x = tfidf.fit_transform(normalizeCorpus(corpus))
    df_tfidf = pd.DataFrame(x.toarray(), columns=tfidf.get_feature_names())

    return  {c: s[s > 0] for c, s in zip(df_tfidf, df_tfidf.T.values)}
