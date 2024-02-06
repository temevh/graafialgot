# A template for Ford Fulkerson algorithm and min cut

from collections import deque
from graph import Graph
from copy import deepcopy as copy
import sys
#from icecream import ic


## This code assumes flow is dictionary with keys (u,v) and values flow(u,v)
## Define the sum of two flows
def SumFlow(f1,f2):
  f = {}
  for (u,v) in set(f1.keys()) | set(f2.keys()):
    if not (u,v) in f1:
      f[(u,v)] = f2[(u,v)]
    elif not (u,v) in f2:
      f[(u,v)] = f1[(u,v)]
    else:
      f[(u,v)] = f1[(u,v)] + f2[(u,v)]
  return f


## This is an EXAMPLE of how the flow network class can be implemented, some implementation is missing
class FlowNetwork:
  def __init__(self,G) -> None:
    self.G = G
    self.FindSource()
    self.FindSink()
  ## Find the source, it is the first vertex with a non-empty adjacency list:
  def FindSource(self):
    for u in range(self.G.n):
      if len(self.G.adj[u]) > 0:
        self.s = u
        print("source set to", self.s)
        return    
  ## Find the sink. It is the last vertex.
  def FindSink(self):
    self.t = self.G.n-1
    print("sink set to", self.t)
  # Define the value of a flow
  def FlowValue(self,f):
    return sum([f[(self.s,u)] for u in G.adj[self.s] if (self.s,u) in f])

  ## Create a residual graph
  def MakeResidual(self, f):
    ## Copy the graph:
    G = copy(self.G)
    for (u,v) in f:
      c = 0
      ## Copy the weight
      if (u,v) in G.w:
        c = G.w[(u,v)]
      #calculate residual capasity
      cf = c - f[(u,v)]
      ## It is an error if the residual capacity is negative
      if cf < 0:
        raise Exception("capacity violation in f")
      ## Add the edge if the residual capacity is positive
      if not v in G.adj[u]:
        G.addEdge(u,v)
      G.w[(u,v)] = cf
    return G

  ## This is not implemented. Implement the augmenting path algorithm here
  def FindAugPath(self,Gr,s=None,t=None):
    if s is None:
      s = self.s
    if t is None:
      t = self.t
    
    # Create dictionaries to store the visited status and the parents
    visited = {v: False for v in range(self.G.n)}
    parent = {v: None for v in range(self.G.n)}

    queue = deque()
    queue.append(s)
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v in self.G.adj[u]:
            # Check for residual capacity
            if (u, v) in Gr.w and Gr.w[(u, v)] > 0 and not visited[v]:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == t:  # Sink reached
                    path = []
                    # Backtrack using parent pointers to reconstruct the path
                    while v:
                        path.insert(0, v)
                        v = parent[v]
                    return path
    return []  # No path found

  ## Make an augmenting flow from a path
  def MakeAugFlow(self,path, Gr = None):
    if Gr is None:
      Gr = self.G
    f = {}
    for i in range(len(path)-1):
      u = path[i]
      v = path[i+1]
      if (u,v) not in Gr.w or Gr.w[(u,v)] == 0:
        raise Exception("Edge not in Gr or saturated")
      f[(u,v)] = 0
    cf = min([Gr.w[(u,v)] for (u,v) in f])
    for (u,v) in f:
      f[(u,v)] = cf
    return f

  def FordFulkerson(self):
    f = {}
    G = self.G
    Gr = self.MakeResidual(f)
    ap = self.FindAugPath(G)
    while ap != []:
      fp = self.MakeAugFlow(ap,Gr)
      f = SumFlow(f,fp)
      Gr = self.MakeResidual(f)
      ap = self.FindAugPath(Gr)
    return f

  def MinCutEdges(self):
    f = self.FordFulkerson()
    # Implementing BFS to find set S of the min cut
    visited = {v: False for v in range(self.G.n)}
    queue = deque()
    queue.append(self.s)
    visited[self.s] = True

    while queue:
        u = queue.popleft()
        for v in self.G.adj[u]:
            if (u, v) in f and f[(u, v)] < self.G.w[(u, v)] and not visited[v]:
                visited[v] = True
                queue.append(v)

    # S is now the set of vertices reached by the BFS
    S = {u for u in range(self.G.n) if visited[u]}

    # Edges from S to T in the original graph
    Edges = [(u, v) for u in S for v in self.G.adj[u] if v not in S and (u, v) in self.G.w]

    return Edges
            
if __name__ == "__main__":
    G = Graph()
    inputgraph = sys.argv[1]
    G.readgraph(inputgraph)
    F = FlowNetwork(G)
    edges = F.MinCutEdges()
  

 