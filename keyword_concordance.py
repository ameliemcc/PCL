#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author(s): michahess & amcco
# date: 28.12.21

import sys, spacy, re, random
from spacy.matcher import DependencyMatcher
from spacy.tokens import DocBin

nlp = spacy.load('en_core_web_sm')
matcher = DependencyMatcher(nlp.vocab)

corpus, target_word, construction, max_n = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
# print(corpus, target_word, construction, max_n)

def context(corpus, target_word, construction, n_max):
    sentences = []
    pattern1 = [ {'RIGHT_ID': f'{target_word}_{construction}1', 'RIGHT_ATTRS': {'LEMMA': target_word}},
            {'LEFT_ID': f'{target_word}_{construction}1', 'REL_OP': '>', 'RIGHT_ID': f'{construction}_dep1', 'RIGHT_ATTRS':{'DEP':construction }}]
    pattern2 = [ {'RIGHT_ID': f'{target_word}_{construction}2', 'RIGHT_ATTRS': {'LEMMA': target_word}},
            {'LEFT_ID': f'{target_word}_{construction}2', 'REL_OP': '<', 'RIGHT_ID': f'{construction}_dep2', 'RIGHT_ATTRS':{'DEP':construction }}]
    matcher.add(f'{target_word}_{construction}', [pattern1, pattern2])
    docbin = DocBin().from_disk(f'{corpus}')
    docs_loaded = docbin.get_docs(nlp.vocab)
    for doc in docs_loaded:
        for matches in matcher(doc):
    
            sentences.append(doc)
            # print(sentences[i].text)

    #print(sentences)
    random.shuffle(sentences)
    out_sent = []
    for i in range(0, random.randrange(0, int(n_max))):
        try:
            out_sent.append(sentences[i].text)
            print(sentences[i].text)
        except IndexError:
            break
    matcher.remove(f'{target_word}_{construction}')
    return out_sent


if __name__ == '__main__':
    context(corpus, target_word, construction, max_n)



"""command:
python keyword_concordance.py was_web_2020_corpus.spacy be aux 10"""