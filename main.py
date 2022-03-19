from dataclasses import dataclass
import math
from Ship import *
from Node import *
import numpy as np
import os
import heapq



if __name__ == "__main__":
    #print("Hello World!")
    new_ship = Ship()
    new_ship.from_manifest("ShipCase4.txt")
    #print(new_ship)
    list_left_half = new_ship.get_list_half_of_ship(1)
    list_right_half = new_ship.get_list_half_of_ship(0)
    #print(list_left_half)
    #print(list_right_half)
    new_ship.to_manifest("ShipCase2Output.txt")
    c = Container(1,2,34,"fifty six")
    #print(c)

def expand_balancing(node):
    list_of_nodes_from_expansion = []
    list_columns_not_full = node.ship.get_list_columns_not_full()
    is_left_side_heavier = node.ship.is_left_side_heavier()

    list_columns_not_full = node.ship.get_list_columns_not_full()
    list_of_top_containers = node.ship.get_list_of_top_containers()
    # get column of column moved to in last node
    # g_n + distance between them + distance between curr col/row and new col/row
    if(is_left_side_heavier):
        for container in list_of_top_containers:
            if container.column < int(node.ship.width/2):
                row_container_moved_from = container.row
                column_moved_from = container.column
                for column_moved_to in list_columns_not_full:
                    if column_moved_from != column_moved_to:
                        row_container_moved_to = node.ship.top_available_container_row_indexes[column_moved_to]
                        node_of_ship_with_new_move = copy.deepcopy(node)
                        #new code
                        if(node.moves_so_far):
                            prev_node_row_moved_to = node.moves_so_far[-1].row_moved_to
                            prev_node_column_moved_to = node.moves_so_far[-1].column_moved_to

                        #        prev_node_row_moved_to, prev_node_column_moved_to, row_container_moved_from, column_moved_from)
                        #new code
                        distance_of_current_move = node_of_ship_with_new_move.ship.calculate_manhattan_distance_of_move(
                            row_container_moved_from, column_moved_from, row_container_moved_to, column_moved_to)
                        node_of_ship_with_new_move.g_n += distance_of_current_move
                        node_of_ship_with_new_move.g_n += 0.000001
                        #node_of_ship_with_new_move.g_n += 1;
                        new_move_made = Move(row_container_moved_from, column_moved_from, row_container_moved_to,
                                             column_moved_to)
                        new_move_made.distance_of_current_move = distance_of_current_move
                        if(node.moves_so_far):
                            new_move_made.distance_end_of_last_move_to_start_of_this_move = node_of_ship_with_new_move.ship.calculate_manhattan_distance_of_move(prev_node_row_moved_to, prev_node_column_moved_to, row_container_moved_from, column_moved_from)
                        # ship_balance_score_before = node_of_ship_with_new_move.ship.get_balance_score()
                        node_of_ship_with_new_move.ship.move_container(column_moved_from, column_moved_to)
                        # ship_balance_score_after = node_of_ship_with_new_move.ship.get_balance_score()
                        node_of_ship_with_new_move.moves_so_far.append(new_move_made)
                        # node_of_ship_with_new_move.balance_score = ship_balance_score_after
                        node_of_ship_with_new_move.ship.calculate_weight_left_right_sides_of_ship()
                        node_of_ship_with_new_move.h_n = node_of_ship_with_new_move.calculate_heuristic()
                        #node_of_ship_with_new_move.h_n = node_of_ship_with_new_move.ship.get_heuristic_balance()
                        list_of_nodes_from_expansion.append(node_of_ship_with_new_move)
    else:
        for container in list_of_top_containers:
            if container.column >= int(node.ship.width / 2):
                row_container_moved_from = container.row
                column_moved_from = container.column
                for column_moved_to in list_columns_not_full:
                    if column_moved_from != column_moved_to:
                        row_container_moved_to = node.ship.top_available_container_row_indexes[column_moved_to]
                        node_of_ship_with_new_move = copy.deepcopy(node)
                        distance_of_current_move = node_of_ship_with_new_move.ship.calculate_manhattan_distance_of_move(
                            row_container_moved_from, column_moved_from, row_container_moved_to, column_moved_to)
                        node_of_ship_with_new_move.g_n += distance_of_current_move
                        node_of_ship_with_new_move.g_n += 0.000001
                        new_move_made = Move(row_container_moved_from, column_moved_from, row_container_moved_to,
                                             column_moved_to)
                        new_move_made.distance_of_current_move = distance_of_current_move
                        # ship_balance_score_before = node_of_ship_with_new_move.ship.get_balance_score()
                        node_of_ship_with_new_move.ship.move_container(column_moved_from, column_moved_to)
                        # ship_balance_score_after = node_of_ship_with_new_move.ship.get_balance_score()
                        node_of_ship_with_new_move.moves_so_far.append(new_move_made)
                        # node_of_ship_with_new_move.balance_score = ship_balance_score_after
                        node_of_ship_with_new_move.ship.calculate_weight_left_right_sides_of_ship()
                        #node_of_ship_with_new_move.h_n = node_of_ship_with_new_move.ship.get_heuristic_balance()
                        start_h_n = node_of_ship_with_new_move.h_n
                        node_of_ship_with_new_move.h_n = node_of_ship_with_new_move.calculate_heuristic()
                        list_of_nodes_from_expansion.append(node_of_ship_with_new_move)
    return list_of_nodes_from_expansion






"""
def a_star_balance(nodes, nodes_from_expansion, heap):
    max_heap_size = 0
    while(nodes_from_expansion):
        new_h_n = nodes_from_expansion[-1].ship.get_heuristic_balance()
        nodes.append(nodes_from_expansion[-1])
        if(len(nodes) > max_heap_size):
            max_heap_size = len(nodes)
        nodes_from_expansion.pop(-1)
        nodes.sort()
        for node in nodes:
            heap.heappush(node)
"""

def a_star(heap, nodes_from_expansion):
    for node in nodes_from_expansion:
        heapq.heappush(heap,node)


def general_search_balancing(ship_initial_state, is_balance_search):
    balance_score_last_node = 10
    total_distance = 0
    initial_node = Node(ship_initial_state,0,0)
    initial_node.h_n = initial_node.calculate_heuristic()
    nodes = []
    nodes.append(initial_node)
    heapq.heapify(nodes)
    while True:
        if nodes == []:
            print('error, empty heap, no solution found, returning ship passed in')

            return Node(ship_initial_state,0,0)
        #print('front of heap')
        #print(nodes[0].ship)
        #print('back of heap')
        #print(nodes[-1].ship)
        popped_node = heapq.heappop(nodes) #for printing/testing
        if(balance_score_last_node == popped_node.ship.get_balance_score()):
            if(popped_node.ship.check_ship_for_containers_too_heavy()):
                popped_node.balance_score = popped_node.ship.get_balance_score()
                print('Cant balance ship to 0.9 balance score, container too heavy')
                if(popped_node.moves_so_far):
                    for move in popped_node.moves_so_far:
                        total_distance += move.distance_end_of_last_move_to_start_of_this_move
                    popped_node.g_n += total_distance
                popped_node.g_n = int(popped_node.g_n)
                #   print('total_distance: ')
                #   print(popped_node.g_n)
                #   print(popped_node.moves_so_far)
                return popped_node
            elif(popped_node.ship.lightest_container_each_side_above_deficit()):
                popped_node.balance_score = popped_node.ship.get_balance_score()
                print('Lightest containers above deficit')
                if(popped_node.moves_so_far):
                    for move in popped_node.moves_so_far:
                        total_distance += move.distance_end_of_last_move_to_start_of_this_move
                    popped_node.g_n += total_distance
                popped_node.g_n = int(popped_node.g_n)
                #   print('total_distance: ')
                #   print(popped_node.g_n)
                #   print(popped_node.moves_so_far)
                return popped_node

        balance_score_last_node = popped_node.ship.get_balance_score()
        found_solution = False
        if(is_balance_search):
            found_solution = (popped_node.ship.is_balanced())
        else:
            pass # TODO: figure out exit condition

        if(found_solution):
            popped_node.balance_score = popped_node.ship.get_balance_score()
            if (popped_node.moves_so_far):
                for move in popped_node.moves_so_far:
                    total_distance += move.distance_end_of_last_move_to_start_of_this_move
                popped_node.g_n += total_distance
            popped_node.g_n = int(popped_node.g_n)
            #   print('total_distance: ')
            #   print(popped_node.g_n)
            #   print('Goal! Ship is balanced')
            #   print('Solution: ' + str(popped_node))
            #print(popped_node.moves_so_far)
            return popped_node
        #print('expanded: \n')
        #print(popped_node)
        #print(popped_node.ship)
        list_nodes_from_expansion = expand_balancing(popped_node)
        if(list_nodes_from_expansion):
            a_star(nodes, list_nodes_from_expansion)
            nodes.sort()

    return

def balance_ship(ship):
    if(ship.containers == []):
        raise Exception('ship not constructed from manifest yet')

    solution = general_search_balancing(ship,1)
    if(solution):
        solution.ship.to_manifest('output_of_balance_ship.txt')
    else:
        print('no solution found')
    return solution
"""
def expand_balancing(node):

    list_of_nodes_from_expansion = []
    list_columns_not_full = node.ship.get_list_columns_not_full() #should this be only on heavier side?
    for column_moved_from in range(node.ship.width):   #column
        for column_moved_to in list_columns_not_full:
            if column_moved_to != column_moved_from:
                if not (node.ship.is_column_empty(column_moved_from)):
                    node_of_ship_with_new_move = copy.deepcopy(node)

                    if node.ship.top_available_container_row_indexes[column_moved_from] == -1:
                        row_container_moved_from = node.ship.height - 1
                    else:
                        row_container_moved_from = node.ship.top_available_container_row_indexes[column_moved_from] - 1

                    row_container_moved_to = node.ship.top_available_container_row_indexes[column_moved_to]
                    node_of_ship_with_new_move.g_n += node_of_ship_with_new_move.ship.calculate_manhattan_distance_of_move(row_container_moved_from,column_moved_from,row_container_moved_to,column_moved_to)

                    # Add a small decimal for each move that is taken, so that single moves travelling X distance will
                    # win over multiple moves travelling the same distance. This will cause us to expand nodes less.
                    node_of_ship_with_new_move.g_n += 0.000001

                    new_move_made = Move(row_container_moved_from,column_moved_from,row_container_moved_to,column_moved_to)
                    ship_balance_score_before = node_of_ship_with_new_move.ship.get_balance_score()
                    node_of_ship_with_new_move.ship.move_container(column_moved_from,column_moved_to)
                    ship_balance_score_after = node_of_ship_with_new_move.ship.get_balance_score()
                    node_of_ship_with_new_move.moves_so_far.append(new_move_made)
                    node_of_ship_with_new_move.balance_score = ship_balance_score_after
                    node_of_ship_with_new_move.ship.calculate_weight_left_right_sides_of_ship()
                    node_of_ship_with_new_move.h_n = node_of_ship_with_new_move.ship.get_heuristic_balance()

                    list_of_nodes_from_expansion.append(node_of_ship_with_new_move)
    return list_of_nodes_from_expansion
"""
    # for onload, offload, should always offload first right?
