#!/usr/bin/env python3

import csv
import re
import pickle
import operator
import numpy as np
from matplotlib import pyplot as plt

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
			#print(i)

	def dump(self):
		pickle.dump(self.data, open("%s.p" % self.data_file[:-4], "wb"))
		pickle.dump(self.header, open("header.p", "wb"))

	def load(self, data_file=None):
		if data_file==None:
			self.data = pickle.load(open("%s.p" % self.data_file[:-4], "rb"))
			self.header = pickle.load(open("header.p", "rb"))
		else:
			return pickle.load(open("%s.p" % data_file, "rb"))

	def print_data(self, spec_field="all"):
		local_header = self.header
		for num in self.data:
			for field in local_header:
				if spec_field in field:
					print("data[%s][%s]: %s" % (num, field, self.data[num][field]))
				elif spec_field == "all":
					print("data[%s][%s]: %s" % (num, field, self.data[num][field]))
				pass

	def print_headers(self):
		#print(self.header)
		for field in self.header:
			print(field)
			pass

	def gather_comparison(self, general_headers, gender_headers, i, j):
		x = [] # X data for plot
		y = [] # Y data for plot
		m = []
		m_sum = 0
		f = []
		f_sum = 0
		y_sum = 0
		z = {} # dict representing relavent data
		#print("general_header[i]: %s\t| gender_headers[j]: %s" % (general_headers[i], gender_headers[j]))
		#quit()
		
		for num in self.data:
			# Update X 
			x_data = self.data[num][general_headers[i]]
			x.append(str(x_data))
	
			# Update Y
			for field in self.header:
				if gender_headers[j] in field:
					if ("Totals" in field) and ("Female" in field):
						#print(self.data[num][field])
						if self.data[num][field] != "":
							y_sum += int(self.data[num][field]) 
							f_sum += int(self.data[num][field]) 
					if ("Totals" in field) and ("Male" in field):
						#print(self.data[num][field])
						if self.data[num][field] != "":
							y_sum += int(self.data[num][field]) 
							m_sum += int(self.data[num][field]) 
			y.append(y_sum)
			f.append(f_sum)
			m.append(m_sum)

			# Populate Z dict
			try:
				z[x_data] = y_sum
			except:
				z[x_data] = {}
				z[x_data] = y_sum
			pass

		if general_headers[i][-1] == "?":
			pickle.dump(z, open("%s_vs_%s.p" % (general_headers[i][:-1], gender_headers[j]), "wb"))
		else:
			pickle.dump(z, open("%s_vs_%s.p" % (general_headers[i], gender_headers[j]), "wb"))
		#print(z)

		x = []
		y = []
		for inst in z:
			y.append(z[inst])
		
		y_np = np.array(y)
		y = y_np[np.argsort(y_np)[:10]]

		for inst in z:
			if z[inst] in y:
				x.append(str(inst))
		#print(x)
		#print(y)

		lists = sorted(z.items(), key=lambda x:x[1])[:10]
		#print(lists)
		x1, y = zip(*lists)
		for i in range(len(x)):
			#print("x: %s" % x1[i])
			if x1[i] == "":
				continue

			if "," in x1[i]:
				x[i] = str(x1[i].replace(',', ''))
				#print(x[i])
			else:
				x[i] = str(x1[i])

			if i == 0:
				print("label,value", file=open("data/plots_f_data.csv", "w"))
				print("label,value", file=open("data/plots_m_data.csv", "w"))
				print("label,value", file=open("data/plots_total_data.csv", "w"))
			print("%s,%s" % (x[i], int(f[i])), file=open("data/plots_f_data.csv", "a"))
			print("%s,%s" % (x[i], int(m[i])), file=open("data/plots_m_data.csv", "a"))
			print("%s,%s" % (x[i], int(y[i])), file=open("data/plots_total_data.csv", "a"))
			print("f[%s]: %s\t| m[%s]: %s\t| t[%s]: %s" % (i, f[i], i, m[i], i, y[i]))
	
		return x, y, z, m, f

	def test_plot(self, x, y, x_label="X_Vals", y_label="Y_Vals", title="XvsY"):
		plt.bar(x, y, label="title")
		plt.title(title)
		plt.legend()
		plt.xlabel(x_label)
		plt.ylabel(y_label)
		plt.savefig(title+str(".png"))
		plt.show()


if __name__ == '__main__':
	print("Starting...")
	general_headers = ["Record #", #1
						"CIP# Only", # 2
						"Major Program Name", # 3
						"Degree Level", # 4
						"NCWIT Participant", # 5
						"Institution", # 6 
						"What degrees does your institution offer?", # 7
						"School Year", # 8
						"When do students typically declare their major?"] # 9
	gender_headers = ["Asian",  # 1
						"Black/African American", # 2
						"Cumulative GPA",  # 3
						"Enrolled in DIFFERENT MAJOR", # 4
						"Enrolled in SAME MAJOR", # 5
						"Graduated",# 6 
						"Hispanics of any race",  # 7
						"Left Institution (not graduated)", # 8
						"American Indian/Alaska Native", # 9
						"Native Hawaiian/Other Pacific Islander",# 10
						"Two or more races", # 11
						"Total Declared Majors", # 12
						"US Citizens", # 13
						"White"]  # 14

	# Declare data class to scrub in
	data = ScrubData()

	# Scrub data and dump/load
	#data.scrub()
	#data.dump()
	data.load()

	# Test output funcs
	#data.print_data()
	#data.print_headers()

	# Generate plottable dataset and plot
	i = 6
	j = 0
	data_file = "%s_vs_%s" % (general_headers[i], gender_headers[j])
	x, y, z, m, f = data.gather_comparison(general_headers, gender_headers, i, j)
	print(z)
	#z = data.load(data_file)
	#data.test_plot(x, y)
