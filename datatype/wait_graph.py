class wait_graph:
    def __init__(self):
        self.adj_list = {}
    
    def addNode(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = []

    def addEdge(self, node1, node2):
        self.adj_list[node1].append(node2)
    
    def removeNode(self, node):
        # Remove the node from the adjacency list
        del self.adj_list[node]

        # Remove the edges to the node by finding all adjacent nodes
        # and removing the edges to the node that is being removed
        for adjacent_nodes in self.adj_list.values():
            if node in adjacent_nodes:
                adjacent_nodes.remove(node)
                
    def hasCycle(self):
        visited = set()
        # DFS traversal
        node = list(self.adj_list.keys())[0]
        visited.add(node)
        if self.dfs(node, visited):
            return True

        return False

    def dfs(self, node, visited):
        
        for adjacent_node in self.adj_list[node]:
            if adjacent_node not in visited:
                visited.add(adjacent_node)
                if self.dfs(adjacent_node, visited):
                    return True
            else:
                return True

        return False

    def removeEdge(self, node1, node2):
        self.adj_list[node1].remove(node2)

    def getAdjacentNodes(self, node):
        return self.adj_list[node]  
    