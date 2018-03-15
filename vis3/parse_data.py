#!/usr/bin/env python3

import csv
import json
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
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            i = 0
            for row in reader:
                if i > 0:
                    for j in range(len(self.header)):
                        if j == 0:
                            self.data[row[0]] = {}
                        else:
                            self.data[row[0]][self.header[j]] = row[j]
                else:
                    self.header = row
                i += 1
            self.header.pop(0)

    """
    Function that formats the data into two different nested dicts 
    for male and male
    Output Format: 
        dict[institution][major][year][race] = number of students
    """
    def format_data(self):
        for num in self.data:
            try:
                institution = self.data[num]['Institution']
                school_year = self.data[num]['School Year']
                school_year = school_year.split('-')[0]
                major = self.data[num]['Major Program Name']


                aggregate = self.get_student_numbers('Male', num)
            except KeyError:
                #for key in self.data[num].keys():
                #    print(key)
                #    print(self.data[num][key])
                #    break
                #print(self.data[num].keys())
                print("Dammit!")

    def get_student_numbers(self, gender, record_num):
        # extract data from relevant fields
        for field in self.header:
            #pattern = ""
            #regex = re.compile(pattern)
            #result = prog.match(string)
            if gender in field:
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
                else:
                    continue
                race = str(field.split(': ')[1].split('(')[0]).strip()
                print(race)

            """
            Enroll, Female: Asian (Enrl F)
            """

            """
            year0 = 'Enroll'
            elif "Freshmen" in field:
            year1 = 'Freshmen'
            elif "Sophomores" in field:
            year2 = 'Sophomores'
        elif "Juniors" in field:
            year3 = 'Juniors'
            elif "Seniors" in field:
            year4 = 'Seniors'

            # split data into M and F
            """

    def valid_race(self, race):
        valid_races = [
            "White",
            "Hispanics of any race",
            "Asian",
            "American Indian/Alaska Native",
            "Two or more races",
            "Black/African American",
            "Native Hawaiian/Other Pacific Islander",
        ]

        if race in valid_races:
            return True
        else:
            return False

if __name__ == '__main__':
    vis = MaleFemaleVis()
    vis.read_data()
    vis.format_data()

    # year --> major --> race --> #
    #totals = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    # example how to access number of candidates for a school and major over all years
    # print(vis.female)
    total = 0
    for year in vis.female.keys():
        for major in vis.female[year].keys():
            for race in vis.female[year][major].keys():
                print(race)

            import sys
            sys.exit()

        # total += sum(vis.female[year]['Computer Science'].values_flat())

    #

