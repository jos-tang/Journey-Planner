from graph import Graph


class A_Star_NeighbourNode:
    AStarNode = None
    timeCost = 0
    priceCost = 0

    def __init__(self, AStarNode, timeCost, priceCost):
        self.AStarNode = AStarNode
        self.timeCost = timeCost
        self.priceCost = priceCost


class A_Star_Node:
    name = "Default Name"  # Name of Node
    parent = None  # Parent Node - Points to next path node
    gTimeCost = 0  # Cost from source
    gPriceCost = 0  # Cost from source
    hTimeCost = 0  # Estimated Cost from destination
    hPriceCost = 0  # Estimated Cost from destination
    neighbourList = []  # List of adjacent Nodes

    # Total Movement Cost due to g and h
    def getTimeFCost(self):
        return self.gTimeCost + self.hTimeCost

    def getPriceFCost(self):
        return self.gPriceCost + self.hPriceCost

    def __init__(self, name):
        self.name = name
        self.parent = None
        self.gTimeCost = 0
        self.gPriceCost = 0
        self.hTimeCost = 0
        self.hPriceCost = 0
        self.neighbourList = []

    def containsNeighbour(self, nodeName):
        return self.getNeighbourNode(nodeName) is not None

    def getNeighbourNode(self, nodeName):
        for neighbour in self.neighbourList:
            if neighbour.AStarNode.name == nodeName:
                return neighbour
        else:
            return None

    def getSmallestHTimeValueByDepth(self, ignorePrev, depth, destination, hTimeValue=0):
        if depth <= 0:
            return hTimeValue

        smallestNeighbour = self.neighbourList[0].AStarNode
        smallestValue = float('inf')
        for neighbour in self.neighbourList:
            if neighbour.AStarNode.name is destination:
                return hTimeValue + neighbour.timeCost
            if neighbour is not ignorePrev and neighbour.timeCost < smallestValue:
                smallestValue = neighbour.timeCost
                smallestNeighbour = neighbour
        return smallestNeighbour.AStarNode.getSmallestHTimeValueByDepth(self, depth - 1, hTimeValue + smallestValue)

    def getSmallestHPriceValueByDepth(self, ignorePrev, depth, destination, hPriceValue=0):
        if depth <= 0:
            return hPriceValue

        smallestNeighbour = self.neighbourList[0].AStarNode
        smallestValue = float('inf')
        for neighbour in self.neighbourList:
            if neighbour.AStarNode.name is destination:
                return hPriceValue + neighbour.priceCost
            if neighbour is not ignorePrev and neighbour.priceCost < smallestValue:
                smallestValue = neighbour.priceCost
                smallestNeighbour = neighbour
        return smallestNeighbour.AStarNode.getSmallestHPriceValueByDepth(self, depth - 1, hPriceValue + smallestValue)

    def addNeighbour(self, AStarNode, timeCost, priceCost):
        if not self.containsNeighbour(AStarNode.name):
            self.neighbourList.append(A_Star_NeighbourNode(AStarNode, timeCost, priceCost))
        return True

    def to_string(self):
        str = "[" + self.name + "'s Neighbours: "
        for neighbour in self.neighbourList:
            str += neighbour.AStarNode.name + " "
        str += "\n"
        return str

    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name


class AStarMap:
    source = None
    stationList = {}  # Node List
    openList = []
    closedList = []

    def getNode(self, nodeName):
        for node in self.stationList:
            if node == nodeName:
                return self.stationList[node]
        else:
            return None

    def __init__(self, edgeGraph, source):
        self.source = source
        self.stationList = {}
        self.openList = []
        self.closedList = []
        
        for allEdgeKey in edgeGraph.adjList:
            for edge in edgeGraph.adjList[allEdgeKey]:
                if not self.stationList.__contains__(edge.source):
                    self.stationList[edge.source] = A_Star_Node(edge.source)
                if not self.stationList.__contains__(edge.destination):
                    self.stationList[edge.destination] = A_Star_Node(
                        edge.destination)

                self.stationList[edge.source].addNeighbour(
                    self.getNode(edge.destination),
                    float(edge.time),
                    float(edge.cost)
                )

                self.stationList[edge.destination].addNeighbour(
                    self.getNode(edge.source),
                    float(edge.time),
                    float(edge.cost)
                )

        return None

    def FindTimePath(self, destination):
        self.openList.append(self.stationList[self.source])
        while len(self.openList) > 0:
            currentNode = self.openList[0]
            # Check if any other nodes have lower F Cost
            for i in range(1, len(self.openList)):
                temp = self.openList[i]
                if temp.getTimeFCost() < currentNode.getTimeFCost() or temp.getTimeFCost() == currentNode.getTimeFCost() and temp.hTimeCost < currentNode.hTimeCost:
                    currentNode = temp

            self.openList.remove(currentNode)
            self.closedList.append(currentNode)
            if currentNode.name == destination:
                return self.PathOutput(currentNode)

            for neighbour in currentNode.neighbourList:
                if self.closedList.__contains__(neighbour.AStarNode):
                    continue
                newMovementCost = currentNode.gTimeCost + currentNode.getNeighbourNode(
                    neighbour.AStarNode.name).timeCost
                if newMovementCost < neighbour.AStarNode.getTimeFCost() or neighbour.AStarNode not in self.openList:
                    neighbour.AStarNode.gTimeCost = newMovementCost
                    neighbour.AStarNode.hTimeCost = neighbour.AStarNode.getSmallestHTimeValueByDepth(currentNode, 2,
                                                                                                     destination)
                    neighbour.AStarNode.parent = currentNode

                    if not self.openList.__contains__(neighbour.AStarNode):
                        self.openList.append(neighbour.AStarNode)

    def FindPricePath(self, destination):
        self.openList.append(self.stationList[self.source])

        while len(self.openList) > 0:
            currentNode = self.openList[0]
            # Check if any other nodes have lower F Cost
            for i in range(1, len(self.openList)):
                temp = self.openList[i]
                if temp.getPriceFCost() < currentNode.getPriceFCost() or temp.getPriceFCost() == currentNode.getPriceFCost() and temp.hPriceCost < currentNode.hPriceCost:
                    currentNode = temp

            self.openList.remove(currentNode)
            self.closedList.append(currentNode)

            if currentNode.name == destination:
                return self.PathOutput(currentNode)

            for neighbour in currentNode.neighbourList:
                if self.closedList.__contains__(neighbour.AStarNode):
                    continue

                newMovementCost = currentNode.gPriceCost + currentNode.getNeighbourNode(
                    neighbour.AStarNode.name).priceCost
                if newMovementCost < neighbour.AStarNode.getPriceFCost() or neighbour.AStarNode not in self.openList:
                    neighbour.AStarNode.gPriceCost = newMovementCost
                    neighbour.AStarNode.hPriceCost = neighbour.AStarNode.getSmallestHPriceValueByDepth(currentNode, 2,
                                                                                                       destination)
                    neighbour.AStarNode.parent = currentNode

                    if not self.openList.__contains__(neighbour.AStarNode):
                        self.openList.append(neighbour.AStarNode)

    def PathOutput(self, destinationNode):
        totalTime = 0
        totalPrice = 0
        path = []
        temp = destinationNode
        while temp is not None:
            if temp.parent is not None:
                neighbourNode = temp.getNeighbourNode(temp.parent.name)
                totalPrice += neighbourNode.priceCost
                totalTime += neighbourNode.timeCost
            path.append(temp.name)
            temp = temp.parent

        path.append(totalPrice)
        path.append(totalTime)
        path.reverse()
        return path

    def FindPath(self, destination, isTimeWeighted=True):
        if isTimeWeighted:
            return self.FindTimePath(destination)
        else:
            return self.FindPricePath(destination)

