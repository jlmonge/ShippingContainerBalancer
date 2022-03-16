from Container import *
import math
import os
import copy
import numpy as np

def line_of_manifest_to_container(line):
    container_row = int(line[1:3]) - 1  #remove '-1' if we are indexing starting at 1, this assumes 0,0 to 11,11
    container_column = int(line[4:6]) - 1  #remove '-1' if we are indexing starting at 1, this assumes 0,0 to 11,11
    container_weight = int(line[10:15])
    container_description = line[18:]
    container_description = container_description.strip()

    return Container(container_row, container_column, container_weight, container_description)


class Ship:
    def __init__(self):
        self.height = -1
        self.width = -1
        self.containers = [] # first index is the row, 2nd index is column
        self.top_available_container_row_indexes = []
        self.weight_left_side = 0
        self.weight_right_side = 0

    def setup_top_available_container_row_indexes(self):

        self.top_available_container_row_indexes = [-1]*self.width

        for i in range(self.width):
            for j in range(self.height):
                if self.containers[j][i].is_unused():
                    self.top_available_container_row_indexes[i] = j
                    break

    #added 3/10
    def get_balance_score(self):
        if self.weight_right_side == 0 or self.weight_left_side == 0:
            return 0.0000
        else:
            balance_score = (min(self.weight_left_side,self.weight_right_side)
                             / max(self.weight_left_side,self.weight_right_side))
            return balance_score

    def is_balanced(self):

        return self.get_balance_score() > 0.9

    def calculate_weight_left_right_sides_of_ship(self):
        weight_left_side = 0
        weight_right_side = 0
        left_side_containers = self.get_list_half_of_ship(1)
        right_side_containers = self.get_list_half_of_ship(0)
        for i in range(len(left_side_containers)):
            for j in range(len(left_side_containers[i])):
                weight_left_side += left_side_containers[i][j].weight
        for i in range(len(right_side_containers)):
            for j in range(len(right_side_containers[i])):
                weight_right_side += right_side_containers[i][j].weight
        self.weight_left_side = weight_left_side
        self.weight_right_side = weight_right_side



    def get_balance_mass(self):
        return ((self.weight_left_side + self.weight_right_side)/2)

    def get_balance_deficit(self):
        return (self.get_balance_mass()) - min(self.weight_left_side,self.weight_right_side)

    def is_left_side_heavier(self):
        if self.weight_left_side > self.weight_right_side:
            return True
        return False

    def get_sorted_container_list_least_to_greatest(self,list_of_containers):
        list_to_be_sorted = []
        for i in range(len(list_of_containers)):
            for j in range(len(list_of_containers[i])):
                container = list_of_containers[i][j]
                if not container.is_unused() and not container.is_invalid():
                    list_to_be_sorted.append(container)




        sorted_list = copy.deepcopy(list_to_be_sorted)
        sorted_list.sort()
        return sorted_list
    #problem: currently sorted list is a full half of ship include nan/unused containers
    def get_container_in_sorted_list_with_weight_lte_threshold(self,sorted_container_list_ltg, threshold):
        for i in range((len(sorted_container_list_ltg)-1), -1, -1):   # count down from last index to 0
            container = sorted_container_list_ltg[i]

            #if (container.weight == 0):
            #    raise Exception("Could not find container; ran out of valid containers to check")

            if container.weight <= threshold:
                return container

        if (i == 0):
            raise Exception("Could not find container; ran out of containers to check")

    # done on 3/8 TMC
    def from_manifest(self,file_path):

        file = open(file_path,"r")
        line_count = 0
        content = []
        for line in file:
            line_count += 1
            content.append(line)

        if (line_count == 0):
            raise Exception("Specified file of " + file_path + " is empty!")

        last_line = content[line_count - 1]

        self.height = int(last_line[1:3])
        self.width = int(last_line[4:6])

        self.containers = []
        for i in range(self.height):
            self.containers.append([])
            for j in range(self.width):
                self.containers[i].append(Container(-1, -1, -1, ""))

        row_index = 0
        col_index = 0
        for line_num in range(line_count):
            if ( (row_index >= self.height ) or (col_index >= self.width) ):
                raise Exception("Number of lines is more than should be allowed by ship dimensions")

            new_container = line_of_manifest_to_container(content[line_num])
            self.containers[row_index][col_index] = new_container
            if col_index >= self.width - 1:
                col_index = 0
                row_index += 1
            else:
                col_index += 1

        self.setup_top_available_container_row_indexes()
        file.close()

    def to_manifest(self,file_path):
        file = open(file_path,"w")

        for i in range(len(self.containers)):
            for j in range(len(self.containers[i])):
                container = self.containers[i][j]
                # Don't add a newline for the last line in the manifest
                if (i == len(self.containers) - 1) and (j == len(self.containers[i]) - 1):
                    file.write(container.__repr__())
                else:
                    file.write(container.__repr__() + '\n')
        file.close()

    def lift_container(self,column_index):
        # Error if we lift from an empty column
        if(self.top_available_container_row_indexes[column_index] == 0):
            raise Exception("Tried to lift from an empty column!")

        # If full column, set top available slot equal to height, to make following operations work
        if(self.top_available_container_row_indexes[column_index] == -1):
            self.top_available_container_row_indexes[column_index] = self.height

        container_lifted = self.containers[self.top_available_container_row_indexes[column_index] - 1][column_index]

        # Error if we lift an empty or invalid container
        if(container_lifted.is_invalid()):
            raise Exception("Tried to lift an invalid container!")
        elif (container_lifted.is_unused()):
            raise Exception("Tried to lift an empty container!")

        empty_container = Container(self.top_available_container_row_indexes[column_index] - 1,column_index,0,"UNUSED")
        # make top container of column_index into an empty container
        self.containers[self.top_available_container_row_indexes[column_index] - 1][column_index] = empty_container
        if column_index < (self.width/2):
            self.weight_left_side -= container_lifted.weight
        else:
            self.weight_right_side -= container_lifted.weight
        # decrement top available position at column index
        self.top_available_container_row_indexes[column_index] -= 1

        return container_lifted

    def place_container(self,column_index,container):

        # Error if we try to place a container onto a full column
        if(self.top_available_container_row_indexes[column_index] == -1):
            raise Exception("Tried to place container onto a full column!")

        container.row = self.top_available_container_row_indexes[column_index]
        container.column = column_index
        self.containers[self.top_available_container_row_indexes[column_index]][column_index] = container

        # increment top available position at column index
        self.top_available_container_row_indexes[column_index] += 1

        # if we fill up a column, no valid top available row
        if(self.top_available_container_row_indexes[column_index] == self.height):
            self.top_available_container_row_indexes[column_index] = -1

        if column_index < self.width/2:
            self.weight_left_side += container.weight
        else:
            self.weight_right_side += container.weight

    def move_container(self,column_of_container_to_move, column_container_moved_to):
        #place container in new position first to preserve the container, then remove the container from the column lifted from
        if column_container_moved_to == column_of_container_to_move:
            raise Exception("column moved from is same column as moved to")
        self.place_container(column_container_moved_to, self.lift_container(column_of_container_to_move))


    def swap_containers_in_ship(self,row1, column1, row2, column2):
        # Only allow swapping of two valid containers, so we don't have to worry about updating container indexes
        if(self.containers[row1][column1].is_unused() or self.containers[row2][column2].is_unused() or self.containers[row1][column1].is_invalid() or self.containers[row2][column2].is_invalid()):
            raise Exception('one of the containers to be swapped is invalid or unused')
        # Only allow swapping of two containers on the same side, so we don't have to worry about updating weights on
        # each side
        container1_is_left = column1 < (self.width/2)
        container2_is_left = column2 < (self.width/2)
        if (container1_is_left and (not container2_is_left)) or ((not container1_is_left) and container2_is_left):
            raise Exception("Tried to swap two containers that were not on the same side!")


        self.containers[row2][column2].row = row1
        self.containers[row2][column2].column = column1
        self.containers[row1][column1].row = row2
        self.containers[row1][column1].column = column2

        copy_of_container1 = copy.deepcopy(self.containers[row1][column1])
        self.containers[row1][column1] = self.containers[row2][column2]
        self.containers[row2][column2] = copy_of_container1

    def get_centermost_available_column(self,is_left_side):
        if(is_left_side):
            for i in range(int((self.width / 2) - 1), -1, -1):
                if(self.top_available_container_row_indexes[i] != -1):
                    return i
        else:
            for i in range(int(self.width / 2), int(self.width), 1):
                if (self.top_available_container_row_indexes[i] != -1):
                    return i

        raise Exception("No available centermost column found! is_left_side: " + str(is_left_side))

    def get_list_half_of_ship(self,is_left_side):
        if(is_left_side):
            np_array_containers = np.array(self.containers)
            #index_to_stop = self.width / 2
            nparray_sliced = np_array_containers[:,:int(self.width / 2)]
        else:
            np_array_containers = np.array(self.containers)
            nparray_sliced = np_array_containers[:,int(self.width / 2):]
        list_one_side = np.ndarray.tolist(nparray_sliced)
        return list_one_side

    def get_heuristic(self):
        remaining_deficit = self.get_balance_deficit()
        if self.is_left_side_heavier():
            list_to_sort = self.get_list_half_of_ship(1)
        else:

            list_to_sort = self.get_list_half_of_ship(0)

        sorted_heavier_side = self.get_sorted_container_list_least_to_greatest(list_to_sort)
        copy_of_ship = copy.deepcopy(self)
        heuristic_sum = 0
        while copy_of_ship.is_balanced() == False:
            try:
                container_to_move = copy_of_ship.get_container_in_sorted_list_with_weight_lte_threshold(sorted_heavier_side,remaining_deficit)

            # Stop incrementing heuristic if we can't find a container to move
            # with weight less than or equal to the remaining deficit. This
            # should be OK, since our heuristic just needs to under estimate
            # the actual remaining amount of work.
            except Exception:
                break

            # if this container is not on the top of its column in ship_copy
            row_index_of_top_container_in_column = copy_of_ship.top_available_container_row_indexes[container_to_move.column] - 1

            if ((container_to_move.row != self.height - 1)
                and (container_to_move.row != row_index_of_top_container_in_column)):
                # call swap on ship_copy with the container on top of its column, so it will go to top
                copy_of_ship.swap_containers_in_ship(container_to_move.row,container_to_move.column,
                                                     row_index_of_top_container_in_column, container_to_move.column)

            #     subtract this container weight from deficit variable
            remaining_deficit -= container_to_move.weight

            #     call move_container to move this container to other side of ship_copy
            is_left_side = (container_to_move.column < (copy_of_ship.width/2 - 1))
            available_column = copy_of_ship.get_centermost_available_column(is_left_side)
            copy_of_ship.move_container(container_to_move.column,available_column)

            # Add the horizontal distance moved to the heuristic0
            heuristic_sum += abs(available_column - container_to_move.column)

            # remove heaviest container from sorted_heavier_sde
            sorted_heavier_side.remove(container_to_move)

        # heuristic is the sum variable that we incremented in the while loop
        return heuristic_sum

    def __repr__(self):

        string_repr = ""

        # outer loop starts at top row and works our way down
        for i in range((self.height-1), -1, -1):
            # inner loop starts at left column and works its way to the right
            for j in range(self.width):
                container = self.containers[i][j]
                if(container.is_unused()):
                    string_repr += "0 "
                elif(container.is_invalid()):
                    string_repr += "- "
                else: # is normal container
                    string_repr += "1 "

            # Reached end of a row, so print newline
            string_repr += '\n'

        return string_repr