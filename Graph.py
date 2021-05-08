#  File: Graph.py

#  Description: Creates then manipulates graphs, given city, edge coordinates, and vertex name
#  >>     then, print adjacency matrices.

#  Student Name: Jeremy Ulfohn

#  Student UT EID: jau392

#  Course Name: CS 313E

#  Unique Number: 52240

#  Date Created: 27 April 2021

#  Date Last Modified: 27 April 2021

import sys
class Stack(object):
    def __init__(self):
        self.stack = []

    # add an item to the top of the stack
    def push(self, item):
        self.stack.append(item)

    # remove an item from the top of the stack
    def pop(self):
        return self.stack.pop()

    # check the item on the top of the stack
    def peek(self):
        return self.stack[-1]

    # check if the stack is empty
    def is_empty(self):
        return len(self.stack) == 0

    # return the number of elements in the stack
    def size(self):
        return len(self.stack)


class Queue(object):
    def __init__(self):
        self.queue = []

    # add an item to the end of the queue
    def enqueue(self, item):
        self.queue.append(item)

    # remove an item from the beginning of the queue
    def dequeue(self):
        return (self.queue.pop(0))

    # check if the queue is empty
    def is_empty(self):
        return (len(self.queue) == 0)

    # return the size of the queue
    def size(self):
        return (len(self.queue))

class Edge (object): # attributes: fromVertex (u), toVertex (v), weight (=1 def)
  def __init__ (self, fromVertex, toVertex, weight = 1):
    self.u = fromVertex
    self.v = toVertex
    self.weight = weight

  # comparison operators all Boolean
  def __lt__ (self, other):
    return self.weight < other.weight

  def __le__ (self, other):
    return self.weight <= other.weight

  def __gt__ (self, other):
    return self.weight > other.weight

  def __ge__ (self, other):
    return self.weight >= other.weight

  def __eq__ (self, other):
    return self.weight == other.weight

  def __ne__ (self, other):
    return self.weight != other.weight


class Vertex(object):
    # attributes/methods: label, visited
    def __init__(self, label):
        self.label = label
        self.visited = False

    # determine if a vertex was visited
    def was_visited(self):
        return self.visited

    # determine the label of the vertex
    def get_label(self):
        return self.label

    # string representation of the vertex
    def __str__(self):
        return str(self.label)


class Graph(object):
    # check if a vertex is already in the graph
    def __init__(self): # attributes: vertices (list of Vertex()), adjMat
        self.vertices = []
        self.adjMat = []

    def has_vertex(self, label): # Boolean; does graph have vertex with given label?
        num_vert = len(self.vertices)
        for i in range(num_vert):
            if label == self.vertices[i].get_label():
                return True
        return False # else false

    # get the index from the vertex label
    def get_index(self, label): # returns index, or -1 if N/A
        num_vert = len(self.vertices)
        for i in range(num_vert):
            if label == self.vertices[i].get_label():
                return i
        return -1 # else invalid label

    # add a Vertex object with a given label to the graph
    # modify self in-place; no return. equivalently, make adjMat larger by 1
    def add_vertex(self, label):
        if not self.has_vertex(label):
            self.vertices.append(Vertex(label)) # add new Vertex to self (Graph)

            # add a new column in adjMat for new Vertex
            num_vert = len(self.vertices)
            for i in range(num_vert - 1):
                self.adjMat[i].append(0)
            # add a new row too
            new_row = []
            for i in range(num_vert):
                new_row.append(0)
            self.adjMat.append(new_row)

    # add weighted directed edge to graph. adjMat - asymmetrical
    def add_directed_edge(self, start, finish, weight=1):
        self.adjMat[start][finish] = weight

    # add weighted undirected edge to graph
    # for undirected, adjMat is symmetrical
    def add_undirected_edge(self, start, finish, weight=1):
        self.adjMat[start][finish] = weight
        self.adjMat[finish][start] = weight

    # get edge weight between two vertices
    # return -1 if edge does not exist
    def get_edge_weight(self, fromVertexLabel, toVertexLabel):
        from_index = self.get_index(fromVertexLabel)
        to_index = self.get_index(toVertexLabel)
        weight = self.adjMat[from_index][to_index]

        if weight == 0: # 0 <==> nonexistent
            return -1
        else:
            return weight

    # get a list of immediate neighbors that you can go to from a vertex
    # return a list of indices or an empty list if there are none
    def get_neighbors(self, vertexLabel):
        neighbors = []
        vert_index = self.get_index(vertexLabel)
        for i in range(len(self.vertices)): # iterate through columns, L-R
            if self.adjMat[vert_index][i] > 0:
                neighbors.append(self.vertices[i]) # neighbors now has all connecting vertices
        return neighbors # default == None == []

    # return an index to an unvisited vertex adjacent to vertex v (index), or -1 if N/A
    def get_adj_unvisited_vertex(self, v):
        num_vert = len(self.vertices)
        for i in range(num_vert): # iterate through columns of adjMat, preferring left
            if self.adjMat[v][i] > 0 and not self.vertices[i].was_visited():
                return i # return FIRST adjacent i
        return -1

    # get a copy of the list of Vertex objects
    def get_vertices(self):
        copy = []
        for vert in self.vertices:
            copy.append(vert)
        return copy

    # do a depth first search in a graph starting at vertex v (index). DFS uses STACK, not Q
    #       >> prints, does not return. therefore, simply run it in main()
    def dfs(self, v):
        # create the Stack object
        theStack = Stack()

        # mark the vertex v as visited and push it on the stack
        self.vertices[v].visited = True
        print(self.vertices[v]) # print starting vertex label first
        theStack.push(v)

        # visit the other vertices according to depth
        while not theStack.is_empty():
            # loop through adjacent vertices of theStack, either pushing or popping if valid
            u = self.get_adj_unvisited_vertex(theStack.peek())
            if u == -1:
                u = theStack.pop()
            else:
                self.vertices[u].visited = True
                print(self.vertices[u]) # print subsequent vertices
                theStack.push(u)

        # the stack is now empty, so we reset the flags in self.matrix to (visited = False)
        num_vert = len(self.vertices)
        for i in range(num_vert):
            self.vertices[i].visited = False

    # do a breadth first search in a graph starting at vertex v (index)
    def bfs(self, v):
        # create Queue object
        theQueue = Queue()

        # mark v as visited and enqueue. print it as the first vertex label
        self.vertices[v].visited = True
        print(self.vertices[v])
        theQueue.enqueue(v)

        # same procedure as dfs, but with queue
        while not theQueue.is_empty():
            # get the first vertex in the queue
            v1 = theQueue.dequeue() # keep making v1 the first vertex in the queue
            # then get another vertex adjacent to this one
            v2 = self.get_adj_unvisited_vertex(v1)
            while v2 != -1: # while adjacent vertices still exist
                self.vertices[v2].visited = True
                print(self.vertices[v2])
                theQueue.enqueue(v2) # print and enqueue current v2
                v2 = self.get_adj_unvisited_vertex(v1) # move to the next adjacent vertex (v2)

        # now, theQueue is empty. reset all flags back to False in self.vertices
        num_vert = len(self.vertices)
        for i in range(num_vert):
            self.vertices[i].visited = False


    # delete an edge from the adjacency matrix. 2 cases:
    # >>      delete a single edge (~ make 0) if the graph is directed
    # >>      delete two edges if the graph is undirected
    def delete_edge(self, fromVertexLabel, toVertexLabel):
        start = self.get_index(fromVertexLabel)
        finish = self.get_index(toVertexLabel)
        self.adjMat[start][finish] = 0
        self.adjMat[finish][start] = 0 # only relevant when undirected


    # delete a vertex from the vertex list and all edges from and
    # to it in the adjacency matrix
    def delete_vertex(self, vertexLabel):
        vert_index = self.get_index(vertexLabel)
        num_vert = len(self.vertices)

        # delete vertex's column from adjMat
        for row in range(num_vert):
            for col in range(vert_index, num_vert-1):
                self.adjMat[row][col] = self.adjMat[row][col+1]
            self.adjMat[row].pop() # from each row, remove the extra column from the shift

        # delete its row itself from adjMat, making adjMat square again
        self.adjMat.pop(vert_index)

        # remove vertex from the LIST of graph's vertices
        for vertex in self.vertices:
            if vertex.label == vertexLabel:
                self.vertices.remove(vertex)

# function to print adjMat for any graph object
# does NOT print a new line below the grid
def print_adjMat(adjMat):
    num_vert = len(adjMat)
    for i in range(num_vert):
        for j in range(num_vert):
            # space between each number, but NOT at the end of the line! add "if" statement
            if j < num_vert - 1:
                print(adjMat[i][j], end=" ")
            else:
                print(adjMat[i][j], end="")
        print()

def main():
    # create the Graph object
    cities = Graph()

    # read the number of vertices
    line = (sys.stdin.readline()).strip()
    num_vertices = int(line)
    ## print(num_vertices)

    # add the vertices to the graph
    for i in range(num_vertices):
        city = (sys.stdin.readline()).strip()
        ## print(city)
        cities.add_vertex(city)

    # read the number of edges
    line = (sys.stdin.readline()).strip()
    num_edges = int(line)

    # read the edges and add them to the adjacency matrix
    for i in range(num_edges):
        line = (sys.stdin.readline()).strip()
        ## print(line)
        edge = line.split()
        start = int(edge[0])
        finish = int(edge[1])
        weight = int(edge[2])

        cities.add_directed_edge(start, finish, weight)

    # read the starting vertex for dfs and bfs
    start_vertex = (sys.stdin.readline()).strip()
    ## print(start_vertex)

    # get the index of the starting vertex
    start_index = cities.get_index(start_vertex)
    ## print(start_index)

    # gather next line, i.e. "Dallas Atlanta", which contains cities whose connecting...
    # edge must be made 0
    del_edge = sys.stdin.readline().strip().split()
    del_edge_1 = del_edge[0]
    del_edge_2 = del_edge[1]

    # gather final line, cities from which to delete vertex and all connecting edges
    del_vertex = sys.stdin.readline().strip()

    # test depth first search
    print("Depth First Search")
    cities.dfs(start_index)
    print()

    # test breadth first search
    print("Breadth First Search")
    cities.bfs(start_index)
    print()

    # test deletion of an edge
    # >> print deletion of an edge, then adj matrix. NO list of edges, obviously
    print("Deletion of an edge")
    print()
    cities.delete_edge(del_edge_1, del_edge_2)
    print("Adjacency Matrix")
    print_adjMat(cities.adjMat)
    print()

    # test deletion of a vertex
    # >> print deletion of a vertex, list of vertices, then adj matrix
    print("Deletion of a vertex")
    print()
    cities.delete_vertex(del_vertex)
    print("List of Vertices")
    for city in cities.vertices:
        print(city)
    print()
    # finally, print vertex-removed adjacency matrix
    print("Adjacency Matrix")
    print_adjMat(cities.adjMat)
    print()

if __name__ == "__main__":
    main()
