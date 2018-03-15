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
                if not self.is_computer_science(major):
                    continue
                print("[{}, Male]: i:{}, y:{}, m:{}".format(num, institution, school_year, major))
                aggregate = self.get_student_numbers('Male', num)
                self.male[institution][school_year] = aggregate
                print(aggregate.keys())
                for year in aggregate.keys():
                    total = 0
                    for race in aggregate[year].keys():
                        try:
                            total += int(aggregate[year][race])
                            print(aggregate[year][race])
                        except ValueError:
                            # missing data value!
                            #continue
                            pass
                    print("  year:{}, total:{}".format(year, total))
            except KeyError:
                #for key in self.data[num].keys():
                #    print(key)
                #    print(self.data[num][key])
                #    break
                #print(self.data[num].keys())
                print("Dammit!")

    def write_data(self, gender):
        outfile = "filtered-v3-" + gender + ".csv"
        if gender is "Male":
            data = self.male
        else:
            data = self.female
        f = open(outfile, 'w', encoding='utf-8')
        writer = csv.writer(f, delimiter=',', quotechar='"')
        for item in data:
            # filter data, write ones that are appropriate
            row = []
            writer.writerow(row)

    def get_student_numbers(self, gender, record_num):
        # extract data from relevant fields
        d = defaultdict(dict)
        for field in self.header:
            #print("  {}, {}, {}".format(record_num, gender, field))
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
                #elif "Totals" in field:
                #    year = 'Totals'
                else:
                    continue
                race = str(field.split(': ')[1].split('(')[0]).strip()
                if self.valid_race(race):
                    try:
                        value = int(self.data[record_num][field])
                        d[year][race] = value
                        if not isinstance(d[year]['Total'], int):
                            d[year]['Total'] = value
                        else:
                            d[year]['Total'] += value
                    except ValueError:
                        print("Oh noes")
                        pass
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
    vis.write_data()

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

