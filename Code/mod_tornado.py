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
# This script reads in the data from the TORNADO team and modifies the angle data to account for
# the two 90 degree turns taken from changing column data. It also fixes wrong row numbering for some columns.
#
# Main Method: generateDataTPs()
#
# REQUIRES PYTHON 2.7 TO EXECUTE
#
####################################################################################

import csv

def generateDataTPs(SENSOR_CSV_OUTPUT_FILENAME = 'sensor_data.csv', INPUT_CSV_FILENAME = 'readings_tornadoes_001.csv'):
	headers = []            # Stores headers
	data = []               # Stores data from file being read

	# Creating File to store output
	f = open(SENSOR_CSV_OUTPUT_FILENAME, "ab+")
	writer = csv.writer(f)

	# Reading in the TORNADO team data
	with open(INPUT_CSV_FILENAME) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if (line_count == 0):
				headers = row                   # Reading headers
				writer.writerow(headers)        # Adding headers to new file
				line_count += 1
			else:
				data.append(row)                  # Reading rows
				line_count += 1
		print('Processed line_count lines ' + str(line_count))

		for rows in data:
			# Correcting data in rows
			if ((rows[0] == str(1)) or (rows[0] == str(3))):
				for i in range(0,8):
					if (rows[1] == str(i)):
						rows[1] = str(7-i)
						break


				# Now to account for the two 90 deg turns taken while switching columns 1 and 3
				rows[2] = str(int(rows[2])+160)
				if (int(rows[2]) > 310):
					rows[2] = str(int(rows[2])-320)  # NOTE: 310 and 320 are the error in the code stating the complete circle is only 320 degrees. Corrected in calculation.

			# Writing modifies rows to file
			writer.writerow(rows)