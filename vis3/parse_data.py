#!/usr/bin/env python3

import csv
import json
#from nested_dict import nested_dict
from collections import defaultdict

nested_dict = lambda: defaultdict(nested_dict)

class MaleFemaleVis():
    """
    Class that contains the functions needed to read in a csv file and filter it to provide data for a visualization
    """
    def __init__(self, filename='../data/NCWIT-TrackingToolData-Scrubbed.csv'):
        self.data = {}
        self.header = []
        self.filename = filename
        self.parsed = nested_dict()

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
                if not self.is_computer_science(major):
                    # only look at CS majors for now
                    continue
                print("[{}, M]: i:{}, y:{}, m:{}".format(
                    num, institution, school_year, major))
                aggregate = self.get_student_numbers('Male', num)
                self.parsed[institution][school_year]['Male'] = aggregate
                print("[{}, F]: i:{}, y:{}, m:{}".format(
                    num, institution, school_year, major))
                aggregate = self.get_student_numbers('Female', num)
                self.parsed[institution][school_year]['Female'] = aggregate
                #for year in aggregate.keys():
                #    calc_total = aggregate[year]['calc_tot']
                #    given_total = aggregate[year]['giv_tot']
                #    print("  year:{}, calc_total:{}, given_total:{}, \tdiff:{}".format(year, calc_total, given_total, calc_total-given_total))
            except KeyError:
                #for key in self.data[num].keys():
                #    print(key)
                #    print(self.data[num][key])
                #    break
                #print(self.data[num].keys())
                print("Dammit!")

    def write_data(self):
        outfile = "filtered-v3-data.csv"
        data = self.parsed
        f = open(outfile, 'w', encoding='utf-8')
        writer = csv.writer(f, delimiter=',', quotechar='"')
        for item in data:
            # filter data, write ones that are appropriate
            row = []
            writer.writerow(row)

    def group_by_class(self):
        grouped_d = nested_dict()
        for inst in self.parsed.keys():
            years = [year for year in self.parsed[inst].keys()]
            years.sort()
            #print(years)
            # ignore institutions without >=4 years of data
            if len(years) >= 4:
                # is the data within those years valid?
                for year in years:
                    valid = True
                    cls = ['Freshmen', 'Sophomores', 'Juniors', 'Seniors']
                    class_d = nested_dict()
                    for i, cl in enumerate(cls):
                        year_i = str(int(year) + i)
                        if year_i in years:
                            d = self.parsed[inst][year_i]['Female']
                            class_d[i] = d[cl]['calc_tot']
                        else:
                            valid = False
                    # is the class valid for all 4 years? 
                    # add to dict if so
                    if valid:
                        print("{}: {}".format(inst, year))
                        print(class_d)
                        grouped_d[inst][year][gen] = class_d
        self.grouped_dict = grouped_d

    def get_student_numbers(self, gender, record_num):
        # extract data from relevant fields
        d = defaultdict(dict)
        for field in self.header:
            #print("  {}, {}, {}".format(record_num, gender, field))
            #pattern = ""
            #regex = re.compile(pattern)
            #result = prog.match(string)
            if gender in field:
                #if "Enroll" in field:
                #    year = 'Enroll'
                if "Freshmen" in field:
                    year = 'Freshmen'
                elif "Sophomores" in field:
                    year = 'Sophomores'
                elif "Juniors" in field:
                    year = 'Juniors'
                elif "Seniors" in field:
                    year = 'Seniors'
                else:
                    continue
                race = str(field.split(': ')[1].split('(')[0]).strip()
                if self.valid_race(race):
                    try:
                        value = int(self.data[record_num][field])
                    except ValueError:
                        # missing value! data not present. put 0
                        value = 0
                    d[year][race] = value
                    if 'calc_tot' not in d[year]:
                        d[year]['calc_tot'] = value
                    else:
                        d[year]['calc_tot'] += value
                elif "Total Declared Majors" in field:
                    # compare total from dataset against calc data
                    # from adding up races
                    try:
                        value = int(self.data[record_num][field])
                    except ValueError:
                        value = 0
                    d[year]['giv_tot'] = value
        return d

    def is_computer_science(self, major):
        if "Computer Science" in major:
            return True
        elif "CS" in major:
            return True
        else:
            return False

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
    vis.group_by_class()
    #vis.write_data()

    # year --> major --> race --> #
    #totals = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

