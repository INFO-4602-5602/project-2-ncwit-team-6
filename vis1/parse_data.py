#!/usr/bin/env python3

import csv
import json
from nested_dict import nested_dict

class MaleFemaleVis():
    """
    Class that contains the functions needed to read in a csv file and filter it to provide data for a visualization
    """
    def __init__(self, filename='../data/NCWIT_DataV2_RawData.csv'):
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
    Output Format: dict[institution][year][major][race] = number of students
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
                # do not add in the totals
                elif "Total" in field:
                    continue
                if 'Female' in field and not 'ACT' in field and not 'SAT' in field and not 'GPA' in field:
                    race = str(field.split(': ')[1].split('(')[0]).rstrip()
                    try:
                        if not isinstance(self.female[cur_institution][race], int):
                            self.female[cur_institution][race] = int(self.data[num][field])
                        else:
                            self.female[cur_institution][race] += int(self.data[num][field])
                    except ValueError:
                        pass
                elif 'Male' in field and not 'ACT' in field and not 'SAT' in field and not 'GPA' in field:
                    race = str(field.split(': ')[1].split('(')[0]).rstrip()
                    try:
                        if not isinstance(self.male[cur_institution][race], int):
                            self.male[cur_institution][race] = int(self.data[num][field])
                        else:
                            self.male[cur_institution][race] += int(self.data[num][field])
                    except ValueError:
                        pass

    """
    Function to format data for the following specifications:
        1.  Dict of # of male and female students
        2.  Keyed in by the school
        3.  Over all years
    """
    def format_1(self):
        df = {}
        dm = {}
        for fkey, mkey in zip(self.female.keys(), self.male.keys()):
            df[fkey] = sum(self.female[fkey].values_flat())
            dm[mkey] = sum(self.male[mkey].values_flat())
        return df, dm

    """
    Function to format data for the following specifications:
        1.  Dict of # of male and female students
        2.  Keyed in by the school
        3.  Exports a dict of dicts
    """
    def format_2(self):
        df = {}
        dm = {}
        for fkey, mkey in zip(self.female.keys(), self.male.keys()):
            df[fkey] = {}
            dm[mkey] = {}
            for fkey1, mkey1 in zip(self.female[fkey].keys(), self.male[mkey].keys()):
                df[fkey][fkey1] = sum(self.female[fkey][fkey1].values_flat())
                dm[mkey][mkey1] = sum(self.male[mkey][mkey1].values_flat())
        return df, dm

    def format_3(self):
        df = {}
        dm = {}
        for fkey, mkey in zip(self.female.keys(), self.male.keys()):
            for fkey1, mkey1 in zip(self.female[fkey].keys(), self.male[mkey].keys()):
                if 'Asian' in fkey1:
                    df[fkey] = self.female[fkey][fkey1]
                if 'Asian' in mkey1:
                    dm[mkey] = self.male[mkey][mkey1]
        return df, dm

    def dump_csv(self, df, dm):
        with open('dictf.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in df.items():
               writer.writerow([key, value])
        with open('dictm.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in dm.items():
               writer.writerow([key, value])

    """
    Function to dump a given dict or dict of dicts to json format
    """
    def dump(self, data_female, data_male, dict_of_dicts=False):
        if not dict_of_dicts:
            with open('data/female.json', 'w') as outfile:
                json.dump(data_female, outfile)
            with open('data/male.json', 'w') as outfile:
                json.dump(data_male, outfile)
        else:
            years = ['2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017']
            for year in years:
                new_fdata = {}
                new_mdata = {}
                for fkey, mkey in zip(data_female.keys(), data_male.keys()):
                    for fkey1, mkey1 in zip(data_female[fkey].keys(), data_male[mkey].keys()):
                        if fkey1 == year:
                            new_fdata[fkey] = data_female[fkey][fkey1]
                        if mkey1 == year:
                            new_mdata[mkey] = data_male[mkey][mkey1]
                    with open('data/female_' + year.replace('-', '_') + '.json', 'w') as outfile:
                        json.dump(new_fdata, outfile)
                    with open('data/male_' + year.replace('-', '_') + '.json', 'w') as outfile:
                        json.dump(new_mdata, outfile)


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
    #df, dm = vis.format_1()
    #vis.dump(df, dm)
    df, dm = vis.format_3()
    vis.dump_csv(df, dm)
