### Read in a graph, a set of vertices, and a pair of vertices. 

import graph
import sys

#For testpair1, v = 0, w = 7
#g = testcase1.txt, B = 2 4 6

#Start from first pair (v) 
#check adjacency list 
#if list contains a element that is in B 
  #-> go to that element, increment n by one
#else if no B element found 
  #-> go to 

def algorithm(g, B, v, w):
    n = 0
    node = v
    visited = set()

    while True:
      print("node", node)
      if node == w:
          return n

      visited.add(node)
      adjacent = [neighbor for neighbor in g.adj[node] if neighbor not in visited]
      print("adjacent", adjacent)

      if not adjacent:
          print("END")
          # No more reachable nodes
          break

      common_nodes = set(adjacent) & B
      if common_nodes:
          # Move to the first node in set B
          print("common nodes", common_nodes)
          next_node = common_nodes.pop()
          n += 1
      else:
          # No adjacent node in set B, choose the smallest adjacent node
          print("no common nodes")
          next_node = min(adjacent)

      print("next_node", next_node)
      node = next_node

    return 0

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
  

