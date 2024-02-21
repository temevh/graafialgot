import networkx as nx
from networkx.algorithms.community import girvan_newman

# Create a graph
G = nx.Graph()
G.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6)])

# Apply the Girvan-Newman algorithm
communities = girvan_newman(G)

# Skip the first two levels (one and two communities)
next(communities)
next(communities)

# Get the third level (four communities)
for i, community in enumerate(next(communities), 1):
    print(f"Community {i}: {list(community)}")