from graph import Graph
from IndexMinPQ import IndexMinPQ


class Dijkstra:
    source = None
    list = {}
    pq = None

    def __init__(self, G, source):
        self.source = source

        # Initialize list keys with all MRT/Bus
        for v in G.adjList:
            self.list[v] = []
            self.list[v].append(Dijkstra_node(None, False, 9999, 0))

        # Initialize priority queue
        self.pq = IndexMinPQ()
        self.pq.insert(source, 0.0)

        # Set source edges time to 0
        for node in self.list[source]:
            node.time = 0.0

        # Loop while priority queue is not empty
        while not self.pq.isEmpty():
            # delete minimum in priority queue and return minimum
            v = self.pq.del_min()

            # Mark true for mrt/bus visited
            for node in self.list[v]:
                node.marked = True

            # Relax edges of mrt/bus
            for e in G.adjList[v]:
                self.relax(e)

    def relax(self, e):
        v = e.src()
        w = e.dest()

        # Get Dijkstra node in list[source]
        for node in self.list[v]:
            source_node = node

        # Get Dijkstra node in list[destination]
        for node in self.list[w]:
            dest_node = node

        # Check if Destination node current time is bigger than new time
        # If bigger change values of Designation node
        if dest_node.time > source_node.time + float(e.time):
            dest_node.time = source_node.time + float(e.time)
            dest_node.cost = source_node.cost + float(e.cost)
            dest_node.edge = e

            # If priority queue contains Destination node, change destination node time
            if self.pq.contains(w):
                self.pq.change(w, dest_node.time)
            # If Marked is False, Destination node was not visited before
            elif dest_node.marked is False:
                self.pq.insert(w, dest_node.time)

    # Find path using List
    def find_path(self, dest):
        path = [dest]
        for node in self.list[dest]:
            time = node.time
            cost = node.cost
      
        while dest != self.source:
            for node in self.list[dest]:
                temp = node.edge
                temp = temp.src()
                path.append(temp)
                dest = temp
        path.append(cost)
        path.append(time)
        path.reverse()
        return path

# Dijkstra_node  class to contain variables
class Dijkstra_node:
    edge = None
    marked = False
    time = 0
    cost = 0.0

    def __init__(self, edge, marked, time, cost):
        self.edge = edge
        self.marked = marked
        self.time = time
        self.cost = cost

        def edge(self):
            return self.edge.src()

        def marked(self):
            return self.marked.src()

        def dist(self):
            return self.src()

        def dist(self):
            return self.cost()

