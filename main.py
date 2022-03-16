from dataclasses import dataclass
import math
from Ship import *
from Node import *
import numpy as np
import os



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
    #for each column which is not empty(has some container) (column moved from)
        #for i in range num columns
            #if column not full && if i != column moved from
                #create deepcopy of ship
                #copy_ship.move_container(column moved from, i)
                #temp_node = Node(ship)
                #temp_node.g_n = node.g_n + abs(i - column moved from)
                #move_made = Move(node.ship.top_available_slot[column_moved_from], column_moved_from, node.ship.top_available_slot[i],i.column
                #temp_node.moves_so_far = node.moves_so_far
                #temp_node.moves_so_far.append(move_made)
    return