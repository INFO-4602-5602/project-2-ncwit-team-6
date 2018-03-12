import csv

with open('NCWIT-TrackingToolData-Scrubbed.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    content = []
    for row in spamreader:
        content.append(row)

import re

by_demographic = dict()

header = content[0]
print(len(header))
print(header[0])

# for field in header:
#     # if re.match('Male', line) 
#     print(field)
