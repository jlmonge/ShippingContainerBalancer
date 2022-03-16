from dataclasses import dataclass
import math
from Ship import *
from Node import *
import numpy as np
import os
import heapq



if __name__ == "__main__":
    print("Hello World!")
    new_ship = Ship()
    new_ship.from_manifest("ShipCase4.txt")
    print(new_ship)
    list_left_half = new_ship.get_list_half_of_ship(1)
    list_right_half = new_ship.get_list_half_of_ship(0)
    print(list_left_half)
    print(list_right_half)
    new_ship.to_manifest("ShipCase2Output.txt")
    c = Container(1,2,34,"fifty six")
    print(c)

def expand_balancing(node):

    list_of_nodes_from_expansion = []
    list_columns_not_full = node.ship.get_list_columns_not_full()
    for column_moved_from in range(node.ship.width):   #column
        for column_moved_to in list_columns_not_full:
            if column_moved_to != column_moved_from:
                if not node.ship.is_column_empty(column_moved_from):
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

                    node_of_ship_with_new_move.ship.move_container(column_moved_from,column_moved_to)

                    node_of_ship_with_new_move.moves_so_far.append(new_move_made)
                    try:
                        node_of_ship_with_new_move.h_n = node_of_ship_with_new_move.ship.get_heuristic_balance()
                    except:
                        node_of_ship_with_new_move.h_n = 10000
                    list_of_nodes_from_expansion.append(node_of_ship_with_new_move)
    return list_of_nodes_from_expansion

def expand_unload_offload(node,heap):


    return



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

    initial_node = Node(ship_initial_state,0)
    nodes = []
    nodes.append(initial_node)
    heapq.heapify(nodes)
    while True:
        if nodes == []:
            raise Exception('error, empty heap, no solution found')
            return 0

        popped_node = heapq.heappop(nodes) #for printing/testing

        found_solution = False
        if(is_balance_search):
            found_solution = popped_node.ship.is_balanced()
        else:
            pass # TODO: figure out exit condition

        if(found_solution):
            print('Goal! Ship is balanced')
            print('Solution: ' + str(popped_node))
            return popped_node

        list_nodes_from_expansion = expand_balancing(popped_node)
        a_star(nodes, list_nodes_from_expansion)

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

    # for onload, offload, should always offload first right?
