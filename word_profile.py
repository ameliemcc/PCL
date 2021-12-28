#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author(s): michahess & amcco
# date: 22.12.21

import math, sys, re
from typing import Iterable

inp_files = r''

'''
main
    get_profile
        get_logdice_and_freq
            calc_logdice
            dict_to_tup'''

def get_profile(target_word, file):
    """ takes a target word and a tsv-file. iterates through the file and looks for the target word.
    returns a dict with each pair-word as key and its count as a value"""
    #initializing dict
    collocations = {}
    with open(file, 'r', encoding='utf-8') as tsv:
        for line in tsv:
            # splits each line at the tab
            word_a, word_b = line.split('\t')
            # if word a is the target word:
            word_b = word_b.rstrip('\n')
            if (word_a == target_word):
                # updates/
                try:
                    collocations[word_b] += 1
                # /initializes the count
                except KeyError:
                    collocations[word_b] = 1
            # if word b is the target word:
            elif (word_b == target_word):
                # same as above
                try:
                    collocations[word_a] += 1
                except KeyError:
                    collocations[word_a] = 1
        # from the pair-word count and the file, returns a tuple in the format (paired word, log_dice, freq)
        results = get_logdice_and_freq(collocations, tsv)
        print(results)
        # creates a logdice-sorted version of the results
        logdice_sort = sorted(results, key=lambda x: x[1], reverse=True)
        print(f'logdice_sort\n{logdice_sort}')
        # creates a frequency-sorted version of the results
        frq_sort = sorted(results, key=lambda x: x[2], reverse=True)
        print(f'frq_sort:\n{frq_sort}')
        

def dict_to_tup(dct):
    """converts a dict of format {word1:(logdice1, freq1), ...}
    into a tuple of format ((word1, logdice1, freq1), ...)"""
    outtup = []
    for key in dct.keys():
        keytup = [key]
        for item in dct[key]:
            keytup.append(item)
        outtup.append(tuple(keytup))
    return tuple(outtup)

    
def calc_logdice(f_xy, f_x, f_y):
    """ calculates the log-dice of a word """
    logDice = 14 + math.log((2*f_xy)/(f_x+f_y), 2)
    logDice = round(logDice, 4)
    return logDice

def get_logdice_and_freq(collocation_dict, file):
    ld_frq = {}
    f_x = sum([collocation_dict[word] for word in collocation_dict.keys()])
    for word in collocation_dict.keys():
        f_y = 0
        f_xy = collocation_dict[word]
        for line in file:
            if word in line:
                f_y += 1
        # key = collocated word : (logdice, frequency)
        ld_frq[word] = (calc_logdice(f_xy, f_x, f_y), collocation_dict[word])
    # TO BE IMPLEMENTED:
    # KEY : VAL1, VAL2 --> (KEY, VAL1, VAL2)
    # --> sort by VAL1 & VAL2
    ld_frq_tup = dict_to_tup(ld_frq)
    return ld_frq_tup


files_n_words = {'off': ('off_profile_prep_news_2014_data.tsv', 'off_profile_prep_news_2020_data.tsv', 'off_profile_prt_news_2014_data.tsv', 'off_profile_prt_news_2020_data.tsv'),
# 'was': ('a', 'b'),
'refugee': ('refugee_profile_amod_news_2007_data.tsv', 'refugee_profile_nmod_news_2007_data.tsv')}

def main():
    for word in files_n_words.keys():
        for filename in files_n_words[word]:
            get_profile(word, filename)
    
    pass

if __name__ == '__main__':
    main()