import graph
import sys
from collections import deque

#For testpair1, v = 0, w = 7
#g = testcase1.txt, B = 2 4 6

#Start from first pair (v) 
#check adjacency list 
#if list contains a element that is in B 
  #-> go to that element, increment n by one
#else if no B element found 
  #-> go to 

def algorithm(g, B, s, t):
    visited  = [False] * 8;
    queue = []
    n = 0

    queue.append(s)
    visited[s] = True

    while queue:
      s = queue.pop(0)
      print(s, end=" ")
      adjacent = [neighbor for neighbor in g.adj[s] if neighbor not in visited]     
      
      for i in g.adj[s]:
        if visited[i] == False:
          if i in B:
            n+=1
          queue.append(i)
          visited[i] = True
        
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
  print("result:",n)
  

