#!/usr/bin/env python3

import csv
import re
import pickle

class ScrubData():
	def __init__(self, data_dir = "../data/", data_file = "NCWIT-TrackingToolData-Scrubbed.csv"):
		self.data_dir = data_dir
		self.data_file = data_file
		self.scrubbed_data_file = data_dir+data_file
		self.data = {}
		self.header = []

	def scrub(self):
		with open(self.scrubbed_data_file, 'r', encoding='utf-8-sig') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			i = 0
			for row in spamreader:
				if i>0:
					for j in range(len(row)):
						#print("data[%s][%s]): %s" % (row[0], self.header[j], row[j]))
						if j==0:
							self.data[row[0]] = {}
							self.data[row[0]][self.header[j]] = row[j]
							#print(self.data[row[0]][self.header[j]])
						else:
							self.data[row[0]][self.header[j]] = row[j]
				else:
					self.header = row
				i += 1
			print(i)

	def dump(self):
		pickle.dump(self.data, open("%s.p" % self.data_file[:-4], "wb"))

	def print_data(self):
		local_header = self.header
		#local_header.pop(0)
		#print(local_header)
		for num in self.data:
			for field in local_header:
				print("data[%s][%s]: %s" % (num, field, self.data[num][field]))
				pass

	def print_headers(self):
		for field in self.header:
			print(field)
			pass

if __name__ == '__main__':
	print("Starting...")
	data = ScrubData()
	data.scrub()
	data.dump()
	data.print_data()
	#data.print_headers()
