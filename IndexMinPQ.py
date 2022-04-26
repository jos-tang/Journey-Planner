class IndexMinPQ:
    priority_queue = {}

    def __init__(self):
        pass

    def insert(self, destination, weight):
        self.priority_queue[destination] = []
        self.priority_queue[destination].append(weight)

    def isEmpty(self):
        if not self.priority_queue:
            return True
        else:
            return False

    def contains(self, key):
        if key in self.priority_queue:
            return True
        else:
            return False

    def change(self, key, weight):
        self.priority_queue[key][0] = weight

    def del_min(self):
        temp_weight = float('inf')
        for node in self.priority_queue:
            for weight in self.priority_queue[node]:
                if weight < temp_weight:
                    temp_weight = weight
                    temp = node

        del self.priority_queue[temp]
        return temp

    def print_pq(self):
        print(self.priority_queue)


