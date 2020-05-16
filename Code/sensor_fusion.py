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
# This script reads in the sensor_data.csv file generated from the mod_tornado.py script
# and finds the landmark and sonar CPTs.
# It generates landmark.csv, sensorLeft.csv, and sensorRight.csv (or whatever CSV filenames are inputted)
# The order of the CPTs generated followed the order in which readings were recorded. This was changed in the
# newly generated CPTs by hand.
#
# Assumptions:
# + Maze has 4 columns and 8 rows
# + All initial probabilities are 1/32
# + Circle Degree correction of 1.125 is needed
#
# Main Method: generateLandmarkAndSonarTPs()
#
# REQUIRES PYTHON 2.7 TO EXECUTE
#
####################################################################################

import csv


def generateLandmarkAndSonarTPs(SENSOR_INPUT_CSV_FILENAME='sensor_data.csv',
                                LANDMARK_OUTPUT_CSV_FILENAME='landmark.csv',
                                LEFT_SENSOR_OUTPUT_CSV_FILENAME='sensorLeft.csv',
                                RIGHT_SENSOR_OUTPUT_CSV_FILENAME='sensorRight.csv'):
    data = []
    headers = []

    with open(SENSOR_INPUT_CSV_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                headers = row
            else:
                data.append(row)
            line_count += 1

        # print len(data)

    #######################################################
    # CONSTANTS
    #######################################################
    # This constant fixes the hack in the data that says a complete circle is 320 degrees not 360.
    CIRCLE_DEGREE_CORRECTION = 1.125

    #######################################################
    # Location node (x,y,Gamma)
    # (X,Y) ==> (Column, Row) ==> Positions
    # Gamma ==> Torso Angle/Body Yaw in Degrees
    #######################################################
    # All initial Probabilities will be 4*8*32 ==> 1/1024
    # This file is only used for indexing and sampling

    num_columns = 4
    num_rows = 8

    f_l = open("location.csv", "ab+")
    loc_writer = csv.writer(f_l)

    # Writing file headers
    loc_writer.writerow(["Column", "Row", "Angle", "P(Location)"])

    for x in range(0, num_columns):
        for y in range(0, num_rows):
            for gamma in range(0, 311, 10):
                loc_writer.writerow([x, y, (gamma * CIRCLE_DEGREE_CORRECTION), (float(1) / 1024)])

    #######################################################
    # Angle node (Alpha, Beta)
    # Alpha ==> Head Yaw
    # Beta ==> Head Pitch (Taken as 0 fixed)
    #######################################################
    # All initial Probabilities will be 1/32
    # This file is only used for indexing and sampling

    f_angle = open("angle.csv", "ab+")
    ang_writer = csv.writer(f_angle)

    # Writing file headers
    ang_writer.writerow(["Alpha", "Beta", "P(Angle)"])

    for alpha in range(0, 311, 10):
        for beta in range(0, 1):
            ang_writer.writerow([(alpha * CIRCLE_DEGREE_CORRECTION), beta, (float(1) / 32)])

    #######################################################
    # Landmark Node
    # Parent Nodes: Location, Angles
    # Variables: x, y, gamma+alpha, Beta, P(Landmarks)
    #######################################################

    # Creating File to store landmark output
    # Implementation 1: Probability of landmark detection
    f_lmark = open(LANDMARK_OUTPUT_CSV_FILENAME, "ab+")
    L_writer = csv.writer(f_lmark)

    # Writing file header
    L_writer.writerow(["Column", "Row", "Angle (Body + Head Yaw)", "Head Pitch", "Landmark Detection"])
    print "Creating Landmark CPT"

    index = 0
    landmark_count = [0.0] * 1024
    for x in range(0, num_columns):
        for y in range(0, num_rows):
            for yaw in range(0, 311, 10):
                count = 0
                # Checking for landmark detection for any (x,y,yaw) in all 5 runs
                if not x % 2:
                    for i in range(0, 5):
                        row = data[index + (1024 * i)]
                        if row[0] == str(x) and row[1] == str(y) and row[2] == str(yaw) and (
                                row[7] == 'TRUE' or row[7] == 'True'):
                            landmark_count[index] += 1
                        count += 1
                else:
                    for i in range(0, 5):
                        for row in data[index + (1024 * i) - (index % 32):index + (1024 * i) - (index % 32) + 32]:
                            if row[0] == str(x) and row[1] == str(7 - y) and row[2] == str(yaw) and (
                                    row[7] == 'TRUE' or row[7] == 'True'):
                                landmark_count[index] += 1
                            count += 1
                if count != 0:
                    landmark_count[index] /= count
                if not x % 2:
                    print x, y, yaw
                    L_writer.writerow([x, y, (yaw * CIRCLE_DEGREE_CORRECTION), 0, landmark_count[index]])
                else:
                    print x, 7 - y, yaw
                    L_writer.writerow([x, 7 - y, (yaw * CIRCLE_DEGREE_CORRECTION), 0, landmark_count[index]])
                index += 1

    '''
    # Implementation 2: Probability of 3 individual landmark detection

    # Creating File to store landmark output
    f_lmark2 = open(LANDMARK_OUTPUT_CSV_FILENAME, "ab+")
    L_writer2 = csv.writer(f_lmark2)

    # Writing file header
    L_writer2.writerow(
        ["Column", "Row", "Angle (Body + Head Yaw)", "Head Pitch", "Landmark 68 (58-74)", "Landmark 85 (75-95)", "Landmark 112 (102-122)"])
    print "Creating Landmark CPT"

    index = 0
    landmark1_count = [0.0] * 1024
    landmark2_count = [0.0] * 1024
    landmark3_count = [0.0] * 1024
    for x in range(0, num_columns):
        for y in range(0, num_rows):
            for yaw in range(0, 311, 10):
                # Checking for landmark detection for any (x,y,yaw) in all 5 runs
                count = 0
                # Checking for landmark detection for any (x,y,yaw) in all 5 runs
                if not x % 2:
                    for i in range(0, 5):
                        row = data[index + (1024 * i)]
                        if row[0] == str(x) and row[1] == str(y) and row[2] == str(yaw) and (
                                row[7] == 'TRUE' or row[7] == 'True'):
                            if 58 <= int(row[8]) <= 74 or 58 <= int(row[13]) <= 74 or 58 <= int(
                                    row[18]) <= 74 or 58 <= int(row[23]) <= 74:
                                landmark1_count[index] += 1
                            elif 75 <= int(row[8]) <= 95 or 75 <= int(row[13]) <= 95 or 75 <= int(
                                    row[18]) <= 95 or 75 <= int(row[23]) <= 95:
                                landmark2_count[index] += 1
                            else:
                                landmark3_count[index] += 1
                        count += 1
                else:
                    for i in range(0, 5):
                        for row in data[index + (1024 * i) - (index % 32):index + (1024 * i) - (index % 32) + 32]:
                            if row[0] == str(x) and row[1] == str(7 - y) and row[2] == str(yaw) and (
                                    row[7] == 'TRUE' or row[7] == 'True'):
                                if row[0] == str(x) and row[1] == str(y) and row[2] == str(yaw) and (
                                        row[7] == 'TRUE' or row[7] == 'True'):
                                    if 58 <= int(row[8]) <= 74 or 58 <= int(row[13]) <= 74 or 58 <= int(
                                            row[18]) <= 74 or 58 <= int(row[23]) <= 74:
                                        landmark1_count[index] += 1
                                    elif 75 <= int(row[8]) <= 95 or 75 <= int(row[13]) <= 95 or 75 <= int(
                                            row[18]) <= 95 or 75 <= int(row[23]) <= 95:
                                        landmark2_count[index] += 1
                                    else:
                                        landmark3_count[index] += 1
                            count += 1
                if count != 0:
                    landmark1_count[index] /= count
                    landmark2_count[index] /= count
                    landmark3_count[index] /= count
                if not x % 2:
                    print x, y, yaw
                    L_writer2.writerow(
                        [x, y, (yaw * CIRCLE_DEGREE_CORRECTION), 0, landmark1_count[index], landmark2_count[index],
                         landmark3_count[index]])
                else:
                    print x, 7 - y, yaw
                    L_writer2.writerow(
                        [x, 7 - y, (yaw * CIRCLE_DEGREE_CORRECTION), 0, landmark1_count[index], landmark2_count[index],
                         landmark3_count[index]])
                index += 1
    '''

    #######################################################
    # Sonar Left (Probabilities for Location node)
    # Parent Nodes: Location
    # Variables: x, y, gamma, P(Sonar data)
    #######################################################

    # Creating File to store SL output
    f_sl = open(LEFT_SENSOR_OUTPUT_CSV_FILENAME, "ab+")
    SL_writer = csv.writer(f_sl)

    # Writing file header
    SL_list = [str(float(p) / 100) for p in range(0, 296)]
    SL_writer.writerow(["Column", "Row", "Angle"] + SL_list)

    print "Creating Sonar Left CPT"
    SL_max = 296  # 2.96
    index = 0

    for x in range(0, num_columns):
        for y in range(0, num_rows):
            for gamma in range(0, 311, 10):
                sensor_count = 0  # Keeps track of sensor value being counted
                SL_prob = [0.00] * SL_max
                row_sum = 0
                for sensor_left in range(0, SL_max):
                    # Resetting count before each sonar value
                    count = 0

                    if not x % 2:
                        # Counting a sensor value for any (x,y,gamma)
                        for i in range(0, 5):
                            row = data[index + (1024 * i)]
                            if row[0] == str(x) and row[1] == str(y) and row[2] == str(gamma) and round(float(row[5]),
                                                                                                        2) == (
                                    sensor_left * 0.01):
                                count += 1
                                row_sum += 1
                    else:
                        for i in range(0, 5):
                            for row in data[index + (1024 * i) - (index % 32):index + (1024 * i) - (index % 32) + 32]:
                                if row[0] == str(x) and row[1] == str(7 - y) and row[2] == str(gamma) and round(
                                        float(row[5]),
                                        2) == (
                                        sensor_left * 0.01):
                                    count += 1
                                    row_sum += 1

                    SL_prob[sensor_count] += (float(count))
                    # Update count for next sensor value
                    sensor_count += 1

                # print row_sum, SL_prob
                for i in range(len(SL_prob)):
                    SL_prob[i] /= row_sum
                index += 1
                if not x % 2:
                    print x, y, (gamma * 1.125)
                    SL_writer.writerow([x, y, (gamma * CIRCLE_DEGREE_CORRECTION)] + SL_prob)
                else:
                    print x, 7 - y, (gamma * 1.125)
                    SL_writer.writerow([x, 7 - y, (gamma * CIRCLE_DEGREE_CORRECTION)] + SL_prob)

    #######################################################
    # Sonar Right (Probabilities for Location node)
    # Parent Nodes: Location
    # Variables: x, y, gamma, P(Sonar data)
    #######################################################

    # Creating File to store SR output
    f_sr = open(RIGHT_SENSOR_OUTPUT_CSV_FILENAME, "ab+")
    SR_writer = csv.writer(f_sr)

    # Writing file header
    SR_list = [str(float(p) / 100) for p in range(0, 198)]
    SR_writer.writerow(["Column", "Row", "Angle"] + SR_list)

    print "Creating Sonar Right CPT"
    SR_max = 198  # 1.98
    index = 0

    for x in range(0, num_columns):
        for y in range(0, num_rows):
            for gamma in range(0, 311, 10):
                sensor_count = 0  # Keeps track of sensor value being counted
                SR_prob = [0.00] * SR_max
                row_sum = 0
                for sensor_right in range(0, SR_max):
                    # Resetting count before each sonar value
                    count = 0
                    # Counting a sensor value for any (x,y,gamma)
                    if not x % 2:
                        # Counting a sensor value for any (x,y,gamma)
                        for i in range(0, 5):
                            row = data[index + (1024 * i)]
                            if row[0] == str(x) and row[1] == str(y) and row[2] == str(gamma) and round(float(row[6]),
                                                                                                        2) == (
                                    sensor_right * 0.01):
                                count += 1
                                row_sum += 1
                    else:
                        for i in range(0, 5):
                            for row in data[index + (1024 * i) - (index % 32):index + (1024 * i) - (index % 32) + 32]:
                                if row[0] == str(x) and row[1] == str(7 - y) and row[2] == str(gamma) and round(
                                        float(row[6]),
                                        2) == (
                                        sensor_right * 0.01):
                                    count += 1
                                    row_sum += 1

                    SR_prob[sensor_count] += (float(count))
                    # Update count for next sensor value
                    sensor_count += 1

                # print row_sum, SR_prob
                for i in range(len(SR_prob)):
                    SR_prob[i] /= row_sum
                index += 1
                if not x % 2:
                    print x, y, (gamma * 1.125)
                    SR_writer.writerow([x, y, (gamma * CIRCLE_DEGREE_CORRECTION)] + SR_prob)
                else:
                    print x, 7 - y, (gamma * 1.125)
                    SR_writer.writerow([x, 7 - y, (gamma * CIRCLE_DEGREE_CORRECTION)] + SR_prob)
