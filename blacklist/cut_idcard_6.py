# coding=utf-8

import sys

idcard = set()
with open(sys.argv[1], 'r') as f:
    for line in f:
        idcard.add(line[:6])

#print idcard

with open(sys.argv[2], 'w') as f2:
    for item in idcard:
        f2.write(item + '\n')

