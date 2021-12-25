#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author(s): michahess
# date: 18.12.21
"""
command-line:
python \txt_to_spacy.py file1 file2 file3
"""


import spacy, sys
from spacy.tokens import DocBin
nlp = spacy.load('en_core_web_sm')
# files = ['off_news_2014_corpus.txt', ...  ]
files = (sys.argv[1], sys.argv[2], sys.argv[3])
def txt_to_disk(file_tuple):
    i = 1
    for file in file_tuple:
        docbin = DocBin()
        with open(file, 'r', encoding='utf-8') as txt:
            # snt_ls = [sentence for sentence in txt.readlines()]
            for sentence in txt:
                docbin.add(nlp(sentence))
        
        docbin.to_disk(f'C:\\Users\\mhess\\Documents\\UZH\\PCL\\PCL_PROJECT\\part_1\\{sys.argv[i][:-4]}.spacy')
        i += 1
if __name__ == '__main__':
    txt_to_disk(files)

