import uuid
from collections import Counter

class Graph:

    def __init__(self, nodes=[], edges=dict()):
        self.nodes = nodes
        self.edges = edges

    def get_nodes(self):
        return self.nodes

    def insert_node(self, n1):
        self.nodes.append(n1)

    def get_edges(self, uuid1):
        return self.edges[uuid1]

    def insert_edge(self, uuid1, uuid2):
        if uuid1 not in self.edges:
            self.edges[uuid1] = [uuid2]
        else:
            self.edges[uuid1].append(uuid2)

    def remove_nodes(self, nodes):
        new_nodes = [node for node in self.get_nodes() if node.get_uuid() not in nodes]
        new_edges = {k: v for k, v in self.edges.items() if k not in nodes}

        for k, v in new_edges.items():
            intersection = Counter(v) & Counter(nodes)
            new_edges[k] = list(Counter(v) - intersection)


        return new_nodes, new_edges

class Node:

    def __init__(self, p, owner):
        self.uuid = str(uuid.uuid4())
        self.p = p          # priority
        self.owner = owner

    def get_priority(self):
        return self.p

    def set_priority(self, p):
        self.p = p

    def get_owner(self):
        return self.owner

    def set_owner(self, owner):
        self.owner = owner

    def get_uuid(self):
        return self.uuid
