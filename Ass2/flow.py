# A template for Ford Fulkerson algorithm and min cut

from graph import Graph
from copy import deepcopy as copy
import sys
# from icecream import ic
from collections import deque


## This code assumes flow is dictionary with keys (u,v) and values flow(u,v)
## Define the sum of two flows
def SumFlow(f1, f2):
    f = {}
    for (u, v) in set(f1.keys()) | set(f2.keys()):
        if not (u, v) in f1:
            f[(u, v)] = f2[(u, v)]
        elif not (u, v) in f2:
            f[(u, v)] = f1[(u, v)]
        else:
            f[(u, v)] = f1[(u, v)] + f2[(u, v)]
    return f


## This is an EXAMPLE of how the flow network class can be implemented, some implementation is missing
class FlowNetwork:
  def __init__(self, G) -> None:
      self.G = G
      self.FindSource()
      self.FindSink()

  ## Find the source, it is the first vertex with a non-empty adjacency list:
  def FindSource(self):
      for u in range(self.G.n):
          if len(self.G.adj[u]) > 0:
              self.s = u
              return
              ## Find the sink. It is the last vertex.

  def FindSink(self):
      self.t = self.G.n - 1

  # Define the value of a flow
  def FlowValue(self, f):
      return sum([f[(self.s, u)] for u in G.adj[self.s] if (self.s, u) in f])

  ## Create a residual graph
  def MakeResidual(self, f):
      ## Copy the graph:
      G = copy(self.G)
      for (u, v) in f:
          c = 0
          ## Copy the weight
          if (u, v) in G.w:
              c = G.w[(u, v)]
          # calculate residual capasity
          cf = c - f[(u, v)]
          ## It is an error if the residual capacity is negative
          if cf < 0:
              raise Exception("capacity violation in f")
          ## Add the edge if the residual capacity is positive
          if not v in G.adj[u]:
              G.addEdge(u, v)
          G.w[(u, v)] = cf
      return G

  ## This is not implemented. Implement the augmenting path algorithm here
  def FindAugPath(self, Gr, s=None, t=None):
      if s is None:
          s = self.s
      if t is None:
          t = self.t
      ## Now calculate the path.

      visited = set()
      queue = deque([(s, [])])  # BFS queue, each element is a tuple (vertex, path)

      while queue:
          current, path = queue.popleft()

          if current == t:
              return path  # Found an augmenting path

          visited.add(current) # Mark the current vertex as visited

          for neighbor in Gr.adj[current]:  # Add all neighbors to the queue
              if neighbor not in visited and Gr.w[(current, neighbor)] > 0: # If the edge has residual capacity
                  new_path = path + [neighbor] # Add the neighbor to the path
                  queue.append((neighbor, new_path)) # Add the neighbor to the queue

      return []

  ## Make an augmenting flow from a path
  def MakeAugFlow(self, path, Gr=None):
      if Gr is None:
          Gr = self.G
      f = {}
      for i in range(len(path) - 1):
          u = path[i]
          v = path[i + 1]
          if (u, v) not in Gr.w or Gr.w[(u, v)] == 0:
              raise Exception("Edge not in Gr or saturated")
          f[(u, v)] = 0
      cf = min([Gr.w[(u, v)] for (u, v) in f])
      for (u, v) in f:
          f[(u, v)] = cf
      return f

  def FordFulkerson(self):
      f = {}
      G = self.G
      Gr = self.MakeResidual(f)
      ap = self.FindAugPath(G)

      while ap != []:
          fp = self.MakeAugFlow(ap, Gr)
          f = SumFlow(f, fp)
          Gr = self.MakeResidual(f)
          ap = self.FindAugPath(Gr)


      return f

  def MinCutEdges(self):
      f = self.FordFulkerson()
      S = set([])
      ### Find the cut (S,T) by finding the set S.
      visited = set()

      def dfs(v):
          nonlocal visited # Use the nonlocal keyword to modify the variable in the outer scope
          visited.add(v) # Mark the vertex as visited
          S.add(v) # Add the vertex to the set S
          for u in self.G.adj[v]: # Visit all neighbors
              if u not in visited and self.MakeResidual(f).w[(v, u)] > 0: # If the edge has residual capacity
                  dfs(u) # Visit the neighbor

      dfs(self.s) # Start the DFS from the source


      ## Return the edges that cross the cut:
      Edges = [(u, v) for u in S for v in G.adj[u] if v not in S]
      flowValue = 0
      for (u,v) in Edges:
          flowValue += f[(u, v)]

      print(Edges)
      print(flowValue)


      ### Find the edges that cross the cut (S,T), i.e., they start from S and end in T.
      ### Return these edges.
      return Edges


if __name__ == "__main__":
    G = Graph()
    inputgraph = sys.argv[1]
    G.readgraph(inputgraph)
    F = FlowNetwork(G)
    edges = F.MinCutEdges()
