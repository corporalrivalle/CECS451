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
        self.pathlist=[]


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
    print("Map generated")
    for node in nodelist:
        print(node.cityname)
        print(node.connections)
        print(node.connectionlist)
        print(node.coords)
    return nodelist


#determines a heuristic based on absolute distance of node to goal node, and the current cost of getting there. 
def heuristic(cost, current_loc, goal_loc):
    cloc = tuple(current_loc.split(","))
    gloc = tuple(goal_loc.split(","))
    dist = haversine(cloc, gloc)
    f = cost + dist
    return f

def haversine(coord1, coord2):
    #coord1 and coord2 are tuples of the form (latitude, longitude)
    #returns distance in miles
    lat1 = float(coord1[0])
    lat2 = float(coord2[0])
    lon1 = float(coord1[1])
    lon2 = float(coord2[1])
    R = 3958.8 #radius of earth in miles
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

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
    conditioncheck(map, openlist, closedlist)
    for node in map:
        if node.cityname == startnode:
            startnode = node
            openlist.append(node)
            costdict[node.cityname]=0
        if node.cityname == endnode:
            endnode = node
    #main loop
    while len(openlist) > 0:
        for node in openlist:
            if node == endnode:
                return node
        currentnode = openlist[0]
        openlist.remove(currentnode)
        closedlist.append(currentnode)
        if isinstance(currentnode, str):
            print("Current node is a string")
            for node in map:
                if node.cityname == currentnode:
                    currentnode = node
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

    conditioncheck(map, openlist, closedlist)

def conditioncheck(map, openlist, closedlist):
    print("Map:")
    for node in map:
        print(node.cityname)
        print(node.connections)
        print(node.connectionlist)
        print(node.coords)
        print(node.cost)
        print(node.distance)
        print(node.pathlist)
    print("Openlist:")
    for node in openlist:
        print(node.cityname)
        print(node.connections)
        print(node.connectionlist)
        print(node.coords)
        print(node.cost)
        print(node.distance)
        print(node.pathlist)
    print("Closedlist:")
    for node in closedlist:
        print(node.cityname)
        print(node.connections)
        print(node.connectionlist)
        print(node.coords)
        print(node.cost)
        print(node.distance)
        print(node.pathlist)





def main(startloc, endloc):
    map = generate_map()
    a_Star_algo(map, startloc, endloc)
    return

main("SanJose", "SanFrancisco")