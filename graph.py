import csv

class mrtList:
    dropdown = []
    def __init__(self, file):
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                mode = row[0]
                v1 = row[1]
                if mode == "MRT":
                    self.dropdown.append(v1)

class Graph:
    adjList = {}

    def __init__(self, file,tag,congest):
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Read a row from CSV file
            for row in csv_reader:
                mode = row[0]   # type  Mrt or Bus data
                v1 = row[1]     # v1    source
                v2 = row[2]     # v2    destination
                time = float(row[3])   # time  time from source to destination
                cost = row[4]   # cost  cost from source to destination

                if v1 == congest:
                    time +=50
                
                if mode in tag or mode == 'WALK':
                    e = Edge(v1, v2, time, cost, mode)    # e edge from source to destination
                    e1 = Edge(v2, v1, time, cost, mode )  # e1 edge from destination to source

                    # Uni direction implementation for buses
                    # Check if mrt/bus is already in graph
                    # If in graph add only edge to mrt/bus key
                    # Else initialize mrt/bus key and add edge

                    if v1 in self.adjList:
                        # Check if edge has already been added to mrt/bus key
                        edge_in_graph = False
                        for edge in self.adjList[v1]:
                            if v2 == edge.dest():
                                edge_in_graph = True

                        # If edge is not in graph add edge
                        if not edge_in_graph:
                            self.adjList[v1].append(e)

                        # If edge in graph do not add edge
                        elif edge_in_graph:
                            pass

                    # Mrt/Bus not found in the graph, add key and edge into graph
                    else:
                        self.adjList[v1] = []
                        self.adjList[v1].append(e)

                    # Dual direction
                    # MRT are dual direction
                    if mode == "MRT" or mode == "WALK":
                        if v2 in self.adjList:
                            # Check if edge has already been added to mrt/bus key
                            edge_in_graph = False
                            for edge in self.adjList[v2]:
                                if v1 == edge.dest():
                                    edge_in_graph = True

                            # If edge is not in graph add edge
                            if not edge_in_graph:
                                self.adjList[v2].append(e1)

                            # If edge in graph do not add edge
                            elif edge_in_graph:
                                pass
                        else:
                            self.adjList[v2] = []
                            self.adjList[v2].append(e1)

    # Print all Mrt with their edges, cost and time
    def print_list(self):
        for node in self.adjList:
            for edge in self.adjList[node]:
                print(node + " " + edge.to_string())


# Edge  Class to contain variables
class Edge:
    source = None
    destination = None
    time = None
    cost = None

    def __init__(self, v, w, time, cost, mode):
        self.source = v
        self.destination = w
        self.time = time
        self.cost = cost
        self.mode = mode

    def src(self):
        return self.source

    def dest(self):
        return self.destination

    def time(self):
        return self.time

    def cost(self):
        return self.cost

    def mode(self):
        return self.mode

    def to_string(self):
        return "[" + str(self.source) + "-" + str(self.destination) + "," + str(self.time) + "," + str(self.cost) + "] "


