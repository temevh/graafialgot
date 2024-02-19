import graph
import sys

def algorithm(g, B, s, t):
    visited  = [False] * (g.n) #Create an array that has false for each node
    queue = []
    n = 0 #counter to get the result

    queue.append(s) #Add the starting node s to the queue
    visited[s] = True #mark s visited

    while queue:
      s = queue.pop(0) #Get the first/leftmost node from the queue
      if s == t: #If current node matches the end node break
        break
   
      for i in g.adj[s]: #Loop through the adjacent nodes (from current node)
        if visited[i] == False: #If an adjacent node has not been visited yet
          if i in B: #If the not visited node is in set B 
            n+=1 #increase counter
          queue.append(i) #add the node to queue
          visited[i] = True 
        
    return n #Finally return the end result (number of nodes in set)

### Read in a set of vertices from a file. These are just numbers separated by whitespace.
def readset(filename):
  f = open(filename, 'r')
  s = set()
  for line in f:
    for v in line.split():
      s.add(int(v))
  return s

## Read the pair, again, just two integers separated by whitespace.
def readpair(filename):
  f = open(filename, 'r')
  for line in f:
    (v,w) = line.split()
    return (int(v), int(w))


### If ran from the command line:
if __name__ == "__main__":
  # Graph is the first command line argument:
  g = graph.Graph()
  g.readgraph(sys.argv[1])
  # Vertices are the second command line argument:
  B = readset(sys.argv[2])
  # Pair is the third command line argument:
  (v,w) = readpair(sys.argv[3])

  ### Call your algorithm:

  n = algorithm(g, B, v, w)

  # Print the result:
  print("result:",n)