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
# This script gets the data and weight information and generates the expected transition step.
#
# Main Method: getTransitionStep()
#
# REQUIRES PYTHON 2.7 TO EXECUTE
#
####################################################################################

from random import randint, seed
from datetime import datetime
import csv


def normalize(w1, w2):
    # Function to normalize weights
    total_weight = w1 + w2
    return [w1 / total_weight, w2 / total_weight]


def random_sample():
    # Function to generate Pseudo-random numbers for sampling
    # seed random number generator
    seed(datetime.now())
    return randint(0, 100)


def transition_for_action():
    # Returns transition probabilities for any action command
    transition_line = 0
    for i in range(0, 9):
        if action_pos == str(i):
            if action_ori == "L":
                transition_line = i * 3
            elif action_ori == "R":
                transition_line = (i * 3) + 1
            else:
                transition_line = (i * 3) + 2
            break
    return Transition_total[transition_line]


def state_to_coordinate(state, angle):
    # Function to map estimates state to coordinates
    # Note: Action Input only asks for +/-90 deg rotation.
    # Following code only takes 90 deg rotations into account
    x = 0
    y = 0
    if angle == 0 or angle == 180:
        if state in [0, 3, 6]:
            x = int(X) - (1 if angle == 0 else -1)
        elif state in [1, 4, 7]:
            x = int(X)
        else:
            x = int(X) + (1 if angle == 0 else -1)
        if state in [0, 1, 2]:
            y = int(Y) + (1 if angle == 0 else -1)
        elif state in [3, 4, 5]:
            y = int(Y)
        else:
            y = int(Y) - (1 if angle == 0 else -1)
    elif angle == abs(90):
        if state in [0, 3, 6]:
            y = int(Y) + (1 if angle == 90 else -1)
        elif state in [1, 4, 7]:
            y = int(Y)
        else:
            y = int(Y) - (1 if angle == 90 else -1)
        if state in [0, 1, 2]:
            x = int(X) + (1 if angle == 90 else -1)
        elif state in [3, 4, 5]:
            x = int(X)
        else:
            x = int(X) - (1 if angle == 90 else -1)

    if not (0 <= x <= 3) or not (0 <= y <= 7):
        # Assuming it bumps into walls outside this range
        x = int(X)
        y = int(Y)
    return x, y

def getTransitionStep(LOCATION_INPUT_CSV_FILENAME = 'location.csv', ANGLE_INPUT_CSV_FILENAME = 'angle.csv',
					  LANDMARK_INPUT_CSV_FILENAME = 'landmark.csv', SENSOR_LEFT_INPUT_CSV_FILENAME = 'sensorLeft.csv',
					  SENSOR_RIGHT_INPUT_CSV_FILENAME = 'sensorRight.csv', PROBABILITIES_INPUT_TXT_FILENAME = 'probabilities.txt'):
	Location = []
	Angle = []
	Landmark = []
	SL = []
	SR = []
	Transition_total = []
	torso_angle = 0
	###########################################################
	# Reading CPT's
	###########################################################


	with open(LOCATION_INPUT_CSV_FILENAME) as csv_location:
		location_reader = csv.reader(csv_location, delimiter=',')
		line_count = 0
		for row in location_reader:
			if line_count > 0:
				Location.append(row)
			line_count += 1

	with open(ANGLE_INPUT_CSV_FILENAME) as csv_angle:
		angle_reader = csv.reader(csv_angle, delimiter=',')
		line_count = 0
		for row in angle_reader:
			if line_count > 0:
				Angle.append(row)
			line_count += 1

	with open(LANDMARK_INPUT_CSV_FILENAME) as csv_land:
		land_reader = csv.reader(csv_land, delimiter=',')
		line_count = 0
		for row in land_reader:
			if line_count > 0:
				Landmark.append(row)
			line_count += 1

	with open(SENSOR_LEFT_INPUT_CSV_FILENAME) as csv_SL:
		SL_reader = csv.reader(csv_SL, delimiter=',')
		line_count = 0
		for row in SL_reader:
			if line_count > 0:
				SL.append(row)
			line_count += 1

	with open(SENSOR_RIGHT_INPUT_CSV_FILENAME) as csv_SR:
		SR_reader = csv.reader(csv_SR, delimiter=',')
		line_count = 0
		for row in SR_reader:
			if line_count > 0:
				SR.append(row)
			line_count += 1

	with open(PROBABILITIES_INPUT_TXT_FILENAME) as csv_transition:
		transition_reader = csv.reader(csv_transition, delimiter=',')
		for row in transition_reader:
			Transition_total.append(row)

	###########################################################
	# User Inputs
	###########################################################
	print("For t = 0:")
	# Enter starting cell position
	X = raw_input("Enter integer Start Column (0-3): ")
	Y = raw_input("Enter integer Start Row (0-7)   : ")
	# Assuming start at position 4 with orientation S (0 deg)

	# Enter Action
	action_pos = raw_input("Enter goal position (0-9)      : ")
	action_ori = raw_input("Enter goal orientation (S,L,R) : ")

	# Enter Evidence
	print("Evidence for t = 1:")
	SL_evidence = float(raw_input("Sonar Left Evidence (0-2.95)   : "))
	SR_evidence = float(raw_input("Sonar Right Evidence (0-1.97)  : "))
	Landmark_evidence = raw_input("Landmark Detection (True/False): ")

	if ((not (0 <= int(X) <= 3)) or (not (0 <= int(Y) <= 7)) or (not (0 <= int(action_pos) <= 8))
		or (not (action_ori in ['S', 'L', 'R'])) or (not (0.0 <= SL_evidence <= 2.95))
		or (not (0.0 <= SR_evidence <= 1.97)) or (not (Landmark_evidence in ['True', 'False']))):
		print("Values invalid or out of range\nExiting program")
		exit()

	###########################################################
	# Retrieving action probabilities
	transitions = transition_for_action()
	print("transition probabilities for location at next time-step:\n" + str(transitions))

	# Random number sampling of transition
	count = 0
	total = 0
	pseudo_rand = random_sample()
	for j in transitions:
		total += float(j)
		if (total >= float(pseudo_rand) / 100):
			break
		else:
			count += 1

	# Retrieving state and orientation after sampling
	if (count % 3 == 0):
		sampled_orientation = "L"
		torso_angle -= 90
	elif ((count - 1) % 3 == 0):
		sampled_orientation = "R"
		torso_angle += 90
	else:
		sampled_orientation = "S"
	sampled_position = int(float(count) / 3)

	# Random number sampling of Angle node
	head_yaw = 0.0
	total_yaw = 0.0
	angle_count = 0
	total = 0
	pseudo_rand = random_sample()
	for angle in Angle:
		total += float(angle[2])
		if (total >= float(pseudo_rand) / 100):
			break
		else:
			angle_count += 1

	head_yaw = head_yaw + float(Angle[angle_count][0])

	# torso_angle is robots angle with respect to the world or labyrinth's coordinate frame
	if (torso_angle < 0):
		torso_angle += 360
	elif (torso_angle >= 360):
		torso_angle -= 360
		
	# total yaw is head yaw wrt the world frame
	total_yaw = head_yaw + torso_angle
	if (total_yaw < 0):
		total_yaw += 360
	elif (total_yaw >= 360):
		total_yaw -= 360

	# Getting part of index value to locate row with total_yaw for estimate position in landmark
	angle_count = 0
	for i in range(0, 320, 10):
		if (total_yaw == i*1.125):
			break
		angle_count += 1

	# Retrieving coordinates of estimated state
	x_estimate, y_estimate = state_to_coordinate(sampled_position, torso_angle)

	sampled_location = [x_estimate, y_estimate, sampled_orientation]
	print("Estimated Location: " + str(sampled_location))

	line_count = 0
	for i in Location:
		if ((i[0] == str(x_estimate)) and (i[1] == str(y_estimate)) and (float(i[2]) == torso_angle)):
			break
		line_count += 1
	location_count = line_count

	# Initial weights for SonarLeft, SonarRight, Landmark respectively
	W = [1.0, 1.0, 1.0]
	W_normalized = []

	W[0] = W[0] * float(SL[location_count][int(float(SL_evidence) * 100) + 3])
	W[1] = W[1] * float(SR[location_count][int(float(SR_evidence) * 100) + 3])


	landmark_count = location_count - int(torso_angle / 11.25) + angle_count
	
	# Note: This code has not been updated yet to account for landmark probabilities. 
	#	It works on an earlier assumption that if landmark is true the probability is high.
	#	Change/correction is pending.
	
	W[2] = W[2] * (0.95 if (Landmark[landmark_count][4] == Landmark_evidence) and (total_yaw == float(Landmark[landmark_count][2])) else 0.05)
	# W_normalized = normalize(W[0], W[1], W[2])
	print("Weights for [SL, SR, Landmark] evidences = " + str(W))

	# Probability of being in estimated location
	P_location = float(Location[location_count][3])
	P_not_location = 1 - P_location

	# Probability of transitioning to current state
	P_transition_from_same_state = float(transitions[count])
	P_transition_from_other_state = 1 - P_transition_from_same_state

	Prob_of_state = P_location * P_transition_from_same_state + P_not_location * P_transition_from_other_state
	Prob_of_not_state = P_not_location * P_transition_from_same_state + P_location * P_transition_from_other_state

	# Weights for evidences
	Weights = W[0] + W[1] + W[2]

	Prob_1 = [Prob_of_state * W[0], Prob_of_state * W[1], Prob_of_state * W[2]]
	Prob_2 = [Prob_of_not_state * (1 - W[0]), Prob_of_not_state * (1 - W[1]), Prob_of_not_state * (1 - W[2])]
	Prob_of_state = 0.0
	Prob_of_not_state = 0.0
	for i in range(0, len(Prob_1)):
		Prob_of_state += Prob_1[i]
	for i in range(0, len(Prob_2)):
		Prob_of_not_state += Prob_2[i]
	Prob_of_state, Prob_of_not_state = normalize(Prob_of_state, Prob_of_not_state)
	print("Probability of current location: " + str(Prob_of_state))

	# Probability of state can now be pushed on to the respective location_count row in Location node before the next iteration
