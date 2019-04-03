import random

"""
adjacency list
this graph is supported by a dict of dict
{start: {dest : num}}
"""


class Graph(object):
    def __init__(self):
        self.g_dict = {}

    def addNode(self, node):
        """add a single node to graph"""

        # self.node_set.add(node)
        if node not in self.g_dict:
            self.g_dict[node] = {}

    def addEdge(self, dest, start=None):
        """ start -> dest"""

        if start is None:  # this node is first to this graph
            self.addNode(dest)

        else:
            if start in self.g_dict:
                if dest in self.g_dict[start]:
                    self.g_dict[start][dest] += 1
                else:
                    self.g_dict[start][dest] = 1
            else:
                self.g_dict[start] = {dest: 1}

    def walkNode(self, start):
        """given the input of start node, random pick next node"""

        if start in self.g_dict:
            total = sum(self.g_dict[start].values())
            if total == 0:  # a node with no outgoing edge
                return self.newPick()
            randint = random.randint(1, total)
            for edge in self.g_dict[start]:
                randint -= self.g_dict[start][edge]
                if randint <= 0:
                    return edge
        else:
            return self.newPick()

    def newPick(self):
        """ find a new starting point in this node"""

        return random.choice(tuple(self.g_dict))


# TEST CODE
# if __name__ == "__main__":
#     g = Graph()
#     g.addEdge("a", "b")
#     g.addEdge("h", "a")
#     g.addEdge("h", "a")

#     g.addEdge("a", "c")
#     g.addEdge("a", "c")
#     g.addEdge("c", "b")
#     g.addEdge("b", "a")
#     g.addEdge("f", "a")
#     print(g.walkNode("a"))
#     print(g.__dict__)
