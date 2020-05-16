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
# This program is part of milestone 2. It implements a function to return Probability using likelihood weighting
# Returns: distribution of P(L|SL,SR,Lmark)
#
# Main Method: generateLiklihoodWeighting()
#
# REQUIRES PYTHON 2.7 TO EXECUTE
#
####################################################################################

from random import seed, randint
from datetime import datetime
from cpt import ReadInCPTs

Location, Angle, SL, SR, Landmark = ReadInCPTs()[:-1]
arg_list = []


def random_sample(length):
    # Function to generate Pseudorandom numbers for sampling
    # seed random number generator
    seed(datetime.now())
    num = []
    for i in range(length):
        num.append(randint(0, 100))
    return num


def likelihood_weighting(evidence, N):
    # Function returns probability distribution of Location given Sonar and landmark values as evidences

    nodes = ["Location", "Angle", "SL", "SR", "Landmark"]
    # Initial weight
    weight_all = 1.0
    x = {}
    W = {}  # Returned distribution

    # Evidence keys to filter through
    sl_key = 'SL(' + str(format(float(evidence['SL'][0]), '.2f')) + ')'
    sr_key = 'SR(' + str(format(float(evidence['SR'][0]), '.2f')) + ')'
    lmark_key = (evidence["Landmark"][0]).upper()

    for n in range(N):
        arguments = ""  # (L|SL, SR, Lmark)
        weight = 1.0  # Initial weight for sample
        location_index = 0  # Stores index of Location node after sampling
        angle_index = 0  # Stores index of Angle node after sampling
        landmark_index = 0  # Stores index of Landmark node
        sl_sampled = 0.0  # Used when evidence does not exit
        sr_sampled = 0.0  # Used when evidence does not exist

        # Generating pseudo-random numbers for non-evidence nodes
        sample = random_sample(len(nodes) - len(evidence))  # Used for sampling non-evidence nodes

        # Scanning each node in our Belief network to separate evidence variables from non-evidence
        for node in nodes:
            if node in evidence:
                if node == "Landmark":
                    # Taking both head and torso angles into account
                    total_yaw = float(Location[location_index][2]) + float(Angle[angle_index][0])
                    if total_yaw >= 360:
                        total_yaw -= 360

                    # Searching for index value
                    landmark_index += location_index
                    if float(Landmark[landmark_index][2]) > total_yaw:
                        landmark_index = location_index - 31
                    for index in Landmark[landmark_index:]:
                        if float(index[2]) == total_yaw:
                            break
                        landmark_index += 1
                    # Computing weight
                    if (evidence["Landmark"][0]).upper() == 'TRUE':
                        # If evidence says landmark detected
                        if float(Landmark[landmark_index][4]) > 0.0:
                            # Using probability of detection
                            weight = weight * float(Landmark[landmark_index][4])
                        else:
                            # Giving lesser weight to fields with zero probability
                            weight = weight * 0.05  # float(random_sample(1)[0])*0.01
                    else:
                        # If evidence says landmark not detected
                        if float(Landmark[landmark_index][4]) > 0.0:
                            # Using probability of not detection: 1-P(detection)
                            weight = weight * (1 - float(Landmark[landmark_index][4]))
                        else:
                            # Using high weight for not detection
                            weight = weight * 0.95  # float(random_sample(1)[0])*0.01
                    arguments += "Lmark(" + ("TRUE" if float(Landmark[landmark_index][4]) > 0.0 else "FALSE") + ")"

                elif node == "SL":
                    # Checking if given Sonar Left evidence exists
                    # If not, then sampling Sonar Left

                    if float(SL[location_index][int(float(evidence["SL"][0]) * 100) + 3]) == 0.0:
                        total = 0.0
                        randnum = random_sample(1)[0]

                        # Sonar Left data only exists in range 0 to 2.95
                        for index in range(3, 299):
                            total += float(SL[location_index][index])
                            if total >= float(randnum) / 100:
                                sl_sampled = float(index) / 100
                                arguments += "SL(" + str(format(sl_sampled, '.2f')) + "),"
                                break

                        # Computing weight
                        weight = weight * float(SL[location_index][int(sl_sampled * 100)])
                    else:
                        weight = weight * float(SL[location_index][int(float(evidence["SL"][0]) * 100) + 3])
                        arguments += "SL(" + str(format(float(evidence["SL"][0]), '.2f')) + "),"

                else:  # node == "SR"
                    # Checking if given Sonar Right evidence exists
                    # If not, then sampling Sonar Right'

                    if float(SR[location_index][int(float(evidence["SR"][0]) * 100) + 3]) < 0.01:
                        total = 0.0
                        randnum = random_sample(1)[0]

                        # Sonar Right data only exists in range 0 to 1.97
                        for index in range(3, 198):
                            total += float(SR[location_index][index])
                            if total >= float(randnum) / 100:
                                sr_sampled = float(index) / 100
                                arguments += "SR(" + str(format(sr_sampled, '.2f')) + "),"
                                break

                        # Computing weight
                        weight = weight * float(SR[location_index][int(sr_sampled * 100)])
                    else:
                        weight = weight * float(SR[location_index][int(float(evidence["SR"][0]) * 100) + 3])
                        arguments += "SR(" + str(format(float(evidence["SR"][0]), '.2f')) + "),"

            elif node == "Location":
                # Search for Location index
                total = 0.0
                for index in Location:
                    total += float(index[3])
                    if total < float(sample[0]) / 100:
                        location_index += 1
                    else:
                        break
                # [:-2] if query over position only, [:-1] for all of location parameters
                arguments += "L(" + str(Location[location_index][:-2]) + "),"

            elif node == "Angle":
                # Search for Angle index
                total = 0.0
                for index in Angle:
                    total += float(index[2])
                    if total >= float(sample[1]) / 100:
                        break
                    else:
                        angle_index += 1
                # Neither query nor evidence. Therefore, update to argument not needed
                # arguments += "A(" + str(Angle[angle_index][:-1]) + "),"

        # Adding processed sample to dictionary
        # Summing if previously processed sample is a match

        if arguments in x:
            x[arguments] += weight
        else:
            x[arguments] = weight

    for key in x:
        if ((sl_key in key) and (sr_key in key) and (lmark_key in key)):
            print lmark_key, key, x[key]
            W[key] = x[key]

    for key in W:
        weight_all += W[key]

    for key in W:
        W[key] = W[key] / weight_all

    return W  # distribution of W / weight_all


def generateLiklihoodWeighting():
    # A function call to likelihood_weighting() requires following prerequisite inputs and variables
    N = int(raw_input("Enter sampling number: "))
    evidence = {"SL": [],
                "SR": [],
                "Landmark": []}

    # Enter evidence values
    sl_evidence = raw_input('Enter Sonar Left Evidence (0-2.95): ')
    sr_evidence = raw_input('Enter Sonar Right Evidence (0-1.97): ')
    # torso_evidence = float(raw_input('Enter angle: '))
    landmark_evidence = raw_input('Enter Landmark Evidence (TRUE/FALSE): ')
    evidence["SL"].append(sl_evidence)
    evidence["SR"].append(sr_evidence)
    evidence["Landmark"].append(landmark_evidence)

    if len(evidence["SL"]) == len(evidence["SR"]) and len(evidence["SR"]) == len(evidence["Landmark"]):
        distribution = likelihood_weighting(evidence, N)

        print("Length of distribution return: " + str(len(distribution)))
        print("Probability distribution: " + str(distribution))
    else:
        print("Not enough or too many inputs provided")
