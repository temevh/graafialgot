
### Read in a graph, a set of vertices, and a pair of vertices. 

import graph
import sys

## Implement your algorithm here:
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
    visited = set()
    node = v
    print("Starting from node:", node)
    print("Set B:", B)

    while True:
        adjacent = g.adj[node]
        print("Adjacent vertices of", node, ":", adjacent)

        # Check if any adjacent node is in set B
        common_nodes = set(adjacent) & B
        if common_nodes:
            # Move to the first node in set B
            next_node = common_nodes.pop()
            print(f"Moving to node {next_node} from set B")
            node = next_node
            n += 1
        else:
            break  # No adjacent node in set B

    print("Total nodes from set B on the path:", n)
    return n


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
  print(n)
  

