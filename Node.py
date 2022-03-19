class Move:
    def __init__(self,row_moved_from,column_moved_from,row_moved_to,column_moved_to):
        self.row_moved_from = row_moved_from
        self.column_moved_from = column_moved_from
        self.row_moved_to = row_moved_to
        self.column_moved_to = column_moved_to
        self.distance_end_of_last_move_to_start_of_this_move = 0
        self.distance_of_current_move = 0
    def __repr__(self):

        move_string = 'move container from ['

        if (self.row_moved_from + 1) < 10:
            move_string += '0'
        move_string += str(self.row_moved_from + 1) + ','

        if (self.column_moved_from + 1) < 10:
            move_string += '0'
        move_string += str(self.column_moved_from + 1) + ']'

        move_string += ' to ['

        if (self.row_moved_to + 1) < 10:
            move_string += '0'
        move_string += str(self.row_moved_to + 1) + ','

        if (self.column_moved_to + 1) < 10:
            move_string += '0'
        move_string += str(self.column_moved_to + 1) + ']'

        return move_string

    def get_list_representation(self):
        move = []
        initial_position = []
        final_position = []
        distance = int(self.distance_of_current_move)
        initial_position.append(self.row_moved_from)
        initial_position.append(self.column_moved_from)
        final_position.append(self.row_moved_to)
        final_position.append(self.column_moved_to)
        move.append(initial_position)
        move.append(final_position)
        move.append(distance)
        return move


        return move

class Node:
    def __init__(self,ship,g_n,h_n):
        self.ship = ship
        self.g_n = g_n
        #self.h_n = ship.get_heuristic_balance()
        self.h_n = h_n
        self.moves_so_far = []
        self.balance_score = 0

    def __lt__(self,other):
        #return (int(len(self.moves_so_far)) + self.g_n + self.h_n) < int(len(self.moves_so_far)) + (other.g_n + other.h_n)
        #return (self.h_n < other.h_n)
        #return((self.g_n + self.h_n < other.g_n + other.h_n) or self.ship.is_balanced())
        #return (len(self.moves_so_far) + self.h_n < len(other.moves_so_far) + other.h_n)
        #return self.g_n < other.g_n
        #if(self.balance_score == other.balance_score):
        #return (1 - self.balance_score) * self.h_n * self.g_n < (1 - other.balance_score) * other.h_n * other.g_n
        return (1 - self.balance_score)*(self.h_n + self.g_n) < (1 - other.balance_score)*(other.h_n + other.g_n)
        #return (1 - self.balance_score)*(self.h_n) + self.g_n < (1 - other.balance_score)*(other.h_n) + other.g_n
        #  return (self.h_n + self.g_n + (1 - self.balance_score)) < (other.h_n + other.g_n + (1 - other.balance_score))
        #return (1 - self.balance_score) < (1 - other.balance_score)

    def calculate_heuristic(self): #could we instead take min(abs(deficit - heaviest)?
        self.ship.calculate_weight_left_right_sides_of_ship()
        balance_mass = (self.ship.weight_left_side + self.ship.weight_right_side) / 2
        if(self.ship.weight_left_side < self.ship.weight_right_side):

            deficit = abs(balance_mass - self.ship.weight_left_side) #take deficit of lighter side
            right_side_of_ship = self.ship.get_list_half_of_ship(0)
            sorted_containers = self.ship.get_sorted_container_list_least_to_greatest(right_side_of_ship)
            available_column = self.ship.get_centermost_available_column(1)
            last_column_moved_to = -1
            heuristic_val = 0
            for i in range((len(sorted_containers) - 1), -1, -1):  # count down from last index to 0

                if sorted_containers[i].weight < deficit:
                    if last_column_moved_to > -1:
                        heuristic_val += abs(last_column_moved_to - sorted_containers[i].column)
                    heuristic_val += abs(sorted_containers[i].column - available_column)
                    last_column_moved_to = sorted_containers[i].column
                    deficit -= sorted_containers[i].weight


        elif(self.ship.is_balanced()):
            return 0
        else:
            deficit = abs(balance_mass - self.ship.weight_right_side)  # take deficit of lighter side
            left_side_of_ship = self.ship.get_list_half_of_ship(1)
            sorted_containers = self.ship.get_sorted_container_list_least_to_greatest(left_side_of_ship)
            available_column = self.ship.get_centermost_available_column(0)
            last_column_moved_to = -1
            heuristic_val = 0
            for i in range((len(sorted_containers) - 1), -1, -1):  # count down from last index to 0

                if sorted_containers[i].weight <= deficit:
                    if last_column_moved_to > -1:
                        heuristic_val += abs(last_column_moved_to - sorted_containers[i].column)
                    heuristic_val += abs(sorted_containers[i].column - available_column)
                    last_column_moved_to = sorted_containers[i].column
                    deficit -= sorted_containers[i].weight
            if not heuristic_val:
                centermost_left_container = abs(self.ship.get_centermost_container(1) - int(self.ship.width/2))
                centermost_right_container = abs(self.ship.get_centermost_container(0) - int(self.ship.width/2) - 1)
                heuristic_val = centermost_left_container + centermost_right_container
        self.balance_score = self.ship.get_balance_score()
        return heuristic_val + self.h_n
        #return heuristic_val

    def __repr__(self):
        # TODO: round g_n to int when done debugging
        node_string = 'Total minutes to complete this set of moves: ' + str(self.g_n) + '\n' \
                      + 'Moves so far: \n'
        for move in self.moves_so_far:
            node_string += str(move) + '\n'

        return node_string
        # currently not printing ship for each individual node as it will make output hard to read

    def get_moves(self):
        list_moves = []
        if(self.moves_so_far):
            for move in self.moves_so_far:
                move_list_representation = move.get_list_representation()
                list_moves.append(move_list_representation)
        return list_moves
