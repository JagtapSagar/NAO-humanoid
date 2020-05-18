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
# This script determines the movements based on the particle filtering.
# It writes/overwrites the probabilities.txt file
#
# Main Method: generateProbabilitiyMatrix()
#
# REQUIRES PYTHON 2.7 TO EXECUTE
#
####################################################################################

import csv


def find_position(position):
    # This function returns 9 state matrix equivaluent values for states recorded outside 0-8
    # The following was the order of numbering for the 5x5 matrix
    # |16|15|14|13|12|
    # |17| 0| 1| 2|11|
    # |18| 3| 4| 5|10|
    # |19| 6| 7| 8| 9|
    # |20|21|22|23|24|
    if 15 <= position <= 17:
        return 0
    elif 19 <= position <= 21:
        return 6
    elif 11 <= position <= 13:
        return 2
    elif position == 9 or position == 23 or position == 24:
        return 8
    elif position == 14:
        return 1
    elif position == 22:
        return 7
    elif position == 18:
        return 3
    elif position == 10:
        return 5

def generateProbabilitiyMatrix():
	with open('movements_particle_filtering.txt', 'r') as file:
		data = file.read().replace('\n', '$')
	movements_list = data.split('$')
	readings_list = []

	for reading in movements_list:
		val = reading.split('  ')
		dict = {'Given Position': int(val[0]), 'Given Orientation': val[1], 'Recorded Position': int(val[2]),
				'Recorded Orientation': val[3]}
		readings_list.append(dict)

	output_file = open('probabilities.txt', 'ab+')
	output_writer = csv.writer(output_file)

	probability_matrix = []

	for index in range(0, 27):
		count = [0] * 27
		for val in range(0, 10):
			index_value = val * 27 + index
			if (readings_list[index_value]['Given Position'] == readings_list[index_value]['Recorded Position']) and (
					readings_list[index_value]['Given Orientation'] == readings_list[index_value]['Recorded Orientation']):
				count[index] += 1
			elif readings_list[index_value]['Given Position'] == readings_list[index_value]['Recorded Position']:
				if readings_list[index_value]['Recorded Orientation'] == 'left':
					if readings_list[index_value]['Given Orientation'] == 'right':
						count[index + 1] += 1
					elif readings_list[index_value]['Given Orientation'] == 'still':
						count[index + 2] += 1
				if readings_list[index_value]['Recorded Orientation'] == 'right':
					if readings_list[index_value]['Given Orientation'] == 'left':
						count[index + 1] += 1
					elif readings_list[index_value]['Given Orientation'] == 'still':
						count[index - 1] += 1
				if readings_list[index_value]['Recorded Orientation'] == 'still':
					if readings_list[index_value]['Given Orientation'] == 'left':
						count[index - 2] += 1
					elif readings_list[index_value]['Given Orientation'] == 'right':
						count[index - 1] += 1
			elif readings_list[index_value]['Recorded Position'] < 9:
				if readings_list[index_value]['Recorded Orientation'] == 'left':
					new_index = readings_list[index_value]['Recorded Position'] * 3
					count[new_index] += 1
				elif readings_list[index_value]['Recorded Orientation'] == 'right':
					new_index = readings_list[index_value]['Recorded Position'] * 3 + 1
					count[new_index] += 1
				elif readings_list[index_value]['Recorded Orientation'] == 'still':
					new_index = readings_list[index_value]['Recorded Position'] * 3 + 2
					count[new_index] += 1
			elif readings_list[index_value]['Recorded Position'] > 9:
				if readings_list[index_value]['Recorded Orientation'] == 'left':
					new_index = find_position(readings_list[index_value]['Recorded Position']) * 3
					count[new_index] += 1
				elif readings_list[index_value]['Recorded Orientation'] == 'right':
					new_index = find_position(readings_list[index_value]['Recorded Position']) * 3 + 1
					count[new_index] += 1
				elif readings_list[index_value]['Recorded Orientation'] == 'still':
					new_index = find_position(readings_list[index_value]['Recorded Position']) + 2
					count[new_index] += 1
			temp_count = [float(k) / 10 for k in count]

		output_writer.writerow(temp_count)

	# Print the probability matrix to the output file
	for i in probability_matrix:
		for j in i:
			output_file.write(str(j) + ',')
		output_file.write('\n')
