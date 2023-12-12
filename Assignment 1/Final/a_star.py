import os
import math
import sys

class mapNode:
    def __init__(self, mapstring, coordstring): 
        infodict = mapstring_parse(mapstring)
        self.cityname = infodict["CityName"]
        self.connections = infodict["Connections"]
        self.connectionlist = infodict["ConnectionList"]
        self.coords = coord_parse(coordstring)
        self.dfe=0 #dfe = distance from end
        self.cost=float('inf')
        self.parent=None
        self.heuristic=float('inf')



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
    #remove +\\Assignment 1\\ when running outside of dev environment
    path = os.getcwd()+"\\"
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
    cloc = tuple(current_loc.split(","))
    gloc = tuple(goal_loc.split(","))
    dist = haversine(cloc, gloc)
    f = cost + dist*10
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

def cost_calc(startnode, endnode): #only works for neighbors
    cost = startnode.connections[endnode.cityname]
    return float(cost)

#a star algorithm
def a_star(map, start, end): #need to pass in nodes in start and end (not strings)
    openlist = []
    closedlist = []
    openlist.append(start)
    costdict={}

    while len(openlist)>0:
        #calculate cost of each node in open list, eventually finding cost of every node via expansion
        #find path of least resistance and track with self.parent attribute
        current = openlist[0]
        #calculate cost of each neighboring node from current node
        for node in current.connectionlist: #grabs strings of city names that neighbor the current node
            for mapnode in map:
                if mapnode.cityname == node:
                    neighbor = mapnode
            if neighbor in closedlist:
                pass
            else:
                #neighbor is a node that is not in the closed list
                #need to calculate the relative cost of reaching neighbor from the current node
                neighbor.cost = cost_calc(current, neighbor)
                neighbor.parent = current
                neighbor.heuristic = heuristic(neighbor.cost, neighbor.coords, end.coords)
                openlist.append(neighbor)
        #add current node to closed list
        closedlist.append(current)
        #remove current node from open list
        openlist.remove(current)
        #sort open list by heuristic
        openlist.sort(key=lambda x: x.heuristic)
        #check if end node is in closed list
        if end in closedlist:
            break
        else:
            pass
    #end of while loop
    #print path
    path = []
    total_travelled = 0 
    current = end
    while current != start:
        total_travelled += current.cost
        path.append(current)
        current = current.parent
    print_path(path, total_travelled, start)



def print_path(path, total_travelled, start):
    print("Best path: ",start.cityname,end=" ")
    for node in reversed(path):
        print("-",node.cityname,end=" ")
    print("\nTotal distance :",total_travelled,"mi")

#main function
def main(startstr, endstring):
    map = generate_map()
    for node in map:
        if node.cityname == startstr:
            start = node
        if node.cityname == endstring:
            end = node
    for node in map:
        if node.cityname == endstring:
            pass
        else:
            #calculate distance from end node
            node.dfe = haversine(tuple(node.coords.split(",")), tuple(end.coords.split(",")))

    print("From City: "+start.cityname)
    print("To city: "+end.cityname)
    a_star(map, start, end)
    # map_check(map)


#testing functions
def map_check(map):
    for node in map:
        # print("City name:",node.cityname)
        # print("Connections:",node.connections)
        # print("Connection list:",node.connectionlist)
        # print("Coordinates:",node.coords)
        # print("Distance:",node.dfe)
        print("City name:",node.cityname,"Distance:",node.dfe, "Cost:",node.cost, "Heuristic:",node.heuristic)
        print("=====================================")

# main("SanFrancisco", "LongBeach")
# main("SanJose", "SanFrancisco")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python a_star.py [arg1] [arg2]")
        sys.exit(1)

    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    main(arg1, arg2)

