import os
import math

class mapNode:
    def __init__(self, mapstring, coordstring): 
        connectionlist=[]
        infodict = mapstring_parse(mapstring)
        self.cityname = infodict["CityName"]
        self.connections = infodict["Connections"]
        self.connectionlist = infodict["ConnectionList"]
        self.coords = coord_parse(coordstring)
        self.parent = None

def mapstring_parse(mapstring):
    #SanJose-SanFrancisco(48.4),Monterey(71.7),Fresno(149),SantaCruz(32.7)
    infodict={}
    split = mapstring.split("-")
    infodict["CityName"]=split[0]
    split = split[1].split(",")

    distdict={}
    connlist=[]
    for value in split:
        split2 = value.split("(")
        split2[1]=split2[1].strip(")")
        distdict[split2[0]]=float(split2[1])
        connlist.append(split2[0])
    infodict["Connections"]=distdict
    infodict["ConnectionList"]=connlist
    return infodict

def coord_parse(coordstring):
    #SanJose:(37.38305013,-121.8734782)
    split = coordstring.split(":")
    split[1]=split[1].strip("(")
    split[1]=split[1].strip(")")
    return split[1]
    
def generate_map():
    path = os.getcwd()+"\\Assignment 1\\"
    print(path)
    nodelist = []
    mapstring_list = []
    coordstring_list = []
    maptxt = open(path+"map.txt", "r")
    for line in maptxt:
        mapstring_list.append(line.strip("\n"))
    coordtxt = open(path+"coordinates.txt", "r")
    for line in coordtxt:
        coordstring_list.append(line.strip("\n"))
    for i in range(len(mapstring_list)):
        nodelist.append(mapNode(mapstring_list[i], coordstring_list[i]))
    return nodelist


#determines a heuristic based on absolute distance of node to goal node, and the current cost of getting there. 
def heuristic(cost, current_loc, goal_loc):
    cloc = current_loc.split(",")
    gloc = goal_loc.split(",")
    h = abs(math.sqrt(((cloc[0]-gloc[0])**2)+((cloc[1]-gloc[1])**2))) #closeness to goal heuristic
    f = cost + h
    return f

class path:
    def __init__(self):
        self.pathlist = []
        self.distance = 0
        self.cost = 0

    def clonePath(self):
        clone = path()
        clone.pathlist = self.pathlist.copy()
        clone.distance = self.distance
        clone.cost = self.cost
        return clone

def a_Star_algo(map, startnode, endnode):
    openlist=[]
    closedlist=[]

    costdict ={}
    costdict[startnode.cityname]=0
    
    
    #main loop
    while len(openlist) > 0:
        for node in openlist:
            if node.cityname == endnode.cityname:
                return node
        currentnode = openlist[0]
        openlist.remove(currentnode)
        closedlist.append(currentnode)
        for connection in currentnode.connectionlist:
            if connection in closedlist:
                continue #already been checked, skips 
            if connection not in openlist:
                openlist.append(connection) #adds to openlist if not already there
            newcost = costdict[currentnode.cityname] + currentnode.connections[connection]
            if connection not in costdict or newcost < costdict[connection]:
                costdict[connection] = newcost
                currentnode.cost = newcost
                currentnode.distance = heuristic(newcost, currentnode.coords, endnode.coords)
                currentnode.pathlist.append(connection)

    if len(openlist) == 0:
        print("No path found")
        return None
    
    




def main(startloc, endloc):
    map = generate_map()
    a_Star_algo(map, startloc, endloc)
    return
