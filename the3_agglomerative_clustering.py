import math
import numpy as np
import pandas as pd

'''
Read input file to get (x,y) coordinates of points. After the data is read from the file, it should return the data points
as a list of tuples.Each data point is denoted with a tuple (x,y) where "x" denotes the x-coordinate and "y" denotes 
the y-coordinate.
'''


def read_input_file(input_file_name):
    # TODO: Implement here
    # creating empty list in order to append tuples in it and return list of tuple
    result_list = []

    # open input file with open command in only readable mode
    input_file = open(input_file_name, 'r')

    # read all lines in the input file and store it in list
    lists_of_rows_in_input_files = input_file.readlines()

    # for each row read the line and delete the unnecessary parenthesis and '\n' characters
    for row in lists_of_rows_in_input_files:

        # split each line according to ',' so element[0] = "(0.40" and element[1] = "0.53)\n"
        elements_in_row = row.split(',')
        x_coordinate = elements_in_row[0]
        y_coordinate = elements_in_row[1]

        # delete the '(' from the beginning of element[0]
        x_coordinate = float(x_coordinate[1:])

        # delete the last three character which are ")\n" from element[1]
        y_coordinate = float(y_coordinate[:-2])

        # create a tuple which includes x_coordinate and y_coordinate
        new_tuple = (x_coordinate, y_coordinate)

        # add this tuple to result list
        result_list.append(new_tuple)

    # close input file
    input_file.close()

    # return the result list
    return result_list




class AgglomerativeClustering:
    LINKAGE = {
        'MIN': 0,
        'MAX': 1,
        'GROUP_AVG': 2
    }

    def __init__(self, input_data):
        self.data = input_data
        self.clusters_current = []
        # Add your member variables(if any here)

    '''
    Explanations for AgglomerativeClustering class members:

    data:                   list of tuples including input 2-D data points. 
                            Each data point is denoted with a tuple (x,y) where "x" denotes the x-coordinate and 
                            "y" denotes the y-coordinate. Ex:[(1,2),(3,4),(100,101),....]
    clusters_current:       list of lists which includes the current elements of each cluster as tuples in a list and
                            where each data point is a member of one of the clusters. 
                            Ex:[[(1,2),(3,4),..],[(100,101),(100,102),....]]

    
    *** Make sure you keep template structure that is given to you. 
    *** YOU CAN ADD TO THE template STRUCTURE, BUT CAN NOT REMOVE FROM IT. ***
    '''

    '''
    This method is the first step of the algorithm: Initialize all "n" different data points to "n" different clusters.
    This "n" clusters are kept as list of lists. This method will convert each element of self.clusters_current attribute
    into a separate list and assign the new list into self.clusters_current attribute.
    Ex:  Before this method is invoked, self.clusters_current=[(1,2),(3,4),(5,6),(7,8)]
         After this method is invoked, self.clusters_current= [[(1,2)],[(3,4)],[(5,6)],[(7,8)]]
    '''

    def initialize_clustering(self):
        # TODO: Implement here
        for each_tuple in self.data:
            # for each tuple create a new list and put tuple in it and append this list to clusters_current
            new_list = [each_tuple]
            self.clusters_current.append(new_list)


    '''This method returns the resultant clusters as the result of the clustering given the linkage. The method should
    exit the loop of the algorithm and return the resultant clusters when the number of clusters is equal the given 
    number_of_clusters argument. In order to clarify, the following example is given: Assume input data consists of 100 data points,
    number_of_clusters=3 and linkage is "MIN". Then "fit_predict" should return a list of lists where each list denotes an 
    independent cluster and includes the data points(a tuple with x,y coordinates) inside each cluster.
    Ex: [[(0,2),(1,3),...],[(10,20),(11,21),(12,22),...],[(100,100),(101,100),(102,100),...]]
    '''

    def fit_predict(self, number_of_clusters, linkage):
        # TODO: Implement here
        current_proximity_matrix = self.make_deep_copy()
        if linkage == 0:
            current_number_of_clusters = len(current_proximity_matrix)
            while current_number_of_clusters > number_of_clusters:
                clusters_with_smallest_proximity = self.find_smallest_proximity(current_proximity_matrix)

                cluster_have_to_merge_1 = self.clusters_current[clusters_with_smallest_proximity[0]]
                cluster_have_to_merge_2 = self.clusters_current[clusters_with_smallest_proximity[1]]

                self.merge_two_cluster(cluster_have_to_merge_1, cluster_have_to_merge_2)

                current_number_of_clusters = current_number_of_clusters - 1
                current_proximity_matrix = self.update_proximity_matrix_min(self.clusters_current)
            return self.clusters_current

        if linkage == 1:
            current_number_of_clusters = len(current_proximity_matrix)
            while current_number_of_clusters > number_of_clusters:
                clusters_with_smallest_proximity = self.find_smallest_proximity(current_proximity_matrix)

                cluster_have_to_merge_1 = self.clusters_current[clusters_with_smallest_proximity[0]]
                cluster_have_to_merge_2 = self.clusters_current[clusters_with_smallest_proximity[1]]

                self.merge_two_cluster(cluster_have_to_merge_1, cluster_have_to_merge_2)

                current_number_of_clusters = current_number_of_clusters - 1
                current_proximity_matrix = self.update_proximity_matrix_max(self.clusters_current)
            return self.clusters_current

        if linkage == 2:
            current_number_of_clusters = len(current_proximity_matrix)
            while current_number_of_clusters > number_of_clusters:
                clusters_with_smallest_proximity = self.find_smallest_proximity(current_proximity_matrix)

                cluster_have_to_merge_1 = self.clusters_current[clusters_with_smallest_proximity[0]]
                cluster_have_to_merge_2 = self.clusters_current[clusters_with_smallest_proximity[1]]

                self.merge_two_cluster(cluster_have_to_merge_1, cluster_have_to_merge_2)

                current_number_of_clusters = current_number_of_clusters - 1
                current_proximity_matrix = self.update_proximity_matrix_avg(self.clusters_current)
            return self.clusters_current

    def update_proximity_matrix_avg(self, current_clusters):
        result_matrix = []


        for each_cluster_x in current_clusters:
            temporary_row = []
            for each_cluster_y in current_clusters:
                sum_of_distance = 0
                for each_tuple_point_x in each_cluster_x:
                    for each_tuple_point_y in each_cluster_y:
                        sum_of_distance = sum_of_distance + self.calculate_euclidian_distance(each_tuple_point_x, each_tuple_point_y)
                sum_of_distance = sum_of_distance / (len(each_cluster_x) * len(each_cluster_y))
                sum_of_distance = round(sum_of_distance, 2)
                temporary_row.append(sum_of_distance)
            result_matrix.append(temporary_row)
        return result_matrix

    def update_proximity_matrix_max(self, current_clusters):
        result_matrix = []
        for each_cluster_x in current_clusters:
            temporary_row = []
            for each_cluster_y in current_clusters:
                maximum_distance = -1
                for each_tuple_point_x in each_cluster_x:
                    for each_tuple_point_y in each_cluster_y:
                        if self.calculate_euclidian_distance(each_tuple_point_x, each_tuple_point_y) > maximum_distance:
                            maximum_distance = self.calculate_euclidian_distance(each_tuple_point_x, each_tuple_point_y)
                temporary_row.append(maximum_distance)
            result_matrix.append(temporary_row)
        return result_matrix

    def update_proximity_matrix_min(self, current_clusters):
        result_matrix = []

        for each_cluster_x in current_clusters:
            temporary_row = []
            for each_cluster_y in current_clusters:
                minimum_distance = math.inf
                for each_tuple_point_x in each_cluster_x:
                    for each_tuple_point_y in each_cluster_y:
                        if self.calculate_euclidian_distance(each_tuple_point_x, each_tuple_point_y) < minimum_distance:
                            minimum_distance = self.calculate_euclidian_distance(each_tuple_point_x, each_tuple_point_y)
                temporary_row.append(minimum_distance)
            result_matrix.append(temporary_row)
        return result_matrix

    def merge_two_cluster(self, cluster_have_to_merge_1, cluster_have_to_merge_2):

        new_merged_cluster = []
        for each_point in cluster_have_to_merge_1:
            new_merged_cluster.append(each_point)

        for each_point2 in cluster_have_to_merge_2:
            if each_point2 not in new_merged_cluster:
                new_merged_cluster.append(each_point2)
        index_1 = 0
        index_2 = 0
        for cluster_x in self.clusters_current:
            if cluster_x == cluster_have_to_merge_1:
                self.clusters_current.remove(self.clusters_current[index_1])
            index_1 = index_1 + 1

        for cluster_y in self.clusters_current:
            if cluster_y == cluster_have_to_merge_2:
                self.clusters_current.remove(self.clusters_current[index_2])
            index_2 = index_2 + 1

        self.clusters_current.append(new_merged_cluster)

    def make_deep_copy(self):
        initial_proximity_matrix = self.calculate_initial_proximity_matrix()
        # Making Deep Copy
        current_proximity_matrix = []
        for each_list in initial_proximity_matrix:
            temporary_list_for_copiyng = []
            for each_entry in each_list:
                temporary_element_for_copiyng = each_entry
                temporary_list_for_copiyng.append(temporary_element_for_copiyng)
            current_proximity_matrix.append(temporary_list_for_copiyng)
        return current_proximity_matrix

    def find_smallest_proximity(self, proximity_matrix):
        minimum = [0, 0]
        minimum_value = math.inf
        index_row = 0
        index_colomn = 0
        for each_row_x in proximity_matrix:
            for each_row_y in proximity_matrix:
                if (index_row != index_colomn) and (proximity_matrix[index_row][index_colomn] < minimum_value):
                    minimum_value = proximity_matrix[index_row][index_colomn]
                    minimum[0] = index_row
                    minimum[1] = index_colomn
                index_colomn = index_colomn + 1
            index_colomn = 0
            index_row = index_row + 1
        return minimum

    def calculate_initial_proximity_matrix(self):
        result_matrix = []
        # for each point create a temporary list and store the euclidean calculation results for that point and the
        # other points in that temporary list after the all calculations for one point ends, add this row to
        # proximity matrix, for example take p1 and create temporary list for storing p1 and store p1 to p1,
        # p1 to p2, p1 to p3, p1 to p4, p1 to p5 and p1 to p6 euclidean distances and append this temporary list
        # to proximity matrix a.k.a. result_matrix and do the same for p2, p3, p4, p5 and p6

        for each_coordinate_x in self.data:
            temporary_row_list = []
            for each_coordinate_y in self.data:
                euclidean_distance = self.calculate_euclidian_distance(each_coordinate_x, each_coordinate_y)
                temporary_row_list.append(euclidean_distance)
            result_matrix.append(temporary_row_list)
        return result_matrix

    def calculate_euclidian_distance(self, tuple_x, tuple_y):
        x1 = float(tuple_x[0])
        x2 = float(tuple_y[0])
        y1 = float(tuple_x[1])
        y2 = float(tuple_y[1])
        result = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        result = round(result, 2)
        return  result

    def print_matrix(self, matrix):
        for row in matrix:
            print(row)
