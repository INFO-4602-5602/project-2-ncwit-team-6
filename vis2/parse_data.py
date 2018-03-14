#!/usr/bin/env python3

import csv
from nested_dict import nested_dict
from collections import defaultdict

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
        self.parsed = nested_dict()

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
                    school_year = school_year.split('-')[0]

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
                    gender = 'Female'
                    race = str(field.split(': ')[1].split('(')[0]).rstrip()
                    
                    if self.valid_race(race):
                        try:
                            if not isinstance(self.parsed[gender][school_year][cur_major], int):
                                self.parsed[gender][school_year][cur_major] = int(self.data[num][field])
                            else:
                                self.parsed[gender][school_year][cur_major] += int(self.data[num][field])
                        except ValueError:
                            pass
                elif 'Male' in field and not 'ACT' in field and not 'SAT' in field and not 'GPA' in field:
                    gender = 'Male'
                    race = str(field.split(': ')[1].split('(')[0]).rstrip()

                    if self.valid_race(race):
                        try:
                            if not isinstance(self.parsed[gender][school_year][cur_major], int):
                                self.parsed[gender][school_year][cur_major] = int(self.data[num][field])
                            else:
                                self.parsed[gender][school_year][cur_major] += int(self.data[num][field])
                        except ValueError:
                            pass

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

    keys_set = {
        'years' : [],
        'majors' : []
    }

    male_years = list(vis.parsed['Male'].keys())
    female_years = list(vis.parsed['Female'].keys())

    keys_set['years'] = list(set(male_years + female_years))

    for gender in ['Male', 'Female']:
        for year in keys_set['years']:
            keys_set['majors'] += list(vis.parsed[gender].get(year, []))

    keys_set['majors'] = list(set(keys_set['majors']))

    # year --> major --> #
    totals = defaultdict(lambda: defaultdict(int))

    for gender in ['Male', 'Female']:
        gender_data = vis.parsed[gender]
        for year in keys_set['years']:
            year_data = gender_data[year]

            for major in keys_set['majors']:
                if year_data[major]:
                    totals[year][major] += year_data[major]

    # year --> major --> #
    percentages = defaultdict(lambda: defaultdict(int))
    for year in keys_set['years']:
        for major in keys_set['majors']:
            female_count = vis.parsed['Female'][year][major]
            totals_count = totals[year][major]

            if female_count and totals_count:
                percentages[year][major] = female_count / totals_count

    content = []
    for year in keys_set['years']:
        for major in keys_set['majors']:
            if percentages[year][major]:
                line = f"{year},{major},{percentages[year][major]}\n"
                content.append(line)

    with open('testit.csv', 'w') as f:
        for line in content:
            f.write(line)
