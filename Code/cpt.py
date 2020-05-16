##########
#
# Team Awesome
# Group Members:
#	Ran Bi
#	Samantha Eaton
#	Sagar Vilas Jagtap
# Instructor: Dr. M. Silaghi
# CSE 5694 Spring 2020
#
##########
# 
# This script reads data from the conditional probability tables of the belief network and stores them in memory for use
# Location[]       - data from location.csv
# Angle []         - data from angle.csv
# SL[]             - Sonar left CPT from sonarLeft.csv
# SR[]             - Sonar Right CPT from sonarRight.csv
# Landmark[]       - Landmark CPT from landmark.csv
# Transition_total - Transition probabilities from probabilities.txt
#
# MUST be in the same directory as the CSV files and Probabilities.TXT file!
# The filenames can be specified else they are defaulted to the files listed above.
#
# Main Method: ReadInCPTs()
#
# REQUIRES PYTHON 2.7 TO EXECUTE
#
####################################################################################

import csv

def ReadInCPTs(Location_CSV_Filename = 'location.csv', Angle_CSV_Filename = 'angle.csv', Landmark_CSV_Filename = 'landmark.csv',
			   Sensor_Left_CSV_Filename = 'sensorLeft.csv', Sensor_Right_CSV_Filename = 'sensorRight.csv',
			   Probabilities_Filename = 'probabilities.txt'):

	Location = []
	Angle = []
	Landmark = []
	SL = []
	SR = []
	Transition_total = []

	with open(Location_CSV_Filename) as csv_location:
		location_reader = csv.reader(csv_location, delimiter=',')
		line_count = 0
		for row in location_reader:
			if (line_count > 0):
				Location.append(row)
			line_count += 1

	with open(Angle_CSV_Filename) as csv_angle:
		angle_reader = csv.reader(csv_angle, delimiter=',')
		line_count = 0
		for row in angle_reader:
			if (line_count > 0):
				Angle.append(row)
			line_count += 1

	with open(Landmark_CSV_Filename) as csv_land:
		land_reader = csv.reader(csv_land, delimiter=',')
		line_count = 0
		for row in land_reader:
			if (line_count > 0):
				Landmark.append(row)
			line_count += 1

	with open(Sensor_Left_CSV_Filename) as csv_SL:
		SL_reader = csv.reader(csv_SL, delimiter=',')
		line_count = 0
		for row in SL_reader:
			if (line_count > 0):
				SL.append(row)
			line_count += 1

	with open(Sensor_Right_CSV_Filename) as csv_SR:
		SR_reader = csv.reader(csv_SR, delimiter=',')
		line_count = 0
		for row in SR_reader:
			if (line_count > 0):
				SR.append(row)
			line_count += 1

	with open(Probabilities_Filename) as csv_transition:
		transition_reader = csv.reader(csv_transition, delimiter=',')
		for row in transition_reader:
			Transition_total.append(row)