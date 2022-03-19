
class Container:

    def __init__(self,row,column,weight,description):
        self.row = row
        self.column = column
        self.weight = weight
        self.description = description

    def __lt__(self,other):
        return self.weight < other.weight

    #def __gt__(self,other):
    #    return self.weight > other.weight

    def __repr__(self):     # prints in format [row,column], {weight}, description
        container_manifest_string = '['

        if (self.row + 1) < 10:
            container_manifest_string += '0'
        container_manifest_string += str(self.row + 1) + ','

        if (self.column + 1) < 10:
            container_manifest_string += '0'
        container_manifest_string += str(self.column + 1) + '], {' #col + 1 because we start at col 0 in python

        if self.weight < 10000:
            container_manifest_string += '0'
        if self.weight < 1000:
            container_manifest_string += '0'
        if self.weight < 100:
            container_manifest_string += '0'
        if self.weight < 10:
            container_manifest_string += '0'
        container_manifest_string += str(self.weight)

        container_manifest_string += '}, ' + self.description

        return container_manifest_string


    def is_same_container_as(self, container_to_compare_to): # for use in 'if theres an identical container closer, you can move that one instead' situations
        if self.row == container_to_compare_to.row:
            if self.column == container_to_compare_to.column:
                if self.weight == container_to_compare_to.weight:
                    if self.description == container_to_compare_to.description:
                        return True
        return False

    def is_unused(self):
        return self.description == "UNUSED"

    def is_invalid(self):
        return self.description == 'NAN'

    def data_for_onload(self):
        return self.weight, self.description

