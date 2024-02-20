'''
Input: A graph, given as directed, but interpreted to be nondirected

Interpretation: The vertices are players of a clandestine game. Edges denote observed
interactions between players. Players have formed four secret societies. Players are more
likely to interact with players that are members of the same society, and less likely to
interact with outsiders (though these interactions may occur). Every player belongs to
one of the four secret societies. The societies try to form in such a way that they are
roughly the same size, though the sizes may in some cases differ.

Task: Based on the edges, formulate an estimate as to what are the four secret societies.
Return a list of four lists in such a way that every vertex belongs to exactly one list.
Order the lists internally from the smallest vertex number to the largest.
'''

import graph
import sys

def algorithm(g):
  for i in range(7):
    print(i, g.adj[i])
    
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


if __name__ == "__main__":
  g = graph.Graph()
  g.readgraph(sys.argv[1])
  algorithm(g)
