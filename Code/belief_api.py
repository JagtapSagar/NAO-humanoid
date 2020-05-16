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
# This script MUST be executed after the cpt.py script. This takes the CPT information
# and generates the belief network.
#
# Main Method: generateBN()
#
# REQUIRES PYTHON 2.7 TO EXECUTE
#
####################################################################################


from cpt import ReadInCPTs
Location, Angle, SL, SR, Landmark = ReadInCPTs()[:-1]


def belief(sonar_left, sonar_right, landmark, total_yaw):
    # Returns belief of what location NAO might be in

    bn = []
    list_index = []
    location_index = []  # Stores index of Location node after sampling
    # angle_index = []  # Stores index of Angle node after sampling
    landmark_index = []  # Stores index of Landmark node

    # Checking for indices where landmark inputs match
    count = 0
    for land in Landmark:
        if land[2] == str(total_yaw):
            # Checks if probability is non-zero
            # If input evidence is True, then skipping over locations with zero probability of landmark detection
            if ('TRUE' == landmark or 'True' == landmark) and float(land[4]) != 0.0:
                landmark_index.append(count)
            # If input evidence is False, then skipping over locations with non-zero probability of landmark detection
            elif ('False' == landmark or 'False' == landmark) and float(land[4]) == 0.0:
                landmark_index.append(count)
        count += 1

    # Shifting landmark indices to beginning of their x,y position for location index
    for index in landmark_index:
        location_index.append(index - index % 32)

    # Checking whether any of the potential locations match with sonar values
    for index in location_index:
        for num in range(0, 32):
            if (SL[index + num][int(sonar_left * 100) + 3] != str(0.0)) and (
                    SR[index + num][int(sonar_right * 100) + 3] != str(0.0)):
                # if match found, add index to list
                list_index.append(index + num)

    if len(list_index) == 0:
        # If none of the potential locations have probabilities for input sonar data
        print "Returning empty belief list"
    else:
        # If any of the potential locations have probabilities for input sonar data
        for i in list_index:
            bn.append([Location[i][0], Location[i][1], Location[i][2]])
    return bn


def generateBN():
    sonar_left = float(raw_input("Enter Left Sonar Data (0-2.95): "))
    sonar_right = float(raw_input("Enter Right Sonar Data (0-1.97): "))
    landmark = raw_input("Enter landmark (TRUE/False): ")
    total_yaw = float(raw_input("Enter total yaw (0-360) in multiple of 11.25 degrees: "))

    bn = belief(sonar_left, sonar_right, landmark, total_yaw)
    if len(bn) == 0:
        print("Zero probabilities for some sensor values")
    else:
        print("belief(x,y,heading_angle): \n", bn)
