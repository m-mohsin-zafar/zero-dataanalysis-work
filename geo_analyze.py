# Name: Muhammad Mohsin Zafar
# Roll No. MS-18-ST-504826

import distance
import numpy as np
import geo_data
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D


# Returns a square matrix/array containing pairwise distances
def populate_pairwise_distance():
    # Input filename to fetch data from
    data = geo_data.get_data_as_array("countries.csv")

    result_size = data.shape[0]
    result = np.zeros((result_size, result_size))

    i = 0
    for row in data:

        j = 0
        for brow in data:
            dist = distance.get_distance_kms(row[2], row[3], brow[2], brow[3])
            result[i, j] = dist

            j += 1

        i += 1

    return result


# Plots the resultant pairwise square matrix to 3D histogram
# Personally, this approach is a mess, it would have been better if
# 240 sub plots were made
def plot_result(xdata):
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')

    x_data, y_data = np.meshgrid(np.arange(xdata.shape[1]),
                                 np.arange(xdata.shape[0]))

    x_data = x_data.flatten()
    y_data = y_data.flatten()
    z_data = xdata.flatten()
    ax1.bar3d(x_data,
              y_data,
              np.zeros(len(z_data)),
              1, 1, z_data)
    ax1.set_xlabel('Capitals')
    ax1.set_ylabel('Capitals')
    ax1.set_zlabel('Distance')

    plt.show()


# Finds Closest and Farthest Capital For every Capital
# This calculation is based simply on maximum and minimum distances
# Palestine/Jerusalem might deviate from the results because I was considering
# min values except for zero.
# Anyway, We don't accept Jerusalem, for us there exists only the 'Palestine'
# Indexes for max and min values are calculated here which are then used to find out the capitals
def get_closest_and_farthest_capitals(pairwise_array):
    cnf_array = np.zeros((pairwise_array.shape[0], 2))
    r = 0
    for row in pairwise_array:
        # minval = np.min(row[np.nonzero(row)])
        # maxval = np.max(row[np.nonzero(row)])
        minval_index = np.argmin(row[np.nonzero(row)])
        maxval_index = np.argmax(row[np.nonzero(row)])
        if minval_index > r:
            cnf_array[r, 0] = minval_index + 1
        else:
            cnf_array[r, 0] = minval_index
        if maxval_index > r:
            cnf_array[r, 1] = maxval_index + 1
        else:
            cnf_array[r, 1] = maxval_index

        r += 1

    return cnf_array


# In response to Question 2 of the Assignment, a new file is written in csv format
# Thus file contains all the original data along with two additional columns
# Which are Closest Capital & Farthest Capital
# These closes and farthest capital values are calculated via function:
# get_closest_and_farthest_capitals(pairwise_array)
def write_cnf_data_to_file(close_n_far_vals, original_data):
    with open('output_q2.csv', mode='w', encoding='utf-8') as outputfile:
        ofilewriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

        ofilewriter.writerow(['country', 'capital', 'latitude', 'longitude', 'closest_capital', 'farthest_capital'])

        capitals = original_data[:, 1]
        r = 0
        for row in original_data:
            close_index = close_n_far_vals[r, 0].astype(int)
            farth_index = close_n_far_vals[r, 1].astype(int)
            ofilewriter.writerow([row[0], row[1], row[2], row[3],
                                  capitals[close_index], capitals[farth_index]])
            r += 1


# Two Farthest Capitals are calculated simply from analyzing maximum distance
def find_two_farthest_of_all_capitals(pairwise_array, original_data):

    r = 0
    second_index = 0
    maxval = 0
    maxval_index = 0
    for row in pairwise_array:
        if np.max(row[np.nonzero(row)]) > maxval:
            maxval = np.max(row[np.nonzero(row)])
            maxval_index = np.argmax(row[np.nonzero(row)]).astype(int)
            if maxval_index > r:
                maxval_index += 1
            second_index = r

        r += 1

    capitals = original_data[:, 1]

    capital_a = capitals[maxval_index]
    capital_b = capitals[second_index]
    dist = maxval

    return capital_a, capital_b, dist


# Two Closest Capitals are calculated simply from analyzing minimum distance
def find_two_closest_of_all_capitals(pairwise_array, original_data):

    r = 0
    second_index = 0
    minval = 20000
    minval_index = 0
    for row in pairwise_array:
        if np.min(row[np.nonzero(row)]) < minval:
            minval = np.min(row[np.nonzero(row)])
            minval_index = np.argmin(row[np.nonzero(row)])
            if minval_index > r:
                minval_index += 1
            second_index = r

        r += 1

    capitals = original_data[:, 1]

    capital_a = capitals[minval_index]
    capital_b = capitals[second_index]
    dist = minval

    return capital_a, capital_b, dist


# Most Isolated Capital of all is calculated by calculating mean value of distance for
# each capital from all other capitals (self inclusive) and then checking for maximum
# mean value
def find_isolated_of_all_capitals(pairwise_array, original_data):

    avg_distance = 0
    index = 0
    r = 0
    for row in pairwise_array:
        if np.mean(row) > avg_distance:
            avg_distance = np.mean(row)
            index = r

        r += 1

    capitals = original_data[:, 1]
    isolated_capital = capitals[index]

    return isolated_capital, avg_distance


# Most Closest Capital to most of the other capitals  is calculated by calculating mean value of distance for
# each capital from all other capitals (self inclusive) and then checking for minimum
# mean value
def find_closest_to_most_capitals(pairwise_array, original_data):

    avg_distance = 14000
    index = 0
    r = 0
    for row in pairwise_array:
        if np.mean(row) < avg_distance:
            avg_distance = np.mean(row)
            index = r

        r += 1

    capitals = original_data[:, 1]
    close_capital = capitals[index]

    return close_capital, avg_distance


# A capital with approximately equal distances to most capitals is found by
# calculating standard deviation and the analyzing based on minimum deviation
def find_equidistant_to_most_capitals(pairwise_array, original_data):

    standard_deviation_dist = 14000
    index = 0
    r = 0
    for row in pairwise_array:
        if np.std(row) < standard_deviation_dist:
            standard_deviation_dist = np.std(row)
            index = r

        r += 1

    capitals = original_data[:, 1]
    close_capital = capitals[index]

    return close_capital, standard_deviation_dist


# Test Code
if __name__ == '__main__':
    # print("Contents of Resultant Array are: \n", populate_pairwise_distance())
    original = geo_data.get_data_as_array("countries.csv")
    data = populate_pairwise_distance()
    closenfarth = get_closest_and_farthest_capitals(data)
    # write_cnf_data_to_file(closenfarth, original)
    # plot_result(data)
    print("Closest of All", find_two_closest_of_all_capitals(data, original))
    print("Farthest of All", find_two_farthest_of_all_capitals(data, original))
    print("Isolated of All", find_isolated_of_all_capitals(data, original))
    print("Close to Most Capitals", find_closest_to_most_capitals(data, original))
    print("Equidistant to Most Capitals", find_equidistant_to_most_capitals(data, original))


