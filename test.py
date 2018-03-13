#!/usr/bin/env python3

import csv
import re

data = {}
header = []
with open('NCWIT-TrackingToolData-Scrubbed.csv', 'r', encoding='utf-8-sig') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in spamreader:
        if i>0:
            if i>len(header):
                break
            for j in range(len(row)):
                #print("data[%s][%s]): %s" % (row[0], header[j], row[j]))
                if j==0:
                    data[row[0]] = {}
                else:
                    data[row[0]][header[j]] = row[j]
        else:
            header = row
        i += 1
        #print("content[0][%i]: %s" % (i, content[0][i-1]))
        #print("len(content[0]: %s" % len(content[0]))

#by_demographic = dict()
#print(data['2156'])

header.pop(0)
for num in data:
    for field in header:
        print("num: %s\t| field: %s\t" % (num, field))
        print("data[%s][%s]: %s" % (num, field, data[num][field]))
        pass
