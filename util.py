import os
from datetime import date, datetime
from typing import List

def log(description : str, isDev: bool=False):

    subdirectory = "./devlog" if isDev else "./log"
    logfilename = "devlog.txt" if isDev else "log.txt"

    if not os.path.isdir(subdirectory):
        os.makedirs(subdirectory)

    current_date = date.today().strftime("%m/%d/%Y")
    current_time = datetime.now().strftime("%H:%M:%S")

    f = open("{0}/{1}".format(subdirectory, logfilename), "a")
    f.write("[{0}] [{1}] {2}\n".format(current_date, current_time, description))
    f.close()
    

def parseManifest(manifest_filename : str) -> List:

    if not os.path.isfile(manifest_filename):
        log("parseManifest(): Failed to locate {0}".format(manifest_filename), isDev=True)
        return False

    f = open(manifest_filename, 'r')
    containers = [] # e.g. [ (01, 01), 6, "Olive Oil"]
    current_line_number = 0

    for line in f:
        if len(line) < 18: break
        if line[0] != '[': break
        if not line[1:3].isnumeric() or int(line[1:3]) > 8: break
        if line[3] != ',': break
        if not line[4:6].isnumeric() or int(line[1:3]) > 12: break
        if line[6] != ']': break
        if line[7] != ',': break
        if line[8] != ' ': break
        if line[9] != '{': break
        if not line[10:15].isnumeric(): break
        if line[15] != '}': break
        if line[16] != ',': break
        if line[17] != ' ': break

        container_position = ( int(line[1:3]), int(line[4:6]) )
        container_weight = int(line[10:15])
        container_description = line[18:][:-1] if line[-1] == '\n' else line[18:]

        containers.append([container_position, container_weight, container_description])

        current_line_number += 1

    if current_line_number < 96:
        log("parseManifest(): Error in manifest file on line {0}".format(current_line_number+1), isDev=True)
        return False

    return containers
 
def writeOutboundManifest(containers: List):

    path_to_desktop = "{0}\{1}".format(os.environ['USERPROFILE'], 'Desktop')
    f = open("{0}\{1}".format(path_to_desktop, "manifest_OUTBOUND.txt"), 'w')

    for position, weight, description in containers:

        x = "0{0}".format(position[0]) if len(str(position[0])) == 1 else position[0]
        y = "0{0}".format(position[1]) if len(str(position[1])) == 1 else position[1]
        
        weight = str(weight)

        while len(weight) < 5:
            weight = "0" + weight

        f.write("[{0},{1}], {{{2}}}, {3}\n".format(x, y, weight, description))

    f.close()