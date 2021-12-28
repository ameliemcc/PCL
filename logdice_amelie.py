#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author(s): amcco & michahess
# date: 02.12.21

import math

numberOfX = int(input('how many X words? '))
numberOfY = int(input('how many Y words? '))

cooccurrences =  int(input('how many coocurrences of words X and Y? '))

def getDice(X, Y, coOc):
    result = (2*coOc)/(X+Y)
    return result

# print(getDice(numberOfX,numberOfY, cooccurrences))


def getLogDice():
    dice = getDice(numberOfX, numberOfY, cooccurrences)
    logDice = 14 + math.log(dice, 2)
    return logDice

# print(getLogDice())