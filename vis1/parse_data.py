#!/usr/bin/env python3

import csv
from nested_dict import nested_dict

class MaleFemaleVis():
    """
    Class that contains the functions needed to read in a csv file and filter it to provide data for a visualization
    """
    def __init__(self, filename='../data/NCWIT-TrackingToolData-Scrubbed.csv'):
        self.data = {}
        self.header = []
        self.filename = filename
        self.male = nested_dict()
        self.female = nested_dict()

    """
    Function that opens up the csv file and reads in the data into a large dict
    """
    def read_data(self):
        with open(self.filename, 'r', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            i = 0
            for row in spamreader:
                if i>0:
                    for j in range(len(self.header)):
                        if j==0:
                            self.data[row[0]] = {}
                        else:
                            self.data[row[0]][self.header[j]] = row[j]
                else:
                    self.header = row
                i += 1
            self.header.pop(0)

    """
    Function that formats the data into two different nested dicts for male and female
    Output Format: dict[institution][major][year][race] = number of students
    """
    def format_data(self):
        for num in self.data:
            for field in self.header:
                if self.data[num][field] == '':
                    continue
                if field == 'Institution' and not field in self.male.keys():
                    cur_institution = self.data[num][field]
                if field == 'Major Program Name':
                    cur_major = self.data[num][field]
                if field == 'School Year':
                    school_year = self.data[num][field]
                if "Enroll" in field:
                    year = 'Enroll'
                elif "Freshmen" in field:
                    year = 'Freshmen'
                elif "Sophomores" in field:
                    year = 'Sophomores'
                elif "Juniors" in field:
                    year = 'Juniors'
                elif "Seniors" in field:
                    year = 'Seniors'
                elif "Totals" in field:
                    year = 'Totals'
                if 'Female' in field and not 'ACT' in field and not 'SAT' in field and not 'GPA' in field:
                    race = str(field.split(': ')[1].split('(')[0]).rstrip()
                    try:
                        if not isinstance(self.female[cur_institution][cur_major][year][race], int):
                            self.female[cur_institution][cur_major][school_year][year][race] = int(self.data[num][field])
                        else:
                            self.female[cur_institution][cur_major][school_year][year][race] += int(self.data[num][field])
                    except ValueError:
                        pass
                elif 'Male' in field and not 'ACT' in field and not 'SAT' in field and not 'GPA' in field:
                    race = str(field.split(': ')[1].split('(')[0]).rstrip()
                    try:
                        if not isinstance(self.male[cur_institution][cur_major][school_year][year][race], int):
                            self.male[cur_institution][cur_major][school_year][year][race] = int(self.data[num][field])
                        else:
                            self.male[cur_institution][cur_major][school_year][year][race] += int(self.data[num][field])
                    except ValueError:
                        pass

if __name__ == '__main__':
    vis = MaleFemaleVis()
    vis.read_data()
    vis.format_data()

    # example how to access number of candidates for a school and major over all years
    print(vis.female)
    total = 0
    for key in vis.female['91']['Computer Science'].keys():
        total += sum(vis.female['91']['Computer Science'][key].values_flat())
    print(total)
    print(sum(vis.female['91']['Computer Science'].values_flat()))
