class Move:
    def __init__(self,row_moved_from,column_moved_from,row_moved_to,column_moved_to):
        self.row_moved_from = row_moved_from
        self.column_moved_from = column_moved_from
        self.row_moved_to = row_moved_to
        self.column_moved_to = column_moved_to

    def __repr__(self):

        move_string = 'move container from ['

        if (self.column_moved_from + 1) < 10:
            move_string += '0'
        move_string += str(self.column_moved_from + 1) + ','

        if (self.row_moved_from + 1) < 10:
            move_string += '0'
        move_string += str(self.row_moved_from + 1) + ']'

        move_string += ' to ['

        if (self.column_moved_from + 1) < 10:
            move_string += '0'
        move_string += str(self.column_moved_from + 1) + ','

        if (self.row_moved_from + 1) < 10:
            move_string += '0'
        move_string += str(self.row_moved_from + 1) + ']'

        return move_string

class Node:
    def __init__(self,ship,g_n):
        self.ship = ship
        self.g_n = g_n
        self.h_n = ship.get_heuristic()
        moves_so_far = []

    def __repr__(self):
        node_string = 'Node g_n: ' + self.g_n + '\n' \
                      + 'h_n: ' + self.h_n + '\n' \
                      + 'Moves so far: ' + self.moves_so_far + '\n'

        return node_string
        # currently not printing ship for each individual node as it will make output hard to read
